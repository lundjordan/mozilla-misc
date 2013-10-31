
# checkconfigs
source /path/to/buildbot/virtualenv
PYTHONPATH=$PYTHONPATH:$BUD:$BUD/build-tools/lib/python buildbot checkconfig .  > jlund.py

make reconfig
