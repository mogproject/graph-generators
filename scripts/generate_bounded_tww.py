#!/usr/bin/env python3

"""
Generates bounded-twin-width instances.
"""

import sys
import os
import argparse
import logging
import networkx as nx
from random import Random
import math

__version__ = '0.0.1'
__license__ = 'Apache License, Version 2.0'

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PYTHON_MAIN = os.path.join(PROJECT_DIR, 'src', 'main', 'python')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')  # modify if necessary

if PYTHON_MAIN not in sys.path:
    sys.path.insert(0, PYTHON_MAIN)

from generator import *
from readwrite import *


def get_logger(log_level=logging.CRITICAL + 1):
    """Logger settings."""

    logging.basicConfig(level=log_level, format='%(asctime)s [%(levelname)s] %(message)s', stream=sys.stderr)
    logger = logging.getLogger(__name__)
    return logger


def get_parser():
    """Argument parser."""

    parser = argparse.ArgumentParser(description='Twinwidth solver prototype.')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--log-level', choices=['crit', 'error', 'warn', 'info', 'debug', 'none'], default='info', help='log level')
    parser.add_argument('--seed', type=int, default=12345, help='seed for pseudorandom number generator (default:12345)')
    return parser


def generate_tww_bounded_graph(n: int, rand: Random) -> nx.Graph:
    k = int(math.floor(math.log2(n) ** 2))
    d = int(math.floor(math.log2(n)))
    return twin_width_bounded_graph(rand, n, k, d)


def main(args):
    """Entry point of the program. """

    # get logger
    logger = get_logger({
        'crit': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'none': logging.CRITICAL + 1
    }[args.log_level])

    logger.info(f'Started: {SCRIPT_PATH}')
    logger.info(f'Seed: {args.seed}')

    rand = Random(args.seed)

    for n in [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000]:
        for t in range(3):
            path = os.path.join(DATA_DIR, f'btww_n{n:07d}_t{t:02d}.gr')

            k = int(math.floor(math.log2(n) ** 2))
            d = int(math.floor(math.log2(n)))
            G = twin_width_bounded_graph(rand, n, k, d)

            save_pace_2023(path, G)
            logger.info(f'Generated: {path}')

    logger.info(f'Finished: {SCRIPT_PATH}')


if __name__ == '__main__':
    main(get_parser().parse_args())
