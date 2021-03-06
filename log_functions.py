from sqlalchemy import and_
from sqlalchemy import update
import db_functions
from datetime import datetime




def parseimgstrings(logtext,xmlimglist_plus_db_details,num_img_xml):
    for imgfromxml in xmlimglist_plus_db_details:
        #flickrlink='<img src="http://benko.login.cx:8080/flickr/%s/%s/%s/%s/%s">' % (img_detail.flickrfarm,img_detail.flickrserver,img_detail.flickrphotoid,img_detail.flickrsecret,'_m')
        if imgfromxml.logphoto=='True':
            print imgfromxml.number
            print imgfromxml.name
            i=1
            while i <= num_img_xml:
                print 'currentimgnumber: img'+str(i)
                if imgfromxml.number=='img'+str(i):
                    print '[img'+str(i)+']'
                    logtext=logtext.replace('[img'+str(i)+']','[imgid'+str(imgfromxml.imageinfo_detail.id)+']')
                i=i+1
    return logtext



def log2db(topic,logtext,createdate,xmlimglist_plus_db_details,num_img_xml,infomarker_id,database):
    session=database.db_session()
    db_log=database.db_log
    parsed_logtext=parseimgstrings(logtext,xmlimglist_plus_db_details,num_img_xml)
    print parsed_logtext
    query_log=session.query(db_log).filter(and_(db_log.topic==topic,db_log.content==parsed_logtext,db_log.infomarker_id==infomarker_id))
    if query_log.count() == 1:
        for detail in query_log.all():
            log_detail=detail
        print 'Log already exists - id:' + str(log_detail.id) + ' details:' + str(log_detail)
    elif query_log.count() > 1:
        for detail in query_log.all():
            log_detail=detail
        print 'Log duplicate found! - id:' + str(log_detail.id) + ' - details:' + str(log_detail)
    else:
        session.add(db_log(infomarker_id,topic,parsed_logtext,createdate))
        session.commit()
        for log_detail in query_log.all():
            print 'Log created - id:' + str(log_detail.id) + ' details:' + str(log_detail.topic)

    return log_detail
