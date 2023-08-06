import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Cp2kData",
    version="0.2.0",
    author="Yongbin Zhuang",
    author_email="robinzhuang@outlook.com",
    description="Small Package to Postprocessing Cp2k Output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robinzyb/cp2kdata",
    packages=setuptools.find_packages(where="cp2kdata"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)"
    ],
    python_requires='>=3.6',
    install_requires=[
        "numpy >= 1.19.5",
        "scipy >= 1.5.4",
        "matplotlib >= 3.3.2",
        "ase >= 3.20.1",
        "regex",
        "pytest",
        "pytest-cov"
  ]
#    entry_points={
#        'console_scripts': [
#            'tlk=toolkit.main:cpdat']
#        }
)
