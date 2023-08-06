import setuptools

file = open("README.md")
long_description = file.read()
file.close()

setuptools.setup(
	name="PySimpleTest",
	version="1.0.3",
	author="Time-Coder",
	author_email="binghui.wang@foxmail.com",
	description="A very simple test framework",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/Time-Coder/PySimpleTest",
	packages=setuptools.find_packages(),
	install_requires=[
		"PySimpleGUI",
		"pywin32",
		"pypiwin32",
		"pyttsx3"
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: Microsoft :: Windows"
	],
)