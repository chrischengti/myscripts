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


urlGetReport="http://www.alibench.com/jingpin_get_report.php"
urlNewTask="http://www.alibench.com/jingpin_new_task.php"
allTestType=('3basic','tcp_stream','udp_stream','tcp_rr','tcp_cc','udp_rr')


LOG_FILE = 'nettest.log-'+str(os.getpid())

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

logger = logging.getLogger('netTest')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def executeLinkTest(linkInfo,testType,outRegion=True):
    #invoke the test and get the result
    testTarget = ''
    if outRegion == True:
        testTarget = linkInfo[1][2]
    else:
        testTarget = linkInfo[1][3]
    testClientID=linkInfo[0][1]
    data = None
    result = None
    if testType==allTestType[0]:
        data = "scripts=@echo off;ping %s  &client_id=%s&ac=http" %(testTarget,testClientID)
        result = postAndParseResult(data,parsePingResult)
    elif testType ==allTestType[1]:
        data = "scripts=@echo off; cd \"%%~dp0%%\"; netperf -H %s  &client_id=%s&ac=http" %(testTarget,testClientID)
        result = postAndParseResult(data,parseNetperfTcpStream)
    elif testType == allTestType[2]:
        data = "scripts=@echo off; cd \"%%~dp0%%\"; netperf -H %s -t udp_stream &client_id=%s&ac=http" %(testTarget,testClientID)
        result = postAndParseResult(data,parseNetperfUdpStream)
    elif testType == allTestType[3]:
        data = "scripts=@echo off; cd \"%%~dp0%%\"; netperf -H %s -t tcp_rr &client_id=%s&ac=http" %(testTarget,testClientID)
        result = postAndParseResult(data,parseNetperfTcprr)
    elif testType == allTestType[4]:
        data = "scripts=@echo off; cd \"%%~dp0%%\"; netperf -H %s -t tcp_cc &client_id=%s&ac=http" %(testTarget,testClientID)
        result = postAndParseResult(data,parseNetperfTcpcc)
    elif testType == allTestType[5]:
        data = "scripts=@echo off; cd \"%%~dp0%%\"; netperf -H %s -t udp_rr &client_id=%s&ac=http" %(testTarget,testClientID)
        result = postAndParseResult(data,parseNetperfUdprr)
    else:
        logger.error("unsupported test type")
        result = "unsupported type"
        pass
    dataAndResult = data + '\n' + json.dumps(result)
    logger.debug(dataAndResult)
    return result

def executeLinkTestsSequential(linkInfos,testType):
    #execute sequentially and return the results
    linksResults=[]
    logger.info(linkInfos)

    for linkInfo in linkInfos:
        result = executeLinkTest(linkInfo,testType)
        linksResults.append({'link':linkInfo,'result':result})
    return linksResults

def postAndParseResult(data,parser):
    if data != 'unspported type':

        taskID = submitTask(data)['data'][0] #todo
        result= getTaskResult(taskID,10,12) #todo tune the timeout
        '''
        #mock
        time.sleep(2)
        result = {'INET_NTOA(client_ip)': '52.8.8.144',
              'done_time': '2015-06-04 11:07:52',
              'http_response_head':'\r\r\nPinging baidu.com [123.125.114.144] with 32 bytes of data:\r\r\n\r\r\nReply from 123.125.114.144: bytes=32 time=27ms TTL=50\r\r\nReply from 123.125.114.144: bytes=32 time    =27ms TTL=50\r\r\nReply from 123.125.114.144: bytes=32 time=27ms TTL=51\r\r\nReply from 123.125.114.144: bytes=32 time=27ms TTL=51\r\r\n\r\r\nPing statistics for 123.125.114.144:\r\r\n    Packets: Sen    t = 4, Received = 4, Lost = 0 (0% loss),\r\r\nApproximate round trip times in milli-seconds:\r\r\n    Minimum = 27ms, Maximum = 27ms, Average = 27ms\r\r\n',
              'node_id': '11221162',
              'start_time': '2015-06-04 11:07:39'}
        result = {'INET_NTOA(client_ip)': '123.59.10.244',
            'done_time': '2015-06-05 16:01:18',
            'http_response_head': '\r\n\\u6b63\\u5728 Ping baidu.com [220.181.57.217] \\u5177\\u6709 32 \\u5b57\\u8282\\u7684\\u6570\\u636e:\r\n\\u6765\\u81ea 220.181.57.217 \\u7684\\u56de\\u590d: \\u5b57\\u8282    =32 \\u65f6\\u95f4=2ms TTL=47\r\n\\u6765\\u81ea 220.181.57.217 \\u7684\\u56de\\u590d: \\u5b57\\u8282=32 \\u65f6\\u95f4=2ms TTL=47\r\n\\u6765\\u81ea 220.181.57.217 \\u7684\\u56de\\u590d: \\u5b57\\u8282    =32 \\u65f6\\u95f4=2ms TTL=47\r\n\\u6765\\u81ea 220.181.57.217 \\u7684\\u56de\\u590d: \\u5b57\\u8282=32 \\u65f6\\u95f4=2ms TTL=47\r\n\r\n220.181.57.217 \\u7684 Ping \\u7edf\\u8ba1\\u4fe1\\u606f:\r\n        \\u6570\\u636e\\u5305: \\u5df2\\u53d1\\u9001 = 4\\uff0c\\u5df2\\u63a5\\u6536 = 4\\uff0c\\u4e22\\u5931 = 0 (10% \\u4e22\\u5931)\\uff0c\r\n\\u5f80\\u8fd4\\u884c\\u7a0b\\u7684\\u4f30\\u8ba1\\u65f6\\u95f    4(\\u4ee5\\u6beb\\u79d2\\u4e3a\\u5355\\u4f4d):\r\n    \\u6700\\u77ed = 2ms\\uff0c\\u6700\\u957f = 2ms\\uff0c\\u5e73\\u5747 = 5ms\r\n',
            'node_id': '11224365',
            'start_time': '2015-06-05 16:01:09'}
        '''
        if result == None:
            return None
        else:
            result['postParse']=parser(result)
            #print data,'dadadada\n'
            return result

