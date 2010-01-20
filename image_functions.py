#!/usr/bin/python2.5

import talk2flickr #custom
import os
from sqlalchemy import and_
from sqlalchemy import update
import hashlib
import glob


def checkimghash(imagepath_fullsize,imagepath_smallsize,xmlimglist,num_of_img):
    print imagepath_fullsize, imagepath_smallsize, num_of_img
    if len(glob.glob(imagepath_fullsize+'*.jpg'))==num_of_img:
        print 'Found '+str(num_of_img)+' pictures in the fullsize-path'
        hashok=True
        for image in xmlimglist:
            if hashlib.sha256(open(imagepath_fullsize+image.name).read()).hexdigest()!=image.hash_full:
                print imagepath_fullsize+image.name
                print hashlib.sha256(imagepath_fullsize+image.name).hexdigest()
                print image.hash_full
                hashok=False
                errorimage=image.name
                errorpath=imagepath_fullsize
                print 'Hash OK?: '+str(hashok)
        if hashok==True:
            return 0,imagepath_fullsize
        else:
            errormessage='ERROR: UPLOADED IMAGES ARE NOT COMPLETE/MISSING/MODIFIED!\n'+errorimage+'\n'+errorpath
            return 2,errormessage
    elif len(glob.glob(imagepath_smallsize+'*.jpg'))==num_of_img:
        print 'Found '+str(num_of_img)+' pictures in the smallsize-path'
        hashok=True
        for image in xmlimglist:
            if hashlib.sha256(open(imagepath_smallsize+image.name).read()).hexdigest()!=image.hash_resized:
                print imagepath_smallsize+image.name
                print hashlib.sha256(open(imagepath_smallsize+image.name).read()).hexdigest()
                print image.hash_resized
                hashok=False
                errorimage=image.name
                errorpath=imagepath_smallsize
                print 'Hash OK?: '+str(hashok)
        if hashok==True:
            return 0,imagepath_smallsize
        else:
            errormessage='ERROR: UPLOADED IMAGES ARE NOT COMPLETE/MISSING/MODIFIED!\n'+errorimage+'\n'+errorpath
            return 2,errormessage
    else:
        fullsize_number=len(glob.glob(imagepath_fullsize+'*.jpg'))
        resize_number=len(glob.glob(imagepath_fullsize+'*.jpg'))
        errorimage='Number of images not matching, i count '+ str(fullsize_number) + 'in fullsize and ' + str(resize_number)+'in resize'
        errorpath=''
        errormessage='ERROR: UPLOADED IMAGES ARE NOT COMPLETE/MISSING!\n'+errorimage+'\n'+errorpath
        return 2,errormessage

def geotag(imagepath_fullsize,imagepath_smallsize,trackpath):#geotag the pictures in imagepaths with data from gpxfile
    print 'FUNCTION GEOTAG:'
    #we have to check if the pictures are already geotagged
    print imagepath_fullsize
    if os.popen("/usr/bin/exiftool -specialinstructions "+imagepath_fullsize+"*|grep -v '==='|grep -v 'read'|awk '{printf \"%s\", $0} {print $5 $7}'").readlines():
        print 'Pictures are already geotagged'
        #os.system("/usr/bin/perl /root/scripts/gpsPhoto.pl --dir "+imagepath_fullsize+" --delete-geotag > /var/log/poab/geotag.log 2>&1")
    else:
        print 'no GPS-Tags found, geotagging now'
        if os.system("/usr/bin/perl /root/scripts/gpsPhoto.pl --dir "+imagepath_fullsize+" --gpsdir "+trackpath+" --timeoffset 0 --maxtimediff 1200 > /var/log/poab/geotag.log 2>&1") == 0:
            pass
        else:
            print 'An error occured at geotag'

    #and we do the same for the small images
    print imagepath_smallsize
    if os.popen("/usr/bin/exiftool -specialinstructions "+imagepath_smallsize+"*|grep -v '==='|grep -v 'read'|awk '{printf \"%s\", $0} {print $5 $7}'").readlines():
        print 'Pictures are already geotagged'
        #os.system("/usr/bin/perl /root/scripts/gpsPhoto.pl --dir "+imagepath_smallsize+" --delete-geotag > /var/log/poab/geotag.log 2>&1")
    else:
        print 'no GPS-Tags found, geotagging now'
        if os.system("/usr/bin/perl /root/scripts/gpsPhoto.pl --dir "+imagepath_smallsize+" --gpsdir "+trackpath+" --timeoffset 0 --maxtimediff 1200 > /var/log/poab/geotag.log 2>&1") == 0:
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
    
