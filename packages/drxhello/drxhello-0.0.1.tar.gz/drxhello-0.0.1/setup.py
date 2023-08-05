from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='drxhello',
    version='0.0.1',
    description='drxhello',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='drewxa',
    author_email='drewxa@gmail.com',
    keywords=['helloworld', 'drewxa'],
    url='https://github.com/drewxa/pypi-test',
    download_url='https://pypi.org/project/drxhello/'
)

install_requires = [
    'request'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)