from setuptools import setup, find_packages


setup(
    name='aquantresearch',
    version='0.2',
    license='Aquant',
    author="Amir Dafnai",
    author_email='amirdafnai@aquant.io',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/AquantIO/AquantReasearch',
    keywords='example project'

)