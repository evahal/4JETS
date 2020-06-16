import RUPICOTREE_2017
from RUPICOTREE_2017 import *
import ROOT
from ROOT import *
import XRootD
from pyxrootd import client

if __name__ == "__main__":

	### need to update with QCD autumn 18 is copied over ###
	triggers = ["HLT_PFHT1050"]
	# note for jer it is the 2017 one -- need to change this wehn it becomes available
	jess = {"JES": PREPJESU("fromMarc/2018/Autumn18_V3_MC_Uncertainty_AK4PFPuppi.txt")}
	jers = {"JER": PREPJERU("fromMarc/2017/Fall17_V3_MC_SF_AK8PFPuppi.txt")}
	filelist = "filelist_QCD_HT_1500to2000_2018_Dec2018.txt"
	inputjson = 'Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt'
        outputjson = 'json/qcdmc2018.json'
	PicoTreeTest = picoTree("trees/2018/QCD_HT_1500to2000/tree_QCD_HT_1500to2000",filelist, 0.1215/11433973., triggers, jess, jers, True,inputjson,outputjson)
	# Name, Folder, Weight, trigger (list), JES, JER, MCorDATA, inputjson, outputjson #
	# cross section in pb/1000

		
