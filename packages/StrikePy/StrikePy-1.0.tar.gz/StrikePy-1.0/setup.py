import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='StrikePy',
    version='1.0',
    author='David Rey Rostro',
    author_email='davidreyrostro@gmail.com',
    description='A package for observability and identifiability analysis of non-linear systems ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/afvillaverde/StrikePy',
    download_url='https://github.com/afvillaverde/StrikePy',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    install_requires=['numpy', 'sympy', 'symbtools'],
    python_requires='>=3.9',
    keywords=['StrikePy','STRIKE-GOLDD','analysis','non-linear','observability','identifiability','dynamic modelling','biosystems'],
    package_dir={'StrikePy': 'StrikePy'},
    include_package_data = True
)