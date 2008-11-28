#!/usr/bin/python2.5

from lxml import etree
import os
import string
import gpx2list
import tktogpx2
import flickrupload

basepath='/srv/trackdata/bydate/'

def parsexml(xmlfile):
    tree = etree.fromstring(file(basepath+xmlfile, "r").read())
    topic =  etree.tostring(tree.xpath('//topic')[0]).split("<topic>")[1].split("</topic>")[0].replace("\n","").replace("&gt;",">").replace("&lt;","<")
    logtext =  etree.tostring(tree.xpath('//logtext')[0]).split("<logtext>")[1].split("</logtext>")[0].replace("\n","").replace("&gt;",">").replace("&lt;","<")
    filepath =  etree.tostring(tree.xpath('//filepath')[0]).split("<filepath>")[1].split("</filepath>")[0].replace("\n","")
    trackfile =  etree.tostring(tree.xpath('//trackfile')[0]).split("<trackfile>")[1].split("</trackfile>")[0].replace("\n","")
    photoset =  etree.tostring(tree.xpath('//photoset')[0]).split("<photoset>")[1].split("</photoset>")[0].replace("\n","")
    i=1
    imglist=dict()
    while i < 100:
	try:
	    imglist[i]=etree.tostring(tree.xpath('//img'+str(i))[0]).split("<img"+str(i)+">")[1].split("</img"+str(i)+">")[0].replace("\n","")
	    i=i+1
	except IndexError:
	    i=i+1
	    pass
    return topic,logtext,filepath,trackfile,photoset,imglist		


def gpx2database(gpxfile):
    trkptlist=gpx2list.trkptlist(gpxfile)
    for lat,long in trkptlist:
	print lat
	print long    

def geotag(imagepath,gpxfile):#geotag the pictures in imagepath with data from gpxfile
    print imagepath
    print gpxfile
    if os.system("/usr/bin/perl /root/scripts/gpsPhoto.pl --dir "+imagepath+" --gpsfile "+gpxfile+" --timeoffset 0 --overwrite-geotagged > /var/log/poab/geotag.log 2>&1") == 0:
	pass
    else:
	print 'An error occured at geotag'
			

def img2database(flickrphotoid,flickrimgdetails):
   print flickrphotoid 
		
def img2flickr(imagepath,imglist,gpxfile):
    filetypes=('.png','.jpg','.jpeg','.gif')
    for image in os.listdir(imagepath):
	if image.lower().endswith(filetypes):
	    #get the exif-geo-info with jhead
	    geoinfo=os.popen("/usr/bin/jhead -exifmap "+imagepath+image+"|/bin/grep Spec|/usr/bin/awk {'print $5 $7'}").readlines()
	    latitude,longitude=geoinfo[0].strip('\n').split(',',1)
	    print latitude
	    print longitude
	    try:
		flickrphotoid=flickrupload.imgupload(imagepath+image,'testtitle','testdescription','blabla "sadfa asfaf" asfd')
		flickrimgdetails = flickrupload.getimginfo(flickrphotoid)
	    except AttributeError:
		print 'A AttributeError occured'
	    img2database(flickrphotoid,flickrimgdetails)
			


def main(basepath):
    for xmlfile in os.listdir(basepath):
	if xmlfile.lower().endswith('.xml'):
	    xmlcontent=parsexml(xmlfile)
	    topic=xmlcontent[0]
	    logtext=xmlcontent[1]
	    filepath=xmlcontent[2]
	    trackfile=xmlcontent[3]
	    photoset=xmlcontent[4]
	    imglist=xmlcontent[5]
	    imagepath=filepath+'images_sorted/'
	    try:
		trackpath=filepath+'trackfile/'
		#passes outputDir,gpx-filename and tkFileName to tk2togpx.interactive to convert the tk1 to gpx
		tktogpx2.interactive(trackpath,filepath.rsplit('/',2)[1]+'.gpx',trackpath+trackfile) 
		gpxfile=trackpath+filepath.rsplit('/',2)[1]+'.gpx'
	    except IOError:
		print 'trackfile missing!'
		gpxfile=None
	    gpx2database(gpxfile)
	    geotag(imagepath,gpxfile)
	    img2flickr(imagepath,imglist,gpxfile)

main(basepath)

