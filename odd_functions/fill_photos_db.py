## downloads photos of a specified flickr-set and adds details to the db

import talk2flickr
from optparse import OptionParser
import db_functions
from sqlalchemy import and_
import hashlib
import ConfigParser
import urllib
import os
import hashlib

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

def resize_990(bestpath,resizepath,imagename):
    os.system("/usr/bin/convert "+bestpath+imagename+" -resize 990 "+resizepath+"/"+imagename)
    photohash_resized=hashlib.sha256(open(resizepath+imagename).read()).hexdigest()
    return photohash_resized

def copy_to_trackpath(setpath,trackpath,imagename):
    bestpath=trackpath+'best/'
    resizepath=trackpath+'best_990/'
    if os.path.exists(bestpath):
        print 'bestpath exists'+bestpath
    else:
        os.makedirs(bestpath) 
    if os.path.exists(resizepath):
        print 'resizepath exists'+resizepath
    else:
        os.mkdir(resizepath)
    os.system("cp "+setpath+'/'+imagename+" "+bestpath)
    photohash_resized=resize_990(bestpath,resizepath,imagename)
    return photohash_resized

def find_trackdatapath(imageinfo,database):
    session=database.db_session()
    db_log=database.db_log
    q = session.query(db_log).filter(db_log.infomarker_id==imageinfo.infomarker_id)
    loginfo=q.one()
    logdate=loginfo.createdate.strftime('%Y-%m-%d')
    print logdate
    trackpath='/srv/trackdata/bydate/'+str(logdate)+'/images/'
    return trackpath,loginfo 


def update_imageinfo(database,photohash,photohash_resized,imagename,imageinfo,loginfo):
    session=database.db_session()
    db_imageinfo=database.db_imageinfo
    print imageinfo.id
    print photohash
    q = session.query(db_imageinfo).filter(and_(db_imageinfo.id==imageinfo.id,db_imageinfo.flickrphotoid==imageinfo.flickrphotoid))
    for column in q.all():
        column.imgname=imagename
        column.photohash=photohash
        column.photohash_990=photohash_resized
        column.log_id=loginfo.id
        session.commit()
    if q.count() == 1:
        print photohash + '=\n' + q.one().photohash

def downloadphoto(photoset,farm,server,photoid,originalsecret,originalformat,imageinfo):
    print imageinfo.id
    trackpath,loginfo=find_trackdatapath(imageinfo,database)
    url="http://farm%s.static.flickr.com/%s/%s_%s_o.%s" % (farm,server,photoid,originalsecret,originalformat)
    print url
    setpath='/srv/flickrbackup/'+photoset.flickrsetid
    photopath=setpath+'/'+url.split('/')[-1]
    imagename="%s_%s_o.%s" % (photoid,originalsecret,originalformat)
    if os.path.exists(setpath):
        print 'setpath exists'+setpath
    else:
        os.mkdir(setpath)
    if os.path.exists(photopath):
        print 'photopath exists'+photopath
    else:
        flickrfile=urllib.urlopen(url)
        localcopy = open(photopath, 'w')
        localcopy.write(flickrfile.read())
        flickrfile.close()
        localcopy.close()
    imagefile=open(photopath).read()
    photohash_resized=copy_to_trackpath(setpath,trackpath,imagename)
    photohash=hashlib.sha256(open(photopath).read()).hexdigest()
    print imagename,photohash, photohash_resized
    return photohash,photohash_resized,imagename,loginfo

def getphotodetails(photoset,database):
    photos=talk2flickr.get_photosetphotos(photoset.flickrsetid)
    for photo in photos:
        session=database.db_session()
        db_imageinfo=database.db_imageinfo
        farm,server,photoid,secret,originalsecret,originalformat,date_taken,tags,url,title,description=talk2flickr.getimginfo(photo.photoid)
        query_imageinfo=session.query(db_imageinfo).filter(and_(db_imageinfo.photoset_id==photoset.id,db_imageinfo.flickrphotoid==photo.photoid))
        if query_imageinfo.count() >= 1:
            print 'Photo already exists in database'
            imageinfo=query_imageinfo.one()
            photohash,photohash_resized,imagename,loginfo=downloadphoto(photoset,farm,server,photoid,originalsecret,originalformat,imageinfo)
            update_imageinfo(database,photohash,photohash_resized,imagename,imageinfo,loginfo)
        else:
            print photohash,photoid
            session.add(db_imageinfo(None,photoset.id,None,None,farm,server,photoid,secret,date_taken,title,description,photohash))
            session.commit()
        
        
        

if __name__ == "__main__":
        parser = OptionParser()
        parser.add_option("--id", action="append", dest="flickrsetid",
                help="list of flickrsetids")



        (options, args) = parser.parse_args()

        flickrsetids=options.flickrsetid
        pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('credentials.ini')
        database=db_functions.initdatabase(pg_user,pg_passwd)
        for flickrsetid in flickrsetids:
            owner,primary,count,title,description=talk2flickr.get_photosetinfo(flickrsetid)
            session=database.db_session()
            db_photosets=database.db_photosets
            query_photoset=session.query(db_photosets).filter(db_photosets.flickrsetid==flickrsetid)
            if query_photoset.count() == 1:
                for detail in query_photoset.all():
                    print 'Photoset already exists - id:' + str(detail.id) + ' details:' + str(detail)
            else:
                session.add(db_photosets(flickrsetid,owner,primary,count,title,description))
                session.commit()
            query_photoset=session.query(db_photosets).filter(db_photosets.flickrsetid==flickrsetid)
            photoset=query_photoset.one()
            print photoset
            photodetails=getphotodetails(photoset,database)
