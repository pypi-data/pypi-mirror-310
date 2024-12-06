# setup.py

from setuptools import setup, find_packages
from pathlib import Path

# Read the README.md file
this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name='ot_grn',
    version='0.1.1',
    description='Double Optimal Transport for Differential Gene Regulatory Network Inference with Unpaired Samples',
    long_description=long_description,  # Add the README content
    long_description_content_type="text/markdown",  # Specify the content type (Markdown)
    author='Mengyu Li',
    author_email='limengyu516@ruc.edu.cn',
    url='https://github.com/Mengyu8042/ot_grn',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'scikit-learn',
        'pot',  # Python Optimal Transport library
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    python_requires='>=3.7', 
)
