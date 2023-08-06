from setuptools import setup, find_packages

setup(
    name='django_sso',
    version='1.0.1',
    author="DAVIDhaker",
    author_email='me@davidhaker.ru',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/davidhaker/django-sso',
    keywords='Django SSO Single Sign-On',
    install_requires=[
        'django',
        'requests',
    ],
    python_requires='>=3',
)
