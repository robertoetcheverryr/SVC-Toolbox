# ****************************************************************************
# * svc-toolbox                                                              *
# * Collection of tools for SVC                                              *
# * Author: Roberto Etcheverry (retcheverry@roer.com.ar)                     *
# * Ver: 1.0.0 2020/09/20                                                    *
# ****************************************************************************
# Import argparse and path to parse command line arguments and use path utilities
import argparse
# Import JSON to output json files
import json
# Import os to use file functions
import os
# Import sys, exit() is only for interactive sessions, when using PyInstaller you need to use sys.exit()
import sys
# Import date to get current date
from datetime import datetime
# Import pathlib to work with paths
from pathlib import Path
# Import logger for the main log file
from loguru import logger
# Import common classes and functions from common.py
from common import print_red
# Import the RemoteClient class from the sshclient file
from sshclient import RemoteClient
from sshclient import AuthenticationException
# Import colorama for console colors
from colorama import init, Fore, Back, Style

# Program START!
try:
    # Colorama initialization
    init()
    # Firstly, disable logger, we'll only have console output until output_dir is defined.
    logger.remove()
    # Create parser and define arguments for the program
    #TODO refactor generic console code for svc toolbox instead of powercollector
    parser = argparse.ArgumentParser(prog='svc-toolbox',
                                     description='Connect to an HMC to collect configuration and events. A full '
                                                 'collection will also connect to each Running LPAR to collect '
                                                 'OS-level data. To only collect HMC-level data, use the --hmconly '
                                                 'flag. To only collect the OS-level data, provide a previously '
                                                 'generated JSON file with the --input parameter.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--hmc', metavar='hmc00', type=str, help='HMC Hostname or IP Address.')
    parser.add_argument('--user', metavar='hscroot', type=str, help='HMC Username.')
    parser.add_argument('--password', metavar='abc123', type=str, help='HMC Password.')
    parser.add_argument('--hmconly', action='store_true', help='Collect HMC and Managed Systems information only.')
    group.add_argument('--input', metavar='Path', type=Path, help='Not compatible with --hmc, specifies a previously '
                                                                  'created JSON file to use as the base for OS-level '
                                                                  'data collection.')
    parser.add_argument('--hmcscanpath', metavar='Path', type=Path, help='Path to the HMC Scanner package. Defaults to '
                                                                         'HMCScanner in the current directory')
    parser.add_argument('--output', metavar='Path', type=Path, help='Output path for all generated files. Defaults to '
                                                                    'the current directory')
    # TODO Add web service to receive data directly and implement uploading
    # parser.add_argument('--upload_url', metavar='URL', type=str, help='URL of the webservice that receives the data.')

    # Obtain the arguments
    args = parser.parse_args()

    # If no valid input, print help and exit
    if args.input is None:
        if args.hmc is None or args.user is None or args.password is None:
            parser.print_help()
            sys.exit(0)

    print('powercollector version 1.0.11')
    # Create folder for output and set folder variables
    # now is an object, we turn that into a string with a format of our choosing
    today = datetime.now().strftime("%Y%m%d-%H-%M")
    # https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
    # when frozen into an exe, the path resolving methods change. In this case we want to bundle HMC Scanner OUTSIDE of
    # the exe, so we use sys._MEIPASS to obtain the exe's path
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the pyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable sys._MEIPASS'.
        # But app path != exe path, and that is what we need, so, changing to sys.executable
        base_dir = str(Path(sys.executable).resolve().parent)
    else:
        base_dir = str(Path(__file__).resolve().parent)
    # If the user specified an input file, set the output directory to the input file's. Otherwise create a new one.

    # If no output is specified, use the base dir for output
    if args.output:
        output_dir = str(args.output)
    else:
        output_dir = base_dir + '\\' + args.hmc + '-' + today
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
    try:
        # Try to write to the specified directory, if it fails default to the EXE's dir.
        dir_test = open(output_dir + '\\' + 'temp.file', 'w+')
    except Exception as e:
        print_red('Output directory is invalid. Defaulting to .exe location: ' + base_dir)
        logger.error('Output directory is invalid. Defaulting to .exe location: ' + base_dir)
        if args.hmc:
            output_dir = base_dir + '\\' + args.hmc + '-' + today
        else:
            output_dir = base_dir + '\\' + today
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
    else:
        dir_test.close()
        os.remove(output_dir + '\\' + 'temp.file')
# TODO: obtain fw version
# TODO: obtain hdd qties
# TODO: obtain enclosures
# TODO: obtain controller / iogrp
# TODO: obtain relationships? flashcopies?
# TODO: obtain hdd id + fw level
# TODO: upload disk fw
# TODO: apply fw to downlevel disk (how to decide? parse the .txt file of the update?) MUST report before and after
# TODO: run svcupgradetest
# TODO: generate lvl4 snap and download

except KeyboardInterrupt:
    # Cleanup?
    logger.error('powercollector killed by ctrl-C. Output may be invalid.')
    print_red('powercollector killed by ctrl-C. Output may be invalid.')
