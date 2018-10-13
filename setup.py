import setuptools

with open("README.md", "r") as file:
	long_description = file.read()

setuptools.setup(
	name="holland",
	version="0.0.2",
	author="Lambda Life",
	author_email="lambdalife@henrywoody.com",
	description="Genetic Algorithm Library",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/lambdalife/holland",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
	]
)