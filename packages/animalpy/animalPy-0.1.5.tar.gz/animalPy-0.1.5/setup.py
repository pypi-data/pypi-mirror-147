# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['animalpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'animalpy',
    'version': '0.1.5',
    'description': 'Python wrapper using some-random-api.ml that can get animal images and facts with easy plug-and-play syntax!',
    'long_description': 'Animals\n=======\n\n*Created by Cesiyi and KsIsCute*\n\nExamples:\n---------\n\n.. code:: py\n\n   import animals # Importing the library\n   from animals import animal # Import main class\n   picture = animal.picture("dog") # Get a dog picture\n   print(picture) # Print the link to the required picture\n\n======= ==================\nVersion Support\n======= ==================\n>3.8.X  :white_check_mark:\n3.0+    :white_check_mark:\n2.7+    :x:\n>2.6.X  :x:\n======= ==================\n',
    'author': 'ksIsCute',
    'author_email': 'thebeast47ytbusiness@gmail.com',
    'maintainer': 'ksIsCute',
    'maintainer_email': 'thebeast47ytbusiness@gmail.com',
    'url': 'https://github.com/ksIsCute/Animals.py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
