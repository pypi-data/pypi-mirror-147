from setuptools import setup

setup(
    name='tbplots',
    version='0.1.0',
    description='A Python Package used to load data from Tensorboard Logs and Plot them.',
    url='https://github.com/Tran-Research-Group/TB-Plots',
    author='Stephen Hudson',
    author_email='shudson@anl.gov',
    license='BSD 2-clause',
    packages=['tbplots'],
    install_requires=['tensorboard',
                      'numpy',
                      'scipy',
                      'matplotlib',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
