#!/usr/bin/env python
import time
from string import Template
import simplejson as json
import itertools
import pprint
import random
import re,os
import urllib2
import logging
import logging.handlers
from thread_pool import *
from PySTAF import *


allTestType=('3basic','tcp_stream','udp_stream','tcp_rr','tcp_cc','udp_rr','pps')

#create a global logger
LOG_FILE = 'nettest.log-'+str(os.getpid())
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024*2, backupCount = 5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
logger = logging.getLogger('netTest')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def executeLinkTest(linkInfo,testType,outRegion=True):
    #invoke the test and get the result
    sourceHost = linkInfo[0][2]
    if outRegion == True:
        testTarget = linkInfo[1][2]
    else:
        testTarget = linkInfo[1][3]
    result = {}
    if testType==allTestType[0]:
        job = "ping %s" % testTarget
        resParser = parsePingResult
    elif testType ==allTestType[1]:
        job = "netperf -H %s -t TCP_STREAM" % testTarget
        resParser = parseNetperfTcpStream
    elif testType == allTestType[2]:
        job = "netperf -H %s -t udp_stream" % testTarget
        resParser = parseNetperfUdpStream
    elif testType == allTestType[3]:
        job = "netperf -H %s -t tcp_rr" % testTarget
        resParser = parseNetperfTcprr
    elif testType == allTestType[4]:
        job = "netperf -H %s -t tcp_cc" % testTarget
        resParser = parseNetperfTcpcc
    elif testType == allTestType[5]:
        job = "netperf -H %s -t udp_rr" % testTarget
        resParser = parseNetperfUdprr
    elif testType == allTestType[6]:
        job = "del out.txt && start /b netperf -H %s -l 30  -- -m 1 -D > out.txt 2>&1 " % testTarget +\
            " && typeperf \"\\Network Interface(*)\\Packets Sent/sec\" -si 2 -sc 14 -y"
        afterJob = "type out.txt"
        resParser = parsePPS
    else:
        logger.error("unsupported test type")
        return None

    structTime = time.localtime()
    result['start_time'] = "%s-%s-%s %s:%s:%s" % (structTime.tm_year,structTime.tm_mon,structTime.tm_mday,
                                                  structTime.tm_hour,structTime.tm_min,structTime.tm_sec)
    if testType == allTestType[6]:
        jobResult = submitSTAFjob(sourceHost,'process',wrapProcessRequest(job))
        if jobResult != None:
            time.sleep(3)
            netperfResult = submitSTAFjob(sourceHost,'process',wrapProcessRequest(afterJob))
            jobResult = jobResult +"\n"+ str(netperfResult)
    else:
        jobResult = submitSTAFjob(sourceHost,'process',wrapProcessRequest(job))

    structTime = time.localtime()
    result['done_time'] = "%s-%s-%s %s:%s:%s" % (structTime.tm_year,structTime.tm_mon,structTime.tm_mday,
                                                  structTime.tm_hour,structTime.tm_min,structTime.tm_sec)
    testInfo = str(linkInfo)+ '\n' + job

    if jobResult == None:
        result =  None
    else:
        if isNetserverDown(jobResult):
            result['postParse'] = 'netserver unreacheable'
        else:
            result['postParse']=resParser(jobResult)
    logger.debug(testInfo + '\n' + str(result)+'\n' + str(jobResult))
    return result

def wrapProcessRequest(job):
    request = 'start shell command %s' % wrapData(job)
    request += ' RETURNSTDOUT RETURNSTDERR STDERRTOSTDOUT WAIT 300s '
    return request

def executeLinkTestsSequential(linkInfos,testType):
    #execute sequentially and return the results
    linksResults=[]
    #logger.info(linkInfos)

    for linkInfo in linkInfos:
        result = executeLinkTest(linkInfo,testType)
        linksResults.append({'link':linkInfo,'result':result})
    return linksResults

def submitSTAFjob(host,service,request):
    logger.debug("startstafjob" +" "+ host +" " +service+" " + request)
    res =  None
    try:
        handle = STAFHandle("MyTest")
    except STAFException, e:
        logger.info( "Error registering with STAF, RC: %d" % e.rc)
    result = handle.submit(host, service, request)
    if (result.rc != 0):
        debugInfo = host+" "+service+" "+request + '\n' +\
                    "Error submitting request, RC: %d, Result: %s" % (result.rc, result.result)
        logger.debug(debugInfo)
    else:
        #pprint.pprint(result.resultObj)
        #logger.debug(result.result)
        #res = result.resultObj['fileList'][0]['data']
        res = result.result
    logger.debug("finishstafjob" +" "+ host +" " +service+" " + request)
    rc = handle.unregister()
    return res

def isNetserverDown(data):
    match = re.search('establish control: are you sure there is a netserver listening on', data)
    if match:
        return True
    return False

