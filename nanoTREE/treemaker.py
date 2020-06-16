import os
import ROOT
from ROOT import *
from array import array
import math
import numpy
from math import *
import sys
import glob
import csv
import XRootD
from pyxrootd import client
from FWCore.PythonUtilities.LumiList import LumiList

class picoTree:
#	def __init__(self, name, inputFile, weight, folder, mc, year, injfile,outjfile):
	def __init__(self, name, inputFile, weight, folder, mc, year):
                self.year = year
                self.mc = mc == "MC"
                self.weight = weight
                self.__book__(name, folder)
#                self.TrigFile = TFile("TriggerScaleFactors.root")
#                self.TrigHist = self.TrigFile.Get(year)
                self.Fill(inputFile)
                self.O.cd()
                self.O.Write()
                self.O.Close()

#add this back in later - but move to above - see my old example
#		# get json file
#		myList = LumiList (filename = injfile)
#		# initialize output lumilist
#		myrunlumi =[]
#		# open root files
#		files = open(nanotrees,"r")
##		for file in glob.glob(nanotrees + "*root"):
#		for file in files.read().splitlines():
#			self.Fill(file, triggers,myList,myrunlumi)
#
#		# only do this for data			
#		if not (self.mc):
#			outList = LumiList(lumis = myrunlumi)
#			outList.writeJSON(outjfile)

	def __book__(self, name,folder):
                self.O = TFile(folder+"/"+name+".root", "recreate")
                self.O.cd()
                self.T_nominal = TTree("tree_nominal", "tree_nominal")
                if self.mc:
                        self.T_jesCorr_up = TTree("tree_jesCorr_up", "tree_jesCorr_up")
                        self.T_jesCorr_down = TTree("tree_jesCorr_down", "tree_jesCorr_down")
                        self.T_jesUnCorr_up = TTree("tree_jesUnCorr_up", "tree_jesUnCorr_up")
                        self.T_jesUnCorr_down = TTree("tree_jesUnCorr_down", "tree_jesUnCorr_down")
                        self.T_jer_up = TTree("tree_jer_up", "tree_jer_up")
                        self.T_jer_down = TTree("tree_jer_down", "tree_jer_down")
                        # MC ONLY VARIABLES
                        self.W = array('f', [0.0])
                        self.AddBranch('weight_xsN', self.W)
                        self.Wpu = array('f', [0.0])
                        self.AddBranch('weight_PU', self.Wpu)
                        self.Wpuu = array('f', [0.0])
                        self.AddBranch('weight_PU_up', self.Wpuu)
                        self.Wpud = array('f', [0.0])
                        self.AddBranch('weight_PU_dn', self.Wpud)
                        self.PDFup = array('f', [0.0])
                        self.AddBranch('weight_pdf_up', self.PDFup)
                        self.PDFdn = array('f', [0.0])
                        self.AddBranch('weight_pdf_dn', self.PDFdn)
		
		# EVENT VARIABLES
		self.evt_run = array('f', [-1.0])
                self.AddBranch('evt_run', self.evt_run)
		self.evt_lumi = array('f', [-1.0])
                self.AddBranch('evt_lumiblock', self.evt_lumi)
                self.evt_event = array('L', [0])
                self.AddBranchIL('evt_event', self.evt_event)
		self.evt_NPV = array('i', [-1])
                self.AddBranchI('evt_NPV', self.evt_NPV)
		self.evt_4JetM = array('f', [-1.0])
		self.AddBranch('evt_4JetM', self.evt_4JetM)
		self.evt_DeltaDR = array('f', [-1.0])
		self.AddBranch('evt_DeltaDR', self.evt_DeltaDR)
		self.evt_2JetM = array('f', [-1.0])
		self.AddBranch('evt_2JetM', self.evt_2JetM)
		self.evt_Masym = array('f', [-1.0])
		self.AddBranch('evt_Masym', self.evt_Masym)
		self.evt_DEta = array('f', [-1.0])
		self.AddBranch('evt_Deta', self.evt_DEta)
		self.evt_HTAK4 = array('f', [-1.0])
		self.AddBranch('evt_HTAK4', self.evt_HTAK4)
		self.evt_NJets = array('f', [-1.0])
		self.AddBranch('evt_NJets', self.evt_NJets)
		# DIJET PAIR VARIABLES
		self.dj1_pt = array('f', [-1.0])
		self.AddBranch('dj1_pt', self.dj1_pt)
		self.dj1_eta = array('f', [-1.0])
		self.AddBranch('dj1_eta', self.dj1_eta)
		self.dj1_phi = array('f', [-1.0])
		self.AddBranch('dj1_phi', self.dj1_phi)
		self.dj1_m = array('f', [-1.0])
		self.AddBranch('dj1_m', self.dj1_m)
		self.dj1_delta = array('f', [-1.0])
		self.AddBranch('dj1_delta', self.dj1_delta)
		self.dj2_pt = array('f', [-1.0])
		self.AddBranch('dj2_pt', self.dj2_pt)
		self.dj2_eta = array('f', [-1.0])
		self.AddBranch('dj2_eta', self.dj2_eta)
		self.dj2_phi = array('f', [-1.0])
		self.AddBranch('dj2_phi', self.dj2_phi)
		self.dj2_m = array('f', [-1.0])
		self.AddBranch('dj2_m', self.dj2_m)
		self.dj2_delta = array('f', [-1.0])
		self.AddBranch('dj2_delta', self.dj2_delta)
		# SINGLE JET VARIABLES	
		self.j1_pt = array('f', [-1.0])
		self.AddBranch('j1_pt', self.j1_pt)
		self.j1_eta = array('f', [-1.0])
		self.AddBranch('j1_eta', self.j1_eta)
		self.j1_phi = array('f', [-1.0])
		self.AddBranch('j1_phi', self.j1_phi)
		self.j1_m = array('f', [-1.0])
		self.AddBranch('j1_m', self.j1_m)
		self.j1_btag = array('f', [-1.0])
		self.AddBranch('j1_btag', self.j1_btag)
		self.j2_pt = array('f', [-1.0])
		self.AddBranch('j2_pt', self.j2_pt)
		self.j2_eta = array('f', [-1.0])
		self.AddBranch('j2_eta', self.j2_eta)
		self.j2_phi = array('f', [-1.0])
		self.AddBranch('j2_phi', self.j2_phi)
		self.j2_m = array('f', [-1.0])
		self.AddBranch('j2_m', self.j2_m)
		self.j2_btag = array('f', [-1.0])
		self.AddBranch('j2_btag', self.j2_btag)
		self.j3_pt = array('f', [-1.0])
		self.AddBranch('j3_pt', self.j3_pt)
		self.j3_eta = array('f', [-1.0])
		self.AddBranch('j3_eta', self.j3_eta)
		self.j3_phi = array('f', [-1.0])
		self.AddBranch('j3_phi', self.j3_phi)
		self.j3_m = array('f', [-1.0])
		self.AddBranch('j3_m', self.j3_m)
		self.j3_btag = array('f', [-1.0])
		self.AddBranch('j3_btag', self.j3_btag)
		self.j4_pt = array('f', [-1.0])
		self.AddBranch('j4_pt', self.j4_pt)
		self.j4_eta = array('f', [-1.0])
		self.AddBranch('j4_eta', self.j4_eta)
		self.j4_phi = array('f', [-1.0])
		self.AddBranch('j4_phi', self.j4_phi)
		self.j4_m = array('f', [-1.0])
		self.AddBranch('j4_m', self.j4_m)
		self.j4_btag = array('f', [-1.0])
		self.AddBranch('j4_btag', self.j4_btag)
		
	def Fill(self, inputFile):
		print "Filling from " + inputFile
		F = TFile(inputFile)
		
		if F:
			print('is open')
		else:
			print('oops')

		# initialize event count for skipping events below
		nevt=0
		self.T = F.Get("Events")
		for e in self.T:
                        self.e = e
