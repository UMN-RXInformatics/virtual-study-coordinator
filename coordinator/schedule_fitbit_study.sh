#!/bin/bash

[[ $(type -t deactivate) == 'function' ]] && deactivate

export SALSA_SCRIPTS=$(dirname $0)
export SALSASERVER_HOME=$(dirname $SALSA_SCRIPTS)
source $SALSASERVER_HOME/env/bin/activate

python $SALSA_SCRIPTS/redcap_fitbit_check.py >> $(dirname $SALSA_SCRIPTS)/fitbit.log
