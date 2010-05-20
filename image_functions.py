#!/usr/bin/python2.5

import talk2flickr #custom
import os
from sqlalchemy import and_,or_
from sqlalchemy import update
import hashlib
import glob
import sys

def checkimghash(imagepath_fullsize,imagepath_resized,xmlimglist,num_img_xml,num_img_log):
    filetypes=('png','jpg','jpeg','gif','tif')
    print '\nchecking imghash in paths:'+imagepath_fullsize, imagepath_resized, num_img_xml
    if len(glob.glob(imagepath_fullsize+'*.jpg'))==num_img_xml:
        print 'Found '+str(num_img_xml)+' pictures in the fullsize-path'
        hashok=True
        for image in xmlimglist:
            if image.name.split('.')[1] in filetypes:
                if hashlib.sha256(open(imagepath_fullsize+image.name).read()).hexdigest()!=image.hash_full:
                    print imagepath_fullsize+image.name
                    print hashlib.sha256(imagepath_fullsize+image.name).hexdigest()
                    print image.hash_full
                    hashok=False
                    errorimage=image.name
                    errorpath=imagepath_fullsize
                    print 'Hash OK?: '+str(hashok)
        if hashok==True:
            return 0,imagepath_fullsize,True
        else:
            errormessage='ERROR: UPLOADED IMAGES ARE NOT COMPLETE/MISSING/MODIFIED!\n'+errorimage+'\n'+errorpath
            return 2,errormessage,False
    elif len(glob.glob(imagepath_resized+'*.jpg'))==num_img_xml:
        print 'Found '+str(num_img_xml)+' pictures in the resized-path'
        hashok=True
        for image in xmlimglist:
            if image.name.split('.')[1] in filetypes:
                if hashlib.sha256(open(imagepath_resized+image.name).read()).hexdigest()!=image.hash_resized:
                    print imagepath_resized+image.name
                    print hashlib.sha256(open(imagepath_resized+image.name).read()).hexdigest()
                    print image.hash_resized
                    hashok=False
                    errorimage=image.name
                    errorpath=imagepath_resized
                    print 'Hash OK?: '+str(hashok)
        if hashok==True:
            print 'Hash OK?: '+str(hashok)
            return 0,imagepath_resized,False
        else:
            errormessage='ERROR: UPLOADED IMAGES ARE NOT COMPLETE/MISSING/MODIFIED!\n'+errorimage+'\n'+errorpath
            return 2,errormessage,False
    elif len(glob.glob(imagepath_resized+'*.jpg'))==num_img_log:
        print 'Found '+str(num_img_log)+' pictures in the resized-path, log-only'
        hashok=True
        for image in xmlimglist:
            #only photos which are in the log are checked
            if image.logphoto=='True':
                if image.name.split('.')[1] in filetypes:
                    if hashlib.sha256(open(imagepath_resized+image.name).read()).hexdigest()!=image.hash_resized:
                        print imagepath_resized+image.name
                        print hashlib.sha256(open(imagepath_resized+image.name).read()).hexdigest()
                        print image.hash_resized
                        hashok=False
                        errorimage=image.name
                        errorpath=imagepath_resized
                        print 'Hash OK?: '+str(hashok)
        if hashok==True:
            return 0,imagepath_resized,False
        else:
            errormessage='ERROR: UPLOADED IMAGES ARE NOT COMPLETE/MISSING/MODIFIED!\n'+errorimage+'\n'+errorpath
            return 2,errormessage,False
    else:                    
        fullsize_number=len(glob.glob(imagepath_fullsize+'*.jpg'))
        resize_number=len(glob.glob(imagepath_fullsize+'*.jpg'))
        errorimage='Number of images not matching, i count '+ str(fullsize_number) + 'in fullsize and ' + str(resize_number)+'in resize'
        errorpath=''
        errormessage='ERROR: UPLOADED IMAGES ARE NOT COMPLETE/MISSING!\n'+errorimage+'\n'+errorpath
        return 2,errormessage,False


