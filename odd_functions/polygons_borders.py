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

def parsesvg(database):
    session=database.db_session()
    db_country=database.db_country
    db_country_polygons=database.db_country_polygons
    tree = etree.parse('world.svg')
    root = tree.getroot()
    countries=root.getiterator("g")
    i=0
    countrylist=list()
    for country in countries:
        polygons=list()
        countrylist=list()
        isocode=country.attrib['id'].split('-')[1]
        print isocode
        try:
            q = session.query(db_country).filter(db_country.iso_numcode==isocode)
            cindb=q.one()
            print cindb.iso_countryname
            for polygon in country:
                i=i+1
                try:
                   points=polygon.attrib['points']
                except KeyError:
                    print 'Error:'+isocode
                q = session.query(db_country_polygons).filter(and_(db_country_polygons.country_id==isocode,db_country_polygons.polygon==points))
                if q.count()>1:
                    country_polygon=q.one()
                    print country_polygon.id,country_shape.iso_numcode
                else:
                    session.add(db_country_polygons(isocode,points,True))
                    session.commit()
        except:
            print 'Error:'+str(isocode)
            print 'Country not found in db:'+str(country.attrib['id'])
        
if __name__ == "__main__":
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab/credentials.ini')
    database=db_functions.initdatabase(pg_user,pg_passwd)
    parsesvg(database)
