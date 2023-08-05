from distutils.core import setup
from unicodedata import name
setup(
  name = 'ds_bigquery',         # How you named your package folder
  packages = ['ds_bigquery'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Small wrapper to use BigQuery with Dataframes in Google Cloud Functions',   # Give a short description about your library
  author = 'Paul Verse',                   # Type in your name
  author_email = 'paulverse@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/Lembley42',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Lembley42/ds_bigquery/archive/refs/tags/v_0.1.tar.gz',    # Where to find the GitHub
  keywords = ['datastack'],   # Keywords that define your package best
  install_requires=[            # All required packages
          'google-auth',
          'google-cloud-bigquery',
          'google-cloud-bigquery-storage',
          'pandas',
          'pandas-gbq'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)