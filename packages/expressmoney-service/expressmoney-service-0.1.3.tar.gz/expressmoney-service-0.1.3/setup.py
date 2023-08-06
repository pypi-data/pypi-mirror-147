"""
py setup.py sdist
twine upload dist/expressmoney-service-0.1.3.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney-service',
    packages=setuptools.find_packages(),
    version='0.1.3',
    description='Remote services',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=('expressmoney',),
    python_requires='>=3.7',
)
