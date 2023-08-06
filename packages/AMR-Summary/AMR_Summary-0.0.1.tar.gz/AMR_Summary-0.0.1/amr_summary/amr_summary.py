#!/usr/bin/env python
from amr_summary.version import __version__
from olctools.accessoryFunctions.accessoryFunctions import make_path, SetupLogging
from argparse import ArgumentParser
from subprocess import call
from glob import glob
import logging
import sys
import os


def assert_path(path_name, category):
    """
    Clean up user-supplied path to allow user expansion (~). Ensure that the path exists.
    :param path_name: type str: Name and path of user-supplied path
    :param category: type str: Category of supplied path e.g. 'database' or 'sequence'
    return clean_path type str: Name and path of the (optionally) expanded path
    """
    if path_name.startswith('~'):
        clean_path = os.path.expanduser(os.path.abspath(os.path.join(path_name)))
    else:
        clean_path = os.path.abspath(os.path.join(path_name))
    try:
        assert os.path.isdir(clean_path)
    except AssertionError:
        logging.error(f'Cannot locate supplied {category} path: {path_name}. '
                      f'Please ensure that you supplied the correct path.')
        raise SystemExit
    return clean_path


class AMRSummary(object):

    def main(self):
        # Ensure that the necessary databases are present in the supplied database path
        self.resfinder_path, self.mob_recon_path = self.assert_databases(database_path=self.database_path)
        # Perform ResFinder analyses
        self.run_resfinder(
            sequence_path=self.sequence_path,
            database_path=self.resfinder_path,
            report_path=self.report_path
        )
        # Perform MOB-recon analyses
        self.run_mob_recon(
            sequence_path=self.sequence_path,
            database_path=self.database_path,
            report_path=self.report_path
        )

    @staticmethod
    def assert_databases(database_path):
        """
        Ensures that the necessary databases are present in the provided database path. If not, the appropriate
        database will be installed
        :param database_path: type str: Name and path of folder in which the ResFinder and MOB-recon databases
        are stored
        :return resfinder_path: type str: Name and path of folder in which the ResFinder database is stored
        :return mob_recon_path: type str: Name and path of folder in which the MOB-recon database is stored
        """
        # ResFinder
        resfinder_path = os.path.join(database_path, 'resfinder')
        if not os.path.isdir(resfinder_path):
            logging.warning(f'ResFinder database could not be located in database path: {database_path}. '
                            f'Installing it now.')
            call(f'python -m olctools.databasesetup.database_setup -d {resfinder_path} -res', shell=True)
        # MOB-recon
        mob_recon_path = os.path.join(database_path, 'mob_recon')
        return resfinder_path, mob_recon_path

    @staticmethod
    def run_resfinder(sequence_path, database_path, report_path):
        """
        Use GeneSeekr to run ResFinder analyses on the sequence files
        :param sequence_path: type str: Name and path of folder in which the sequence files in FASTA format are located
        :param database_path: type str: Name and path of folder in which the ResFinder database is stored
        :param report_path: type str: Name and path of folder in which the reports are to be created
        """
        logging.info('Running ResFinder analyses')
        # Run the ResFinder method of GeneSeekr
        res_command = f'GeneSeekr blastn -s {sequence_path} -t {database_path} -r {report_path} -A'
        logging.debug(f'ResFinder command: {res_command}')
        # Run the system call
        call(res_command, shell=True)
        # Clean up the outputs
        for resfinder_report in glob(os.path.join(report_path, '*.tsv')):
            os.remove(resfinder_report)

    @staticmethod
    def run_mob_recon(sequence_path, database_path, report_path):
        """
        Run MOB-recon on the assemblies, and create a summary report linking the AMR resistance genes identified by
        ResFinder to the plasmids identified by MOB-recon
        :param sequence_path: type str: Name and path of folder in which the sequence files in FASTA format are located
        :param database_path: type str: Name and path of folder in which the MOB-recon database is stored
        :param report_path: type str: Name and path of folder in which the reports are to be created
        """
        logging.info('Running MOB-recon analyses')
        # Run MOB-recon
        mob_command = f'python -m genemethods.assemblypipeline.mobrecon -s {sequence_path} -r {database_path} ' \
                      f'-o {report_path} -p'
        logging.debug(f'MOB-recon AMR Summary command: {mob_command}')
        # Run the system call
        call(mob_command, shell=True)

    def __init__(self, sequence_path, database_path, report_path):
        logging.info(f'Welcome to the CFIA AMR Summary pipeline, version {__version__}!')
        # Initialise the sequence path
        self.sequence_path = assert_path(
            path_name=sequence_path,
            category='sequence'
        )
        # Initialise the database path
        self.database_path = assert_path(
            path_name=database_path,
            category='database'
        )
        # Report path is different; if it doesn't exist, set it to the default value of sequence_path/reports
        if report_path:
            if report_path.startswith('~'):
                self.report_path = os.path.expanduser(os.path.abspath(os.path.join(report_path)))
            else:
                self.report_path = os.path.abspath(os.path.join(report_path))
        else:
            self.report_path = os.path.join(os.path.join(os.path.dirname(self.sequence_path), 'reports'))
        try:
            make_path(inpath=self.report_path)
        except PermissionError:
            logging.error(f'Could not create the requested report path: {self.report_path}. '
                          f'Please ensure that you entered a valid path, and that you have sufficient permissions '
                          f'to write to that folder')
            raise SystemExit
        self.resfinder_path = str()
        self.mob_recon_path = str()
        logging.debug(f'Sequence path: {self.sequence_path}')
        logging.debug(f'Database path: {self.database_path}')
        logging.debug(f'Report path: {self.report_path}')


def cli():
    # Parser for arguments
    parser = ArgumentParser(
        description='AMR Summary: a pipeline to identify AMR resistance genes located on plasmids by '
                    'combining ResFinder and MOB-recon')
    parser.add_argument(
        '-s', '--sequence_path',
        metavar=str(),
        required=True,
        help='Path of folder containing sequence files in FASTA format to process')
    parser.add_argument(
        '-d', '--database_path',
        metavar=str(),
        required=True,
        help='Path of folder containing ResFinder and MOB-recon databases. If these databases cannot be '
             'located, they will be downloaded')
    parser.add_argument(
        '-r', '--report_path',
        metavar=str(),
        help='Path of folder in which reports are to be created. Default is sequence_path/reports'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug-level messages to be printed to the console'
    )
    parser.add_argument(
        '-v', '--version',
        action='version', version=f'%(prog)s version {__version__}')
    arguments = parser.parse_args()
    # Set up the logging
    SetupLogging(debug=arguments.debug)
    amr_summary = AMRSummary(sequence_path=arguments.sequence_path,
                             database_path=arguments.database_path,
                             report_path=arguments.report_path)
    amr_summary.main()
    logging.info('AMR Summary complete!')
    # Prevent the arguments being printed to the console (they are returned in order for the tests to work)
    sys.stderr = open(os.devnull, 'w')
    return arguments


if __name__ == '__main__':
    cli()
