import sys
from setuptools import setup, find_packages


# Default install_requires
install_requires = [
    "numpy==2.1.3",
    "requests",
    "gdown==5.2.0",
    "bitsandbytes==0.44.1",
    "accelerate==1.1.1",
    "transformers",
]

# Add GPU-supported PyTorch by default
gpu_requirements = [
    "torch==2.5.1+cu121",
    "torchvision==0.20.1+cu121",
    "torchaudio==2.5.1+cu121",
]

cpu_requirements = [
    "torch==2.5.1+cpu",
    "torchvision==0.20.1+cpu",
    "torchaudio==2.5.1+cpu",
]

# Detect if [cpu] is explicitly requested
if "cpu" in sys.argv:
    # Remove the "cpu" argument from sys.argv to prevent installation issues
    sys.argv.remove("cpu")
    print("Installing CPU-only PyTorch dependencies...")
    install_requires += cpu_requirements
else:
    print("Installing GPU-supported PyTorch dependencies by default...")
    install_requires += gpu_requirements




setup(
    name='iges-sentence-splitter',
    version='0.1.10',
    description='A package for sentence splitting using a pre-trained transformer model.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kathryn Chapman',
    author_email='kathryn.chapman@iges.com',
    url='https://github.com/kathrynchapman/sentence_splitter',
    packages=find_packages(),
    package_data={
        'sentence_splitter': ['model/*'],  # Include model files
    },
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
