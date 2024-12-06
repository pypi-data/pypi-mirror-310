from setuptools import setup, find_packages

setup(
    name='pypi_guapo',
    version='0.1.0',
    packages=find_packages(),
    description='A simple example library',
    author='Guapo',
    author_email='guapo@example.com',
    url='https://github.com/yourusername/pypi_guapo',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
