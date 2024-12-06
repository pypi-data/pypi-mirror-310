from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_clahe",
    version="0.0.3",
    author="lucenara_pereira",
    author_email="lucenarapereira@gmail.com",
    description="Algoritmo de processamento de imagens CLAHE (Contrast Limited Adaptive Histogram Equalization).",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucenarapereira/Portfolio-Engenharia-de-Dados/tree/main/Projeto%201/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)