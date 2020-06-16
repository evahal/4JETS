import os
import ROOT
from ROOT import *
from array import array
import math
from math import *
import sys
import glob
import csv
import XRootD
from pyxrootd import client
from FWCore.PythonUtilities.LumiList import LumiList

def GET(E, B):
	return getattr(E, B)
	
class JESUEtaSlice:
	def __init__(self, R):
		self.min = float(R[0])
		self.max = float(R[1])
		self.pTs = []
		for i in range(3,len(R)):
			if i%3 == 0:
				self.pTs.append([float(R[i]),float(R[i+1]),float(R[i+2])])
	def getU(self, J):
		if J.Eta() < self.max and J.Eta() > self.min:
			p = J.Pt()
			I = None
			i = 0
			while (p - self.pTs[i][0]) > 0:
				I = self.pTs[i]
				i += 1
				if i == len(self.pTs): break
			return [I[1], I[2]]
		else: return [-1.0, -1.0]
class PREPJESU:
	def __init__(self, J):
		self.Slices = []
		with open(J) as jecu:
			reader = csv.reader(jecu)
			next(reader)
			for row in reader:
				R = row[0].split()
				self.Slices.append(JESUEtaSlice(R))
				
	def GetU(self, j):
		for i in self.Slices:
			u =  i.getU(j)
			if u != [-1.0,-1.0]: return u
		return [-1.0, -1.0]
		
			
class JERUEtaSlice:
	def __init__(self, R):
		self.min = float(R[0])
		self.max = float(R[1])
		self.cor = [float(R[3]), float(R[4]), float(R[5])]
	def getU(self, J):
		if J.Eta() < self.max and J.Eta() > self.min:
			return self.cor
		else: return [-1.0, -1.0, -1.0]
		
class PREPJERU:
	def __init__(self, J):
		self.Slices = []
		with open(J) as jecu:
			reader = csv.reader(jecu)
			next(reader)
			for row in reader:
				R = row[0].split()
				self.Slices.append(JERUEtaSlice(R))
	def GetU(self, j):
		for i in self.Slices:
			u =  i.getU(j)
			if u != [-1.0,-1.0, -1.0]: return u
		return [-1.0, -1.0, -1.0]
		
		
def GetJerJet(J, G, P, W):
	dM = J.M() - G.M()
	dP = J.Pt() - G.Pt()
	C = P.GetU(J)
	SF = 1 + ((C[0]-1)*dP/J.Pt())
	SFU =	1 + ((C[2]-1)*dP/J.Pt())
	SFD = 1 + ((C[1]-1)*dP/J.Pt())
	Jn = TLorentzVector()
#	print "_"
#	print SFU/SF
#	print SFD/SF
	if W == "up":
		Jn.SetPtEtaPhiM(J.Pt()*SFU/SF, J.Eta(), J.Phi(), J.M()*SFU/SF)
	if W == "down":
		Jn.SetPtEtaPhiM(J.Pt()*SFD/SF, J.Eta(), J.Phi(), J.M()*SFD/SF)
	return Jn

class picoTree:
	def __init__(self, name, nanotrees, weight, triggers, jess, jers, mc,injfile,outjfile):
		self.jess = jess
		self.jers = jers
		self.mc = mc
		self.weight = weight
		self.__book__(name)

		# get json file
		myList = LumiList (filename = injfile)
		# initialize output lumilist
		myrunlumi =[]
		# open root files
		files = open(nanotrees,"r")