def geotag(imagepath_fullsize,imagepath_resized,trackpath):
    #geotag the pictures in imagepaths with data from gpxfile
    print 'FUNCTION GEOTAG:'
    #we have to check if the pictures are already geotagged
    print imagepath_fullsize
    if os.popen("/usr/bin/exiftool -specialinstructions "+imagepath_fullsize+"*|grep -v '==='|grep -v 'read'|awk '{printf \"%s\", $0} {print $5 $7}'").readlines():
        print 'Pictures are already geotagged'
    else:
        print 'no GPS-Tags found, geotagging now'
        if os.system("/usr/bin/perl /root/scripts/gpsPhoto.pl --dir "+imagepath_fullsize+" --gpsdir "+trackpath+" --timeoffset 0 --maxtimediff 1200 > /var/log/poab/geotag.log 2>&1") == 0:
            pass
        else:
            print 'An error occured at geotag'

    #and we do the same for the small images
    print imagepath_resized
    if os.popen("/usr/bin/exiftool -specialinstructions "+imagepath_resized+"*|grep -v '==='|grep -v 'read'|awk '{printf \"%s\", $0} {print $5 $7}'").readlines():
        print 'Pictures are already geotagged'
    else:
        print 'no GPS-Tags found, geotagging now'
        if os.system("/usr/bin/perl /root/scripts/gpsPhoto.pl --dir "+imagepath_resized+" --gpsdir "+trackpath+" --timeoffset 0 --maxtimediff 1200 > /var/log/poab/geotag.log 2>&1") == 0:
            pass
        else:
            print 'An error occured at geotag'

def checkimgindb(database,filehash):
    session=database.db_session()
    db_imageinfo=database.db_imageinfo
    query_imageinfo=session.query(db_imageinfo).filter(db_imageinfo.photohash==filehash)
    if query_imageinfo.count() == 1:
        for detail in query_imageinfo.one():
            imageinfo_detail=detail
            print 'Imageentry already exists - id:'+ str(imageinfo_detail.id) + ' details:' + str(imageinfo_detail)
        return 1,imageinfo_detail
    elif query_imageinfo.count() > 1:
        for detail in query_imageinfo.one():
            imageinfo_detail=detail
            print 'Imageentry duplicate found! - id:'+ str(imageinfo_detail.id) + ' - details:' + str(imageinfo_detail)
        return 2,imageinfo_detail
    else:
        query_imageinfo=session.query(db_imageinfo).filter(db_imageinfo.photohash_990==filehash)
        if query_imageinfo.count() == 1:
            for detail in query_imageinfo.one():
                imageinfo_detail=detail
                print 'Imageentry already exists - id:'+ str(imageinfo_detail.id) + ' details:' + str(imageinfo_detail)
            return 1,imageinfo_detail
        elif query_imageinfo.count() > 1:
            for detail in query_imageinfo.one():
                imageinfo_detail=detail
                print 'Imageentry duplicate found! - id:'+ str(imageinfo_detail.id) + ' - details:' + str(imageinfo_detail)
            return 2,imageinfo_detail
        else:
            print "FUNCTION checkimgindb: image not found in db"
            return 0,None


def photoset2flickrndb(flickrapi_key,flickrapi_secret,flickrphotoid,photosetname,database):
    session=database.db_session()
    db_imageinfo=database.db_imageinfo
    db_photosets=database.db_photosets
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
        flickr_photosetid=talk2flickr.create_photoset(photosetname,'',flickrphotoid)
        owner,primary,count,title,description=talk2flickr.get_photosetinfo(flickr_photosetid)
        session.add(db_photosets(flickr_photosetid,owner,primary,count,title,description))
        session.commit()
        for detail in query_photoset.all():
            photoset_detail=detail
            print 'Photoset created! - id:'+ str(photoset_detail.id)
    return photoset_detail.id

def xmlimglist2db(photosetname,xmlimglist,database):
    for imgfromxml in xmlimglist:
        session=database.db_session()
        db_imageinfo=database.db_imageinfo
        q = session.query(db_imageinfo).filter(or_(db_imageinfo.photohash==imgfromxml.hash_full,db_imageinfo.photohash_990==imgfromxml.hash_resized))
        if q.count()>0:
            print 'Image already in DB: '+str(imgfromxml.name)
        else:
            if imgfromxml.description=='' or imgfromxml.description==None:
                session.add(db_imageinfo(None,None,None,None,None,None,None,None,None,photosetname,None,imgfromxml.hash_full,imgfromxml.hash_resized,imgfromxml.name,None,None,None,None,False,False))
            else:
                session.add(db_imageinfo(None,None,None,None,None,None,None,None,None,photosetname,imgfromxml.description,imgfromxml.hash_full,imgfromxml.hash_resized,imgfromxml.name,None,None,None,None,False,False))
                
            session.commit()
            session.close()

   
