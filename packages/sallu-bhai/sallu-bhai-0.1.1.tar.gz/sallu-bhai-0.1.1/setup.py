from setuptools import setup, find_packages

setup(
    name="sallu-bhai",
    version="0.1.1",
    description="The library for converting your boring innnocous natural language into CLI commands.",
    author="Sudarsh Chaturvedi",
    author_email="chaturvedi.sudarsh@gmail.com",
    packages=find_packages(),
    install_requires=[
        "ollama>=0.1.0"
    ],
     entry_points={
        "console_scripts": [
            "sallu-bhai=optimus_prime.cli_tool:main"  # Update path to match your CLI script
        ]
    },


    python_requires=">=3.7",
)
