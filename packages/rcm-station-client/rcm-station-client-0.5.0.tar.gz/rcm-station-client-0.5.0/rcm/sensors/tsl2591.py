#  Copyright (c) 2022 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

"""
The TSL2591 sensor - High Dynamic Range Digital Light Sensor
============================================================

See https://www.adafruit.com/product/439

Gain & Timing
You can adjust the gain settings and integration time of the sensor to make it more or less sensitive to light, depending on the
environment where the sensor is being used.

Gain:
GAIN_LOW: Sets the gain to 1x (bright light)
GAIN_MEDIUM or GAIN_MED: Sets the gain to 25x (general purpose)
GAIN_HIGH: Sets the gain to 428x (low light)
GAIN_MAX: Sets the gain to 9876x (extremely low light)

The integration time can be set between 100 and 600ms, and the longer the integration time the more light the sensor is able to integrate,
making it more sensitive in low light the longer the integration time. The following values can be used:
100MS
200MS
300MS
400MS
500MS
600MS
"""
import logging

import adafruit_tsl2591

from .sensor import Sensor
from ..constants import GAIN_LOW, GAIN_MEDIUM, GAIN_HIGH, GAIN_MAX, DEFAULT_GAIN, DEFAULT_IT_TIME
from ..constants import IT_TIME_100MS, IT_TIME_200MS, IT_TIME_300MS, IT_TIME_400MS, IT_TIME_500MS, IT_TIME_600MS, SENSOR_TSL2591
from ..settings import tsl2591_gain, tsl2591_integration_time

# Maximum lux the sensor can measure
_MAX_LUX = 88000

_SETTING_GAIN = 'gain'
_SETTING_INTEGRATION_TIME = 'integration_time'

GAIN_VALUES = {
    GAIN_LOW: adafruit_tsl2591.GAIN_LOW,
    GAIN_MEDIUM: adafruit_tsl2591.GAIN_MED,
    GAIN_HIGH: adafruit_tsl2591.GAIN_HIGH,
    GAIN_MAX: adafruit_tsl2591.GAIN_MAX
}

INTEGRATION_TIMES = {
    IT_TIME_100MS: adafruit_tsl2591.INTEGRATIONTIME_100MS,
    IT_TIME_200MS: adafruit_tsl2591.INTEGRATIONTIME_200MS,
    IT_TIME_300MS: adafruit_tsl2591.INTEGRATIONTIME_300MS,
    IT_TIME_400MS: adafruit_tsl2591.INTEGRATIONTIME_400MS,
    IT_TIME_500MS: adafruit_tsl2591.INTEGRATIONTIME_500MS,
    IT_TIME_600MS: adafruit_tsl2591.INTEGRATIONTIME_600MS
}


class TSL2591(Sensor):
    """Concrete implementation of the TSL2591 sensor."""

    def __init__(self):
        """
        Initialize the TSL2591 sensor
        """
        super().__init__()
        self._sensor = adafruit_tsl2591.TSL2591(self._i2c)
        logging.debug('Initialized TSL2591 sensor')

    @property
    def name(self):
        return SENSOR_TSL2591

    @property
    def lux(self):
        """
        In very bright environments the sensor can raise a RuntimeError, in that case it will return the max value of 88000 lx.
        :return: the full spectrum light level in lx (lux).
        """
        try:
            return self._sensor.lux
        except RuntimeError:
            logging.debug("Sensor overflow detected while reading lux")
            return _MAX_LUX

    @property
    def visible_light(self):
        """
        :return: the raw visible light as 32-bit unsigned number
        """
        return self._sensor.visible

    @property
    # pylint: disable=invalid-name
    def IR_light(self):
        """
        :return: the raw IR light as 16-bit unsigned number
        """
        return self._sensor.infrared

    def read(self):
        """Reads the full spectrum light in lux, and raw human visible light plus raw IR light."""
        logging.info('Reading TSL2591 sensor')

        gain = self._get_gain()
        self._sensor.gain = GAIN_VALUES[gain]
        integration_time = self._get_integration_time()
        self._sensor.integration_time = INTEGRATION_TIMES[integration_time]
        logging.debug(f'Applied gain {gain} and integration time: {integration_time}')

        measurements = {
            'lux': self.lux,
            'visible-light': self.visible_light,
            'IR-light': self.IR_light
        }
        logging.info('Measurement: %s', measurements)
        return measurements

    def _get_gain(self):
        """
        :return: the gain setting. First it will try to retrieve the sensor setting. If it is not set, it will check if it was set in the
        .env for backwards compatability. Finally if that one is not set either, it will default to "GAIN_MEDIUM".
        """
        # Get from sensor settings
        if _SETTING_GAIN in self._settings.keys():
            gain_setting = self._settings[_SETTING_GAIN].upper()
            if gain_setting in GAIN_VALUES:
                return gain_setting
            logging.warning(f'Gain {gain_setting} is not supported')

        # Get from .env (deprecated)
        if tsl2591_gain is not None:
            if tsl2591_gain in GAIN_VALUES:
                logging.warning('Setting TSL2591 gain via .env file is deprecated in favour of sensor settings from server!')
                return tsl2591_gain
            logging.warning(f'Gain {tsl2591_gain} is not supported')

        # Default fallback
        return DEFAULT_GAIN

    def _get_integration_time(self):
        """
        :return: the integration time setting. First it will try to retrieve the sensor setting. If it is not set, it will check if it was
        set in the .env for backwards compatability. Finally if that one is not set either, it will default to "100ms".
        """
        # Get from sensor settings
        if _SETTING_INTEGRATION_TIME in self._settings.keys():
            integration_time = self._settings[_SETTING_INTEGRATION_TIME].lower()
            if integration_time in INTEGRATION_TIMES:
                return integration_time
            logging.warning(f'Integration time {integration_time} is not supported')

        # Get from .env (deprecated)
        if tsl2591_integration_time is not None:
            if tsl2591_integration_time in INTEGRATION_TIMES:
                logging.warning('Setting TSL2591 integration time via .env file is deprecated in favour of sensor settings from server!')
                return tsl2591_integration_time
            logging.warning(f'Gain {tsl2591_integration_time} is not supported')

        # Default fallback
        return DEFAULT_IT_TIME
