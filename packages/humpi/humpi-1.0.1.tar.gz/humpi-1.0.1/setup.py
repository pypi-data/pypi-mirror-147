from setuptools import setup, find_packages


setup(
    name='humpi',
    version='1.0.1',
    license='GPL',
    author="Albenis Pérez-Alarcón",
    author_email='albenisp@instec.cu',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/apalarcon/HuMPI-master',
    keywords='hurricane maximum potential intensity',
    install_requires=[
          'netcdf',
          'numpy',
          'scipy',
          'mpi4py'],

) 
