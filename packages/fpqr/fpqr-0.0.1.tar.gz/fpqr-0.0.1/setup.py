from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='fpqr',
    version='v0.0.1',
    author='Alvaro Mendez Civieta',
    author_email='alvaro.mendez@uc3m.es',
    license='GNU General Public License',
    zip_safe=False,
    url='https://github.com/alvaromc317/fpqr',
    description='A quantile based dimension reduction technique for regression',
    long_description=long_description,
    long_description_content_type='text/markdown',
    download_url = 'https://github.com/alvaromc317/fpqr/archive/refs/tags/v_0_0_1.tar.gz',
    keywords=['partial-least-squares', 'quantile-regression', 'dimension-reduction', 'outliers', 'robust'],
    python_requires='>=3.5',
    install_requires=["numpy >= 1.2",
                      "scipy >= 1.7.0",
                      "scikit-learn >= 1.0",
                      "asgl >= 1.0.5",
                      "cvxpy >= 1.2.0"],
    packages=find_packages()
)


setup(
  name = 'YOURPACKAGENAME',         # How you named your package folder (MyLib)
  packages = ['YOURPACKAGENAME'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TYPE YOUR DESCRIPTION HERE',   # Give a short description about your library
  author = 'YOUR NAME',                   # Type in your name
  author_email = 'your.email@domain.com',      # Type in your E-Mail
  url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)