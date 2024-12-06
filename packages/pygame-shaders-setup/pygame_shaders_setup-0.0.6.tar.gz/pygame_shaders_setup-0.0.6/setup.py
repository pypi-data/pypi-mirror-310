from setuptools import setup, find_packages

setup(
    name="pygame_shaders_setup",              # Replace with your package name
    version="0.0.6",                # Package version
    packages=find_packages(),       # Automatically find sub-packages
    description="Basic window class for pygame_shaders", # Short description
    python_requires=">=3.6",
    install_requires= [
        "moderngl==5.8.2",
        "numpy>=2.0.0,<3.0.0",
    ]
)
