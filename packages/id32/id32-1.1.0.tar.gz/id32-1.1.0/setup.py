from setuptools import setup, find_packages

setup(
    name='id32',
    version='1.1.0',
    author='kahnpoint',
    author_email='96557890+kahnpoint@users.noreply.github.com',
    description='32-character RFC 4648 lowercase Base32 IDs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kahnpoint/id32',
    packages=find_packages(),
    keywords=['id', 'id32', 'uuid', 'nanoid', 'base32'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)