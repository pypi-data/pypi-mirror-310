from setuptools import setup, find_packages

setup(
	name="backupper-lf23",
	version="1.1.0",
	description="Un semplice Python script per gestire i backups",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	author="Luca Ferrari",
	author_email="luca10.ferrari@edu.unife.it",
	url="https://github.com/lucaf23/backupper",
	packages=find_packages(),
	py_modules=["backupper"],
	entry_points={
		"console_scripts": [
			"backupper-lf23=backupper.backupper:main",
		],
	},
	install_requires=[ "pyzipper" ],
	license="MIT",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires=">=3.6",
)
