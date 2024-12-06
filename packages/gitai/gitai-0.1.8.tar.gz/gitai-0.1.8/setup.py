from setuptools import setup, find_packages
import yaml
import re

setup(
    name='gitai',
    version='0.1.8',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
		'langchain',
		'python-dotenv',
		'click',
		'langchain-openai',
		'langchainhub',
		'asyncio',
	],
    entry_points='''
        [console_scripts]
        gitai=gitai.main:main
		gitai-agent=gitai.agent:main
    ''',
)
