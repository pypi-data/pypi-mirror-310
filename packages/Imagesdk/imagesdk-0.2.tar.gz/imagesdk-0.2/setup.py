from setuptools import setup, find_packages

setup(
    name='Imagesdk',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'Pillow',  # Image processing library
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    long_description=open('Readme.md').read(),
    long_description_content_type='text/markdown',
)
