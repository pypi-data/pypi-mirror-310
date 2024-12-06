#!/usr/bin/env python
from setuptools import setup


setup(
    name='django-pdf-tables',
    version='1.0.0',
    description='A Django app for processing PDF documents with tables',
    long_description=open('README.rst').read(),
    author='Pragmatic Mates',
    author_email='info@pragmaticmates.com',
    maintainer='Pragmatic Mates',
    maintainer_email='info@pragmaticmates.com',
    url='https://github.com/PragmaticMates/django-pdf-tables',
    packages=[
        'pdf_tables',
    ],
    include_package_data=True,
    install_requires=('fpdf', 'django>=3'),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 3 - Alpha'
    ],
    license='Apache2 License',
    keywords = "django pdf table document export render",
)
