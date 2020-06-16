Install:
cmsrel CMSSW_10_6_2

cd CMSSW_10_6_2/src

git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools

cmsenv

scram b -j8

git clone https://github.com/evahal/4JETS.git

Running (Treemaker):
This code (in the treemaker folder) turns nanoAOD into useable picotrees.

source MakePico.sh [output] [inputPath] [goBetween] [year] [Run/MC] [TriggerList] [weight]

ouput: Name of the output file (must be unique)
inputPath: path to the nanoAOd. Can inlude wildcards if you want to run over a subset of files
goBetween: path to a folder you can store intermediate nanoSkims (so womewhere you have space to store some large-ish files)
year: dataset year
Run/MC: if this is data, the run period, if this is MC, just write "MC"
TriggerList: text file containing the names of the triggers you want to keep
weight: 1 for data, cross-section / Nevents for MC
Example (MC):

source MakePico.sh X1000a50 /cms/xaastorage/NanoAOD/2016/JUNE19/Xaa_Signal/X1000a50/ /cms/osherson/NanoToolOutput 2016 MC triglist.txt 0.0002

Example (Data, just running on one file):

source MakePico.sh Data16C /cms/xaastorage/NanoAOD/2016/JUNE19/JetHT_DATA/Run2016C/910727BA-1093-0343-B569-CD480F6CCC7F /cms/osherson/NanoToolOutput 2016 C triglist.txt 1

source MakePico.sh X1000a50 /cms/xaastorage/NanoAOD/2016/JUNE19/Xaa_Signal/X1000a50/ /cms/osherson/NanoToolOutput 2016 MC triglist.txt 1
