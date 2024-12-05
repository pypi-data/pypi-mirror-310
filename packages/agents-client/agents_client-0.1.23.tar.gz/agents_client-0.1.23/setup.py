from setuptools import setup, find_packages

setup(
    name='agents-client',
    version='0.1.23',
    description='A client library for interacting with the Agents API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Levangie Laboratories',
    author_email='brayden@levangielaboratories.com',
    url='https://github.com/Levangie-Laboratories/agents-client',
    packages=find_packages(exclude=['tests*', 'cookbook*']),
    python_requires='>=3.8',
    install_requires=[
        'requests>=2.25.0',
        'aiohttp>=3.8.0',
        'python-dotenv>=0.19.0',
        'pydantic>=1.8.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-asyncio>=0.18.0',
            'black>=22.0.0',
            'isort>=5.0.0',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='agents, api, client, chatbot, ai',
)