#		for file in glob.glob(nanotrees + "*root"):
		for file in files.read().splitlines():
			self.Fill(file, triggers,myList,myrunlumi)

		# only do this for data			
		if not (self.mc):
			outList = LumiList(lumis = myrunlumi)
			outList.writeJSON(outjfile)

		print "got to the end" 
		files.close()
		self.O.cd()
		self.O.Write()
		self.O.Close()

	def __book__(self, name):
		self.O = TFile(name+".root", "recreate")
		self.O.cd()
		self.T_nominal = TTree("tree_nominal", "tree_nominal")
		if self.mc:
			self.T_jes_up = TTree("tree_jes_up", "tree_jes_up")
			self.T_jes_down = TTree("tree_jes_down", "tree_jes_down")
			self.T_jer_up = TTree("tree_jer_up", "tree_jer_up")
			self.T_jer_down = TTree("tree_jer_down", "tree_jer_down")
		
		# EVENT VARIABLES
		self.evt_run = array('f', [-1.0])
                self.AddBranch('evt_run', self.evt_run)
		self.evt_lumi = array('f', [-1.0])
                self.AddBranch('evt_lumiblock', self.evt_lumi)
		self.evt_event = array('L', [0])
                self.AddBranchI('evt_event', self.evt_event)
		self.evt_NPV = array('f', [-1.0])
                self.AddBranch('evt_NPV', self.evt_NPV)
		self.W = array('f', [-1.0])
                self.AddBranch('weight', self.W)
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
		
	def Fill(self, f, trigs,jlist,rllist):
		print "Working on " + f
#		F = TFile(f)
		F = ROOT.TFile.Open(f,"read")
		
		if F:
			print('is open')
		else:
			print('oops')

		self.T = F.Get("Events")
		for e in self.T:

# Check that events for data pass the golden json file
	       		passJson = False

			if self.mc:
				passJson = True
			else:
				passJson = jlist.contains(self.T.run,self.T.luminosityBlock)

			if not(passJson): continue

# check that the events pass the trigger
			triggered = False
			for t in trigs:
				if GET(e, t) > 0:
					triggered = True
					continue

			if not (triggered): continue

			# fill the run lumi list here after the trigger selection for data
			if not (self.mc):
				rllist.append((self.T.run,self.T.luminosityBlock))

			self.njets=0
			self.HT=0.0
			self.imyJets = []
			for j in range(len(self.T.Jet_pt)):
# tight jet id cut
#				if (self.T.Jet_pt[j]>80.0 and math.fabs(self.T.Jet_eta[j])<2.5 and self.T.Jet_jetId[j]==3): 
# change eta to 2.4
				if (self.T.Jet_pt[j]>80.0 and math.fabs(self.T.Jet_eta[j])<2.4 and self.T.Jet_jetId[j]==3): 