def submitTask(data):
    #print data
    return eval(urllib2.urlopen(urlNewTask,data,10).read())

def getTaskResult(taskId,interval,times):
    #getresult and report to perfkitdb
    for i in range(times):
        #return if there is result
        response = eval(urllib2.urlopen(urlGetReport,"task_id=%s" % taskId,10).read())
        #pprint.pprint(eval(response.read())[0]['http_response_head'].split(';;;'))
        #pprint.pprint(response[0]['http_response_head'].split(';;;'))
        if response!= []:
            return response[0]
        else:
            time.sleep(interval)
            continue
    logger.error('could not get result for taskId %s' % taskId)
    return None

def parsePingResult(result):
    pingLantency = None
    pingLost = None
    pingHops = None
    matchTTL = re.search('.*TTL=([0-9]*)',result['http_response_head'])
    if matchTTL:
        pingHops = 128 - int(matchTTL.group(1))

    for line in result['http_response_head'].split('\r\n'):

        match =re.search('.*Average = ([0-9]*ms)',line) or re.search('.*\\\\u5e73\\\\u5747 = ([0-9])*ms',line)
        if match:
            pingLantency= match.group(1)
            continue
        match2 = re.search('.*\(([0-9]*%) loss.*',line) or re.search('.*\(([0-9]*%) \\\\u4e22\\\\u5931.*',line)
        if match2:
            pingLost = match2.group(1)
            continue
    return {'lostrate': pingLost,'latency': pingLantency, 'hops': pingHops}


def parseNetperfTcpStream(result):
    tcpThroughput = None
    match = re.search('Throughput',result['http_response_head'])
    if match:
        return result['http_response_head'].split('\r\n')[6].split()[4]+'Mb'
    return result['http_response_head']

def parseNetperfUdpStream(result):
    udpThroughput = None
    match = re.search('Throughput',result['http_response_head'])
    if match:
        return result['http_response_head'].split('\r\n')[5].split()[5]+'Mb'
    return result['http_response_head']

def parseNetperfTcprr(result):
    tcprr = None
    match = re.search('Trans',result['http_response_head'])
    if match:
        return result['http_response_head'].split('\r\n')[6].split()[5]
    return result['http_response_head']

def parseNetperfTcpcc(result):
    tcprr = None
    match = re.search('Trans',result['http_response_head'])
    if match:
        return result['http_response_head'].split('\r\n')[6].split()[5]
    return result['http_response_head']


def parseNetperfUdprr(result):
    tcprr = None
    match = re.search('Trans',result['http_response_head'])
    if match:
        return result['http_response_head'].split('\r\n')[6].split()[5]
    return result['http_response_head']

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
        entry['source'] = item[1][0][0][0][:-2]
        entry['target'] = item[1][0][1][0][:-2]
        entry['testType'] = item[1][1]
        entry['provider'] = entry['source'].split('_')[0]
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
    #pprint.pprint(providerInfo)
    #find all links in a given provider
    iter = itertools.combinations(providerInfo.keys(),2)
    linksToTest=[]
    for link in list(iter):
        if vmIndex == 0:
            linksToTest.append([providerInfo[link[0]][vmIndex],providerInfo[link[1]][vmIndex]])
        else:
            linksToTest.append([providerInfo[link[1]][vmIndex],providerInfo[link[0]][vmIndex]])
    #tests in a given provider should be performed sequentially
    logger.info('test out region in provider %s' % providerName)
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
            entry['source'] = res['link'][0][0][:-2]
            entry['target'] =  res['link'][1][0][:-2]
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
    data = "scripts=@echo off;ping baidu.com  &client_id=%s&ac=http" %(2222)
    for value in cloudInfo.values():
        for hostPair in value.values():
            for host in hostPair:
                print host
                tid = submitTask("scripts=@echo off;ping baidu.com  &client_id=%s&ac=http" % host[1])['data'][0]
                print tid
                print getTaskResult(tid,5,36)


def testBothInAndOutRegion(cloudInfo,linkTestType,resultFolder):
    infos = parseCloudhostInfo(cloudInfo)
    pprint.pprint(infos)
    for item in linkTestType.split(','):
        ttype = item.strip()
        logger.info('starting test in region'+ ttype)
        result = parseResultPerfInRegion(testPerfInRegion(infos,ttype))
        fileName=resultFolder+'/netlinkperf'+str(time.time()).split('.')[0]+'.json'
        print 'result file name ' + fileName
        with open(fileName,mode='w') as file:
            file.write(json.dumps(result,indent=4))

        logger.info('starting test out region'+ ttype)
        result = parseResultsPerfAllRegion(testPerfAllRegions(infos,ttype))
        fileName=resultFolder+'/netlinkperf'+str(time.time()).split('.')[0]+'.json'
        print 'result file name ' + fileName
        with open(fileName,mode='w') as file:
            file.write(json.dumps(result,indent=4))

