from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="SigmmaCrawler",
    version="0.0.1.dev",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    author="Kenneth Díaz",
    author_email="admin@unicaribe.dev",
    description="Este proyecto permite obtener datos del SIGMAA, el sistema educativo de la Universidad del Caribe. "
                "Facilita la obtención de información del estudiante, calificaciones, cárdex, oferta académica, "
                "información de pagos de estudiantes, entre otros datos, a través de un SDK de Python.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/unicaribe-dev/sigmaa-crawler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