# tight jet id cut with lepton veto
#				if (self.T.Jet_pt[j]>80.0 and math.fabs(self.T.Jet_eta[j])<2.5 and self.T.Jet_jetId[j]==3 and self.T.Jet_muEF[j]<0.8 and self.T.Jet_chEmEF[j]<0.9): 
					self.njets += 1
					self.HT +=  self.T.Jet_pt[j]
					self.imyJets.append(j)
										

			if not (self.njets>3 and self.HT>900.0): continue
			
			
			ind0 = self.imyJets[0]
			ind1 = self.imyJets[1]
			ind2 = self.imyJets[2]
			ind3 = self.imyJets[3]

			J1 = TLorentzVector()
			J2 = TLorentzVector()
			J3 = TLorentzVector()
			J4 = TLorentzVector()
			
			J1.SetPtEtaPhiM(self.T.Jet_pt[ind0], self.T.Jet_eta[ind0], self.T.Jet_phi[ind0], self.T.Jet_mass[ind0])
			J2.SetPtEtaPhiM(self.T.Jet_pt[ind1], self.T.Jet_eta[ind1], self.T.Jet_phi[ind1], self.T.Jet_mass[ind1])
			J3.SetPtEtaPhiM(self.T.Jet_pt[ind2], self.T.Jet_eta[ind2], self.T.Jet_phi[ind2], self.T.Jet_mass[ind2])
			J4.SetPtEtaPhiM(self.T.Jet_pt[ind3], self.T.Jet_eta[ind3], self.T.Jet_phi[ind3], self.T.Jet_mass[ind3])
			self.FillJetVars([J1,J2,J3,J4], [ind0, ind1, ind2, ind3], self.T_nominal)

			if self.mc:
				G1 = TLorentzVector()
				G2 = TLorentzVector()
				G3 = TLorentzVector()
				G4 = TLorentzVector()
				if self.T.nGenJet > 3:
					G1.SetPtEtaPhiM(self.T.GenJet_pt[0], self.T.GenJet_eta[0], self.T.GenJet_phi[0], self.T.GenJet_mass[0])
					G2.SetPtEtaPhiM(self.T.GenJet_pt[1], self.T.GenJet_eta[1], self.T.GenJet_phi[1], self.T.GenJet_mass[1])
					G3.SetPtEtaPhiM(self.T.GenJet_pt[2], self.T.GenJet_eta[2], self.T.GenJet_phi[2], self.T.GenJet_mass[2])
					G4.SetPtEtaPhiM(self.T.GenJet_pt[3], self.T.GenJet_eta[3], self.T.GenJet_phi[3], self.T.GenJet_mass[3])
				elif self.T.nGenJet == 3:
					G1.SetPtEtaPhiM(self.T.GenJet_pt[0], self.T.GenJet_eta[0], self.T.GenJet_phi[0], self.T.GenJet_mass[0])
					G2.SetPtEtaPhiM(self.T.GenJet_pt[1], self.T.GenJet_eta[1], self.T.GenJet_phi[1], self.T.GenJet_mass[1])
					G3.SetPtEtaPhiM(self.T.GenJet_pt[2], self.T.GenJet_eta[2], self.T.GenJet_phi[2], self.T.GenJet_mass[2])
					G4.SetPtEtaPhiM(self.T.Jet_pt[ind3]*0.8, self.T.Jet_eta[ind3], self.T.Jet_phi[ind3], self.T.Jet_mass[ind3]*0.8)
				elif self.T.nGenJet == 2:
					G1.SetPtEtaPhiM(self.T.GenJet_pt[0], self.T.GenJet_eta[0], self.T.GenJet_phi[0], self.T.GenJet_mass[0])
					G2.SetPtEtaPhiM(self.T.GenJet_pt[1], self.T.GenJet_eta[1], self.T.GenJet_phi[1], self.T.GenJet_mass[1])
					G3.SetPtEtaPhiM(self.T.Jet_pt[ind2]*0.8, self.T.Jet_eta[ind2], self.T.Jet_phi[ind2], self.T.Jet_mass[ind2]*0.8)
					G4.SetPtEtaPhiM(self.T.Jet_pt[ind3]*0.8, self.T.Jet_eta[ind3], self.T.Jet_phi[ind3], self.T.Jet_mass[ind3]*0.8)
				elif self.T.nGenJet == 1:
					G1.SetPtEtaPhiM(self.T.GenJet_pt[0], self.T.GenJet_eta[0], self.T.GenJet_phi[0], self.T.GenJet_mass[0])
					G2.SetPtEtaPhiM(self.T.Jet_pt[ind1]*0.8, self.T.Jet_eta[ind1], self.T.Jet_phi[ind1], self.T.Jet_mass[ind1]*0.8)
					G3.SetPtEtaPhiM(self.T.Jet_pt[ind2]*0.8, self.T.Jet_eta[ind2], self.T.Jet_phi[ind2], self.T.Jet_mass[ind2]*0.8)
					G4.SetPtEtaPhiM(self.T.Jet_pt[ind3]*0.8, self.T.Jet_eta[ind3], self.T.Jet_phi[ind3], self.T.Jet_mass[ind3]*0.8)
				else:
					G1.SetPtEtaPhiM(self.T.Jet_pt[ind0]*0.8, self.T.Jet_eta[ind0], self.T.Jet_phi[ind0], self.T.Jet_mass[ind0]*0.8)
					G2.SetPtEtaPhiM(self.T.Jet_pt[ind1]*0.8, self.T.Jet_eta[ind1], self.T.Jet_phi[ind1], self.T.Jet_mass[ind1]*0.8)
					G3.SetPtEtaPhiM(self.T.Jet_pt[ind2]*0.8, self.T.Jet_eta[ind2], self.T.Jet_phi[ind2], self.T.Jet_mass[ind2]*0.8)
					G4.SetPtEtaPhiM(self.T.Jet_pt[ind3]*0.8, self.T.Jet_eta[ind3], self.T.Jet_phi[ind3], self.T.Jet_mass[ind3]*0.8)
			
				J1sU = self.jess["JES"].GetU(J1)
				J2sU = self.jess["JES"].GetU(J2)
				J3sU = self.jess["JES"].GetU(J3)
				J4sU = self.jess["JES"].GetU(J4)
			
				JsU1 = J1*(1+J1sU[1])			
				JsU2 = J2*(1+J2sU[1])		
				JsU3 = J3*(1+J3sU[1])
				JsU4 = J4*(1+J4sU[1])
				JsD1 = J1*(1-J1sU[0])			
				JsD2 = J2*(1-J2sU[0])		
				JsD3 = J3*(1-J3sU[0])
				JsD4 = J4*(1-J4sU[0])
			
				JrU1 = GetJerJet(J1, G1, self.jers["JER"], "up")
				JrU2 = GetJerJet(J2, G2, self.jers["JER"], "up")
				JrU3 = GetJerJet(J3, G3, self.jers["JER"], "up")
				JrU4 = GetJerJet(J4, G4, self.jers["JER"], "up")
				JrD1 = GetJerJet(J1, G1, self.jers["JER"], "down")
				JrD2 = GetJerJet(J2, G2, self.jers["JER"], "down")
				JrD3 = GetJerJet(J3, G3, self.jers["JER"], "down")
				JrD4 = GetJerJet(J4, G4, self.jers["JER"], "down")
				self.FillJetVars([JsU1,JsU2,JsU3,JsU4], [ind0, ind1, ind2, ind3], self.T_jes_up)
				self.FillJetVars([JsD1,JsD2,JsD3,JsD4], [ind0, ind1, ind2, ind3], self.T_jes_down)
				self.FillJetVars([JrU1,JrU2,JrU3,JrU4], [ind0, ind1, ind2, ind3], self.T_jer_up)
				self.FillJetVars([JrD1,JrD2,JrD3,JrD4], [ind0, ind1, ind2, ind3], self.T_jer_down)
		F.Close()
		
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
		self.W[0] = self.weight
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
			self.T_jes_up.Branch(name, obj, name+"/F")
			self.T_jes_down.Branch(name, obj, name+"/F")
			self.T_jer_up.Branch(name, obj, name+"/F")
			self.T_jer_down.Branch(name, obj, name+"/F")
