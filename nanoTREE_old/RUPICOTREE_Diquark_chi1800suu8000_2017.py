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
	filelist = "filelist_Diquark_chi1800suu8000_2017.txt"
	inputjson = 'Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
        outputjson = 'json/diquarkmc2017.json'
	PicoTreeTest = picoTree("trees/2017/Diquark_chi1800suu8000/tree_Diquark_chi1800suu8000",filelist, 1.5/100000., triggers, jess, jers, True,inputjson,outputjson)
	# Name, Folder, Weight, trigger (list), JES, JER, MCorDATA, inputjson, outputjson #
	# cross section in fb -- taken from Robert paper - 1.5fb

		