def img2database(farm,server,flickrphotoid,secret,originalformat,date_taken,title,description,infomarker_id,photoset_id,trackpoint_id,database,photohash,photohash_resized):
    session=database.db_session()
    db_imageinfo=database.db_imageinfo
    query_imageinfo=session.query(db_imageinfo).filter(and_(db_imageinfo.infomarker_id==infomarker_id,db_imageinfo.trackpoint_id==trackpoint_id,db_imageinfo.flickrfarm==farm,db_imageinfo.flickrserver==server,db_imageinfo.flickrphotoid==flickrphotoid,db_imageinfo.flickrsecret==secret,db_imageinfo.flickrdatetaken==date_taken))
    #check if we have this img in the db
    if query_imageinfo.count() == 1:
        #we have this img in the db
        for detail in query_imageinfo.all():
            imageinfo_detail=detail
            print 'Imageentry already exists - id:'+ str(imageinfo_detail.id) + ' details:' + str(imageinfo_detail)
        #find the imagesets of this photo
        query_imagesetid=session.query(db_imageinfo).filter(and_(db_imageinfo.id==imageinfo_detail.id,db_imageinfo.photoset_id==photoset_id))
        if query_imagesetid.count() == 1:
            #there is one exact match for this image and given photoset
            print 'Photoset is already set for the image'
        elif query_imagesetid.count() == 0:
            #there was no entry of given photoset for this img
            if imageinfo_detail.photoset_id == None:		    
                print 'flickrphotoset not in the image-record, updating image-record now'
                for column in query_imageinfo.all():
                    column.photoset_id=photoset_id
                    session.commit()
            else:
		          print 'there is a photoset-id-entry in the database, but it\'s different from the one we\'ve just created, photoset_id is: ' + str(photoset_id) + ', db_entry is:' + str(imageinfo_detail.photoset_id)
    elif query_imageinfo.count() > 1:
        for detail in query_imageinfo.all():
            imageinfo_detail=detail
            print 'Imageentry duplicate found! - id:'+ str(imageinfo_detail.id) + ' - details:' + str(imageinfo_detail)
    else:
        #Image with this flickrdetails was not found in the db, we create it now
        if description == None:
            session.add(db_imageinfo(None,photoset_id,infomarker_id,trackpoint_id,farm,server,flickrphotoid,secret,date_taken,title,None,photohash,photohash_resized))
        else:
            session.add(db_imageinfo(None,photoset_id,infomarker_id,trackpoint_id,farm,server,flickrphotoid,secret,date_taken,title,description,photohash,photohash_resized))
        session.commit()
        for detail in query_imageinfo.all():
            imageinfo_detail=detail
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
    l = os.listdir(imagepath)
    l.sort(cmpfunc)
    return l

def img2flickr(upload2flickrpath,xmlimglist,xmltaglist,photosetname,phototitle,flickrapi_key,flickrapi_secret,infomarker_id,database):
    filetypes=('.png','.jpg','.jpeg','.gif','.tif')
    session=database.db_session()
    db_trackpoint=database.db_trackpoint
    db_imageinfo=database.db_imageinfo
    db_image2tag=database.db_image2tag
    db_phototag=database.db_phototag
    db_photosets=database.db_photosets
    xmlimglist_plus_db_details=list()
    for image in sortedlistdir(upload2flickrpath):
        print 'imagename=' + image
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

	        #------------ HASHING --------------

