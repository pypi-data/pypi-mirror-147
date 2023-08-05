from setuptools import setup, find_packages


necessary_dependencies = [
    # 'pytest',
]
testing_dependencies = [
    'pylint',
    'pytest'
]

setup(  name='jidutest-framework',
        version='0.1',
        description='JiduTest framework',
        # url='git@jidudev.com:ee/jidutest/jidutest-sdk/jidutest-framework.git',
        author='ee',
        author_email='ee@jiduauto.com',
        license='MIT',
        packages=find_packages(exclude=['doc', 'test']),
        install_requires=necessary_dependencies,
        test_suite='test',
        tests_require=testing_dependencies,
        zip_safe=False
    )
