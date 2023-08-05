from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='valdezds',
    version='0.0.1',
    description='Some tweaks and stuff to be more productive',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Omar Valdez',
    author_email='info@valdezdata.com',
    license='MIT',
    classifiers=classifiers,
    keywords='view_df',
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'rich']
)