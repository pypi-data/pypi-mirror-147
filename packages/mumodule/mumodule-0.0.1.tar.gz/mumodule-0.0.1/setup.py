from setuptools import setup, find_packages

classifiers = {
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
}

setup(
    name='mumodule',
    version='0.0.1',
    description='A short summary about your package',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    author='Álvaro Navarro',
    author_email='alvaro.nl@ua.es',
    license='MIT',
    classifiers=classifiers,
    keywords='',
    packages=find_packages(),
    install_requires=['']
)