from getfromxml import parsexml as parsexml
import os
import ConfigParser
import db_functions
from sqlalchemy import and_,or_

basepath='/srv/trackdata/bydate/'

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


pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('credentials.ini')
database=db_functions.initdatabase(pg_user,pg_passwd)

for xmlfile in os.listdir(basepath):
        if xmlfile.lower().endswith('.xml'):
            print 'xmlfile: '+xmlfile
            topic,logtext,filepath,photosetname,phototitle,num_of_img,createdate,trk_color,xmlimglist,xmltaglist=parsexml(basepath,xmlfile,False)
            for imgfromxml in xmlimglist:
                session=database.db_session()
                db_imageinfo=database.db_imageinfo
                db_photosets=database.db_photosets
                db_log=database.db_log
                q = session.query(db_imageinfo).filter(or_(db_imageinfo.photohash==imgfromxml.hash_full,db_imageinfo.photohash_990==imgfromxml.hash_resized))
                if q.count()>0:
                    print 'Image already in DB: '+str(imgfromxml.name)
                else:
                    #take care of duplicate image-names in DB! Disabled function to make sure you do check!
                    #q = session.query(db_imageinfo).filter(db_imageinfo.imgname==imgfromxml.name)
                    if q.count()>0:
                        print 'Image found in DB: '+str(imgfromxml.name)+' but hash doesn\'t match'
                    else:
                        print 'Image not found in DB: '+str(imgfromxml.name)
                        print photosetname
                        q_photoset=session.query(db_photosets).filter(db_photosets.flickrtitle==photosetname)
                        if q_photoset.count()>0:
                            photoset=q_photoset.one()
                            print 'photoset exists'
                            q_log=session.query(db_log).filter(db_log.topic==topic)
                            log=q_log.one()
                            session.add(db_imageinfo(log.id,photoset.id,None,None,None,None,None,None,None,photosetname,imgfromxml.description,imgfromxml.hash_full,imgfromxml.hash_resized,imgfromxml.name,None,None,None,None,False,False))
                            session.commit()
                        else:
                            print 'no photoset exists, assuming there\'s nothing else too'
                
                
            
