import sys
sys.path.append('/root/poab')
from lxml import etree
from xml.etree import ElementTree
import glineenc
from sqlalchemy import and_, or_
import ConfigParser
import db_functions

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

def parsegpx(database):
    session=database.db_session()
    db_country=database.db_country
    db_country_shapes=database.db_country_shapes
    tree = etree.parse('borders_world_proper.gpx')
    root = tree.getroot()
    segments=root.getiterator("rte")
    i=0
    countrylist=list()
    for segment in segments:
        latlonlist=list()
        isocode=segment.find('cmt').text
        print isocode
        try:
            q = session.query(db_country).filter(db_country.iso_numcode==isocode)
            country=q.one()
            print country.iso_countryname
#            q = session.query(db_country_shapes).filter(db_country_shapes.iso==country.iso_numcode)
            for trkpt in segment:
               i=i+1
               try:
                   lat=trkpt.attrib['lat']
                   lon=trkpt.attrib['lon']
                   latlonlist.append((float(lat),float(lon)))
               except KeyError:
                   pass
            gencpoly=glineenc.encode_pairs(latlonlist)
            q = session.query(db_country_shapes).filter(and_(db_country_shapes.country_id==isocode,db_country_shapes.gencpoly_pts==gencpoly[0].replace('\\','\\\\')))
            if q.count()>1:
                country_shape=q.one()
                print country_shape.id,country_shape.iso_numcode
            else:
                session.add(db_country_shapes(country.iso_numcode,gencpoly[0].replace('\\','\\\\'),gencpoly[1]))
                session.commit()
        except:
            print 'Error:'+str(isocode)
            print segment.find('name').text
        
if __name__ == "__main__":
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab/credentials.ini')
    database=db_functions.initdatabase(pg_user,pg_passwd)
    parsegpx(database)
