from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="rvc-dv-clone",
    version="0.4.0",
    description="Retrieval-based Voice Conversion library",
    author="Alakxender",
    author_email="alakxender@gmail.com",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        "numpy",
        "scipy",
        "librosa",
        "fairseq",
        "ffmpeg-python",
        "soundfile",
        "pyworld",
        "faiss-cpu",
        "torchcrepe",
        "pyyaml",
        "praat-parselmouth",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "rvc_dv_clone": ["*.yaml", "*.json", "configs/*"],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
