# checks for newly uploaded "big-size" images, adds to db and flickr and links to corresponding ids
# replaces 990px-images on flickr with full-size

from sqlalchemy import and_, or_
import hashlib
import ConfigParser
import urllib
import os
import hashlib
import sys
sys.path.append('/root/poab')
from image_functions import sortedlistdir as sortedlistdir,tags2flickrndb as tags2flickrndb
from geo_functions import get_country as get_country,get_timezone as get_timezone
from fill_photos_db import resize_990 as resize_990
import talk2flickr
import db_functions
from getfromxml import parsexml as parsexml

def getcredentials(credentialfile):
    config=ConfigParser.ConfigParser()
    open(credentialfile)
    config.read(credentialfile)
    pg_user=config.get("postgresql","username")
    pg_passwd=config.get("postgresql","password")
    flickrapi_key=config.get("flickrcredentials","api_key")
    flickrapi_secret=config.get("flickrcredentials","api_secret")
    wteapi_key=config.get("worldtimeengine","api_key")
    return pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key


def add2flickrndb(imageinfo,resizepath,image,database,topic,photosetname,phototitle,xmlimglist,xmltaglist,flickrapi_key,flickrapi_secret):
    session=database.db_session()
    db_trackpoint=database.db_trackpoint
    db_imageinfo=database.db_imageinfo
    db_image2tag=database.db_image2tag
    db_phototag=database.db_phototag
    db_photosets=database.db_photosets
    db_trackpoint=database.db_trackpoint
    geoinfo=os.popen("/usr/bin/exiftool -specialinstructions "+resizepath+image+"|/usr/bin/awk {'print $5 $7'}").readlines()
    print geoinfo
    if geoinfo:
        latitude,longitude=geoinfo[0].strip('\n').split(',',1)
        query_trackpoint=session.query(db_trackpoint).filter(and_(db_trackpoint.latitude==latitude,db_trackpoint.longitude==longitude))
        trackpoint_id=query_trackpoint.first().id
    #no trackpoint was near this image, so we have no
    #respective link for the db
    else:
        trackpoint_id=None
    print 'photo linked to trackpoint id:'+str(trackpoint_id)
    q=session.query(db_imageinfo).filter(db_imageinfo.id==imageinfo.id)
    imageinfo=q.one()
    imageinfo.flickrphotoid=talk2flickr.imgupload(resizepath+image,phototitle,imageinfo.flickrdescription,'')
    print imageinfo.flickrphotoid
    try:
        #sets the geolocation of the newly uploaded picture on flickr
        talk2flickr.setlocation(imageinfo.flickrphotoid,latitude,longitude,'16')
    except UnboundLocalError:
        print 'No geolocation in photo-exim-data :-('
    imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.originalsecret,originalformat,imageinfo.flickrdatetaken,flickr_tags,url,title,flickrdescription = talk2flickr.getimginfo(imageinfo.flickrphotoid)
    imageexif=talk2flickr.getexif(imageinfo.flickrphotoid,imageinfo.flickrsecret)
    imageinfo.aperture=imageexif['Aperture_clean']
    imageinfo.shutter=imageexif['Exposure_clean']
    imageinfo.focal_length=imageexif['Focal Length_clean']
    imageinfo.iso=imageexif['ISO Speed_raw']
    imageinfo.online=True
    imageinfo.imgname='/'+resizepath.split('/',2)[2]+image
    session.commit()
    #add photo to existing photoset on flickr
    q_photoset=session.query(db_photosets).filter(db_photosets.id==imageinfo.photoset_id)
    photoset_detail=q_photoset.one()
    talk2flickr.photoset_addphoto(photoset_detail.flickrsetid,imageinfo.flickrphotoid)
    #update photocount
    owner,primary,count,title,description=talk2flickr.get_photosetinfo(photoset_detail.flickrsetid)
    if count != photoset_detail.flickrphotocount:
        photoset_detail.flickrphotocount=count
        session.commit()
    #add tags
    tags2flickrndb(imageinfo.id,imageinfo.flickrphotoid,xmltaglist,database)
    #update trackpoint
    q = session.query(db_trackpoint).filter(db_trackpoint.id==trackpoint_id)
    if q.count() == 1:
        trackpoint=q.one()
        lat=trackpoint.latitude
        lon=trackpoint.longitude
        country=get_country(lat,lon,database)
        location=talk2flickr.findplace(lat,lon,8)
        tz_detail=get_timezone(database,lat,lon,trackpoint.timestamp,wteapi_key)
        trackpoint.timezone_id=tz_detail.id
        trackpoint.country_id=country.iso_numcode
        trackpoint.location=location
        session.commit()
        print "Added trkpt-details for imgid:"+str(imageinfo.id)+", trkptid:"+str(trackpoint.id)+", tzabb:"+tz_detail.abbreviation+", location:"+location
    else:
        print "No trackpoint for this image - therefore no timezone, location or country-details :-("
    session.close 

