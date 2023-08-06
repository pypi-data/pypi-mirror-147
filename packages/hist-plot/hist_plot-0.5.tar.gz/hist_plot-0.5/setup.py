from setuptools import setup
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir/ "README.md").read_text()

setup(name='hist_plot', 
    version='0.5',
    description='Histogram-based visualization '\
                'approach for visualizing anomaly '\
                'detection algorithm performance and '\
                'prediction confidence',
    author='Emmanuel Aboah Boateng',
    author_email='emmanuelaboah01@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=False,
    packages=['hist_plot'])