##we need to make sure that for images that have not been geotagged after checkimghash the hash that has been modified by GEO is used to verify. Not sure what this part of img2flickr is good for anyway...
            imagefile=open(upload2flickrpath+image).read()
            photohash=None
            photohash_resized=None
            filehash=hashlib.sha256(open(upload2flickrpath+image).read()).hexdigest()
            print image, filehash
            hashok=True
            for imgfromxml in xmlimglist:
                if imgfromxml.name == image:
                    if filehash == imgfromxml.hash_full:
                        print 'Matching fullsize image found in xmlimglist!'
                        #save the description from the xml-file, we need it for flickr and the db-entry later
                        imgdescription=imgfromxml.description
                        print 'imgdescription='+str(imgdescription)
                        photohash=filehash
                    elif filehash==imgfromxml.hash_resized:
                        print 'Matching resized image found in xmlimglist!'
                        imgdescription=imgfromxml.description
                        print 'imgdescription='+str(imgdescription)
                        photohash_resize=filehash
                    else:
                        hashok=False
                        errorimage=image
                        errorimagepath=upload2flickrpath
                        print 'ERROR: UPLOADED IMAGES ARE NOT COMPLETE!\n'+errorimage+'\n'+errorimagepath+'\nfilehash:'+filehash +'\nfullhash: '+imgfromxml.hash_full+'\nhash_resized: '+imgfromxml.hash_resized
                        return 0
                else:
                    print image, imgfromxml.name
            print 'filehash: ' + filehash
            print 'photo linked to trackpoint_id: ' + str(trackpoint_id)
            #check if the photo already exists
            result,imageinfo_detail=checkimgindb(database,filehash)

            #----------------------------------
    
            #------------ FLICKR --------------

            if result > 0:
                #we already have the picture in the database, we extract the info we've found to variables we'll use elsewhere
                farm=imageinfo_detail.flickrfarm
                server=imageinfo_detail.flickrserver
                flickrphotoid=imageinfo_detail.flickrphotoid
                secret=imageinfo_detail.flickrsecret
            else:
                #try:
                    #image not in db and we assume also not on flickr, initiate upload
                flickrphotoid=talk2flickr.imgupload(upload2flickrpath+image,phototitle,imgdescription,'')
                print flickrphotoid
                try:
                    #sets the geolocation of the newly uploaded picture on flickr
                    talk2flickr.setlocation(flickrphotoid,latitude,longitude,'16') 
                except UnboundLocalError:
                    print 'No geolocation in photo-exim-data :-('
                #except AttributeError:
                    #print 'A AttributeError occured'
	
                #---------------------------------
                
                #----------- PHOTOSET ------------
                
                photoset_id=photoset2flickrndb(flickrapi_key,flickrapi_secret,flickrphotoid,photosetname,database)
                
                #---------------------------------
                
                #----------- IMG2DATABASE --------	   
                
                #try adding photo to imageinfo
                farm,server,flickrphotoid,secret,originalsecret,originalformat,date_taken,flickr_tags,url,title,description = talk2flickr.getimginfo(flickrphotoid)
                imageinfo_detail=img2database(farm,server,flickrphotoid,secret,originalformat,date_taken,title,description,infomarker_id,photoset_id,trackpoint_id,database,photohash,photohash_resized)
                photoid=imageinfo_detail.id
                farm=imageinfo_detail.flickrfarm
                server=imageinfo_detail.flickrserver
                flickrphotoid=imageinfo_detail.flickrphotoid
                secret=imageinfo_detail.flickrsecret
                
                #---------------------------------
                
                #----------- TAGS2FLICKRNDB ------
                
                tags2flickrndb(photoid,flickrphotoid,xmltaglist,database)
                     
                
                #------- RETURN IMAGEINFO -------
                
                #add imageinfo_detail to imgfromxml-class and append
                #imgfromxml-class to xmlimglist_plus_db_details
                for imgfromxml in xmlimglist:
                    if imgfromxml.name==image:
                        imgfromxml.name
                        imageinfo_detail.flickrphotoid 
                        imgfromxml.imageinfo_detail=imageinfo_detail
                        xmlimglist_plus_db_details.append(imgfromxml)
    return xmlimglist_plus_db_details


def logid2images(log_detail,xmlimglist_plus_db_details,database):
    session=database.db_session()
    db_imageinfo=database.db_imageinfo
    db_image2tag=database.db_image2tag
    db_phototag=database.db_phototag
    for imgfromxml in xmlimglist_plus_db_details:
        query_imageinfo=session.query(db_imageinfo).filter(db_imageinfo.id==imgfromxml.imageinfo_detail.id)
        query_imagelogid=session.query(db_imageinfo).filter(and_(db_imageinfo.id==imgfromxml.imageinfo_detail.id,db_imageinfo.log_id==log_detail.id))
        if query_imagelogid.count() == 1:
            print 'Log_id has already been set for this image record'
        elif query_imagelogid.count() == 0:
            print 'log_id not in the image-record, updating image-record now'
            for column in query_imageinfo.all():
                column.log_id=log_detail.id
                session.commit()
    print 'logid2images DONE'
