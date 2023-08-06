import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="styled-pyqtwidgets",
    author="Dixon Leuenberger",
    version="0.1.0",
    description="create stylized table widget",
    keywords="qTableWidget, pypi, package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.is4s.com/DixonLeuenberger/table_model_package",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["pyqt5"],
    extras_require={
        "dev": ["check-manifest"],
    },
)
