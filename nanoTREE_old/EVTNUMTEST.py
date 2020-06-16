import os
import ROOT
from ROOT import *
from array import array
import math
from math import *
import sys
import glob
import csv


class TEST:
	def __init__(self, files):
		self.__book__()
		for file in glob.glob(files + "*root"):
			self.ana(file)
			
	def __book__(self):
		self.T = TTree("t", "t")
		# EVENT VARIABLES
		self.evt_f = array('f', [0.])
		self.AddBranch('evt_f', self.evt_f)
		self.evt_i = array('L', [0])
		self.AddBranchI('evt_i', self.evt_i)
	def AddBranchI(self, name, obj):
		self.T.Branch(name, obj, name+"/L")
	def AddBranch(self, name, obj):
		self.T.Branch(name, obj, name+"/F")
	def ana(self, F):
		Ro = TFile(F)
		T = Ro.Get("Events")
		for e in T:
			pure = T.event
			self.evt_f[0] = T.event
			self.evt_i[0] = T.event
			difff = pure - int(self.evt_f[0])
			diffi = pure - int(self.evt_i[0])
			print T.event
			if difff != 0 and diffi != 0:
				print "-=-=-=-=-=-=-"
				print str(difff) + " :(float): " + str(pure)
				print str(diffi) + " :(int): " + str(pure)			
					
if __name__ == "__main__":
	test = TEST(sys.argv[1])
