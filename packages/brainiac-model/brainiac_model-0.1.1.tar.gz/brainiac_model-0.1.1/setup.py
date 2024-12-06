from setuptools import setup, find_packages

setup(
    name="brainiac-model",
    version="0.1.1",
    author="Divyanshu",
    description="A 3D ResNet50 model for brain MRI analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://huggingface.co/Divytak/brainiac",
    packages=find_packages(),
    install_requires=[
        "torch>=1.9.0",
        "transformers>=4.20.0",
        "monai>=1.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)