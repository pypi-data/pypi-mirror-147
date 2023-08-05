from setuptools import setup, find_packages


setup(
    name='test-app-hleb',
    version='1.0',
    author="Hleb Serafimovich",
    author_email='hleb.serafimovich@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
)