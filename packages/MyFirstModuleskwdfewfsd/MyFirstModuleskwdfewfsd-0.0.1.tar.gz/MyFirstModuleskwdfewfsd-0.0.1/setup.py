from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='MyFirstModuleskwdfewfsd',
    version='0.0.1',
    description='Very short desc',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url= '',
    author='CookiesKush420',
    author_email='cookies@mail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)