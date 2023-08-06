from setuptools import setup, Extension, find_packages
setup(
    name="nubcrypt",
    version="0.0.1",
    description="Data encryption",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author="Anggi Kharisma Putra",
    license="MIT",
    author_email="anggikharismaputra@gmail.com",
    url="https://github.com/nubcakee/nubcrypt",
    packages = find_packages(),
    setup_requires=["cython"],
    ext_modules= [
        Extension(
            'nubcrypt.core._core',
            sources=["nubcrypt/core/_core.pyx"]
        )
    ],
    keywords=["encryption", "data-encryption", "cryptography"]
)
