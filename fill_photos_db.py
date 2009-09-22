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


def downloadphoto(photoset,farm,server,photoid,originalsecret,originalformat):
    url="http://farm%s.static.flickr.com/%s/%s_%s_o.%s" % (farm,server,photoid,originalsecret,originalformat)
    print url
    setpath='/srv/flickrbackup/'+photoset.flickrsetid
    photopath=setpath+'/'+url.split('/')[-1]
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
    photohash=hashlib.sha256(open(photopath).read()).hexdigest()
    print photohash, photopath
    return photohash

def getphotodetails(photoset,session,db_imageinfo):
    photos=talk2flickr.get_photosetphotos(photoset.flickrsetid)
    for photo in photos:
        farm,server,photoid,secret,originalsecret,originalformat,date_taken,tags,url,title,description=talk2flickr.getimginfo(photo.photoid)
        query_imageinfo=session.query(db_imageinfo).filter(and_(db_imageinfo.photoset_id==photoset.id,db_imageinfo.flickrphotoid==photo.photoid))
        if query_imageinfo.count() >= 1:
            print 'Photo already exists in database'
        else:
            photohash=downloadphoto(photoset,farm,server,photoid,originalsecret,originalformat)
            print photohash,photoid
            session.add(db_imageinfo(None,photoset.id,None,None,farm,server,photoid,secret,date_taken,title,description,photohash))
            session.commit()
        
        
        

if __name__ == "__main__":
        parser = OptionParser()
        parser.add_option("--id", action="append", dest="flickrsetid",
                help="list of flickrsetids")



        (options, args) = parser.parse_args()


        flickrsetids=options.flickrsetid
        pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/home/peletiah/poab/credentials.ini')
        Session,db_log,db_comments,db_continent,db_country,db_photosets,db_imageinfo,db_track,db_trackpoint,db_timezone,db_image2tag,db_phototag=db_functions.initdatabase(pg_user,pg_passwd)
        session=Session()
        for flickrsetid in flickrsetids:
            owner,primary,count,title,description=talk2flickr.get_photosetinfo(flickrsetid)
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
            photodetails=getphotodetails(photoset,session,db_imageinfo)
