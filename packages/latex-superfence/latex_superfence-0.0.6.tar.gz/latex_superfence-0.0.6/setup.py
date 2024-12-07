from setuptools import setup, find_packages

setup(
    name='latex_superfence',
    version='0.0.6',
    py_modules=['latex_superfence'],
    author='Davy Cottet',
    description='A superfence pymarkdown extension to convert tex code to svg',
    url='https://latex-superfence.gitlab.io',
    license='GNU General Public License v3.0',
    platforms=['Any'],
    install_requires=[
          'markdown',
          'pymdown-extensions'
      ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
)