# Check that events for data pass the golden json file
#	       		passJson = False

#			if self.mc:
#				passJson = True
#			else:
#				passJson = jlist.contains(self.T.run,self.T.luminosityBlock)
#
#			if not(passJson): continue

#			# fill the run lumi list here after the trigger selection for data
#			if not (self.mc):
#				rllist.append((self.T.run,self.T.luminosityBlock))

########################################################################################
			# FOR NOW READ ONLY EVERY 15th event for 2017 and 2018 DATA

			# increment event counter
			nevt += 1
			if not (self.mc):
                                if not (self.year == "2016"): 
                                        if nevt % 15 !=0: continue
                                        
#######################################################################################

                        if self.year == "2016": IDCUT = 2
                        if self.year == "2017": IDCUT = 5
                        if self.year == "2018": IDCUT = 5


			self.njets=0
			self.HT=0.0
			self.imyJets = []

			for j in range(len(self.T.Jet_pt_nom)):
				# tight jet id cut =3 for 2016
#				if (self.T.Jet_pt_nom[j]>80.0 and math.fabs(self.T.Jet_eta[j])<2.5 and self.T.Jet_jetId[j]==3): 
				# tight jet id cut with lepton veto - 2016
#				if (self.T.Jet_pt_nom[j]>80.0 and math.fabs(self.T.Jet_eta[j])<2.5 and self.T.Jet_jetId[j]==3 and self.T.Jet_muEF[j]<0.8 and self.T.Jet_chEmEF[j]<0.9): 
				# jetid tight lepton veto =6 for 2017 and 2018
				if (self.T.Jet_pt_nom[j]>50.0 and math.fabs(self.T.Jet_eta[j])<2.4 and self.T.Jet_jetId[j]> IDCUT): 
					self.njets += 1
					self.HT +=  self.T.Jet_pt_nom[j]
					self.imyJets.append(j)

                        if self.mc:
                                self.W[0] = float(self.weight)
                                self.Wpu[0] = self.T.puWeight
                                if self.T.puWeight > 0:
                                        self.Wpuu[0] = self.T.puWeightUp/self.T.puWeight
                                        self.Wpud[0] = self.T.puWeightDown/self.T.puWeight

                                self.PDFup[0] = 1 + numpy.std(self.T.LHEPdfWeight)
                                self.PDFdn[0] = 1 - numpy.std(self.T.LHEPdfWeight)										


			if not (self.njets>3 and self.HT>900.0): continue
			
			
			ind0 = self.imyJets[0]
			ind1 = self.imyJets[1]
			ind2 = self.imyJets[2]
			ind3 = self.imyJets[3]

			J1 = TLorentzVector()
			J2 = TLorentzVector()
			J3 = TLorentzVector()
			J4 = TLorentzVector()
			
			J1.SetPtEtaPhiM(self.T.Jet_pt_nom[ind0], self.T.Jet_eta[ind0], self.T.Jet_phi[ind0], self.T.Jet_mass_nom[ind0])
			J2.SetPtEtaPhiM(self.T.Jet_pt_nom[ind1], self.T.Jet_eta[ind1], self.T.Jet_phi[ind1], self.T.Jet_mass_nom[ind1])
			J3.SetPtEtaPhiM(self.T.Jet_pt_nom[ind2], self.T.Jet_eta[ind2], self.T.Jet_phi[ind2], self.T.Jet_mass_nom[ind2])
			J4.SetPtEtaPhiM(self.T.Jet_pt_nom[ind3], self.T.Jet_eta[ind3], self.T.Jet_phi[ind3], self.T.Jet_mass_nom[ind3])
			self.FillJetVars([J1,J2,J3,J4], [ind0, ind1, ind2, ind3], self.T_nominal)


			if self.mc:

