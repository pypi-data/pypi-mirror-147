from setuptools import setup, find_packages

setup(name="mess_server_tsnv",
      version="0.0.1",
      description="mess_server",
      author="Tsymbalyuk Nikolay & Co",
      author_email="tsnv76@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodom', 'pycryptodomex']
      )