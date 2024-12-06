import fitz
import boto3
import json

# Variable global para el cliente de Textract
textract_client = None

def credentials(aws_access_key_id, aws_secret_access_key, region="us-east-1"):
    """
    Configura las credenciales de AWS para usar Textract
    """
    global textract_client
    textract_client = boto3.client(
        service_name='textract',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )

def extract_text_with_textract(image_bytes):
    """
    Extrae texto de una imagen usando AWS Textract.
    """
    if textract_client is None:
        raise ValueError("AWS credentials not set. Call credentials() first.")
    
    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})
    extracted_text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            extracted_text += item["Text"] + "\n"
    
    return extracted_text

def process_pdf(file_path):
    """
    Procesa un PDF mixto (texto e imágenes) y extrae el contenido en orden.
    """
    if textract_client is None:
        raise ValueError("AWS credentials not set. Call credentials() first.")

    pdf_file = fitz.open(file_path)
    full_text = ""

    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        #print(f"--- Procesando Página {page_index + 1} ---")

        # Calcular el área de la página
        page_rect = page.rect
        page_width = page_rect.width
        page_height = page_rect.height
        page_area = page_width * page_height

        # Obtener las imágenes primero
        image_list = page.get_images(full=True)
        image_regions = []

        # Crear un conjunto de regiones ocupadas por imágenes
        for img in image_list:
            xref = img[0]
            bbox = page.get_image_bbox(img)
            
            image_width = bbox.width
            image_height = bbox.height
            image_area = image_width * image_height
            percentage = (image_area / page_area) * 100

            if percentage > 5:
                image = pdf_file.extract_image(xref)
                image_bytes = image["image"]
                image_regions.append({
                    "type": "image",
                    "content": image_bytes,
                    "bbox": bbox
                })

        # Obtener bloques de texto que no se superponen con imágenes
        text_blocks = page.get_text("blocks")
        content_list = []

        for block in text_blocks:
            x0, y0, x1, y1, text, _, _ = block
            block_bbox = fitz.Rect(x0, y0, x1, y1)
            
            # Verificar si el bloque se superpone con alguna imagen
            overlaps_with_image = False
            for img_region in image_regions:
                img_bbox = img_region["bbox"]
                if block_bbox.intersects(img_bbox):
                    overlaps_with_image = True
                    break
            
            # Solo añadir el bloque si no se superpone con una imagen
            if not overlaps_with_image and text.strip():
                content_list.append({
                    "type": "text",
                    "content": text.strip(),
                    "bbox": block_bbox
                })

        # Añadir las regiones de imagen a la lista de contenido
        content_list.extend(image_regions)

        # Ordenar contenido por posición vertical (y0)
        content_list.sort(key=lambda x: x["bbox"].y0)

        # Procesar contenido en orden
        for item in content_list:
            if item["type"] == "text":
                full_text += item["content"] + "\n"
            elif item["type"] == "image":
                ocr_text = extract_text_with_textract(item["content"])
                full_text += ocr_text + "\n"

    pdf_file.close()
    return json.dumps(full_text, ensure_ascii=False)