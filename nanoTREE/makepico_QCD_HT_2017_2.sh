#!/bin/bash    

#source MakePico.sh [output] [inputPath] [goBetween] [year] [Run/MC] [TriggerList] [weight]

# 300-500
xsec=366800.  # in pb
nevt=61630261
wgt=$(echo $xsec / $nevt | bc -l)
echo $wgt

cd /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE
eval `scramv1 runtime -sh`

source MakePico.sh QCD_HT300to500_2017_1 /cms/se/phedex/store/mc/RunIIFall17NanoAODv6/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/260000/ /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE/gobetween 2017 MC triglist2017MC.txt $wgt

cd /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE
eval `scramv1 runtime -sh`

source MakePico.sh QCD_HT300to500_2017_2 /cms/se/phedex/store/mc/RunIIFall17NanoAODv6/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/270000/ /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE/gobetween 2017 MC triglist2017MC.txt $wgt

cd /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE
eval `scramv1 runtime -sh`

source MakePico.sh QCD_HT300to500_2017_3 /cms/se/phedex/store/mc/RunIIFall17NanoAODv6/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano25Oct2019_102X_mc2017_realistic_v7-v1/280000/ /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE/gobetween 2017 MC triglist2017MC.txt $wgt



