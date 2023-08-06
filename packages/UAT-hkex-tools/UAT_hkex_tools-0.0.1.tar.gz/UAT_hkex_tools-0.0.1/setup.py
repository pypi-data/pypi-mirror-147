#import pathlib

from setuptools import setup

#HERE = pathlib.Path(__file__).parent
#README = (HERE / "README.md").read_text()
setup(
    name='UAT_hkex_tools',
    version='0.0.1',
    description='Reader for HKEX daily report',
    py_modules=['UAT_hkex_tools'],
    package_dir={'' :'src'},
    author='marchlam',
    license='GPLv3',

    install_requires=['re','os', 'datatime']
)