# JEC up Corr			
				JsUc1 = TLorentzVector() 
				JsUc2 = TLorentzVector()
				JsUc3 = TLorentzVector()
				JsUc4 = TLorentzVector()

                                Kin_jesCorrUp0 = self.GetJESComp("C", "Up",ind0)
                                Kin_jesCorrUp1 = self.GetJESComp("C", "Up",ind1)
                                Kin_jesCorrUp2 = self.GetJESComp("C", "Up",ind2)
                                Kin_jesCorrUp3 = self.GetJESComp("C", "Up",ind3)

                                JsUc1.SetPtEtaPhiM(Kin_jesCorrUp0[0][0], self.T.Jet_eta[ind0], self.T.Jet_phi[ind0], Kin_jesCorrUp0[1][0])
                                JsUc2.SetPtEtaPhiM(Kin_jesCorrUp1[0][0], self.T.Jet_eta[ind1], self.T.Jet_phi[ind1], Kin_jesCorrUp1[1][0])
                                JsUc3.SetPtEtaPhiM(Kin_jesCorrUp2[0][0], self.T.Jet_eta[ind2], self.T.Jet_phi[ind2], Kin_jesCorrUp2[1][0])
                                JsUc4.SetPtEtaPhiM(Kin_jesCorrUp3[0][0], self.T.Jet_eta[ind3], self.T.Jet_phi[ind3], Kin_jesCorrUp3[1][0])

