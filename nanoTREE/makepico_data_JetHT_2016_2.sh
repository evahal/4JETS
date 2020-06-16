#!/bin/bash    

#source MakePico.sh [output] [inputPath] [goBetween] [year] [Run/MC] [TriggerList] [weight]

# data
#xsec=27990000.  # in pb
#nevt=82293477
#wgt=$(echo $xsec / $nevt | bc -l)
wgt=1
echo $wgt

cd /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE
eval `scramv1 runtime -sh`

source MakePico.sh data_Run2016D /cms/vlq/NANOAOD/OCT19/JetHT/Run2016D/ /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE/gobetween 2016 D triglist2016BCDEFG.txt $wgt

