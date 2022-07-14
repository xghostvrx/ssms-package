import configparser
from os import mkdir, makedirs
from os.path import isdir, isfile
from shutil import rmtree
from time import sleep

from console import clear_console, logger, dir_path

config = configparser.ConfigParser()


def save(miniconda,
         workspace,
         project_name,
         project_location,
         run_name,
         run,
         reads,
         read_type,
         trimmer,
         trimmomatic_options,
         classifier,
         database,
         adapter,
         trimmer_database,
         classifier_database):
    logger.info('Saving Workflow Configuration...')

    sleep(3)

    config['General Settings'] = {'miniconda': miniconda,
                                  'workspace': workspace}

    config['Project Settings'] = {'project_name': project_name,
                                  'project_location': project_location}

    config['Run Settings'] = {'run_name': run_name,
                              'run': run,
                              'reads': reads,
                              'read_type': read_type,
                              'trimmer': trimmer,
                              'trimmomatic_options': trimmomatic_options,
                              'classifier': classifier,
                              'database_selection': database,
                              'adapter': adapter}

    config['Databases'] = {'trimmer_database': trimmer_database,
                           'classifier_database': classifier_database}

    config.write(open(workspace + '/config.ini', 'w'))

# TODO: Add a configuration prompt about metadata (after prompting for reads)

