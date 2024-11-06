from setuptools import setup

setup(
    name="goalz",  
    version="0.1",
    py_modules=["goals"],  
    install_requires=["rich>=13.0.0", "click>=8.0.0"],  
    entry_points={
        "console_scripts": [
            "goalz=goals:main", 
        ],
    },
    author="Mahe Iram Khan",
    author_email="your.email@example.com",
    description="A simple CLI for managing goals and tasks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ForgottenProgramme/goalz",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)