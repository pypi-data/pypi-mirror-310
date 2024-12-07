from setuptools import find_packages, setup

with open("app/README.md", "r") as f:
    long_description = f.read()

"""
pypi-AgEIcHlwaS5vcmcCJDY0YzU1M2FmLTJhYmYtNDNlNy04Y2JiLTVmY2VkNjA2NWM5ZgACKlszLCI0ODg1NTdjNi04OThjLTQ5YjMtYWU4ZC1kNTY1NmY0MThjMDciXQAABiA7RJ8lMQ0JD4-kiZ-oaqbL0S5kyLUFphk3XmqVg3Tbwg
"""
setup(
    name="opencv_statistical_tools",
    version="0.1.4",
    description="An OpenCV utility package for additional utility functions for probability and statistical operations.",
    package_dir={"": "app"},
    include_package_data=True,
    package_data={'': ['Scenes/*']},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArjanCodes/2023-package",
    author="Stephen Hudson",
    author_email="arjan@arjancodes.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["opencv-python>=4.5.3", "numpy>=1.21.0"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.6",
)