# JEC down Corr
				JsDc1 = TLorentzVector()
				JsDc2 = TLorentzVector()
				JsDc3 = TLorentzVector()
				JsDc4 = TLorentzVector()

                                Kin_jesCorrDown0 = self.GetJESComp("C", "Down",ind0)
                                Kin_jesCorrDown1 = self.GetJESComp("C", "Down",ind1)
                                Kin_jesCorrDown2 = self.GetJESComp("C", "Down",ind2)
                                Kin_jesCorrDown3 = self.GetJESComp("C", "Down",ind3)

                                JsDc1.SetPtEtaPhiM(Kin_jesCorrDown0[0][0], self.T.Jet_eta[ind0], self.T.Jet_phi[ind0], Kin_jesCorrDown0[1][0])
                                JsDc2.SetPtEtaPhiM(Kin_jesCorrDown1[0][0], self.T.Jet_eta[ind1], self.T.Jet_phi[ind1], Kin_jesCorrDown1[1][0])
                                JsDc3.SetPtEtaPhiM(Kin_jesCorrDown2[0][0], self.T.Jet_eta[ind2], self.T.Jet_phi[ind2], Kin_jesCorrDown2[1][0])
                                JsDc4.SetPtEtaPhiM(Kin_jesCorrDown3[0][0], self.T.Jet_eta[ind3], self.T.Jet_phi[ind3], Kin_jesCorrDown3[1][0])

# JEC up unCorr
				JsUu1 = TLorentzVector() 
				JsUu2 = TLorentzVector()
				JsUu3 = TLorentzVector()
				JsUu4 = TLorentzVector()

                                Kin_jesUnCorrUp0 = self.GetJESComp("U", "Up",ind0)
                                Kin_jesUnCorrUp1 = self.GetJESComp("U", "Up",ind1)
                                Kin_jesUnCorrUp2 = self.GetJESComp("U", "Up",ind2)
                                Kin_jesUnCorrUp3 = self.GetJESComp("U", "Up",ind3)

                                JsUu1.SetPtEtaPhiM(Kin_jesUnCorrUp0[0][0], self.T.Jet_eta[ind0], self.T.Jet_phi[ind0], Kin_jesUnCorrUp0[1][0])
                                JsUu2.SetPtEtaPhiM(Kin_jesUnCorrUp1[0][0], self.T.Jet_eta[ind1], self.T.Jet_phi[ind1], Kin_jesUnCorrUp1[1][0])
                                JsUu3.SetPtEtaPhiM(Kin_jesUnCorrUp2[0][0], self.T.Jet_eta[ind2], self.T.Jet_phi[ind2], Kin_jesUnCorrUp2[1][0])
                                JsUu4.SetPtEtaPhiM(Kin_jesUnCorrUp3[0][0], self.T.Jet_eta[ind3], self.T.Jet_phi[ind3], Kin_jesUnCorrUp3[1][0])

