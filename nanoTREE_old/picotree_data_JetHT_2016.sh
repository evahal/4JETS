#!/bin/bash

cluster=$1
process=$2

# CMSSW setup etc
export SCRAM_ARCH="slc6_amd64_gcc700"
export VO_CMS_SW_DIR="/cms/base/cmssoft"
export COIN_FULL_INDIRECT_RENDERING=1
source $VO_CMS_SW_DIR/cmsset_default.sh

cd /cms/evah/workspace/CMSSW_10_2_2/src/nanoTREE
eval `scramv1 runtime -sh`

#export XRD_NETWORKSTACK=IPv4
#export XRD_REQUESTTIMEOUT=1800
#export XRD_REDIRECTLIMIT=5

python RUPICOTREE_data_JetHT_2016_$2.py >& /cms/evah/workspace/CMSSW_10_2_2/src/nanoTREE/condor_logfiles/data_JetHT_2016/logfile_$1_$2.log
