import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="microbit-3",
    version="0.0.1",
    author="Phoneguytech",
    description="Microbit for Python 3",
    # long_description=long_description,
    install_requires=["pyserial"]
)
