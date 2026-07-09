#!/bin/bash

# Verifies the load script is being run from repository root directory.
if [ $# -gt 0 ]; then
    if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
        cat << EOF
Usage: source $0

Verifies script is run from repository root directory.

Options:
  -h, --help    Show this message
EOF
        return 0
    fi
fi

echo "Verifying current directory..."
echo " "

# For sourced scripts, verify we're in the right place
# Check for required files/directories in current directory
if [ ! -f "load_radmon_config.sh" ] || [ ! -d "offline" ]; then
    echo "Error: Not in repository root"
    echo "Current directory: $PWD"
    echo "Please cd to the pyradmon repository root directory"
    echo "Should contain: load_radmon_config.sh, offline/, etc."
    return 1
fi

echo "Current directory Verified."
echo " "

echo "Loading pyradmon environment..."
echo " "

# Verified - set up environment
export PYRADMON=$PWD

# Activate venv and set pyradmon directory environment variable
source /home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/bin/g5_modules

export PYRADMON_SPATIAL=$PYRADMON/offline/spatial/src
export PYRADMON_TIMESERIES=$PYRADMON/offline/timeseries/src
export PYRADMON_RUN=$PYRADMON/offline/run/

echo "\$PYRADMON set to: $PYRADMON"

# update the timeseries yamls automatically
echo " "
echo '(Automation) Editing timeseries input yamls with user info ...'
cp $PYRADMON_TIMESERIES/test_config_yaml_path.tmpl.geosit.yaml $PYRADMON_TIMESERIES/user_geosit_timeseries_input.yaml
cp $PYRADMON_TIMESERIES/test_config_yaml_path.tmpl.m21c.yaml $PYRADMON_TIMESERIES/user_m21c_timeseries_input.yaml
sed -i "s/{user_id}/$USER/g" $PYRADMON_TIMESERIES/user_geosit_timeseries_input.yaml
sed -i "s/{user_id}/$USER/g" $PYRADMON_TIMESERIES/user_m21c_timeseries_input.yaml
sed -i "s|{PYRADMON_TIMESERIES}|$PYRADMON_TIMESERIES|g" $PYRADMON_TIMESERIES/user_geosit_timeseries_input.yaml
sed -i "s|{PYRADMON_TIMESERIES}|$PYRADMON_TIMESERIES|g" $PYRADMON_TIMESERIES/user_m21c_timeseries_input.yaml
sed -i "s|test_config_yaml_path.tmpl.geosit.yaml|user_geosit_timeseries_input.yaml|" $PYRADMON_TIMESERIES/user_geosit_timeseries_input.yaml
sed -i "s|test_config_yaml_path.tmpl.m21c.yaml|user_m21c_timeseries_input.yaml|" $PYRADMON_TIMESERIES/user_m21c_timeseries_input.yaml

# Check if mod_pyradmon alias exists
if alias mod_pyradmon &>/dev/null; then
    echo ""
    echo "-----------------------------------"
    echo "  pyradmon loaded successfully ✓   "
    echo "-----------------------------------"
    echo ""
else
    cat << 'EOF'

mod_pyradmon alias not found - add this to your .bashrc/.zshrc:

alias mod_pyradmon='export PYRADMON=$NOBACKUP/pyradmon-project/pyradmon ; \
                    cd $PYRADMON ; \
                    module load miniforge ; \
                    source $PYRADMON/load_radmon_config.sh'

-----------------------------------
 pyradmon loaded successfully ✓ 
-----------------------------------

EOF
fi