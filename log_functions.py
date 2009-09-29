from sqlalchemy import and_
from sqlalchemy import update
import db_functions




def parseimgstrings(logtext,imglist):
    i=1
    for img_detail in imglist:
        #flickrlink='<img src="http://benko.login.cx:8080/flickr/%s/%s/%s/%s/%s">' % (img_detail.flickrfarm,img_detail.flickrserver,img_detail.flickrphotoid,img_detail.flickrsecret,'_m')
        print imglist
        print '[img'+str(i)+']'
        logtext=logtext.replace('[img'+str(i)+']','[imgid'+str(img_detail.id)+']')
        i=i+1
    return logtext



def log2db(topic,logtext,imglist,infomarker_id,Session,db_log):
    session=Session()
    parsed_logtext=parseimgstrings(logtext,imglist)
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
	session.add(db_log(infomarker_id,topic,parsed_logtext,db_functions.now()))
	session.commit()
	for detail in query_log.all():
            log_detail=detail
            print 'Log created - id:' + str(log_detail.id) + ' details:' + str(log_detail)

    return log_detail
