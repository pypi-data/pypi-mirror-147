import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="helium-api",
    version="1.0.1",
    author="Jakov",
    author_email="author@example.com",
    description="Helium API for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jpopov1/python-heliumapi",
    project_urls={
        "Bug Tracker": "https://github.com/jpopov1/python-heliumapi/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    install_requires=[
        'urllib'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
