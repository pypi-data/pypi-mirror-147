import os
from setuptools import setup

PACKAGE = "allure-pytest-bdd-temp"

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Framework :: Pytest',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Topic :: Software Development :: Quality Assurance',
    'Topic :: Software Development :: Testing',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
]

setup_requires = [
    "setuptools_scm"
]

install_requires = [
    "pytest>=4.5.0",
    "pytest-bdd>=3.0.0",
    "six>=1.9.0",
    "allure-python-commons==2.9.45"
]

def get_readme(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def main():
    setup(
        name=PACKAGE,
        version='2.9.46',
        description="Temporary repo till PR is merged #644",
        url="https://github.com/popescunsergiu/allure-python-temp",
        author="QAMetaSoftware, Stanislav Seliverstov",
        author_email="sseliverstov@qameta.io",
        license="Apache-2.0",
        classifiers=classifiers,
        keywords="allure reporting pytest",
        long_description=get_readme('README.rst'),
        packages=["allure_pytest_bdd"],
        package_dir={"allure_pytest_bdd": "src"},
        entry_points={"pytest11": ["allure_pytest_bdd = allure_pytest_bdd.plugin"]},
        setup_requires=setup_requires,
        install_requires=install_requires
    )


if __name__ == '__main__':
    main()
