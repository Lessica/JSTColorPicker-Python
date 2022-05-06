from setuptools import find_packages, setup

readme_file = open('README.rst', 'rt').read()

dev_requirements = [
    'mypy==0.931',
    'pylint==2.12.2',
]

setup(
    name='jstcolorpicker',
    version='0.1.0',
    author='Lessica',
    author_email='82flex@gmail.com',
    packages=find_packages(),
    scripts=['pixelexif.py'],
    url='https://github.com/Lessica/JSTColorPicker-Python',
    license='BSD 2-clause',
    keywords='exif image metadata photo jstcolorpicker',
    description='Extract JSTColorPicker annotation data models from metadata of bitmap images.',
    long_description=readme_file,
    install_requires=[
        'bpylist2 @ git+https://github.com/Lessica/bpylist2.git@dot-to-camel#egg=bpylist2',
        'ExifRead @ git+https://github.com/Lessica/exif-py.git@develop#egg=ExifRead',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
    ],
    extras_require={
        'dev': dev_requirements,
    },
)

