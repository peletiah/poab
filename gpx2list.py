from commands import *
import sys
import os
from lxml import etree
from optparse import OptionParser
import string
import glineenc

	

def trkptlist(gpxfile):
	tree = etree.fromstring(file(gpxfile, "r").read())
	query_trkptlon='//@lon'
	query_trkptlat='//@lat'
	i=0
	trkpt=list()
	for latitude in tree.xpath(query_trkptlat):
		trkptlat=float(tree.xpath(query_trkptlat)[i])
		trkptlon=float(tree.xpath(query_trkptlon)[i])
		trkpt.append((trkptlat,trkptlon))
		i=i+1
	#print glineenc.encode_pairs(trkpt)
	return trkpt

