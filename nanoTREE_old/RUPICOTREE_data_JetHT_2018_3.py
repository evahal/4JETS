import RUPICOTREE_2017
from RUPICOTREE_2017 import *
import ROOT
from ROOT import *
import XRootD
from pyxrootd import client

			
if __name__ == "__main__":
	triggers = ["HLT_PFHT1050"]
	# note for jer it is the 2017 one -- need to change this wehn it becomes available
	jess = {"JES": PREPJESU("fromMarc/2018/Autumn18_V3_MC_Uncertainty_AK4PFPuppi.txt")}
	jers = {"JER": PREPJERU("fromMarc/2017/Fall17_V3_MC_SF_AK8PFPuppi.txt")}
	filelist = "filelist_JetHT_Run2018D_Dec2018.txt"
	inputjson = 'Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
        outputjson = 'json/data_Run2018D.json'
	PicoTreeTest = picoTree("trees/2018/data_JetHT_Run2018D/tree_data_JetHT_Run2018D", filelist, 1.0, triggers, jess, jers, False, inputjson,outputjson)
        # Name, Folder, Weight, trigger (list), JES, JER, MCorDATA, inputjson, outputjson #

		
