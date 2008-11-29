#!/usr/bin/python2.5

from lxml import etree
import os
import string
import gpx2list
import tktogpx2
import flickrupload
import urllib
import ConfigParser

basepath='/srv/trackdata/bydate/'

def getcredentials(credentialfile):
    config=ConfigParser.ConfigParser()
    open(credentialfile)
    config.read(credentialfile)
    flickrapi_key=config.get("flickrcredentials","api_key")
    flickrapi_secret=config.get("flickrcredentials","api_secret")
    wteapi_key=config.get("worldtimeengine","api_key")
    return flickrapi_key,flickrapi_secret,wteapi_key


def parsexml(xmlfile):
    tree = etree.fromstring(file(basepath+xmlfile, "r").read())
    topic =  (tree.xpath('//topic')[0]).text.replace("&gt;",">").replace("&lt;","<")
    logtext =  (tree.xpath('//logtext')[0]).text.replace("&gt;",">").replace("&lt;","<")
    filepath =  (tree.xpath('//filepath')[0]).text
    trackfile =  (tree.xpath('//trackfile')[0]).text
    photoset =  (tree.xpath('//photoset')[0]).text
    i=1
    imglist=dict()
    while i < 100:
	try:
	    imglist[i]=(tree.xpath('//img'+str(i))[0]).text
	    i=i+1
	except IndexError:
	    i=i+1
	    pass
    return topic,logtext,filepath,trackfile,photoset,imglist		


def query_wte(wteapi_key,lat,long):
    f = urllib.urlopen("http://worldtimeengine.com/api/"+wteapi_key+"/"+str(lat)+"/"+str(long))
    geodetails=f.read()
    f.close()
    return geodetails


def gpx2database(gpxfile,wteapi_key):
######################### replace this shit by worldtimeengine-query when finished #############
    geodetailsfirst=etree.fromstring('''<?xml version="1.0" encoding="UTF-8" ?>
<timezone xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://worldtimeengine.com/timezone.xsd">
    <version>1.1</version>
    <location>
        <region>Taiwan</region>
        <latitude>25.0684016</latitude>
        <longitude>121.6382592</longitude>
    </location>
    <time>
        <utc>2008-11-28 21:35:12</utc>
        <local>2008-11-29 05:35:12</local>
        <zone>
            <hasDST>false</hasDST>
            <current>
                <abbreviation>CST</abbreviation>
                <description>Chinese Standard Time</description>
                <utcoffset>-8:00</utcoffset>
            </current>
        </zone>
    </time>
</timezone>''')

    geodetailslast=etree.fromstring('''<?xml version="1.0" encoding="UTF-8" ?>
<timezone xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://worldtimeengine.com/timezone.xsd">
    <version>1.1</version>
    <location>
        <region>Taiwan</region>
        <latitude>24.9993056</latitude>
        <longitude>121.49152</longitude>
    </location>
    <time>
        <utc>2008-11-28 21:35:12</utc>
        <local>2008-11-29 05:35:12</local>
        <zone>
            <hasDST>false</hasDST>
            <current>
                <abbreviation>CST</abbreviation>
                <description>Chinese Standard Time</description>
                <utcoffset>-8:00</utcoffset>
            </current>
        </zone>
    </time>
</timezone>''')
    ################################################################################

    trkptlist=gpx2list.trkptlist(gpxfile)
    lat,long=trkptlist[0] #first point in the track
    #geodetailsfirst=query_wte(wteapi_key,lat,long)
    lat,long=trkptlist[-1] #last point in the track
    #geodetailslast=query_wte(wteapi_key,lat,long)
    
    if (geodetailsfirst.xpath('//utcoffset')[0]).text == (geodetailslast.xpath('//utcoffset')[0]).text:
	utcoffset=(geodetailsfirst.xpath('//utcoffset')[0]).text
	tz_abbreviation=(geodetailsfirst.xpath('//abbreviation')[0]).text	
	tz_description=(geodetailsfirst.xpath('//description')[0]).text
	tz_region=(geodetailsfirst.xpath('//region')[0]).text	
	print tz_abbreviation,tz_description,tz_region	
    else:
	print 'We need to check this tracklist in more detail, as there was a shift in the timezone'
	print 'between the first and the last trackpoint'
	i=False
	#function to check the tracklist toroughly goes here
    
    
    

	    

def geotag(imagepath,gpxfile):#geotag the pictures in imagepath with data from gpxfile
    if os.system("/usr/bin/perl /root/scripts/gpsPhoto.pl --dir "+imagepath+" --gpsfile "+gpxfile+" --timeoffset 0 --overwrite-geotagged > /var/log/poab/geotag.log 2>&1") == 0:
	pass
    else:
	print 'An error occured at geotag'
			

def img2database(flickrphotoid,flickrimgdetails):
   print flickrphotoid 
		
def img2flickr(imagepath,imglist,gpxfile,flickrapi_key,flickrapi_secret):
    filetypes=('.png','.jpg','.jpeg','.gif')
    for image in os.listdir(imagepath):
	if image.lower().endswith(filetypes):
	    #get the exif-geo-info with jhead
	    geoinfo=os.popen("/usr/bin/jhead -exifmap "+imagepath+image+"|/bin/grep Spec|/usr/bin/awk {'print $5 $7'}").readlines()
	    latitude,longitude=geoinfo[0].strip('\n').split(',',1)
	    try:
		flickrphotoid=flickrupload.imgupload(imagepath+image,'testtitle','testdescription','blabla "sadfa asfaf" asfd')
		flickrimgdetails = flickrupload.getimginfo(flickrphotoid)
	    except AttributeError:
		print 'A AttributeError occured'
	    img2database(flickrphotoid,flickrimgdetails)
			


def main(basepath):
    flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/scripts/credentials.ini')
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
	    gpx2database(gpxfile,wteapi_key)
	    geotag(imagepath,gpxfile)
	    #img2flickr(imagepath,imglist,gpxfile,flickrapi_key,flickrapi_secret)

main(basepath)

