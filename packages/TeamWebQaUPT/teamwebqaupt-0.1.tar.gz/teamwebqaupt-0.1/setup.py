from setuptools import setup, find_packages

setup(
    name="TeamWebQaUPT",  # Nombre del paquete.
    version="0.1",
    description="Un paquete para pruebas automatizadas con Selenium y pytest",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/UPT-FAING-EPIS/proyecto-si8811a-2024-ii-u2-qa-pruebas-valverde-cano",  # Cambia con la URL de tu repositorio.
    author="Jean Valverde y Anthony Cano",
    author_email="jeanvalverdezamora@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pytest",
        "allure-pytest",
        "pytest-selenium",
        "pytest-xdist",
    ],
    entry_points={
        "console_scripts": [
            "ejecutar_pruebas=TeamWebQaUPT.runner:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
