#  Copyright (c) 2022 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

"""
The SHT31-D sensor - High precision Temperature & Humidity sensor
=================================================================

See https://www.adafruit.com/product/2857

Supports two I2C addresses. To set secondary address, set sensor setting `secondary_address` to true.
Supports heater. To enable heater, set sensor setting `heater_enabled` to true.
To control duration of heater, set sensor setting `heat_seconds` to the desired number of seconds. Default is 1 second.
Heating is applied _after_ reading the sensor values, to minimize impact. Please wait a few seconds after heater is turned down before
reading again to let the values settle to normal again.
The heater can only be used when relative humidity is above 80%. It will automatically switch off when below 80%.
"""
import logging
import time

import adafruit_sht31d

from .tmp_hum_sensor import TmpHumSensor
from ..constants import SENSOR_SHT31_D
from ..util.bool import strtobool

_PRIMARY_ADDRESS = 0x44
_SECONDARY_ADDRESS = 0x45
_SETTING_SECONDARY_ADDRESS = 'secondary_address'
_SETTING_HEATER_ENABLED = 'heater_enabled'
_SETTING_HEAT_SECONDS = 'heat_seconds'


class SHT31D(TmpHumSensor):
    """Concrete implementation of SHT31-D sensor."""

    def __init__(self):
        """
        Initialize the SHT31D sensor. It will automatically check the settings to choose the I2C address to use.
        """
        super().__init__()
        address = self._get_address()
        self._sensor = adafruit_sht31d.SHT31D(self._i2c, address)
        logging.debug(f'Initialized SHT31-D sensor on address {address}')

    @property
    def name(self):
        """
        :return: the name of the sensor
        """
        return SENSOR_SHT31_D

    def read(self):
        """
        Reads the temperature and relative humidity.
        """
        logging.info('Reading SHT31-D sensor')
        measurements = {
            'temperature': self.temperature,
            'humidity': self.relative_humidity
            # 'absolute_humidity': self.absolute_humidity
        }
        logging.info('Measurement: %s', measurements)
        self._heat()
        return measurements

    def _heat(self):
        """
        Activate the heater for x time when enabled and relative humidity is 80% or higher.
        """
        if self._is_heater_enabled() and self._sensor.relative_humidity >= 80:
            duration = self._get_heat_seconds()
            logging.debug('Heating for %d seconds', duration)
            self._sensor.heater = True
            time.sleep(duration)
        self._sensor.heater = False

    def _get_address(self):
        """
        :return: the I2C address to use
        """
        return _SECONDARY_ADDRESS \
            if _SETTING_SECONDARY_ADDRESS in self._settings.keys() and strtobool(self._settings[_SETTING_SECONDARY_ADDRESS]) \
            else _PRIMARY_ADDRESS

    def _is_heater_enabled(self):
        """
        :return: True if the heater is enabled (in the settings), false otherwise.
        """
        return _SETTING_HEATER_ENABLED in self._settings.keys() and strtobool(self._settings[_SETTING_HEATER_ENABLED])

    def _get_heat_seconds(self):
        """
        :return: The duration in seconds to activate the heater.
        """
        if _SETTING_HEAT_SECONDS in self._settings.keys():
            try:
                return int(self._settings[_SETTING_HEAT_SECONDS])
            except ValueError as exception:
                logging.exception('Invalid value for setting heat_seconds', exc_info=exception)
                return 1
        return 1