# JEC down unCorr
				JsDu1 = TLorentzVector() 
				JsDu2 = TLorentzVector()
				JsDu3 = TLorentzVector()
				JsDu4 = TLorentzVector()

                                Kin_jesUnCorrDown0 = self.GetJESComp("U", "Down",ind0)
                                Kin_jesUnCorrDown1 = self.GetJESComp("U", "Down",ind1)
                                Kin_jesUnCorrDown2 = self.GetJESComp("U", "Down",ind2)
                                Kin_jesUnCorrDown3 = self.GetJESComp("U", "Down",ind3)

                                JsDu1.SetPtEtaPhiM(Kin_jesUnCorrDown0[0][0], self.T.Jet_eta[ind0], self.T.Jet_phi[ind0], Kin_jesUnCorrDown0[1][0])
                                JsDu2.SetPtEtaPhiM(Kin_jesUnCorrDown1[0][0], self.T.Jet_eta[ind1], self.T.Jet_phi[ind1], Kin_jesUnCorrDown1[1][0])
                                JsDu3.SetPtEtaPhiM(Kin_jesUnCorrDown2[0][0], self.T.Jet_eta[ind2], self.T.Jet_phi[ind2], Kin_jesUnCorrDown2[1][0])
                                JsDu4.SetPtEtaPhiM(Kin_jesUnCorrDown3[0][0], self.T.Jet_eta[ind3], self.T.Jet_phi[ind3], Kin_jesUnCorrDown3[1][0])

				self.FillJetVars([JsUc1,JsUc2,JsUc3,JsUc4], [ind0, ind1, ind2, ind3], self.T_jesCorr_up)
				self.FillJetVars([JsDc1,JsDc2,JsDc3,JsDc4], [ind0, ind1, ind2, ind3], self.T_jesCorr_down)
				self.FillJetVars([JsUu1,JsUu2,JsUu3,JsUu4], [ind0, ind1, ind2, ind3], self.T_jesUnCorr_up)
				self.FillJetVars([JsDu1,JsDu2,JsDu3,JsDu4], [ind0, ind1, ind2, ind3], self.T_jesUnCorr_down)			

