from setuptools import setup, find_packages

setup(
    name='cobra_web',
    version='0.2.1',
    packages=find_packages(),
    install_requires=[
        'Django>=3.2',
        'Sphinx',
        'PyScss',
    ],
    description='Librería para automatizar la creación de sitios web con Django y estilos personalizados.',
    author='Adolfo González Hernández',
    author_email='adolfogonzal@gmail.com',
    url='https://github.com/Alphonsus411/cobra_web' ,# Cambia esto a tu repositorio
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