def img2database(farm,server,flickrphotoid,secret,originalformat,date_taken,title,description,infomarker_id,photoset_id,trackpoint_id,database,photohash,photohash_resized,imgname,aperture,shutter,focal_length,iso,fullsize):
    session=database.db_session()
    db_imageinfo=database.db_imageinfo
    query_imageinfo=session.query(db_imageinfo).filter(and_(db_imageinfo.photohash==photohash,db_imageinfo.photohash_990==photohash_resized))
    #check if we have this img in the db
    if query_imageinfo.count() == 1:
        #we have this img in the db
        image=query_imageinfo.one()
        print 'Imageentry already exists - id:'+ str(image.id) + ' details:' + str(image)
        print 'Adding additional data'
        image.photoset_id=photoset_id
        image.infomarker_id=infomarker_id
        image.trackpoint_id=trackpoint_id
        image.flickrfarm=farm
        image.flickrserver=server
        image.flickrphotoid=flickrphotoid
        image.flickrsecret=secret
        image.flickrdatetaken=date_taken
        image.imgname=imgname
        image.aperture=aperture
        image.shutter=shutter
        image.focal_length=focal_length
        image.iso=iso
        image.online=True
        image.online_fullsize=fullsize
        session.commit()
        
    elif query_imageinfo.count() > 1:
        for imageinfo_detail in query_imageinfo.all():
            print 'Imageentry duplicate found! - id:'+ str(imageinfo_detail.id) + ' - details:' + str(imageinfo_detail)
    else:
        #Image with this flickrdetails was not found in the db, we create it now
        if description == None:
            session.add(db_imageinfo(None,photoset_id,infomarker_id,trackpoint_id,farm,server,flickrphotoid,secret,date_taken,title,None,photohash,photohash_resized,imgname,aperture,shutter,focal_length,iso,True,fullsize))
        else:
            session.add(db_imageinfo(None,photoset_id,infomarker_id,trackpoint_id,farm,server,flickrphotoid,secret,date_taken,title,description,photohash,photohash_resized,imgname,aperture,shutter,focal_length,iso,True,fullsize))
        session.commit()
    for imageinfo_detail in query_imageinfo.all():
        print 'Imageentry created! - id:'+ str(imageinfo_detail.id)
    return imageinfo_detail 



def tags2flickrndb(photoid,flickrphotoid,xmltaglist,database):
    session=database.db_session()
    db_image2tag=database.db_image2tag
    db_phototag=database.db_phototag
    for tag in xmltaglist:
        query_phototag=session.query(db_phototag).filter(db_phototag.tag==tag)
        if query_phototag.count() >= 1:
            for detail in query_phototag.all():
                phototag_id=detail.id
                talk2flickr.addtags(flickrphotoid,tag)
                query_image2tag=session.query(db_image2tag).filter(and_(db_image2tag.imageinfo_id==photoid,db_image2tag.phototag_id==phototag_id))
                #find out if there's already a link between tag in img in the db
                # if not, create one
                if query_image2tag.count() == 0:
		              session.add(db_image2tag(photoid,phototag_id))
		              session.commit()
        #tag does not yet exist in db_phototag, create it
        else:
	         talk2flickr.addtags(flickrphotoid,tag)
	         session.add(db_phototag(tag,None))
	         session.commit()
        for detail in query_phototag.all():
            phototag_id=detail.id
            query_image2tag=session.query(db_image2tag).filter(and_(db_image2tag.imageinfo_id==photoid,db_image2tag.phototag_id==phototag_id))
            if query_image2tag.count() == 0:
		          session.add(db_image2tag(photoid,phototag_id))
		          session.commit()

def sortedlistdir(imagepath, cmpfunc=cmp):
    try:
        l = os.listdir(imagepath)
        l.sort(cmpfunc)
        return l
    except OSError, (value):
        sys.stderr.write("%s\n" % (value, ))
        return ''

