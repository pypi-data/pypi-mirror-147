
from setuptools import setup, find_packages

setup(
    name='RedTaban',
    version='0.2',
    author='HasanSencer',
    author_email='sencerrhs17@icloud.com',
    description = 'Redstone Arayüz Teması',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'nexus>=0.1.1',
    ],
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)