from setuptools import setup, find_packages


setup(
    name="omnicrawls",  # Replace with your library's name
    version="2.1",
    author="Vinayak Pratap Rana",
    author_email="perrcroshado@gmail.com",
    description="A Python library for crawling LinkedIn data and GitHub repos and scrap websites.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # List any external dependencies here, e.g.:
        "requests",
        "bs4",
        "selenium",
        "webdriver_manager",
        "python-dotenv",

    ],

)
