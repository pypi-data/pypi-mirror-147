import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezgame-VP_Dev",
    version="0.0.1",
    author="VP_Dev",
    author_email="vinhphucflash@gmail.com",
    description="A small ezgame package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MineDark909/ezgame.py",
    project_urls={
        "Bug Tracker": "https://github.com/MineDark909/ezgame.py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)