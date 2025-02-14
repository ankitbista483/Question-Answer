from setuptools import find_packages, setup

Hypen_e_dot = '-e .'

def get_requirements(file_path: str) -> list[str]:
    requirements = []
    with open(file_path) as f:
        requirements = [req.replace('\n', ' ') for req in f.readlines()]

    if Hypen_e_dot in requirements:
        requirements.remove(Hypen_e_dot)

    return requirements

setup(
    name='QUESTION-ANSWER',
    version='0.0.1',
    author='Ankit Bista',
    author_email='ankitbista1406@gmail.com',
    packages=find_packages(),  
    install_requires=get_requirements('requirements.txt'),
)
