import talk2flickr
from optparse import OptionParser
import db_functions
from sqlalchemy import and_
import hashlib
import ConfigParser

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


def getphotodetails(flickrsetid):
    photodetails=talk2flickr.get_photosetphotos(flickrsetid)
        
        

if __name__ == "__main__":
        parser = OptionParser()
        parser.add_option("--id", action="append", dest="flickrsetid",
                help="list of flickrsetids")



        (options, args) = parser.parse_args()


        flickrsetids=options.flickrsetid
        pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/scripts/credentials.ini')
        Session,db_log,db_comments,db_continent,db_country,db_photosets,db_imageinfo,db_track,db_trackpoint,db_timezone,db_image2tag,db_phototag=db_functions.initdatabase(pg_user,pg_passwd)
        session=Session()
        for flickrsetid in flickrsetids:
            owner,primary,count,title,description=talk2flickr.get_photosetinfo(flickrsetid)
            session.add(db_photosets(flickrsetid,owner,primary,count,title,description))
            session.commit()
            query_photoset=session.query(db_photosets).filter(db_photosets.flickrsetid==flickrsetid)
            photosetid=query_photoset.one()
            print photosetid
            photodetails=getphotodetails(photosetid)
