import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read().strip()


required = [
    'confluent-kafka==0.11.6'
]

setup(name='ejercicios_python',
      version=read('VERSION'),
      author="Francisco Huertas",
      author_email="pacohuertas@gmail.com",
      license="Apache2",
      packages=["ejercicios"],
      description="Ejercicios modulo streaming UAH-ANGVD",
      long_description=read('README.md'),
      install_requires=required,
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
      ])
