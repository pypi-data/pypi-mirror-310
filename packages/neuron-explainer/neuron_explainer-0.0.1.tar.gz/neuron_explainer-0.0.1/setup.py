from setuptools import setup, find_packages

setup(
    name="neuron_explainer",  # The name of the package
    version="0.0.1",
    author="OpenAI",
    description="A package for neuron activations and explanations",
    url="",  # Add your project's URL or GitHub repository link if available
    packages=find_packages(),  # Automatically discover all packages in the directory
    install_requires=[
        "httpx>=0.22",
        "scikit-learn",
        "boostedblob>=0.13.0",
        "tiktoken",
        "blobfile",
        "numpy",
        "pytest",
        "orjson",
    ],
    python_requires=">=3.9",  # Ensure Python version compatibility
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
