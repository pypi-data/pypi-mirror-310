from setuptools import setup,find_packages
setup(
    name='devinmodone',                  # Package name
    version='0.1.0',                   # Version
    description='A sample Python module',
    author='Devin Mathew',
    author_email='devin@gofreelab.com',
    packages=find_packages(),          # Automatically find modules
    install_requires=[],               # Dependencies (if any)
    python_requires='>=3.6',           # Supported Python versions
)

