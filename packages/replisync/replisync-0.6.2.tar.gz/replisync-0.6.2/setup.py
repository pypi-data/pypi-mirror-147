import os

from setuptools import (
    setup,
)


BASE_PATH = os.path.abspath(os.path.dirname(__file__))


# Get the long description from the README file
with open(os.path.join(BASE_PATH, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(os.path.join(BASE_PATH, 'CHANGES.md'), encoding='utf-8') as f:
    long_description = f'{long_description}\nВерсии\n\n {f.read()}'

# get the dependencies and installs
with open(os.path.join(BASE_PATH, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [
    x.strip()
    for x in all_reqs if
    'git+' not in x
]
dependency_links = [
    x.strip().replace('git+', '')
    for x in all_reqs if
    x.startswith('git+')
]


setup(
    name='replisync',
    version='0.6.2',
    description='Транслятор репликации в задачи Celery',
    license='MIT',
    author='BARS Group',
    author_email='kirov@bars-open.ru',
    url='https://stash.bars-open.ru/projects/BUDG/repos/replisync',
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
    ],
    packages=['replisync'],
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    dependency_links=dependency_links,
    entry_points={
        'console_scripts': ['replisync=replisync.start:main'],
    },
)
