"""
py setup.py sdist
twine upload dist/expressmoney-8.8.3.tar.gz
twine upload dist/points-0.0.1.tar.gz
"""
import setuptools

# setuptools.setup(
#     name='expressmoney',
#     packages=setuptools.find_packages(),
#     version='8.8.3',
#     description='SDK ExpressMoney',
#     author='Development team',
#     author_email='dev@expressmoney.com',
#     install_requires=('requests', 'google-cloud-error-reporting', 'google-cloud-tasks'),
#     python_requires='>=3.7',
# )

setuptools.setup(
    name='expressmoney-points',
    packages=setuptools.find_packages(),
    version='0.0.1',
    description='Service points',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=('expressmoney',),
    python_requires='>=3.7',
)
