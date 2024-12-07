import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name="phidget22",
    version='1.21.20241125',
    author="Phidgets Inc",
    author_email="support@phidgets.com",
    description="Phidget22 Python wrapper library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.phidgets.com",
    packages=setuptools.find_packages(),
    package_data={"Phidget22": [".libs/*"]},
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
