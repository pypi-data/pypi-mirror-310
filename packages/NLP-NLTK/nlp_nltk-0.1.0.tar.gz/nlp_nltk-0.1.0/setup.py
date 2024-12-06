from setuptools import setup, find_packages

setup(
    name='NLP-NLTK',  # Your library name
    version='0.1.0',  # Initial version
    author='Naxio Technology',  # Your name
    author_email='naxiotech.2024@gmail.com',  # Your email
    description='A library for NLP tasks using NLTK',  # Short description
    long_description=open('README.md').read(),  # Detailed description from README.md
    long_description_content_type='text/markdown',
    url='',  # GitHub repository link
    packages=find_packages(),  # Automatically find and include packages
    install_requires=[  # Dependencies
        'nltk',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