def checkimgindb(image,imghash_full,imghash_resized,database,topic,xmlimglist,xmltaglist,flickrapi_key,flickrapi_secret):
    session=database.db_session()
    db_imageinfo=database.db_imageinfo
    q = session.query(db_imageinfo).filter(or_(db_imageinfo.photohash==imghash_full,db_imageinfo.photohash_990==imghash_resized))
    if q.count() == 0:
        print image+': physical image not in db, assuming trackdata&Co. are missing too: '+imghash_resized
        return '',0
        
    else:
        for imageinfo in q.all():
            if imageinfo.fullsize_online==False:
                if imghash_full=='':
                    if imageinfo.online==False:
                        print image+': resized image not on flickr, data missing in DB, adding to flickr and DB'
                        return imageinfo,1
                    else:
                        print image+': resized image in DB and flickr but no fullsize-image available, nothing to do'
                        return imageinfo,2
                else:
                    print image+': fullsizeimage available, replace on flickr'
                    return imageinfo,3
            
    

def roundup_images(database,flickrapi_key,flickrapi_secret):
    for path in os.listdir('/srv/trackdata/bydate/'):
        if os.path.isdir('/srv/trackdata/bydate/'+path) == True:
            xmlfile=path+'-contentfile.xml'
            parsed=False
            if os.path.isfile('/srv/trackdata/bydate/'+xmlfile):
                parsed=parsexml('/srv/trackdata/bydate/',xmlfile,True)
                topic,logtext,filepath,photosetname,phototitle,num_of_img,createdate,trk_color,xmlimglist,xmltaglist=parsexml('/srv/trackdata/bydate/',xmlfile,False)
                print xmlfile,parsed
            if parsed==True:
                fullpath='/srv/trackdata/bydate/'+path+'/images/sorted/'
                resizepath='/srv/trackdata/bydate/'+path+'/images/sorted/990/'
                print 'current directory is '+fullpath
                filetypes=('.png','.jpg','.jpeg','.gif','.tif')
                imghash_full=''
                for image in sortedlistdir(resizepath):
                    if image.lower().endswith(filetypes):
                        try:
                            imghash_full=hashlib.sha256(open(fullpath+image).read()).hexdigest()
                        except IOError:
                            pass
                        imghash_resized=hashlib.sha256(open(resizepath+image).read()).hexdigest()
                        imageinfo,indb=checkimgindb(image,imghash_full,imghash_resized,database,topic,xmlimglist,xmltaglist,flickrapi_key,flickrapi_secret)
                        if indb==1:
                            add2flickrndb(imageinfo,resizepath,image,database,topic,photosetname,phototitle,xmlimglist,xmltaglist,flickrapi_key,flickrapi_secret)


if __name__ == "__main__":
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab/credentials.ini')
    database=db_functions.initdatabase(pg_user,pg_passwd)
    roundup_images(database,flickrapi_key,flickrapi_secret)
     
