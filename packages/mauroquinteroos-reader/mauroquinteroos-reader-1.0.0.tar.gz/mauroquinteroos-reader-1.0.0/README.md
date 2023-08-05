# Pasos para crear un paquete

- [Tutorial oficial de python](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

- [Keywords de setuptools](https://setuptools.pypa.io/en/latest/references/keywords.html)

- [Gestión de dependencias](https://setuptools.pypa.io/en/latest/userguide/dependency_management.html#declaring-dependencies)

- [Gestión de archivos de datos](https://packaging.python.org/en/latest/guides/using-manifest-in/)

- [Configurar setuptools usando setup.cfg](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html)

### Crear el archivo pyproject.toml (si usas setuptools no es necesario crearlo)

pyproject.toml le dice a las herramientas de build (como pip y build) que se necesita para construir el paquete.

### Configuración de la metadata del paquete

Existen 2 archivos [setup.cfg](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html) (estático) y setup.py (dinámico). Se puede colocar toda la metadata en el archivo setup.py a pesar de que sea metadata estática debido a que antes era la única manera de hacerlo, pero ahora se recomienda separar la metadata estática de la dinámica.

### Configuración del manejo de archivos de datos

Al agregar el keyword `includ_package_data` dentro del archivo setup.py, se va agregar al paquete todos los archivos de datos. Si deseamos agregar ciertos archivos se debe crear el archivo `MANIFEST.in`.
