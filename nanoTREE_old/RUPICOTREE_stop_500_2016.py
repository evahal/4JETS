import RUPICOTREE
from RUPICOTREE import *
import ROOT
from ROOT import *

if __name__ == "__main__":
	triggers = ["HLT_PFHT750_4JetPt50","HLT_PFHT750_4JetPt70","HLT_PFHT800_4JetPt50","HLT_PFHT800","HLT_PFHT900"]
	jess = {"JES": PREPJESU("fromMarc/Summer16_07Aug2017_V11_MC_Uncertainty_AK4PFPuppi.txt")}
	jers = {"JER": PREPJERU("fromMarc/Summer16_25nsV1_MC_SF_AK4PFPuppi.txt")}
# cross section in pb
	PicoTreeTest = picoTree("trees/2016/stop_500/tree_stop_500", "/cms/evah/workspace/CMSSW_9_4_9/src/old_runs/RPVStopStopToJets_UDD312_M-500/MultiN/", 518./51048., triggers, jess, jers, True) 
	# cross section above in fb
	# Name, Folder, Weight, trigger (list), JES, JER, MCorDATA #

		
