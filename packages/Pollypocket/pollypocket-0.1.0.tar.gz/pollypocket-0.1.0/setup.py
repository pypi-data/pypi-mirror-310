from setuptools import setup, find_packages

setup(
    name="Pollypocket",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["sympy"],
    test_suite="tests",
    author="Alejandro J. Hernández P., Elvira E. Florez C., Vanessa Orozco M.",
    author_email="",
    description="A Python library for polynomial interpolation, including Lagrange interpolation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/adechlien/pollypocket",
    python_requires='>=3.10.2',
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
