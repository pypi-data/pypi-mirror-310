import pyyamb
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyyamb",
    version=pyyamb.__version__,
    author="Aleksei Korzhenkov",
    author_email="oscypek@ya.ru",
    description="Python implementation of YAMB (Yet Another Metagenome Binner)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laxeye/pyyamb",
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pyyamb = pyyamb.pyyamb:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    python_requires='>=3.10',
    install_requires=[
        'biopython',
        'pandas',
        'seaborn',
        'pysam',
        'matplotlib',
        'numpy',
        'scikit-learn>=1.3',
        'pycoverm',
        'regex'
    ]
)