def img2flickr(upload2flickrpath,fullsize,imagepath_resized,xmlimglist,xmltaglist,photosetname,phototitle,flickrapi_key,flickrapi_secret,infomarker_id,database):
    filetypes=('.png','.jpg','.jpeg','.gif','.tif')
    session=database.db_session()
    db_trackpoint=database.db_trackpoint
    db_imageinfo=database.db_imageinfo
    db_image2tag=database.db_image2tag
    db_phototag=database.db_phototag
    db_photosets=database.db_photosets
    xmlimglist_plus_db_details=list()
    for image in sortedlistdir(upload2flickrpath):
        for imgfromxml in xmlimglist:
            if imgfromxml.name==image:
                print 'imagename=' + image
                #check if image is already in the db and uploaded
                query_imageinfo=session.query(db_imageinfo).filter(and_(db_imageinfo.photohash==imgfromxml.hash_full,db_imageinfo.photohash_990==imgfromxml.hash_resized,db_imageinfo.online==False))
                if query_imageinfo.count()==1:
                    if image.lower().endswith(filetypes):
                        #------------ GEO ------------------
                        #get the exif-geo-info with exiftool
                        #and link image with trackpoint_id
                        geoinfo=os.popen("/usr/bin/exiftool -specialinstructions "+upload2flickrpath+image+"|/usr/bin/awk {'print $5 $7'}").readlines()
                        print geoinfo
                        if geoinfo:
                            latitude,longitude=geoinfo[0].strip('\n').split(',',1)
                            query_trackpoint=session.query(db_trackpoint).filter(and_(db_trackpoint.latitude==latitude,db_trackpoint.longitude==longitude))
                            trackpoint_id=query_trackpoint.first().id
                        #no trackpoint was near this image, so we have no
                        #respective link for the db
                        else:
                            trackpoint_id=None
	                     
    	              #-----------------------------------

                    #------------ FLICKR --------------

                    flickrphotoid=talk2flickr.imgupload(upload2flickrpath+image,phototitle,imgfromxml.description,'')
                    print flickrphotoid
                    try:
                        #sets the geolocation of the newly uploaded picture on flickr
                        talk2flickr.setlocation(flickrphotoid,latitude,longitude,'16') 
                    except UnboundLocalError:
                        print 'No geolocation in photo-exim-data :-('
	
                    #---------------------------------
                    
                    #----------- PHOTOSET ------------
                    
                    photoset_id=photoset2flickrndb(flickrapi_key,flickrapi_secret,flickrphotoid,photosetname,database)
                    
                    #---------------------------------
                    
                    #----------- IMG2DATABASE --------	   
                    
                    #fetch image-related data from flickr, then try adding photo to imageinfo
                    farm,server,flickrphotoid,secret,originalsecret,originalformat,date_taken,flickr_tags,url,title,description = talk2flickr.getimginfo(flickrphotoid)
                    imageexif=talk2flickr.getexif(flickrphotoid,secret)
                    aperture=imageexif['Aperture_clean']
                    shutter=imageexif['Exposure_clean']
                    focal_length=imageexif['Focal Length_clean']
                    iso=imageexif['ISO Speed_raw']
                    
                    imgname='/'+imagepath_resized.split('/',2)[2]+image
                       
                    imageinfo_detail=img2database(farm,server,flickrphotoid,secret,originalformat,date_taken,title,description,infomarker_id,photoset_id,trackpoint_id,database,imgfromxml.hash_full,imgfromxml.hash_resized,imgname,aperture,shutter,focal_length,iso,fullsize)
                    
                    #---------------------------------
                    
                    #----------- TAGS2FLICKRNDB ------
                    
                    tags2flickrndb(imageinfo_detail.id,flickrphotoid,xmltaglist,database)
                         
                else:
                    query_imageinfo=session.query(db_imageinfo).filter(and_(db_imageinfo.photohash==imgfromxml.hash_full,db_imageinfo.photohash_990==imgfromxml.hash_resized,db_imageinfo.online==True))
                    imageinfo_detail=query_imageinfo.one()
                #------- RETURN IMAGEINFO -------
                        
                #add imageinfo_detail to imgfromxml-class and append
                #imgfromxml-class to xmlimglist_plus_db_details
                imgfromxml.imageinfo_detail=imageinfo_detail
                xmlimglist_plus_db_details.append(imgfromxml)
    return xmlimglist_plus_db_details

def getphotosetid(photosetname,database):
    session=database.db_session()
    db_imageinfo=database.db_imageinfo
    db_photosets=database.db_photosets
    query_photoset=session.query(db_photosets).filter(db_photosets.flickrtitle==photosetname)
    photoset=query_photoset.one()
    if query_photoset.count()==1:
        return photoset.id
    else:
        print 'no photoset named '+str(photosetname)+' found :-( Plz elaborate'
        return 0


def logid2images(log_detail,xmlimglist,photoset_id,infomarker_id,database):
    session=database.db_session()
    db_imageinfo=database.db_imageinfo
    db_image2tag=database.db_image2tag
    db_phototag=database.db_phototag
    for imgfromxml in xmlimglist:
        query_imageinfo=session.query(db_imageinfo).filter(or_(db_imageinfo.photohash==imgfromxml.hash_full,db_imageinfo.photohash_990==imgfromxml.hash_resized))
        imageinfo=query_imageinfo.one()
        if imageinfo.log_id:
            print 'Log_id has already been set for this image record'+str(imageinfo.id)
        elif imageinfo.log_id==None:
            print 'log_id not in the image-record, updating image-record now'+str(imageinfo.id)
            imageinfo.log_id=log_detail.id
            #Setting additional values for photos not yet uploaded
            if imageinfo.photoset_id==None:
                print 'adding photoset_id to: '+str(imageinfo.imgname)+' '+str(imageinfo.id)
                imageinfo.photoset_id=photoset_id
            if imageinfo.infomarker_id==None:
                print 'adding infomarker_id to: '+str(imageinfo.imgname)+' '+str(imageinfo.id)
                imageinfo.infomarker_id=infomarker_id
            session.commit()
    print 'logid2images DONE'
