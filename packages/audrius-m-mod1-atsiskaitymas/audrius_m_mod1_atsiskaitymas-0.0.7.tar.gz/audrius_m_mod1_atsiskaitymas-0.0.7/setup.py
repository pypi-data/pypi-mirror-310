import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="audrius_m_mod1_atsiskaitymas",
    version="0.0.7",
    author="Audrius M",
    author_email="balvakokay@gmail.com",
    description="Website crawler",
    long_description=long_description,
    url="https://github.com/audriu/audrius-m-mod1-atsiskaitymas",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests==2.32.3',
        'requests-toolbelt==1.0.0',
        'bs4==0.0.2'
    ],
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.10"
)
