from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))
PROJECT_NAME = 'artifactoryAPI'
PROJECT_AUTHORS = 'LB'
PROJECT_EMAILS = '423497786@qq.com'
PROJECT_URL = 'https://github.com/lb423497786/artifactory'
SHORT_DESCRIPTION = (
    'A API for accessing resources on artifactory '
)

#GLOBAL_ENTRY_POINTS = {
#    'console_scripts': [
#        'artifactory_version=baiduapi.bpcs_operation:getVersion',
#    ]
#}

# Get version
try:
	with open(os.path.join(here, 'VERSION.txt')) as f:
		VERSION = f.read()
except IOError:
    VERSION = 1.0
	
# Get the long description from the relevant file
try:
	with open(os.path.join(here, 'README.rst')) as f:
		DESCRIPTION = f.read()
except IOError:
    DESCRIPTION = SHORT_DESCRIPTION
	
setup(
    name=PROJECT_NAME.lower(),
    version=VERSION,
    author=PROJECT_AUTHORS,
    author_email=PROJECT_EMAILS,
    description=SHORT_DESCRIPTION,
    long_description=DESCRIPTION,
	install_requires=[
        'requests>=2.9,<2.99'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    #zip_safe=True,
    #entry_points=GLOBAL_ENTRY_POINTS,
    url=PROJECT_URL,
	data_files=[],
    license='MIT',
    #classifiers=[
    #    'Development Status :: 4 - Beta',
    #    'Environment :: Console',
    #    'Intended Audience :: Developers',
    #    'License :: OSI Approved :: MIT License',
    #    'Natural Language :: English',
    #    'Operating System :: OS Independent',
    #    'Programming Language :: Python :: 2.7',
    #    'Programming Language :: Python :: 3.3',
    #    'Programming Language :: Python :: 3.4',
    #    'Topic :: Software Development :: Testing',
    #],
)
