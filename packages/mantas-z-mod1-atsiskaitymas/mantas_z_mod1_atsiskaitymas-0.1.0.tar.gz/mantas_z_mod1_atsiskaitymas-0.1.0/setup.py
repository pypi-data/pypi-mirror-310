from setuptools import setup, find_packages

setup(
    name="mantas_z_mod1_atsiskaitymas",
    version="0.1.0",
    author="Mantas",
    author_email="",
    packages=find_packages(),
    install_requires=[
    "certifi==2024.8.30",
    "charset-normalizer==3.4.0",
    "idna==3.10",
    "lxml==5.3.0",
    "requests==2.32.3",
    "setuptools==75.5.0",
    "urllib3==2.2.3"
    ],
    python_requires=">=3.10"
)

# twine sukelimui į PyPi