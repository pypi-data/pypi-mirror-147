from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
	name='cuda_hybrid',
	version='0.1.2',
	license='GPL-3.0-only',
	author="Kareem Ghumrawi",
	author_email="kghumrawi@gmail.com",
	description="Runs ABM/FCM hybrid models on CUDA cores to drastically reduce runtime.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	packages=find_packages('src'),
	package_dir={'': 'src'},
	url="https://gitlab.csi.miamioh.edu/620_final/cse620c_finalproject/-/tree/add-docs",
	project_urls={
		"Documentation": "https://cuda-hybrid.github.io/",
	},
	python_requires=">=3.7",
)