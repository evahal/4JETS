import RUPICOTREE
from RUPICOTREE import *
import ROOT
from ROOT import *

if __name__ == "__main__":
	triggers = ["HLT_PFHT750_4JetPt50","HLT_PFHT750_4JetPt70","HLT_PFHT800_4JetPt50","HLT_PFHT800","HLT_PFHT900"]
#	triggers = ["HLT_PFHT750_4JetPt50","HLT_PFHT750_4JetPt70","HLT_PFHT800_4JetPt50","HLT_PFHT800","HLT_PFHT900","HLT_PFHT1050"]
#	triggers = ["HLT_PFHT1050"]
	jess = {"JES": PREPJESU("fromMarc/Summer16_07Aug2017_V11_MC_Uncertainty_AK4PFPuppi.txt")}
	jers = {"JER": PREPJERU("fromMarc/Summer16_25nsV1_MC_SF_AK4PFPuppi.txt")}
# cross section in pb
	PicoTreeTest = picoTree("trees/2016/Xaa_x2000a500/tree_Xaa_x2000a500", "/cms/evah/workspace/CMSSW_9_4_9/src/runscript/XaaNLOttQED0_BBAR_M-x2000a500/MultiN/", 0.0000008862/22950., triggers, jess, jers, True)
	# Name, Folder, Weight, trigger (list), JES, JER, MCorDATA #

		
