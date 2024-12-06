from setuptools import find_packages, setup

with open("README.md", "r", encoding='utf-8') as arq:
    readme = arq.read()

setup(
    name="metricus",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    long_description=readme,
    long_description_content_type="text/markdown",
    description="Python unit converter with a Tkinter interface for easy and precise conversions across various measurements like force, length, and mass",
    author="Guilherme Freschi, Yaron Buchler",
    author_email="guilhermefreschix@gmail.com, buchleryaron@gmail.com",
    url="https://github.com/guifreschi/Metricus",
    project_urls={
        "Yaron Buchler's GitHub": "https://github.com/YaronBuchler",
        "Guilherme Freschi's GitHub": "https://github.com/guifreschi",
        "Project on GitHub": "https://github.com/guifreschi/Metricus",
    },
    license="MIT",
    keywords="conversion, units, temperature, weight, length, distance, energy, volume, mass, pressure, speed, time, metric, imperial, unit converter...",
)
