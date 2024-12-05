from setuptools import setup, find_packages

setup(
    name='AuthValid',
    version='0.1',
    packages=find_packages(),
    description='A package for JWT token management and authentication',
    author='Mohammad Ridzwan Syah bin Irwan',
    author_email='ridzwansyahirwan@gmail.com',
    url='https://github.com/ridzwansyahirwan/AuthValid.git',
    install_requires=[
        'Flask',
        'python-dotenv',
        'PyJWT',
    ],
)