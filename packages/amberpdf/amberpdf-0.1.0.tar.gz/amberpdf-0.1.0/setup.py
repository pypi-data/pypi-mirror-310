from setuptools import setup, find_packages

setup(
    name="amberpdf",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "PyMuPDF>=1.18.0",
        "boto3>=1.26.0",
    ],
    author="Tu Nombre",
    author_email="tu@email.com",
    description="Una librería para extraer texto de PDFs usando AWS Textract",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tuusuario/amberpdf",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
