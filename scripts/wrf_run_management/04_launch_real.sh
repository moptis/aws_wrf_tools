#!/bin/bash

domain='pilot_hill'
t='distant'

export domain
export t
sbatch ./04b_submit_real.sbatch