def parsePingResult(result):
    pingLantency = None
    pingLost = None
    pingHops = None
    matchTTL = re.search('.*TTL=([0-9]*)',result)
    if matchTTL:
        pingHops = 128 - int(matchTTL.group(1))

    for line in result.split('\r\n'):
        match =re.search('.*Average = ([0-9]*ms)',line) or re.search('.*\\\\u5e73\\\\u5747 = ([0-9])*ms',line) \
               or re.search('.*\\xef\\xbc\\x8c\\xe5\\xb9\\xb3\\xe5\\x9d\\x87 = ([0-9])*ms',line)

        if match:
            pingLantency= match.group(1)
            continue
        match2 = re.search('.*\(([0-9]*%) loss.*',line) or re.search('.*\(([0-9]*%) \\\\u4e22\\\\u5931.*',line)\
            or re.search('.*\(([0-9]*%) \\xe4\\xb8\\xa2\\xe5\\xa4\\xb1\)\\xef\\xbc\\x8c',line)
        if match2:
            pingLost = match2.group(1)
            continue
    return {'lostrate': pingLost,'latency': pingLantency, 'hops': pingHops}


def parseNetperfTcpStream(result):
    match = re.search('Throughput',result)
    if match:
        return {'value': float(result.split('\r\n')[6].split()[4]), 'unit' : 'Mb/sec'}
    return result

def parseNetperfUdpStream(result):
    match = re.search('Throughput',result)
    if match:
        return {'value': float(result.split('\r\n')[5].split()[5]), 'unit':'Mb/sec'}
    return result

def parseNetperfTcprr(result):
    match = re.search('Trans',result)
    if match:
        return {'value': int(float(result.split('\r\n')[6].split()[5])), 'unit':'TPS'}
    return result

def parseNetperfTcpcc(result):
    match = re.search('Trans',result)
    if match:
        return {'value': int(float(result.split('\r\n')[6].split()[5])), 'unit':'CPS'}
    return result


def parseNetperfUdprr(result):
    match = re.search('Trans',result)
    if match:
        return {'value': int(float(result.split('\r\n')[6].split()[5])), 'unit' :'TPS'}
    return result

def parsePPS(result):
    samplesNum = 0
    allPPs = []
    for line in result.split('\r\n'):
        match = re.search('\"[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{1,5}',line)
        if match:
            #print line.split(',')[1:]
            samplesNum += 1
            for item in line.split(',')[1:]:
                allPPs.append( float(item.strip('"')))
    if samplesNum ==0:
        return result
    else:
        return {'value': int(sorted(allPPs)[-1]),'unit':'txpck/s'}

def testPerfInRegion(cloudInfo,testType):
    logger.info('measure the perf for the links in the region')
    #find all test links
    linkstoTest=[]
    for provider in cloudInfo.keys():
        for region in cloudInfo[provider].keys():
            cloudHostInfo = cloudInfo[provider][region]
            linkstoTest.append([cloudHostInfo[0],cloudHostInfo[1]])
    logger.info(linkstoTest)
    #trigger tests, all the test in this list can be performed in parallel.
    wb = WorkerManager()
    for link in linkstoTest:
        wb.add_job(executeLinkTest,link,testType,False)
    wb.wait_for_complete()
    #get results
    return [wb.get_result() for x in range(len(linkstoTest))]

def parseResultPerfInRegion(data):
    result = []
    for item in data:
        entry={}
        entry['linktype'] = 'inner'
        entry['source'] = item[1][0][0][0].split('_')[1]
        entry['sourceFullName'] = str(item[1][0][0])
        entry['target'] = item[1][0][1][0].split('_')[1]
        entry['targetFullName'] = str(item[1][0][1])
        entry['testType'] = item[1][1]
        entry['provider'] = item[1][0][0][0].split('_')[0]
        if item[0] != None:
            entry['done_time'] = item[0]['done_time']
            entry['start_time'] = item[0]['start_time']
            entry['testResult'] = item[0]['postParse']
        else:
            entry['testResult'] = None
        result.append(entry)
    return result

def testPerfOutRegionInProvider(providerInfo,providerName,testType,vmIndex):
    logger.info('measure the perf for the links between the region in a given provider')
    logger.info(providerInfo)
    #find all links in a given provider
    iter = itertools.combinations(providerInfo.keys(),2)
    linksToTest=[]
    for link in list(iter):
        if vmIndex == 0:
            linksToTest.append([providerInfo[link[0]][vmIndex],providerInfo[link[1]][vmIndex]])
        else:
            linksToTest.append([providerInfo[link[1]][vmIndex],providerInfo[link[0]][vmIndex]])
    #tests in a given provider should be performed sequentially
    return executeLinkTestsSequential(linksToTest,testType)

def testPerfOutRegionInProvider1t1(providerInfo,providerName,testType):
    return testPerfOutRegionInProvider(providerInfo,providerName,testType,0)

def testPerfOutRegionInProvider2t2(providerInfo,providerName,testType):
    return testPerfOutRegionInProvider(providerInfo,providerName,testType,1)

