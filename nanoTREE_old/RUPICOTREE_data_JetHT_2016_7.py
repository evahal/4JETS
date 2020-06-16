import RUPICOTREE
from RUPICOTREE import *
import ROOT
from ROOT import *
			
if __name__ == "__main__":
	triggers = ["HLT_PFHT750_4JetPt70","HLT_PFHT800_4JetPt50","HLT_PFHT900","HLT_PFJet450"]
	jess = {"JES": PREPJESU("fromMarc/Summer16_07Aug2017_V11_MC_Uncertainty_AK4PFPuppi.txt")}
	jers = {"JER": PREPJERU("fromMarc/Summer16_25nsV1_MC_SF_AK4PFPuppi.txt")}
#        filelist = "filelist_JetHT_Run2016H_Dec2018.txt"
        filelist = "filelist_JetHT_Run2016H_Feb2018.txt"
#	inputjson = 'Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'
	inputjson = 'Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON_Alejandro.txt'
        outputjson = 'json/data_Run2016H.json'
	PicoTreeTest = picoTree("trees/2016/data_JetHT_Run2016H/tree_data_JetHT_Run2016H",filelist, 1.0, triggers, jess, jers, False, inputjson,outputjson)
	# Name, Folder, Weight, trigger (list), JES, JER, MCorDATA, inputjson, outputjson #

		
