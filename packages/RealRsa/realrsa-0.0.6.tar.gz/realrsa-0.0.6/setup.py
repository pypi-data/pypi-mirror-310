from distutils.core import setup
# from setuptools import setup
from setuptools import find_packages
from distutils.extension import Extension
from Cython.Build import cythonize
import sys, os

if sys.platform == 'win32':
    library_path = os.path.join(os.path.dirname(sys.executable), "Library")
    libraries = ["libssl","libcrypto"]
elif sys.platform == 'linux' or sys.platform == 'linux2':
    library_path = os.path.dirname(sys.executable)
    libraries = ["ssl","crypto"]

include_path = os.path.join(library_path, "include")
libpath = os.path.join(library_path, "lib")

extensions = [
    Extension("RealRsa", ["RealRsa/*.pyx"],
              include_dirs=[include_path],  
              libraries=libraries, 
              library_dirs=[libpath]) 
]


with open("README.md", "r", encoding="utf-8") as f:
  long_description = f.read()
  

setup(name='RealRsa',
      version='0.0.6',
      ext_modules=cythonize(extensions),
      description='python version of rsa',
      long_description=long_description,
      author='zkh',
      author_email='404937333@qq.com',
      keywords="rsa",
      setup_requires=["cython"],
      install_requires=[],
      long_description_content_type='text/markdown',
      packages=find_packages(where="."),
      package_data={
        "RealRsa":["*.pyi"]
      },
      include_package_data=True,
      platforms=["Windows", "Linux"],
      license='MIT License',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ],
)

