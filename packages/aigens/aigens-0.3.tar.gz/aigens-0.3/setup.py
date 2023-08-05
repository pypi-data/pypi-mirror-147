from setuptools import setup, find_packages  # type: ignore


setup(
    name='aigens',
    license='MIT',
    author='TryCrime',
    author_email='lol@trycri.me',
    url='https://bitbucket.org/trycrimegroup/aigens/',
    keywords='rapidapi text generation',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['requests',],
)
