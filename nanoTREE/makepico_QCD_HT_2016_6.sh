#!/bin/bash    

#source MakePico.sh [output] [inputPath] [goBetween] [year] [Run/MC] [TriggerList] [weight]

# 1500-2000
xsec=121.5  # in pb
nevt=11814547
wgt=$(echo $xsec / $nevt | bc -l)
echo $wgt

cd /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE
eval `scramv1 runtime -sh`

source MakePico.sh QCD_HT1500to2000_2016_1 /cms/se/phedex/store/mc/RunIISummer16NanoAODv6/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/270000/ /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE/gobetween 2016 MC triglist2016MC.txt $wgt

cd /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE
eval `scramv1 runtime -sh`

source MakePico.sh QCD_HT1500to2000_2016_2 /cms/se/phedex/store/mc/RunIISummer16NanoAODv6/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7_ext1-v1/70000/ /cms/evah/workspace/CMSSW_10_6_2/src/4Jets/nanoTREE/gobetween 2016 MC triglist2016MC.txt $wgt




