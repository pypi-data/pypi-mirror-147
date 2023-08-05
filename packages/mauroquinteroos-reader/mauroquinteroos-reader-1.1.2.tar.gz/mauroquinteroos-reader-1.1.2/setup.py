from pathlib import Path
from setuptools import setup


# Obtener la ubicación del padre del archivo actual
HERE = Path(__file__).parent
# Leer el archivo README.md
readme = (HERE / "README.md").read_text()

setup(
    # Nombre del paquete. Este nombre debe ser unico
    name="mauroquinteroos-reader",
    # Es una lista de todos los paquetes que deben ser instalados en el paquete
    # Otra manera de hacerlo automático es: packages=find_packages(exclude=["tests"]) para buscar todos los paquetes y subpaquetes dentro del package_dir
    packages=["reader"],
    # Es una descripción corta del paquete
    description="Paquete de prueba de Mauro Quinteros",
    # Es la versión del paquete, esta versión debe ser única por cada vez que se suba el paquete al repositorio
    version="1.1.2",
    # El autor del paquete
    author="Mauro Quinteros",
    # El correo del autor
    author_email="quinterosmauro0599@gmail.com",
    # El tipo de licencia del paquete
    license="MIT",
    # Es el archivo que contiene la descripción detallada del paquete
    long_description=readme,
    # Indica el tipo de archivo que se utiliza para la descripción detallada
    long_description_content_type="text/markdown",
    # Es la dirección del homepage del paquete
    url="https://github.com/mauroquinteroos/mauroquinteroos-reader",
    # Es una lista opcional de direcciones extras que sirven de apoyo para el paquete
    project_urls={
        "Docs": "https://mauroquinteroos.github.io/mauroquinteroos-reader/",
        "Issues": "https://github.com/mauroquinteroos/mauroquinteroos-reader/issues"
    },
    # Brinda metadata adicional a pip sobre el paquete
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    # Indica las versiones de python que soportan el proyecto
    python_requires=">=3.6",
    # Es una lista con todas las dependencias necesarias para que el paquete funcione
    install_requires=["feedparser", "html2text"],
    # Incluye dentro del paquete archivos que no son archivos de código fuente (archivos de texto, binarios, documentación ,etc).
    include_package_data=True,
    # Provee los comandos que se pueden correr en la consola.
    entry_points={
        "console_scripts": [
            "realpython=reader.main:get_news"
        ]
    },
    # Es un diccionario que en el key se indica el nombre del paquete y en el value el directorio. Para este caso, un key vacío significa el paquete root.
    # package_dir={"": "."}
)