def testPerfAllRegions(cloudInfo,testType):
    wb = WorkerManager()
    numberOfProviderForTest=0
    for name,provider in cloudInfo.items():
        if len(provider.keys())>1:
            numberOfProviderForTest += 1
            #trigger tests
            wb.add_job(testPerfOutRegionInProvider1t1,provider,name,testType)
            wb.add_job(testPerfOutRegionInProvider2t2,provider,name,testType)
    wb.wait_for_complete()
    return [wb.get_result() for x in range(numberOfProviderForTest*2)]

def parseResultsPerfAllRegion(data):
    pprint.pprint('all region raw result')
    pprint.pprint(data)
    result = []
    for item in data:
        testType = item[1][2]
        provider = item[1][1]
        for res in item[0]:
            entry = {}
            entry['linktype'] = 'outer'
            entry['testType'] = testType
            entry['provider'] = provider
            entry['source'] = res['link'][0][0].split('_')[1]
            entry['sourceFullName'] = str(res['link'][0])
            entry['target'] =  res['link'][1][0].split('_')[1]
            entry['targetFullName'] = str(res['link'][1])
            if res['result'] != None:
                entry['start_time'] = res['result']['start_time']
                entry['done_time'] = res['result']['done_time']
                entry['testResult'] = res['result']['postParse']
            else:
                entry['testResult'] = None
            result.append(entry)
    return result


def parseCloudhostInfo(fileName):
    infos = {}
    for line in file(fileName).readlines():
        line = line.strip()
        if line.startswith("#"):
            continue
        temlist = line.split()
        if len(temlist)!=4:
           continue
        name, ip, clientid, localip = line.split()
        provider, region, index = name.split("_")
        detail = (name, clientid, ip, localip)
        if infos.has_key(provider):
            provider_infos = infos[provider]
        else:
            provider_infos = {}
            infos[provider] = provider_infos
        if provider_infos.has_key(region):
            region_infos = provider_infos[region]
        else:
            region_infos = []
            provider_infos[region] = region_infos
        region_infos.append(detail)
    #print json.dumps(infos, indent=4)
    return infos

def detectAgent(cloudInfo):
    for value in cloudInfo.values():
        for hostPair in value.values():
            for host in hostPair:
                print host
                logger.info(host)
                job =  'ping baidu.com '
                request = ' start shell command %s'% wrapData(job)
                request += 'STDERRTOSTDOUT RETURNSTDOUT WAIT 300s'
                res = submitSTAFjob(host[2], 'process', request)
                print res

def checkAndStartNetserver(cloudInfo):
    netserverDownList=[]
    stafDownList=[]
    wb = WorkerManager()
    for value in cloudInfo.values():
        for hostPair in value.values():
            for host in hostPair:
                wb.add_job(submitSTAFjob, host[2],'process',
                           wrapProcessRequest("tasklist | findstr netserver ||  restart_aliprobe"))
    wb.wait_for_complete()

    while not wb.resultQueue.empty():
        result = wb.get_result()
        if result[0] == None:
            stafDownList.append(result[1][0])
        elif re.search('AliMaintain',result[0]):
            netserverDownList.append(result[1][0])
        elif re.search('netserver', result[0]):
            #logger.debug(result[1][0]+' is ok' +'\n'+result[0] )
            logger.debug(result[1][0]+' is ok')
        else:
            logger.debug('unknow reason\n' + result[1][0]+'\n'+result[0])
    if stafDownList != []:
        stafDownList.insert(0,'staf service is not available  on below hosts:')
        pprint.pprint(stafDownList)
        logger.info(str(stafDownList))
    if netserverDownList != []:
        netserverDownList.insert(0,'restarted netserver on below hosts:')
        pprint.pprint(netserverDownList)
        logger.info(str(netserverDownList))



def testBothInAndOutRegion(cloudInfo,linkTestType,resultFolder):
    infos = parseCloudhostInfo(cloudInfo)
    pprint.pprint(infos)
    for item in linkTestType.split(','):
        ttype = item.strip()
        if ttype != '3basic':
            checkAndStartNetserver(infos)
        logger.info('starting test in region'+ ttype)
        result = parseResultPerfInRegion(testPerfInRegion(infos,ttype))
        fileName=resultFolder+'/netlinkperf'+str(time.time()).split('.')[0]+'-inner-'+ttype+'.json'
        fileTxt = fileName.strip('.json')+'.txt'
        logger.info( 'result file name ' + fileName)
        with open(fileName,mode='w') as file:
            file.write(json.dumps(result,indent=4))

        with open(fileTxt,mode='w') as file:
            file.write(json.dumps(result,indent=4))

        logger.info('starting test out region'+ ttype)
        result = parseResultsPerfAllRegion(testPerfAllRegions(infos,ttype))
        fileName=resultFolder+'/netlinkperf'+str(time.time()).split('.')[0]+'-outer-'+ttype+'.json'
        fileTxt = fileName.strip('.json')+'.txt'
        logger.info( 'result file name ' + fileName)
        with open(fileName,mode='w') as file:
            file.write(json.dumps(result,indent=4))

        with open(fileTxt,mode='w') as file:
            file.write(json.dumps(result,indent=4))

