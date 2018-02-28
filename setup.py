from setuptools import find_packages, setup

setup(
    name='cspobject',
    description='An object-oriented representation of Content Security Policies',
    url='https://github.com/adambrenecki/cspobject',
    author='Adam Brenecki',
    author_email='adam@brenecki.id.au',
    license='MIT',
    setup_requires=["setuptools_scm>=1.11.1"],
    use_scm_version=True,
    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'attrs>=17.2.0,<18',
    ],
    extras_require={
        'dev': [
            'pytest',
            'prospector',
            'hypothesis>=3.24.1,<3.25',
            'hypothesis-pytest',
            'sphinx==1.6.7',
            'sphinx-rtd-theme==0.2.4',
        ],
        'dev-django': [
            'django',
            'pytest-django==3.1.2',
        ]
    },
)
