from setuptools import setup, find_packages

with open("README.md", "r") as file:
	readme = file.read()

setup(
	name = 'kernel_knockoffs',
	packages = find_packages(),
	package_dir = {'kernel_knockoffs': 'kernel_knockoffs'},
	version = '0.1',
	description = 'Kernel-based knockoff procedure.',
	long_description=readme,
	long_description_content_type='text/markdown',
	author = 'Héctor Climente-González',
	author_email = 'hector.climente@riken.jp',
	license = 'GPL-3',
	url = 'https://github.com/hclimente/kernel_knockoffs',
	keywords = ['fdr', 'feature_selection', 'kernel', 'knockoffs', 'hsic', 'mmd'],
	classifiers = [
        'Development Status :: 3 - Alpha',
		'Topic :: Scientific/Engineering :: Mathematics',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3 :: Only'],
	install_requires = [
		'sklearn >= 1.0.2',
		'numpy >= 1.21.5'],
)
