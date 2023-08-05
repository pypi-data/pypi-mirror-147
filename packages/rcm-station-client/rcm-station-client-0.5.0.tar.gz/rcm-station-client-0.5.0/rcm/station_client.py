#  Copyright (c) 2022 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

"""
This is the Station Client that reads measurements from sensors and reports
them to the station monitoring service. The station client is typically run on
a raspberry-pi. One RPi represents one station.
"""
import logging
import platform
import socket
import sys

import requests

from . import auth
from . import constants
from . import settings
from . import station
from .sensors.bme680 import BME680
from .sensors.sgp30 import SGP30
from .sensors.sht31d import SHT31D
from .sensors.sys import SYS
from .sensors.tsl2591 import TSL2591

DRIVERS = {
    constants.SENSOR_BME680: BME680,
    constants.SENSOR_SHT31_D: SHT31D,
    constants.SENSOR_TSL2591: TSL2591,
    constants.SENSOR_SGP30: SGP30,
    constants.SENSOR_SYS: SYS
}


def main():
    """
    Main entry point for the station client. Reads the connected sensors one by
    one and submits the measurements reports collected from these sensors to
    the station-monitoring-service.
    """
    try:
        get_lock('station_client')
        logging.info('Running RCM Station Client (%s)', settings.station_name)
        sensors = station.get_sensors()

        # Create collection of drivers
        drivers = {}
        for sensor in sensors.split(','):
            if sensor not in DRIVERS:
                raise ValueError('No driver for: ' + sensor)
            driver = DRIVERS[sensor]()
            drivers[sensor] = driver

        # process list of drivers
        for _, driver in drivers.items():
            # Custom logic for SGP30, try to find a temperature+humidity sensor and provide it to it for calibration
            if isinstance(driver, SGP30):
                tmp_hum_driver = None
                if constants.SENSOR_SHT31_D in drivers:
                    tmp_hum_driver = drivers[constants.SENSOR_SHT31_D]
                elif constants.SENSOR_BME680 in drivers:
                    tmp_hum_driver = drivers[constants.SENSOR_BME680]
                if tmp_hum_driver is not None:
                    driver.tmp_hum_sensor = tmp_hum_driver

            # Read sensor
            measurement_report = driver.read()
            _submit(measurement_report)
    except Exception as exception:
        print('Unexpected error: ', exception)
        logging.exception('Unexpected error: ', exc_info=exception)
        sys.exit(1)
    sys.exit(0)


def get_lock(process_name):
    """
    Try to obtain a lock using a socket. It it fails, the process is already running.
    Only works on Linux systems
    """
    if platform.system() == 'Linux':
        get_lock.lock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        try:
            get_lock.lock.bind('\0' + process_name)
            return
        except Exception as exception:
            logging.exception('Unable to acquire lock, process already running?', exc_info=exception)
            sys.exit(1)
    else:
        logging.info(f'Duplicate process prevention not supported for platform {platform.system()}')


def _submit(measurement_report):
    logging.debug('Submitting measurement report for station %s to %s',
                  settings.station_name, settings.reports_endpoint)
    payload = {
        'stationName': settings.station_name,
        'measurements': measurement_report
    }
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {auth.get_token()}'
    }
    try:
        response = requests.post(settings.reports_endpoint, json=payload, headers=headers, verify=settings.verify, timeout=settings.timeout)
        response.raise_for_status()
    except Exception as exception:
        logging.exception('Failed to submit measurements report', exc_info=exception)
        sys.exit(1)


if __name__ == '__main__':
    main()
