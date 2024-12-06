# AmberPDF

Una librería para extraer texto de PDFs usando AWS Textract.

## Instalación

pip install amberpdf

## Uso

import amberpdf

# Configura las credenciales de AWS
amberpdf.credentials('tu_access_key_id', 'tu_secret_access_key')

# Procesa un PDF
text = amberpdf.process_pdf('ruta/al/archivo.pdf')
print(text)
