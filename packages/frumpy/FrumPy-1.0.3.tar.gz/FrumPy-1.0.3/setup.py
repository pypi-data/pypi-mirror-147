import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FrumPy",
    version="1.0.3",
    author="Frumpy",
    author_email="frumpyfrumpster@gmail.com",
    description="It's Frumpy time.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    packages=setuptools.find_packages(where="."),
    install_requires="numpy",
)
