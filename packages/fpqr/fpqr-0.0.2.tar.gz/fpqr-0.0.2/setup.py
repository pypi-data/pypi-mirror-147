from setuptools import setup, find_packages
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='fpqr',
    packages=find_packages(),
    version='0.0.2',
    author='Alvaro Mendez Civieta',
    author_email='alvaro.mendez@uc3m.es',
    license='GNU General Public License',
    zip_safe=True,
    url='https://github.com/alvaromc317/fpqr',
    description='A quantile based dimension reduction technique for regression',
    long_description=long_description,
    long_description_content_type='text/markdown',
    download_url='https://github.com/alvaromc317/fpqr/archive/refs/tags/v_0_0_2.tar.gz',
    keywords=['partial-least-squares', 'quantile-regression', 'dimension-reduction', 'outliers', 'robust'],
    python_requires='>=3.5',
    install_requires=["numpy >= 1.2",
                      "scipy >= 1.7.0",
                      "scikit-learn >= 1.0",
                      "asgl >= 1.0.5",
                      "cvxpy >= 1.2.0"]
)
