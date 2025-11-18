from setuptools import setup

setup(
    name='hostedsms-api',
    version='1.1.0',
    description='Python library for sending SMS via HostedSMS.pl',
    author='dcs.pl',
    author_email='info@dcs.pl',
    url='https://github.com/dcs-pl/hostedsms-python',
    packages=['hostedsms'],
    license='Apache v2 License',
    install_requires=[
        'suds >= 1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
)
