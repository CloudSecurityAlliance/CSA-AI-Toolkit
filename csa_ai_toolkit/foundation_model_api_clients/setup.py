from setuptools import setup, find_packages

setup(
    name='foundation_model_api_clients',
    version='0.1.0',
    description='API client modules for CSA AI Toolkit',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CloudSecurityAlliance/CSA-AI-Toolkit',
    author='Kurt Seifried',
    author_email='kseifried@cloudsecurityalliance.org',
    license='LICENSE',
    packages=find_packages(),
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License'
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='AI, machine learning, API clients',
)
