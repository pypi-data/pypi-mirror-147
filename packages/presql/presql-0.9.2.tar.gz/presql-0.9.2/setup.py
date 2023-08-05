import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = "presql",
    packages = ["presql"],
    version = "0.9.2",
    license="MIT",
    description = "PostgreSQL and Psycopg2 wrapper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = "Rodney Maniego Jr.",
    author_email = "rod.maniego23@gmail.com",
    url = "https://github.com/rmaniego/presql",
    download_url = "https://github.com/rmaniego/presql/archive/v1.0.tar.gz",
    keywords = ["postgresql", "postgres", "psycopg2", "sql", "python"],
    install_requires=["psycopg2"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers", 
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.6"
)