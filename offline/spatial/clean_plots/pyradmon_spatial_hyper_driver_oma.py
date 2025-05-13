#!/usr/bin/env python3

import os
print(f'------------------ current directory: {os.getcwd()}')
print(f'------------------ current file: {os.path.basename(__file__)}')

# module load python/GEOSpyD/Ana2019.10_py3.7

import sys
import pyradmon_spatial as prsp

diagfile = sys.argv[1]

#configfile = './init_config.yaml'
configfile = './init_oma_hyper_config.yaml'

current_file = prsp.pyradmon_spatial(diagfile,configfile,show=False,save=True)
current_file.generate_plots()

