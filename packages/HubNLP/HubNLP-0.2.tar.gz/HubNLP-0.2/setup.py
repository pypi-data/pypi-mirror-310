from setuptools import setup, find_packages

setup(
    name="HubNLP",  # Package name
    version="0.2",  # Initial version
    author="Self-nasu",
    author_email="nexiotech.2024@gmail.com",
    description="A simple NLP utility library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Self-nasu/HubNLP",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pandas",
        "sklearn-crfsuite",
        "seqeval",
        "datasets",
        "transformers",
        "torch",
        "tf-keras",
    ],
)
