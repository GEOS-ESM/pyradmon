#!/bin/csh

# Verifies the load script is being run from repository root directory. 
if ( $#argv > 0 ) then
    if ( "$argv[1]" == "-h" || "$argv[1]" == "--help" ) then
        cat << EOF
Usage: source $0

Verifies script is run from repository root directory.

Options:
  -h, --help    Show this message
EOF
        exit 0
    endif
endif


echo "Verifying current directory..."
echo " "


# For sourced scripts, use $_ or just verify we're in the right place
# Check for required files/directories in current directory
if ( ! -f "load_radmon_config.csh" || ! -d "offline" ) then
    echo "Error: Not in repository root"
    echo "Current directory: $PWD"
    echo "Please cd to the pyradmon repository root directory"
    echo "Should contain: load_radmon_config.csh, offline/, etc."
    exit 1
endif


echo "Current directory Verified."
echo " "

echo "Loading pyradmon environment..."
echo " "


# Verified - set up environment
setenv PYRADMON $PWD

# Activate venv and set pyradmon directory environment variable
source /home/dao_ops/GEOSadas-5_29_5_SLES15/GEOSadas/install/bin/g5_modules

setenv PYRADMON_SPATIAL $PYRADMON/offline/spatial/src
setenv PYRADMON_TIMESERIES $PYRADMON/offline/timeseries/src
setenv PYRADMON_RUN $PYRADMON/offline/run/

echo '$PYRADMON set to:' $PYRADMON

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
alias mod_pyradmon >& /dev/null
if ( $? == 0 ) then
    echo ""
    #echo "✓ mod_pyradmon alias already exists"
    echo "-----------------------------------"
    echo "  pyradmon loaded successfully ✓   "
    echo "-----------------------------------"
    echo ""

else
    cat << 'EOF'

mod_pyradmon alias not found - add this to your .cshrc/.zshrc:

alias mod_pyradmon ' setenv PYRADMON $NOBACKUP/pyradmon-project/pyradmon ; \
                     cd $PYRADMON ; \
                     module load miniforge ; \
                     source $PYRADMON/load_radmon_config.csh'

-----------------------------------
 pyradmon loaded successfully ✓ 
-----------------------------------


EOF
endif

# echo "pyradmon loaded successfully."