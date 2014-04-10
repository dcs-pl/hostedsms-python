try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='hostedsms-api',
    version='0.01a1',
    description='Python library for sending SMS via HostedSMS.pl',
    author='dcs.pl',
    author_email='info@dcs.pl',
    url='https://github.com/dcs-pl/hostedsms-python',
    packages=['hostedsms'],
    license='Apache v2 License',
    install_requires=[
        "suds-jurko == 0.6",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
