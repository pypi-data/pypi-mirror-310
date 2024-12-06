# coding=UTF-8
"""Setup for the pipy package"""
import setuptools

with open('README.md', 'r', encoding='utf-8') as long_description_f:
	long_description = long_description_f.read()

setuptools.setup(
  name = 'diematic_server',
  version = '3.1',
  description = 'Unix daemon and supporting models for publishing data from Diematic DeDietrich boiler',
	long_description = long_description,
	long_description_content_type = 'text/markdown; charset=UTF-8',
  author = 'Ignacio Hernández-Ros',
  author_email = 'ignacio@hernandez-ros.com',
  packages = ['diematic_server'],
  license='MIT',
  url = 'https://github.com/IgnacioHR/diematic_server',
  download_url = 'https://github.com/IgnacioHR/diematic_server/archive/refs/tags/v3.1.tar.gz',
  keywords = ['python', 'home-automation', 'iot', 'influxdb', 'restful', 'modbus', 'de-dietrich', 'diematic', 'mqtt'],
  install_requires=[
					'daemon==1.2',
					'influxdb==5.2.3',
					'pymodbus==2.2.0',
					'python-daemon==2.3.0',
					'PyYAML==6.0.2',
					'aiohttp==3.11.2',
          'paho-mqtt==2.1.0',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
		'Environment :: No Input/Output (Daemon)',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
		'Operating System :: Unix',
    'Programming Language :: Python :: 3.11',
		'Topic :: Home Automation',
	],
)