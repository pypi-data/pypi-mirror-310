from setuptools import setup, find_packages

setup(
    name='TokenForge',
    version='0.3',
    packages=find_packages(),
    description='A package for JWT token management and authentication',
    author='Mohammad Ridzwan Syah bin Irwan',
    author_email='ridzwansyahirwan@gmail.com',
    url='https://github.com/ridzwansyahirwan/TokenForge.git',
    install_requires=[
        'Flask',
        'python-dotenv',
        'PyJWT',
    ],
)