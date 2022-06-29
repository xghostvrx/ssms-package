from os.path import isfile
from time import sleep

from console import logger, dir_path
from settings import configuration


def initialize():
    logger.info('Installation Detected @ ' + dir_path)

    sleep(5)

    def new_config_prompt():
        while True:
            new_config = input('Would you like to start a new configuration (y/n): ')
            if any(new_config.lower() == f for f in ['yes', 'y', '1']):

                # Start settings.py
                configuration()

                break

            elif any(new_config.lower() == f for f in ['no', 'n', '0']):

                logger.error('The user does not want to start a new configuration.')
                logger.critical('Terminating SSMS Package...')
                exit()

            else:
                print('Please enter yes or no.')

    is_file = isfile(dir_path + '/workspace/config.ini')
    if is_file == 1:
        logger.info('An existing configuration has been detected for this installation.')
        while True:
            existing_config = input('Would you like to use the existing configuration (y/n): ')
            if any(existing_config.lower() == f for f in ['yes', 'y', '1']):

                # Start workflow
                # TODO: Add workflow start() function

                break

            elif any(existing_config.lower() == f for f in ['no', 'n', '0']):

                new_config_prompt()

                break

            else:
                print('Please enter yes or no.')
    else:

        logger.info('A configuration does not exist for this installation.')

        sleep(1)

        new_config_prompt()


if __name__ == '__main__':
    initialize()
