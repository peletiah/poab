#!/usr/bin/python2.5

import talk2flickr #custom
import os
from sqlalchemy import and_
from sqlalchemy import update
import hashlib

def checkimgindb(Session,db_imageinfo,photohash):
    session=Session()
    query_imageinfo=session.query(db_imageinfo).filter(db_imageinfo.photohash==photohash)
    if query_imageinfo.count() == 1:
        for detail in query_imageinfo.all():
            imageinfo_detail=detail
            print 'Imageentry already exists - id:'+ str(imageinfo_detail.id) + ' details:' + str(imageinfo_detail)
	return 1,imageinfo_detail
    elif query_imageinfo.count() > 1:
        for detail in query_imageinfo.all():
            imageinfo_detail=detail
            print 'Imageentry duplicate found! - id:'+ str(imageinfo_detail.id) + ' - details:' + str(imageinfo_detail)
	return 2,imageinfo_detail
    else:
	return 0,None


def photoset2flickrndb(flickrapi_key,flickrapi_secret,flickrphotoid,photosetname,Session,db_photosets,db_imageinfo):
    session=Session()
    query_photoset=session.query(db_photosets).filter(db_photosets.flickrtitle==photosetname)
    if query_photoset.count() == 1:
	for detail in query_photoset.all():
	    photoset_detail=detail
	    print 'Photoset already exists - id:' + str(photoset_detail.id) + ' details:' + str(photoset_detail)
	    #check if photoid is in this photoset
	    query_imageinfo=session.query(db_imageinfo).filter(and_(db_imageinfo.photoset_id==photoset_detail.id,db_imageinfo.flickrphotoid==flickrphotoid))
	    if query_imageinfo.count() >= 1:
		print 'Photo already exists in photoset'
	    else:
		#add photo to existing photoset on flickr
		talk2flickr.photoset_addphoto(photoset_detail.flickrsetid,flickrphotoid)
	    #update photocount
	    owner,primary,count,title,description=talk2flickr.get_photosetinfo(photoset_detail.flickrsetid)
	    if count != photoset_detail.flickrphotocount:
		for column in query_photoset.all():
		    column.flickrphotocount=count
		    session.commit()

    elif query_photoset.count() > 1:
        for detail in query_photoset.all():
            photoset_detail=detail
            print 'Photoset duplicate found! - id:'+ str(photoset_detail.id) + ' - details:' + str(photoset_detail)
    else:
        #photoset does not yet exist, create at flickr and insert in the db
	flickr_photosetid=talk2flickr.create_photoset(photosetname,'stuff from the road',flickrphotoid)
	owner,primary,count,title,description=talk2flickr.get_photosetinfo(flickr_photosetid)
        session.add(db_photosets(flickr_photosetid,owner,primary,count,title,description))
        session.commit()
        for detail in query_photoset.all():
            photoset_detail=detail
            print 'Photoset created! - id:'+ str(photoset_detail.id) + ' - details:' + str(photoset_detail)
    return photoset_detail.id

    
def img2database(farm,server,flickrphotoid,secret,originalformat,date_taken,tags,infomarker_id,photoset_id,trackpoint_id,Session,db_imageinfo,photohash):
    session=Session()
    query_imageinfo=session.query(db_imageinfo).filter(and_(db_imageinfo.infomarker_id==infomarker_id,db_imageinfo.trackpoint_id==trackpoint_id,db_imageinfo.flickrfarm==farm,db_imageinfo.flickrserver==server,db_imageinfo.flickrphotoid==flickrphotoid,db_imageinfo.flickrsecret==secret,db_imageinfo.flickrdatetaken==date_taken))
    if query_imageinfo.count() == 1:
	for detail in query_imageinfo.all():
	    imageinfo_detail=detail
	    print 'Imageentry already exists - id:'+ str(imageinfo_detail.id) + ' details:' + str(imageinfo_detail)
	    query_imagesetid=session.query(db_imageinfo).filter(and_(db_imageinfo.id==imageinfo_detail.id,db_imageinfo.photoset_id==photoset_id))
	    if query_imagesetid.count() == 1:
		print 'Everything is fine, photoset is set for the image'
	    elif query_imagesetid.count() == 0:
		if imageinfo_detail.photoset_id == None:		    
		    print 'flickrphotoset not in the image-record, updating image-record now'
		    for column in query_imageinfo.all():
			column.photoset_id=photoset_id
			session.commit()
		else:
		    print 'there is a photoset-id-entry in the record, but it\'s different to what i was told, photoset_id is: ' + str(photoset_id) + ', db_entry is:' + str(imageinfo_detail.photoset_id)
    elif query_imageinfo.count() > 1:
        for detail in query_imageinfo.all():
            imageinfo_detail=detail
            print 'Imageentry duplicate found! - id:'+ str(imageinfo_detail.id) + ' - details:' + str(imageinfo_detail)
    else:
        #Image are unique, insert them now
        session.add(db_imageinfo(None,photoset_id,infomarker_id,trackpoint_id,farm,server,flickrphotoid,secret,date_taken,photohash))
        session.commit()
        for detail in query_imageinfo.all():
            imageinfo_detail=detail
	    print 'Imageentry created! - id:'+ str(imageinfo_detail.id) + ' - details:' + str(imageinfo_detail)
    return imageinfo_detail 

