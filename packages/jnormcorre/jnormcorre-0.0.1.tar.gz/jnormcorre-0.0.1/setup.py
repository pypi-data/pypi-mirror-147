import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="jnormcorre",
    version="0.0.1",
    description="Jax-accelerated implementation of normcorre",
    packages=setuptools.find_packages(),
    install_requires=["future","numpy", "scipy", "h5py", "tqdm", "matplotlib", "opencv", "tifffile", "typing", "pynwb", "pillow", "scikit-image", "jax[cpu]", "scikit-image"],
    classifiers=(
        "Programming Language :: Python :: 3",
    ),
)