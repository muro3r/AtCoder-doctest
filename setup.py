from setuptools import find_packages, setup

setup(
    name="atcoder-doctest",
    version="0.0.1",
    description="Generate texts from AtCoder problem page.",
    url="https://github.com/muro3r/AtCoder-doctest/",
    install_requires=["beautifulsoup4", "requests"],
    packages=find_packages(),
    entry_points={
        "console_scripts": ["atcoder-doctest=atcoder_doctest.atcoder_doctest:main"]
    },
)
