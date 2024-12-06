from setuptools import setup, find_packages
# python setup.py sdist bdist_wheel
# twine upload dist/*
setup(
    name='ttlinks',
    version='0.3.1',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.txt', '*.json', '*.csv']},
    license='MIT',
    description='TTLinks Network Service Packages',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yantao Tao',
    author_email='tytccie@gmail.com',
    url='https://github.com/tyt063144/TTLinks.git',
    install_requires=[
        'inflect'
    ],
    keywords=['network', 'ttlinks', 'networking', 'automation',
              'ip', 'mac', 'python', 'wildcard', 'subnet', 'network automation'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Telecommunications Industry",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Networking",
    ]
)