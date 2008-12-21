from sqlalchemy import and_
from sqlalchemy import update




parseimgstrings(logtext,imglist):
   for img in dictlist:
    #do something!	 




log2db(topic,logtext,imgdict,infomarker_id,photoid,flickrfarm,flickrserver,flickrphotoid,flickrsecret,Session,db_log):
    session=Session()
    parsed_logtext=parseimgstrings(logtext,imgdict)
    query_log=session.query(db_log).filter(db_log.topic==topic,db_log.content==parsed_logtext,db_log.trackpoint==infomarker_id)
    if query_log.count() == 1:
	for detail in query_log.all():
	    log_detail=detail
	    print 'Log already exists - id:' + str(log_detail.id) + ' details:' + str(log_detail)
    elif query_log.count() > 1:
	for detail in query_log.all():
	    log_detail=detail
	    print 'Log duplicate found! - id:' + str(log_detail.id) + ' - details:' + str(log_detail)
    else:
	session.add(db_log(infomarker_id,topic,parsed_logtext)
	session.commit()
	for detail in query_log.all():
            log_detail=detail
            print 'Log created - id:' + str(log_detail.id) + ' details:' + str(log_detail)

    return log_detail
