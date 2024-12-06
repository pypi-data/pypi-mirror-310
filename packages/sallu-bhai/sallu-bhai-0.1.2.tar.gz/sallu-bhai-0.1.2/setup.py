from setuptools import setup, find_packages

setup(
    name="sallu-bhai",
    version="0.1.2",
    description="The library for converting your boring innnocous natural language into CLI commands.",
    author="Sudarsh Chaturvedi",
    author_email="chaturvedi.sudarsh@gmail.com",
    packages=find_packages(),  # Automatically find the 'sallu_bhai' package
    entry_points={
        "console_scripts": [
            "sallu-bhai=sallu_bhai.cli_tool:main"
        ]
    },
    python_requires=">=3.7",
    install_requires=[
        "ollama>=0.1.0"
    ],
)
