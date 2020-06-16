import RUPICOTREE_2017
from RUPICOTREE_2017 import *
import ROOT
from ROOT import *
import XRootD
from pyxrootd import client

if __name__ == "__main__":

	triggers = ["HLT_PFHT1050"]
	jess = {"JES": PREPJESU("fromMarc/2017/Fall17_17Nov2017_V32_MC_Uncertainty_AK8PFPuppi.txt")}
	jers = {"JER": PREPJERU("fromMarc/2017/Fall17_V3_MC_SF_AK8PFPuppi.txt")}
	filelist = "filelist_QCD_HT_100to200_2017_Dec2018.txt"
	inputjson = 'Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
        outputjson = 'json/qcdmc2017.json'
	PicoTreeTest = picoTree("trees/2017/QCD_HT_100to200/tree_QCD_HT_100to200",filelist, 27990./96132453., triggers, jess, jers, True,inputjson,outputjson)
	# Name, Folder, Weight, trigger (list), JES, JER, MCorDATA, inputjson, outputjson #
	# cross section in pb/1000

		
