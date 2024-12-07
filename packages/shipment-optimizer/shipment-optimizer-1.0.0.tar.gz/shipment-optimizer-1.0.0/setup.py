from setuptools import setup, find_packages

setup(
    name='shipment-optimizer',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[],
    description='Optimize shipment assignments in logistics projects.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/yourusername/shipment-optimizer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
