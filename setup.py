import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fractalpaths",
    version="0.0.1",
    author="Elene Karangozishvili",
    author_email="elenekarangozishvili@gmail.com",
    description="Given a fractal and two points in the fractal, finds the shortest taxicab path between the points that stays in the fractal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karangoe/fractalpaths",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)