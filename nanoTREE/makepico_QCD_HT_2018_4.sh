#!/bin/bash    

#source MakePico.sh [output] [inputPath] [goBetween] [year] [Run/MC] [TriggerList] [weight]

# 700-1000
xsec=6524.  # in pb
nevt=48250980
wgt=$(echo $xsec / $nevt | bc -l)
echo $wgt

cd /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE
eval `scramv1 runtime -sh`

source MakePico.sh QCD_HT700to1000_2018 /cms/vlq/NANOAODSIM/OCT19/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv6/ /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE/gobetween 2018 MC triglist2018MC.txt $wgt