def configuration():
    clear_console()
    logger.info('Starting a new workflow configuration.')
    sleep(5)

    while True:
        miniconda = input('Enter the location of your miniconda installation: ')
        is_dir = isdir(miniconda)
        if is_dir == 1:

            logger.info('(' + miniconda + ') has been set as the miniconda installation.')

            sleep(3)

            break
        else:
            clear_console()
            print('Please enter the location of an existing miniconda installation.')

    # Check for an existing workspace
    workspace = str(dir_path + '/workspace')
    is_dir = isdir(workspace)
    if is_dir == 1:

        print('An existing workspace has been detected for this installation.')
        answer = input('Would you like to use this workspace? (y/n): ')
        if any(answer.lower() == f for f in ['yes', 'y', '1']):

            logger.info('An existing workspace will be used for further processes.')

        elif any(answer.lower() == f for f in ['no', 'n', '0']):

            while True:
                answer = input('Would you like to overwrite this workspace? (y/n): ')
                if any(answer.lower() == f for f in ['yes', 'y', '1']):

                    logger.warning('The user has overwritten their existing workspace.')

                    # Overwrite existing workspace
                    rmtree(workspace)
                    mkdir(workspace)

                    break

                elif any(answer.lower() == f for f in ['no', 'n', '0']):

                    logger.warning('The user does not want to overwrite their existing workspace.')

                    print('Please save your existing workspace to a new location before restarting.')

                    logger.critical('Terminating SSMS Package...')

                    exit()
                else:

                    clear_console()

                    print('Please enter yes or no.')
        else:

            clear_console()

            print('Please enter yes or no.')
    else:

        mkdir(workspace)

        logger.info('A new workspace has been created at (' + workspace + ').')

    sleep(3)

    while True:
        project_name = input('Enter the project name: ')
        if project_name.isalnum():

            logger.info('(' + project_name + ') has been specified as the project name.')

            project_location = str(workspace + '/projects/' + project_name)
            is_dir = isdir(project_location)
            if not is_dir == 1:
                makedirs(project_location)

            sleep(3)

            break
        else:

            clear_console()
            print('The project name (' + project_name + ') is not an alphanumeric.')
            print('Please enter the project name as an alphanumeric (ex. A-Z, 1-100).')

    while True:
        run_name = input('Enter the run name: ')
        if run_name.isalnum():

            logger.info('(' + run_name + ') has been specified as the run name.')

            run = str(project_location + '/' + run_name)
            is_dir = isdir(run)
            if not is_dir == 1:
                makedirs(run)

            reads = str(run + '/reads/')
            is_dir = isdir(reads)
            if not is_dir == 1:
                makedirs(reads)

            sleep(3)

            while True:
                print('Please move read(s) into the following location: ' + reads)
                answer = input('Confirm once this has been done (y/n): ')
                if any(answer.lower() == f for f in ['yes', 'y', '1']):

                    logger.info('The user has confirmed that their read(s) have been moved to (' + reads + ').')

                    sleep(3)

                    while True:
                        # noinspection SpellCheckingInspection
                        print('Read(s) must be formatted as the Casava 1.8 format: '
                              'sampleid_barcodeid_lane_direction_set.fastq.gz')
                        answer = input('Are your read(s) formatted correctly? (y/n): ')
                        if any(answer.lower() == f for f in ['yes', 'y', '1']):

                            logger.info('The user has confirmed that their read(s) are formatted in the Casava 1.8 '
                                        'format.')

                            sleep(3)

                            break
                        elif any(answer.lower() == f for f in ['no', 'n', '0']):
                            clear_console()
                            print('Please make sure that your read(s) are formatted as suggested.')
                        else:
                            clear_console()
                            print('Please enter yes or no.')
                    break
                elif any(answer.lower() == f for f in ['no', 'n', '0']):
                    clear_console()
                    print('Please move your read(s) to the specified location.')
                else:
                    clear_console()
                    print('Please enter yes or no.')

            break
        else:

            clear_console()
            print('The run name (' + run_name + ') is not an alphanumeric.')
            print('Please enter the run name as an alphanumeric (ex. A-Z, 1-100).')

    while True:
        read_type = input('Enter the read type ("single" or "paired"): ')
        if read_type == 'single' or read_type == 'paired':

            logger.info('(' + read_type + ') has been specified as the read type.')

            sleep(3)

            break
        else:
            clear_console()
            print('Please enter the correct read type ("single" or "paired").')

    while True:
        trimmer = input('Enter a trimmer selection ("kneaddata" or "trimmomatic"): ')
        if trimmer == 'kneaddata' or trimmer == 'trimmomatic':

            logger.info('(' + trimmer + ') has been specified as the trimmer.')

            if trimmer == 'kneaddata':
                trimmer_database = str(workspace + '/databases/kneaddata')
                is_dir = isdir(trimmer_database)
                if not is_dir == 1:
                    makedirs(trimmer_database)

                sleep(3)

                while True:
                    print('Please move a kneaddata database into the following location: ' + trimmer_database)
                    answer = input('Confirm once this has been done (y/n): ')
                    if any(answer.lower() == f for f in ['yes', 'y', '1']):

                        logger.info(
                            'The user has confirmed that a kneaddata database has been moved to (' + trimmer_database + ').')

                        break
                    elif any(answer.lower() == f for f in ['no', 'n', '0']):
                        clear_console()
                    else:
                        clear_console()
                        print('Please enter yes or no.')

            sleep(3)

            print('WARNING: Enter the following trimmomatic options carefully.')
            trimmomatic_options = input('Enter the trimmomatic options: ')
            logger.info('(' + trimmomatic_options + ') has been specified as the trimmomatic options.')

            sleep(3)

            break
        else:
            clear_console()
            print('Please enter the correct trimmer ("kneaddata" or "trimmomatic").')

    while True:
        classifier = input('Enter the classifier ("kraken2", "metaphlan", or "humann"): ')
        if classifier == 'kraken2':

            logger.info('(' + classifier + ') has been specified as the classifier.')

            sleep(3)

            while True:
                database = input('Select a kraken2 database to use ("NCBI" or "GTDB"): ')
                if database == 'NCBI' or database == 'GTDB':

                    logger.info('(' + database + ') has been specified as the selected database.')

                    classifier_database = str(workspace + '/databases/kraken2/' + database)
                    is_dir = isdir(classifier_database)
                    if not is_dir == 1:
                        makedirs(classifier_database)

                    sleep(3)

                    while True:
                        print('Please move the selected database into the following location: ' + classifier_database)
                        answer = input('Confirm once this has been done (y/n): ')
                        if any(answer.lower() == f for f in ['yes', 'y', '1']):
                            logger.info(
                                'The user has confirmed that the selected database has been moved to (' + classifier_database + ').')
                            sleep(3)
                            break
                        elif any(answer.lower() == f for f in ['no', 'n', '0']):
                            clear_console()
                            print('Please move the selected database to the specified location.')
                        else:
                            clear_console()
                            print('Please enter yes or no.')

                    break
                else:
                    clear_console()
                    print('Please select the correct database ("NCBI" or "GTDB").')

            break
        elif classifier == 'metaphlan' or classifier == 'humann':

            logger.info('(' + classifier + ') has been specified as the classifier.')

            sleep(3)

            clear_console()

            print('The workflow for ' + classifier + ' is currently unavailable.')

            print('Please use a different classifier.')

        else:
            clear_console()
            print('Please enter the classifier ("kraken2", "metaphlan", or "humann").')

    sleep(3)

    adapter = str(workspace + '/adapters')
    is_dir = isdir(adapter)
    if not is_dir == 1:
        mkdir(adapter)

    while True:
        print('Please move an adapter file into the following location: ' + adapter)
        answer = input('Confirm once this has been done (y/n): ')
        if any(answer.lower() == f for f in ['yes', 'y', '1']):
            logger.info('The user has confirmed that the adapter file has been moved to (' + adapter + ').')

            sleep(3)

            answer = input('Enter the filename of the adapter file (ex. adapter_name.fasta): ')
            adapter = adapter + '/' + answer
            is_file = isfile(adapter)
            if is_file == 1:
                logger.info('(' + adapter + ') has been specified as the adapter.')
                sleep(3)
                break
            else:
                clear_console()
                logger.error('The adapter file (' + adapter + ') does not exist.')
                print('Please enter the filename of the adapter file.')
        elif any(answer.lower() == f for f in ['no', 'n', '0']):
            clear_console()
            logger.critical('The user has not moved an adapter file to (' + adapter + ').')
        else:
            clear_console()
            print('Please enter yes or no.')

    # noinspection PyUnboundLocalVariable
    settings = [miniconda,
                workspace,
                project_name,
                project_location,
                run_name,
                run,
                reads,
                read_type,
                trimmer,
                trimmomatic_options,
                classifier,
                database,
                adapter,
                trimmer_database,
                classifier_database]

    save(*settings)
