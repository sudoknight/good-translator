from setuptools import find_packages, setup

DESCRIPTION = "Good Translator - Google + Offline mode"
LONG_DESCRIPTION = (
    "This wrapper supports translation through Google and Offline models."
)

setup(
    name="good_translator",
    version=0.2,
    author="Hassan Ghalib",
    author_email="hassan.best01@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=["good_translator"],
    python_requires=">=3.7",
    install_requires=[
        "torch",
        "deep-translator==1.11.4",
        "transformers==4.40.0",
        "huggingface-hub==0.22.2",
        "fasttext==0.9.2",
        "sentencepiece==0.2.0",
        "numpy==1.26.4",
    ],
    keywords=["python", "translator", "google", "offline"],
)
