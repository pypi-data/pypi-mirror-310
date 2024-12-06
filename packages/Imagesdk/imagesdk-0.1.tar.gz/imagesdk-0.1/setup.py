from setuptools import setup, find_packages

setup(
    name='Imagesdk',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Pillow',  # Image processing library
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)