def img2flickr(imagepath,xmlimglist,xmltaglist,photosetname,photodescription,phototitle,flickrapi_key,flickrapi_secret,infomarker_id,Session,db_trackpoint,db_imageinfo,db_image2tag,db_phototag,db_photosets):
    filetypes=('.png','.jpg','.jpeg','.gif')
    session=Session()
    imglist=list()
    for image in os.listdir(imagepath):
	print 'imagename=' + image
        if image.lower().endswith(filetypes):
            #get the exif-geo-info with jhead
            geoinfo=os.popen("/usr/bin/jhead -exifmap "+imagepath+image+"|/bin/grep Spec|/usr/bin/awk {'print $5 $7'}").readlines()
	    print geoinfo
            latitude,longitude=geoinfo[0].strip('\n').split(',',1)
	    query_trackpoint=session.query(db_trackpoint).filter(and_(db_trackpoint.latitude==latitude,db_trackpoint.longitude==longitude))
	    trackpoint_id=query_trackpoint.first().id
	    imagefile=open(imagepath+image).read()
	    photohash=hashlib.sha256(image).hexdigest()
	    print 'photohash: ' + photohash
	    print 'photo linked to trackpoint_id: ' + str(trackpoint_id)
	    #check if the photo already exists
	    result,imageinfo_detail=checkimgindb(Session,db_imageinfo,photohash)
	    if result > 0:
		#we already have the picture in the database, we extract the info we've found to variables we'll use elsewhere
		farm=imageinfo_detail.flickrfarm
		server=imageinfo_detail.flickrserver
		flickrphotoid=imageinfo_detail.flickrphotoid
		secret=imageinfo_detail.flickrsecret
	    else:
                try:
		    #image not on flickr and db, initiate upload
                    flickrphotoid=talk2flickr.imgupload(imagepath+image,phototitle,photodescription,tags)
                    farm,server,flickrphotoid,secret,originalformat,date_taken,flickr_tags,url = talk2flickr.getimginfo(flickrphotoid)
		    print flickr_tags
		    talk2flickr.setlocation(flickrphotoid,latitude,longitude,'16') #sets the geolocation of the newly uploaded picture on flickr
                except AttributeError:
                    print 'A AttributeError occured'
	    #add photoset
	    photoset_id=photoset2flickrndb(flickrapi_key,flickrapi_secret,flickrphotoid,photosetname,Session,db_photosets,db_imageinfo)
	    if result > 0:
		pass
	    else:
		#try adding photo to imageinfo
		imageinfo_detail=img2database(farm,server,flickrphotoid,secret,originalformat,date_taken,tags,infomarker_id,photoset_id,trackpoint_id,Session,db_imageinfo,photohash)
		photoid=imageinfo_detail.id
		farm=imageinfo_detail.flickrfarm
                server=imageinfo_detail.flickrserver
                flickrphotoid=imageinfo_detail.flickrphotoid
                secret=imageinfo_detail.flickrsecret
	#append imageinfo_detail to imglist for the images in xmlimglist
	for xmlimg in xmlimglist:
	    if xmlimg==image:
		imglist.append(imageinfo_detail)
    return imglist	


def logid2images(log_detail,imglist,Session,db_imageinfo):
    session=Session()
    print imglist
    for imageinfo_detail in imglist:
	query_imageinfo=session.query(db_imageinfo).filter(db_imageinfo.id==imageinfo_detail.id)
	query_imagelogid=session.query(db_imageinfo).filter(and_(db_imageinfo.id==imageinfo_detail.id,db_imageinfo.log_id==log_detail.id))
	if query_imagelogid.count() == 1:
	    print 'Everything is fine, log_id is set for this image record'
	elif query_imagelogid.count() == 0:
	    print 'log_id not in the image-record, updating image-record now'
	    for column in query_imageinfo.all():
		column.log_id=log_detail.id
		session.commit()
    print 'logid2images DONE'
