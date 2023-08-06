#!/usr/bin/env python
import setuptools

setuptools.setup(name='lbg',
                 version='1.0.1',
                 description='Lebesgue Utility',
                 author='DP Technology',
                 packages=setuptools.find_packages(),
                 author_email='baixk@dp.tech',
                 url='https://lebesgue.dp.tech/#/',
                 python_requires='>=3.7',
                 install_requires=['oss2', 'requests', 'requests-toolbelt', 'aliyun-python-sdk-core',
                                   'aliyun-python-sdk-kms', 'aliyun-python-sdk-sts', 'tqdm', 'pytimeparse', 'pyyaml',
                                   'pandas', 'colorama', 'readchar', 'pyreadline3', 'validators'],
                 entry_points={
                     'console_scripts': [
                         'lbg=lbgcli.main_entry:main',
                         'lebesgue=lebesgue_sdk.cmd:main'
                     ]
                 }
                 )
