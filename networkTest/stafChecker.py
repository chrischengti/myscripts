__author__ = 'ziguang'

from PySTAF import *
import sys,pprint,re,time

def submitSTAFProcessjob(host,job):
    request = 'start shell command %s' % wrapData(job)
    request += ' RETURNSTDOUT RETURNSTDERR STDERRTOSTDOUT WAIT'
    res =  None
    try:
        handle = STAFHandle("MyTest")
    except STAFException, e:
        print "Error registering with STAF, RC: %d" % e.rc
    result = handle.submit(host, 'process', request)

    if (result.rc != 0):
        debugInfo = host+' '+request + '\n' +\
                    "Error submitting request, RC: %d, Result: %s" % (result.rc, result.result)
        print debugInfo
    else:
        #pprint.pprint(result.resultObj)
        #logger.debug(result.result)
        #res = result.resultObj['fileList'][0]['data']
        res = result.result
        pprint.pprint(res.split('\r\n'))
    rc = handle.unregister()
    return res