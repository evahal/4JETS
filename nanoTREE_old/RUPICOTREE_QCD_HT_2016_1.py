import RUPICOTREE
from RUPICOTREE import *
import ROOT
from ROOT import *
import XRootD
from pyxrootd import client
			
if __name__ == "__main__":
	triggers = ["HLT_PFHT750_4JetPt50","HLT_PFHT750_4JetPt70","HLT_PFHT800_4JetPt50","HLT_PFHT800","HLT_PFHT900"]
	jess = {"JES": PREPJESU("fromMarc/Summer16_07Aug2017_V11_MC_Uncertainty_AK4PFPuppi.txt")}
	jers = {"JER": PREPJERU("fromMarc/Summer16_25nsV1_MC_SF_AK4PFPuppi.txt")}
	filelist = "filelist_QCD_HT_200to300_2016_Dec2018.txt"
	inputjson = 'Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON.txt'
        outputjson = 'json/qcdmc2016.json'
	PicoTreeTest = picoTree("trees/2016/QCD_HT_200to300/tree_QCD_HT_200to300", filelist, 1735./(18874815.+39037829.), triggers, jess, jers, True,inputjson,outputjson)
	# Name, Folder, Weight, trigger (list), JES, JER, MCorDATA, inputjson, outputjson #
	# cross section in pb/1000

		
