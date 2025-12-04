#!/usr/bin/env python3

import pyradmon_spatial as prsp

diagfile = sys.argv[1]

#configfile = './init_config.yaml'
configfile = './init_oma_hyper_config.yaml'

current_file = prsp.pyradmon_spatial(diagfile,configfile,show=False,save=True)
current_file.generate_plots()

