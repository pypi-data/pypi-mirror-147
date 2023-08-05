from setuptools import setup, find_packages


setup(
    name='Example_game',
    version='1.0',
    license='MIT',
    author="Nikita Neilko",
    author_email='nikita.carasevitch@yandex.by',
    packages=find_packages('src'),
    package_dir={'tank': 'src'},
    url='https://github.com/Karasik99/tank',
    keywords='example project',
    install_requires=[
          'scikit-learn',
      ],

)
