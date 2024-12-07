# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="moonai",
    version="0.1.2",
    author="Bruno Bracaioli",
    author_email="bruno@bracaiolitech.com",
    description="Framework to create teams of AI agents with organized missions and flows.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brunobracaioli/moonai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
        "beautifulsoup4>=4.9.3",
        "colorama>=0.4.4",
        "anthropic>=0.0.0",  # Especifique a versão conforme necessário
        "pydantic>=1.0.0",
        "facebook-business>=17.0.0",  # Para MetaMetricsToolLasts7Days
        "urllib3>=2.0.0",  # Para funções de scraping
        "lxml>=4.9.0",      # Para melhor performance do BeautifulSoup
        "html5lib>=1.1",    # Parser alternativo para BeautifulSoup
    ],
    entry_points={
        "console_scripts": [
            "moonai=moonai.squad:main",
        ],
    },
    include_package_data=True,  # Inclui arquivos especificados em MANIFEST.in
    license="MIT",
    keywords="AI agents framework missions squad tools",
    project_urls={
        "Bug Tracker": "https://github.com/brunobracaioli/moonai/issues",
        "Documentation": "https://github.com/brunobracaioli/moonai#readme",
        "Source Code": "https://github.com/brunobracaioli/moonai",
    },
)