# JER
                                JrU1 = TLorentzVector()
                                JrU2 = TLorentzVector()
                                JrU3 = TLorentzVector()
                                JrU4 = TLorentzVector()

                                JrD1 = TLorentzVector()
                                JrD2 = TLorentzVector()
                                JrD3 = TLorentzVector()
                                JrD4 = TLorentzVector()
			
                                JrU1.SetPtEtaPhiM(self.T.Jet_pt_jerUp[ind0], self.T.Jet_eta[ind0], self.T.Jet_phi[ind0], self.T.Jet_mass_jerUp[ind0])
                                JrU2.SetPtEtaPhiM(self.T.Jet_pt_jerUp[ind1], self.T.Jet_eta[ind1], self.T.Jet_phi[ind1], self.T.Jet_mass_jerUp[ind1])
                                JrU3.SetPtEtaPhiM(self.T.Jet_pt_jerUp[ind2], self.T.Jet_eta[ind2], self.T.Jet_phi[ind2], self.T.Jet_mass_jerUp[ind2])
                                JrU4.SetPtEtaPhiM(self.T.Jet_pt_jerUp[ind3], self.T.Jet_eta[ind3], self.T.Jet_phi[ind3], self.T.Jet_mass_jerUp[ind3])

                                JrD1.SetPtEtaPhiM(self.T.Jet_pt_jerDown[ind0], self.T.Jet_eta[ind0], self.T.Jet_phi[ind0], self.T.Jet_mass_jerDown[ind0])
                                JrD2.SetPtEtaPhiM(self.T.Jet_pt_jerDown[ind1], self.T.Jet_eta[ind1], self.T.Jet_phi[ind1], self.T.Jet_mass_jerDown[ind1])
                                JrD3.SetPtEtaPhiM(self.T.Jet_pt_jerDown[ind2], self.T.Jet_eta[ind2], self.T.Jet_phi[ind2], self.T.Jet_mass_jerDown[ind2])
                                JrD4.SetPtEtaPhiM(self.T.Jet_pt_jerDown[ind3], self.T.Jet_eta[ind3], self.T.Jet_phi[ind3], self.T.Jet_mass_jerDown[ind3])

				self.FillJetVars([JrU1,JrU2,JrU3,JrU4], [ind0, ind1, ind2, ind3], self.T_jer_up)
				self.FillJetVars([JrD1,JrD2,JrD3,JrD4], [ind0, ind1, ind2, ind3], self.T_jer_down)


		F.Close()

        def GET(self, B, i):
                return getattr(self.e, B)[i]

        def GetCorrectedVal(self, var, i, W, C):
            delta = 0.
            if C == "C":
                    Sys = [
                ["AbsoluteMPFBias", 1.],
                ["AbsoluteScale", 1.],
                ["FlavorQCD", 1.],
                ["Fragmentation", 1.],
                ["PileUpDataMC", 2.],
                ["PileUpPtBB", 2.],
                ["PileUpPtEC1", 2.],
                ["PileUpPtEC2", 2.],
                ["PileUpPtHF", 2.],
                ["PileUpPtRef", 2.],
                ["RelativeFSR", 2.],
                ["RelativeJERHF", 2.],
                ["RelativePtBB", 2.],
                ["RelativePtHF", 2.],
                ["RelativeBal", 2.],
                ["SinglePionECAL", 1.],
                ["SinglePionHCAL", 1.]
                    ]
                    for S in Sys:
                            delta += ((self.GET(var+"_jes"+S[0]+W, i) - self.GET(var+"_nom", i))/(S[1]*self.GET(var+"_nom", i)))**2
            if C == "U":
                    Sys = [
                ["AbsoluteStat", 1.],
                ["PileUpDataMC", 2.],
                ["PileUpPtBB", 2.],
                ["PileUpPtEC1", 2.],
                ["PileUpPtEC2", 2.],
                ["PileUpPtHF", 2.],
                ["PileUpPtRef", 2.],
                ["RelativeFSR", 2.],
                ["RelativeJERHF", 2.],
                ["RelativePtBB", 2.],
                ["RelativePtHF", 2.],
                ["RelativeBal", 2.],
                ["RelativeJEREC1", 1.],
                ["RelativeJEREC2", 1.],
                ["RelativePtEC1", 1.],
                ["RelativePtEC2", 1.],
                ["RelativeSample", 1.],
                ["RelativeStatEC", 1.],
                ["RelativeStatFSR", 1.],
                ["RelativeStatHF", 1.],
                ["TimePtEta", 1.]
                    ]
                    for S in Sys:
                            delta += ((self.GET(var+"_jes"+S[0]+W, i) - self.GET(var+"_nom", i))/(S[1]*self.GET(var+"_nom", i)))**2
            fac = 0.
            if W == "Up": fac = 1 + math.sqrt(delta)
            if W == "Down": fac = 1 - math.sqrt(delta)
            return self.GET(var+"_nom", i) * (fac)

        def GetJESComp(self, corr, which, ii):
                PT4 = []
                MASS = []
                for jet in [ii]: 
                        PT4.append(self.GetCorrectedVal("Jet_pt", jet, which, corr))
                        MASS.append(self.GetCorrectedVal("Jet_mass", jet, which, corr))
                return [PT4, MASS]

		
        def FillJetVars(self, JETS, jind, B):
		J1 = JETS[0]
		J2 = JETS[1]
		J3 = JETS[2]
		J4 = JETS[3]

		jind0 = jind[0]
		jind1 = jind[1]
		jind2 = jind[2]
		jind3 = jind[3]
		
		DJ1 = TLorentzVector()
		DJ2 = TLorentzVector()
	
		FourJetMass = (J1+J2+J3+J4).M()
		
		DR12 = J1.DeltaR(J2)
		DR13 = J1.DeltaR(J3)
		DR14 = J1.DeltaR(J4)
		DR23 = J2.DeltaR(J3)
		DR24 = J2.DeltaR(J4)
		DR34 = J3.DeltaR(J4)
		DeltaDR1234 = math.fabs(DR12 - 0.8) + math.fabs(DR34 - 0.8)
		DeltaDR1324 = math.fabs(DR13 - 0.8) + math.fabs(DR24 - 0.8)
		DeltaDR1423 = math.fabs(DR14 - 0.8) + math.fabs(DR23 - 0.8)
		if min(DeltaDR1234, DeltaDR1324, DeltaDR1423) == DeltaDR1234:
			DeltaDR = DeltaDR1234
			DJ1 = J1+J2
			DJ2 = J3+J4	
			self.dj1_pt[0] = DJ1.Pt()
			self.dj1_eta[0] = DJ1.Eta()
			self.dj1_phi[0] = DJ1.Phi()
			self.dj1_m[0] = DJ1.M()
			self.dj1_delta[0] = J1.Pt() + J2.Pt() - ((DJ1.M() + DJ2.M())/2.)
			self.dj2_pt[0] = DJ2.Pt()
			self.dj2_eta[0] = DJ2.Eta()
			self.dj2_phi[0] = DJ2.Phi()
			self.dj2_m[0] = DJ2.M()
			self.dj2_delta[0] = J3.Pt() + J4.Pt() - ((DJ1.M() + DJ2.M())/2.)
			self.j1_pt[0] = J1.Pt()
			self.j1_eta[0] = J1.Eta()
			self.j1_phi[0] = J1.Phi()
			self.j1_m[0] = J1.M()
			self.j1_btag[0] = self.T.Jet_btagCSVV2[jind0]
			self.j2_pt[0] = J2.Pt()
			self.j2_eta[0] = J2.Eta()
			self.j2_phi[0] = J2.Phi()
			self.j2_m[0] = J2.M()
			self.j2_btag[0] = self.T.Jet_btagCSVV2[jind1]
			self.j3_pt[0] = J3.Pt()
			self.j3_eta[0] = J3.Eta()
			self.j3_phi[0] = J3.Phi()
			self.j3_m[0] = J3.M()
			self.j3_btag[0] = self.T.Jet_btagCSVV2[jind2]
			self.j4_pt[0] = J4.Pt()
			self.j4_eta[0] = J4.Eta()
			self.j4_phi[0] = J4.Phi()
			self.j4_m[0] = J4.M()
			self.j4_btag[0] = self.T.Jet_btagCSVV2[jind3]
		elif min(DeltaDR1234, DeltaDR1324, DeltaDR1423) == DeltaDR1324:
			DeltaDR = DeltaDR1324
			DJ1 = J1+J3
			DJ2 = J2+J4	
			self.dj1_pt[0] = DJ1.Pt()
			self.dj1_eta[0] = DJ1.Eta()
			self.dj1_phi[0] = DJ1.Phi()
			self.dj1_m[0] = DJ1.M()
			self.dj1_delta[0] = J1.Pt() + J3.Pt() - ((DJ1.M() + DJ2.M())/2.)
			self.dj2_pt[0] = DJ2.Pt()
			self.dj2_eta[0] = DJ2.Eta()
			self.dj2_phi[0] = DJ2.Phi()
			self.dj2_m[0] = DJ2.M()
			self.dj2_delta[0] = J2.Pt() + J4.Pt() - ((DJ1.M() + DJ2.M())/2.)
			self.j1_pt[0] = J1.Pt()
			self.j1_eta[0] = J1.Eta()
			self.j1_phi[0] = J1.Phi()
			self.j1_m[0] = J1.M()
			self.j1_btag[0] = self.T.Jet_btagCSVV2[jind0]
			self.j2_pt[0] = J3.Pt()
			self.j2_eta[0] = J3.Eta()
			self.j2_phi[0] = J3.Phi()
			self.j2_m[0] = J3.M()
			self.j2_btag[0] = self.T.Jet_btagCSVV2[jind2]
			self.j3_pt[0] = J2.Pt()
			self.j3_eta[0] = J2.Eta()
			self.j3_phi[0] = J2.Phi()
			self.j3_m[0] = J2.M()
			self.j3_btag[0] = self.T.Jet_btagCSVV2[jind1]
			self.j4_pt[0] = J4.Pt()
			self.j4_eta[0] = J4.Eta()
			self.j4_phi[0] = J4.Phi()
			self.j4_m[0] = J4.M()
			self.j4_btag[0] = self.T.Jet_btagCSVV2[jind3]
		elif min(DeltaDR1234, DeltaDR1324, DeltaDR1423) == DeltaDR1423:
			DeltaDR = DeltaDR1423
			DJ1 = J1+J4
			DJ2 = J2+J3	
			self.dj1_pt[0] = DJ1.Pt()
			self.dj1_eta[0] = DJ1.Eta()
			self.dj1_phi[0] = DJ1.Phi()
			self.dj1_m[0] = DJ1.M()
			self.dj1_delta[0] = J1.Pt() + J4.Pt() - ((DJ1.M() + DJ2.M())/2.)
			self.dj2_pt[0] = DJ2.Pt()
			self.dj2_eta[0] = DJ2.Eta()
			self.dj2_phi[0] = DJ2.Phi()
			self.dj2_m[0] = DJ2.M()
			self.dj2_delta[0] = J2.Pt() + J3.Pt() - ((DJ1.M() + DJ2.M())/2.)
			self.j1_pt[0] = J1.Pt()
			self.j1_eta[0] = J1.Eta()
			self.j1_phi[0] = J1.Phi()
			self.j1_m[0] = J1.M()
			self.j1_btag[0] = self.T.Jet_btagCSVV2[jind0]
			self.j2_pt[0] = J4.Pt()
			self.j2_eta[0] = J4.Eta()
			self.j2_phi[0] = J4.Phi()
			self.j2_m[0] = J4.M()
			self.j2_btag[0] = self.T.Jet_btagCSVV2[jind3]
			self.j3_pt[0] = J2.Pt()
			self.j3_eta[0] = J2.Eta()
			self.j3_phi[0] = J2.Phi()
			self.j3_m[0] = J2.M()
			self.j3_btag[0] = self.T.Jet_btagCSVV2[jind1]
			self.j4_pt[0] = J3.Pt()
			self.j4_eta[0] = J3.Eta()
			self.j4_phi[0] = J3.Phi()
			self.j4_m[0] = J3.M()
			self.j4_btag[0] = self.T.Jet_btagCSVV2[jind2]
		# Jet choices are done:
		TwoJetMass = (DJ1.M() + DJ2.M())/2.
		Masym = math.fabs((DJ1.M() - DJ2.M())/(DJ1.M() + DJ2.M()))
		DeltaEta = math.fabs(DJ1.Eta() - DJ2.Eta())
		self.evt_2JetM[0] = TwoJetMass
		self.evt_Masym[0] =  Masym
		self.evt_DEta[0] = DeltaEta
		self.evt_4JetM[0] = FourJetMass
		self.evt_DeltaDR[0] = DeltaDR
		self.evt_HTAK4[0] = self.HT
		self.evt_NJets[0] = self.njets
