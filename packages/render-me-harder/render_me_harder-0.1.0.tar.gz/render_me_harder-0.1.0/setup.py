#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    "numpy",
    "Pillow",
    "pyrender",
    "trimesh",
]

test_requirements = [ ]

setup(
    author="minexew",
    author_email='minexew@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Stupidly simple API for rendering 3D models to images",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='render_me_harder',
    name='render_me_harder',
    packages=find_packages(include=['render_me_harder', 'render_me_harder.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/minexew/render_me_harder',
    version='0.1.0',
    zip_safe=False,
)
