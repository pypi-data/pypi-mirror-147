import setuptools
with open("README.md", "r") as fh:
	long_description = fh.read()

# requirements = ["requests<=2.21.0"]

setuptools.setup(
	name="wot_alexaltai",
	version="0.0.1",
	author="Alex Altaitsev",
	author_email="altaitsiev@gmail.com",
	description="WoT Build Simple Game",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/AlexAltaitsev/WoT",
	packages=setuptools.find_packages(),
    # install_requires=requirements,
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],

	python_requires='>=3.6',
)
