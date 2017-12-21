from setuptools import setup


setup(name='python-recipes',
      version='0.0.1',
      description='Some useful code snippets',
      author='Full name',
      author_email='some_email@domain.com',
      url='PUT URL HERE',
      packages=['recipes'],
      package_dir={'recipes': 'recipes'},
      package_data={
          'recipes': ['SOME_FOLDER/*.txt']
      },
      entry_points={
                        'console_scripts': [
                            'entry-point = recipes.script:main'
                        ],
                    },
      include_package_data=True)
