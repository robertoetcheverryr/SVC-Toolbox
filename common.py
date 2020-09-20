# ****************************************************************************
# * svc-toolbox.common                                                    *
# * Module for common classes and functions                                  *
# * Author: Roberto Etcheverry (retcheverry@roer.com.ar)                     *
# * Ver: 1.0.11 2020/07/04                                                   *
# ****************************************************************************

# Import logger for the main log file
from loguru import logger
# Import subprocess to run external processes
import subprocess
# Import os to use file functions
import os
# Import Jsonizable to store and read the data
from jsonizable import Jsonizable
import json
# Import re to work with regular expressions
import re
# Import socket to do low-level networking
import socket
# Import the RemoteClient class from the sshclient file
from paramiko import AuthenticationException
# Import the RemoteClient to connect to HMC and LPAR
from sshclient import RemoteClient
# Import copy to deepcopy modules
import copy


# Define Storage class
# We inherit form Jsonizable, to have the ability to read and write json, the subclass Meta has a dictionary of
# how the Storage class will be read or written
# TODO Define the Storage class and all the information we might need. Investigate how to deal with multiple IOgrp and
# TODO expansions maybe structure like a tree with the clustername, code level, product name and serial as base
# TODO and then expand with each enclosure?
# TODO create enclosure, node, vdisk, host, pool (and mdisk inside that), classes

class Storage(Jsonizable):
    # Use slots to make Python reduce RAM usage, since it doesn't use a dict to store attributes and
    # the attributes are defined from the start.
    __slots__ = ['cluster_name', 'code_level', 'product_name', 'enclosures', 'nodes', 'vdisks', 'hosts', 'pools',
                  'total_raw_cap', 'total_pool_cap', 'total_free_space']

    # All of our inits will now also accept a json object, which we'll use to call the parent class' init
    def __init__(self, json_in=None, cluster_name=None):
        self.cluster_name = cluster_name or ''
        self.code_level = ''
        self.product_name = ''
        self. = ''
        self. = ''
        self. = ''
        super().__init__(json_in)

    class Meta:
        schema = {
            "cluster_name": str,
            "code_level": str,
            "product_name": str,
            "": str,
            "": str,
            "": str,
        }

def print_red(text):
    print(f"\033[91m{text}\033[00m")

def check_host(hostname):
    """
    :This function checks if a provided hostname is pingable.
    :Returns True if the host is reachable and False if not.
    :Logs to the console and logfile any problems.
    """
    try:
        host = socket.gethostbyname(hostname)
        subprocess.run('ping -n 1 ' + host, check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print_red('Host: ' + hostname + ' is not responding to ICMP Ping.')
        logger.error('Host: ' + hostname + ' is not responding to ICMP Ping.')
        return False
    except socket.error:
        print_red('Host: ' + hostname + ' is not resolvable.')
        logger.error('Host: ' + hostname + ' is not resolvable.')
        return False
    return True
