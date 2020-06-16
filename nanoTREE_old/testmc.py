import RUPICOTREE
from RUPICOTREE import *
import ROOT
from ROOT import *
			
if __name__ == "__main__":

	triggers = ["HLT_PFHT750_4JetPt50","HLT_PFHT750_4JetPt70","HLT_PFHT800_4JetPt50","HLT_PFHT800","HLT_PFHT900"]
	jess = {"JES": PREPJESU("fromMarc/Summer16_07Aug2017_V11_MC_Uncertainty_AK4PFPuppi.txt")}
	jers = {"JER": PREPJERU("fromMarc/Summer16_25nsV1_MC_SF_AK4PFPuppi.txt")}
	PicoTreeTest = picoTree("testmc", "/cms/xaastorage/NanoAOD/2016/2016_QCD_HT/HT_1500to2000/HT_1500to2000_1", 0.1215/3971631., triggers, jess, jers, True)
	# Name, Folder, Weight, trigger (list), JES, JER, MCorDATA #		
