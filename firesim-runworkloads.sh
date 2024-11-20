#!/usr/bin/env bash

# exit script if any command fails
set -e
set -o pipefail

#entire firesim
cd sims/firesim/deploy

rm -rf results-workload/*

rm -rf /scratch/FIRESIMRUNDIR

# run m3500 first
firesim infrasetup && firesim runworkload
mv results-workload/20* results-workload/m3500-ra

# clear out run directly after it finishes
# the run results have already been copied to results-workload
# replace with your simulation_dir path (config_runtime.yaml)
rm -rf /scratch/FIRESIMRUNDIR

sed -i "s/workload_name: m3500/workload_name: cab7k/g" config_runtime.yaml

firesim infrasetup && firesim runworkload
mv results-workload/20* results-workload/cab7k-ra

# clear out run directly after it finishes
# the run results have already been copied to results-workload
# replace with your simulation_dir path (config_runtime.yaml)
rm -rf /scratch/FIRESIMRUNDIR

sed -i "s/workload_name: cab7k/workload_name: sphere/g" config_runtime.yaml

firesim infrasetup && firesim runworkload
mv results-workload/20* results-workload/sphere-ra

# clear out run directly after it finishes
# the run results have already been copied to results-workload
# replace with your simulation_dir path (config_runtime.yaml)
rm -rf /scratch/FIRESIMRUNDIR

sed -i "s/workload_name: sphere/workload_name: cab464/g" config_runtime.yaml

firesim infrasetup && firesim runworkload
mv results-workload/20* results-workload/cab464-ra

# clear out run directly after it finishes
# the run results have already been copied to results-workload
# replace with your simulation_dir path (config_runtime.yaml)
rm -rf /scratch/FIRESIMRUNDIR

# copy over result parsing scripts
cp -r ../../../parser/* results-workload/.

