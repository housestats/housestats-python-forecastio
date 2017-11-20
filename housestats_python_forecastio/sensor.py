import logging
import requests

from housestats.metric import Metric
from housestats.sensor.base import BaseSensor

LOG = logging.getLogger(__name__)


class ForecastioSensor(BaseSensor):
    sensor_type = 'forecastio'
    current_weather_url = ('https://api.darksky.net/forecast/'
                           '{api_key}/{location}')
    params = {
        'exclude': 'minutely,hourly,daily,flags',
        'units': 'si',
    }

    def __init__(self, config):
        super().__init__(config)

    def sample(self):
        url = self.current_weather_url.format(
            location=self.config['location'],
            api_key=self.config['api_key'])
        res = requests.get(url, params=self.params)
        res.raise_for_status()
        data = res.json()
        del data['currently']['time']
        del data['currently']['summary']
        del data['currently']['icon']
        return data

    def fetch(self):
        sample = self.sample()
        LOG.debug('sample = %s', sample)

        tags = dict(
            latitude=sample['latitude'],
            longitude=sample['longitude'],
        )
        tags.update(self.config.get('tags', {}))

        return [Metric.load(dict(
            sensor_type=self.sensor_type,
            sensor_id=str(self.config['location']),
            tags=tags,
            fields=sample['currently']
        ))]
