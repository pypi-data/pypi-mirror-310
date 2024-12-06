import setuptools

def readfile(filename):
    with open(filename, 'r', encoding='latin1') as f:
        return f.read()

setuptools.setup(    
    name="chelydra",
    version=readfile('version.txt'),
    author="Erick Fernando Mora Ramirez",
    author_email="erickfernandomoraramirez@gmail.com",
    description="A zip based backup-restore tool",
    long_description=readfile('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/LostSavannah/chelydra",
    project_urls={
        "Bug Tracker": "https://dev.moradev.dev/chelydra/issues",
        "Documentation": "https://dev.moradev.dev/chelydra/documentation",
        "Examples": "https://dev.moradev.dev/chelydra/examples",
    },
    package_data={
        "":["*.txt"]
    },
    classifiers=[
    "Programming Language :: Python :: 3",
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)