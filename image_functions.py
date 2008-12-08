#!/usr/bin/python2.5

import talk2flickr #custom
import os
from sqlalchemy import and_


def img2database(farm,server,photoid,secret,originalformat,date_taken,tags,infomarker_id,trackpoint_id,Session,imageinfo):
	session=Session()
	query_imageinfo=session.query(imageinfo).filter(and_(imageinfo.infomarker_id==infomarker_id,imageinfo.trackpoint_id==trackpoint_id,imageinfo.flickrfarm==farm,imageinfo.flickrserver==server,imageinfo.flickrphotoid==photoid,imageinfo.flickrsecret==secret,imageinfo.flickrdatetaken==date_taken))
        if query_imageinfo.count() == 1:
            for detail in query_imageinfo.all():
                imageinfo_detail=detail
                print 'Imageentry already exists - id:'+ str(imageinfo_detail.id) + ' details:' + str(imageinfo_detail)
        elif query_imageinfo.count() > 1:
            for detail in query_imageinfo.all():
                imageinfo_detail=detail
                print 'Imageentry duplicate found! - id:'+ str(imageinfo_detail.id) + ' - details:' + str(imageinfo_detail)
        else:
            #trackpoints are unique, insert them now
            session.add(imageinfo(None,None,infomarker_id,None,trackpoint_id,farm,server,photoid,secret,date_taken,None))
            session.commit()
            for detail in query_imageinfo.all():
                imageinfo_detail=detail 

def img2flickr(imagepath,imglist,photoset,tags,flickrapi_key,flickrapi_secret,infomarker_id,Session,trackpoint,imageinfo,image2tag,phototag,photosets):
    filetypes=('.png','.jpg','.jpeg','.gif')
    session=Session()
    for image in os.listdir(imagepath):
        if image.lower().endswith(filetypes):
            #get the exif-geo-info with jhead
            geoinfo=os.popen("/usr/bin/jhead -exifmap "+imagepath+image+"|/bin/grep Spec|/usr/bin/awk {'print $5 $7'}").readlines()
            latitude,longitude=geoinfo[0].strip('\n').split(',',1)
	    query_trackpoint=session.query(trackpoint).filter(and_(trackpoint.latitude==latitude,trackpoint.longitude==longitude))
	    trackpoint_id=query_trackpoint.first().id
	    print trackpoint_id
            try:
                flickrphotoid=talk2flickr.imgupload(imagepath+image,'testtitle','testdescription',tags)
                farm,server,photoid,secret,originalformat,date_taken,tags,url = talk2flickr.getimginfo(flickrphotoid)
            except AttributeError:
                print 'A AttributeError occured'
	    
            img2database(farm,server,photoid,secret,originalformat,date_taken,tags,infomarker_id,trackpoint_id,Session,imageinfo)
