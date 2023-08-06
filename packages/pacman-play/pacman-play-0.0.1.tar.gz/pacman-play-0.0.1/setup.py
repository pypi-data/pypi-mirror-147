import setuptools


with open("README.md", "r") as fp:
    long_description = fp.read()

with open("requirements.txt", "r") as fp:
    requirements = fp.read().strip().split("\n")

setuptools.setup(
    name="pacman-play",
    version="0.0.1",
    author="Patrick Huang",
    author_email="phuang1024@gmail.com",
    description="Pacman game in terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phuang1024/pacman",
    py_modules=["pacman"],
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pacman-play = pacman.main:run",
        ]
    },
)
