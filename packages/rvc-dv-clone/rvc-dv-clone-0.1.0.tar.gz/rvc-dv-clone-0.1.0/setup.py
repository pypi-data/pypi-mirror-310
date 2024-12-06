from setuptools import setup, find_packages

setup(
    name="rvc-dv-clone",
    version="0.1.0",
    description="Retrieval-based Voice Conversion library",
    author="Original: RVC-Project, Package: Alakxender",
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
        "pyyaml"
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "rvc_dv_clone": ["*.yaml", "*.json", "configs/*"],
    },
)