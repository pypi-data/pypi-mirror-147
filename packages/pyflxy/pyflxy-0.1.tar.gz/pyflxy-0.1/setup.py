from setuptools import setup, find_packages


setup(
    name='pyflxy',
    version='0.1',
    license='MIT',
    author="Sourav Suresh",
    author_email='souravs0506@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/souravsuresh/pyflxy.git',
    keywords='pyflxy',
    install_requires=[
        'requests',
    ],
)