#		self.W[0] = self.weight
		self.evt_run[0] = self.T.run
		self.evt_lumi[0] = self.T.luminosityBlock
		self.evt_event[0] = self.T.event
		self.evt_NPV[0] = self.T.PV_npvsGood
		B.Fill()
#		if (self.T.run==280007 and self.T.luminosityBlock==29):
#			print "for run 280007 and lumi block 29, event is: "
#			print self.T.event
#			print self.evt_event[0]



#float			
	def AddBranch(self, name, obj):
		self.T_nominal.Branch(name, obj, name+"/F")
		if self.mc:
			self.T_jesCorr_up.Branch(name, obj, name+"/F")
			self.T_jesCorr_down.Branch(name, obj, name+"/F")
			self.T_jesUnCorr_up.Branch(name, obj, name+"/F")
			self.T_jesUnCorr_down.Branch(name, obj, name+"/F")
			self.T_jer_up.Branch(name, obj, name+"/F")
			self.T_jer_down.Branch(name, obj, name+"/F")
# int
	def AddBranchI(self, name, obj):
	       	self.T_nominal.Branch(name, obj, name+"/I")
		if self.mc:
			self.T_jesCorr_up.Branch(name, obj, name+"/I")
			self.T_jesCorr_down.Branch(name, obj, name+"/I")
			self.T_jesUnCorr_up.Branch(name, obj, name+"/I")
			self.T_jesUnCorr_down.Branch(name, obj, name+"/I")
			self.T_jer_up.Branch(name, obj, name+"/I")
			self.T_jer_down.Branch(name, obj, name+"/I")
#long int
	def AddBranchIL(self, name, obj):
	       	self.T_nominal.Branch(name, obj, name+"/L")
		if self.mc:
			self.T_jesCorr_up.Branch(name, obj, name+"/L")
			self.T_jesCorr_down.Branch(name, obj, name+"/L")
			self.T_jesUnCorr_up.Branch(name, obj, name+"/L")
			self.T_jesUnCorr_down.Branch(name, obj, name+"/L")
			self.T_jer_up.Branch(name, obj, name+"/L")
			self.T_jer_down.Branch(name, obj, name+"/L")
			
picoTree(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

