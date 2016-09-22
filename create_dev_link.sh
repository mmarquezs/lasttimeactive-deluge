#!/bin/bash
cd /home/marcmarquez/repositoris/lasttimeactive-deluge/lasttimeactive
mkdir temp
export PYTHONPATH=./temp
/usr/bin/python2 setup.py build develop --install-dir ./temp
cp ./temp/lasttimeactive.egg-link /home/marcmarquez/.config/deluge/plugins
rm -fr ./temp
