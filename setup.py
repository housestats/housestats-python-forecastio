from setuptools import setup, find_packages

setup(
    name='housestats-python-forecastio',
    version='0.1',
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    description='sensor for forecastio',
    license='GPLv3',
    url='https://github.com/larsks/housestats-python-forecastio',
    packages=find_packages(),
    entry_points={
        'housestats.sensor': [
            'forecastio=housestats_python_forecastio.sensor:ForecastioSensor',
        ],
    }
)
