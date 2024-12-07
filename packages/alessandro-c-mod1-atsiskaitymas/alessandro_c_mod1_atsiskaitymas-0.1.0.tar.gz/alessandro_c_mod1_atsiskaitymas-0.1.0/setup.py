import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alessandro_c_mod1_atsiskaitymas",
    version="0.1.0",
    author="Alessandro Caliva",
    author_email="calivaalessandro@gmail.com",
    description="Web crawler",
    url="https://github.com/ales-sandrito/alessandro-c-mod1-atsiskaitymas",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        'certifi==2024.8.30',
        'charset-normalizer==3.4.0',
        'idna==3.10',
        'lxml==5.3.0',
        'pip==23.2.1',
        'requests==2.32.3',
        'setuptools==75.5.0',
        'soupsieve==2.6',
        'urllib3==2.2.3',
        'wheel==0.45.1',
        'twine==5.1.1',
    ],
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.10"
)