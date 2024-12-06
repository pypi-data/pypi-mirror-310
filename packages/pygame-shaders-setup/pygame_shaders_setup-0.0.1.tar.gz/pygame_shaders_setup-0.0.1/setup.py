from setuptools import setup, find_packages

setup(
    name="pygame_shaders_setup",              # Replace with your package name
    version="0.0.1",                # Package version
    packages=find_packages(),       # Automatically find sub-packages
    description="Basic window class for pygame_shaders", # Short description
    python_requires=">=3.6",
    install_requires= [
        "pygame_shaders>=1.0.9",
        "moderngl==5.8.2",
        "numpy==2.0.0"
    ]
)
