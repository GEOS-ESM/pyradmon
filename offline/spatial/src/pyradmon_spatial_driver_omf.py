#!/usr/bin/env python3

import sys
import pyradmon_spatial as prsp

diagfile = sys.argv[1]

configfile = './init_omf_config.yaml'
#configfile = './init_oma_config.yaml'

current_file = prsp.pyradmon_spatial(diagfile,configfile,show=False,save=True)
current_file.generate_plots()

