from setuptools import setup, find_packages

setup(
    name = 'RealRateCalc',
    version = '0.1',
    packages = find_packages(),
    install_require = [
        'requests>=2.00.0', 
    ],
    entry_point = {
        "console_scripts":[
            "RealRateCalc = RealRateCalc:hello",
        ],
    },
)