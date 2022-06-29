from console import logger, dir_path


def initialize():
    logger.info('Installation Detected @ ' + dir_path)


if __name__ == '__main__':
    initialize()
