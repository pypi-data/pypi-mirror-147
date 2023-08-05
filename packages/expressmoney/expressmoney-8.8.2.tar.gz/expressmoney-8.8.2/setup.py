"""
py setup.py sdist
twine upload dist/expressmoney-8.8.2.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney',
    packages=setuptools.find_packages(),
    version='8.8.2',
    description='SDK ExpressMoney',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=('requests', 'google-cloud-error-reporting', 'google-cloud-tasks'),
    python_requires='>=3.7',
)
