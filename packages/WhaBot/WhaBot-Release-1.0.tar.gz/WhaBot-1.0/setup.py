import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WhaBot",
    version="1.0",
    author="Lanfran02",
    author_email="joacolanfran+pypi@gmail.com",
    description="The (not so official) WhatsApp automation framework!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lanfran02/WhaBot",
    project_urls={
        "Bug Tracker": "https://github.com/lanfran02/WhaBot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        'selenium',
        'Pillow',
        'beautifulsoup4'
    ],
)