#long int
	def AddBranchI(self, name, obj):
	       	self.T_nominal.Branch(name, obj, name+"/L")
		if self.mc:
			self.T_jes_up.Branch(name, obj, name+"/L")
			self.T_jes_down.Branch(name, obj, name+"/L")
			self.T_jer_up.Branch(name, obj, name+"/L")
			self.T_jer_down.Branch(name, obj, name+"/L")
			
if __name__ == "__main__":
	triggers = ["HLT_PFHT750_4JetPt50","HLT_PFHT750_4JetPt70","HLT_PFHT800_4JetPt50","HLT_PFHT800","HLT_PFHT900"]
#	triggers = ["HLT_PFHT750_4JetPt50","HLT_PFHT750_4JetPt70","HLT_PFHT800_4JetPt50","HLT_PFHT800","HLT_PFHT900","HLT_PFHT1050"]
#	triggers = ["HLT_PFHT1050"]
	jess = {"JES": PREPJESU("fromMarc/Summer16_07Aug2017_V11_MC_Uncertainty_AK4PFPuppi.txt")}
	jers = {"JER": PREPJERU("fromMarc/Summer16_25nsV1_MC_SF_AK4PFPuppi.txt")}
	PicoTreeTest = picoTree("trees/2016/QCD_HT_1500to2000/test", "/cms/xaastorage/NanoAOD/2016/2016_QCD_HT/HT_1500to2000/HT_1500to2000_1", 0.1215/3971631., triggers, jess, jers, True)
	# Name, Folder, Weight, trigger (list), JES, JER, MCorDATA #

		
