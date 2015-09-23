__author__ = 'ziguang'

from PySTAF import *
import sys,pprint,re,time

def submitSTAFjob(host,service,job):
    request = 'start shell command %s' % wrapData(job)
    request += ' RETURNSTDOUT RETURNSTDERR STDERRTOSTDOUT WAIT 100s'
    res =  None
    print 'xxxx '+ host +" " + request
    try:
        handle = STAFHandle("MyTest")
    except STAFException, e:
        print "Error registering with STAF, RC: %d" % e.rc
    result = handle.submit(host, service, request)

    if (result.rc != 0):
        debugInfo = host+service+request + '\n' +\
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

service = 'process'
host = '168.61.42.225'
#host = '138.91.159.43'

#result = handle.submit("local", "var", "resolve string {STAF/Config/OS/Name}")

job =  'ping baidu.com'
duration = 30
job = "start /b netperf -H 10.121.104.80 -l %s > out.txt 2>&1 " % duration +\
      "typeperf \"\\Network Interface(*)\\Packets Sent/sec\" -si 3 -sc 3 -y & "

job1 = "del out.txt && start /b netperf -H 10.165.125.199 -l %s  -- -m 1 -D > out.txt 2>&1 " % duration
job2 = "typeperf \"\\Network Interface(*)\\Packets Sent/sec\" -si 2 -sc 8 -y  "
job3 = "type out.txt"
#job2 = "ping -w 1000 192.0.0.1 -n 30 > NUL 2>&1 & type out.txt"
jobCheckStaf="tasklist | findstr netserver"
jobStartNetserver="start /b restart_aliprobe"
jobCheckNetServerAndStart = "tasklist | findstr netserver ||  restart_aliprobe"
'''
submitSTAFjob(host,service,job1)
time.sleep(5)
pps= submitSTAFjob(host,service,job2)
time.sleep(10)
netperf=submitSTAFjob(host,service,job3)

result = pps + '\n' + str(netperf)

pprint.pprint(result)
samplesNum = 0
totalPPs = 0
for line in result.split('\r\n'):
    match = re.search('\"[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{1,5}',line)
    if match:
        print line.split(',')[1:]
        samplesNum += 1
        for item in line.split(',')[1:]:
            totalPPs += float(item.strip('"'))
print samplesNum, totalPPs
print totalPPs/samplesNum
'''
preJob = "del out.txt && start /b netperf -H %s -l 40  -- -m 1 -D > out.txt 2>&1 " % '10.0.0.5' +\
    " && typeperf \"\\Network Interface(*)\\Packets Sent/sec\" -si 2 -sc 18 -y"
job = "typeperf \"\\Network Interface(*)\\Packets Sent/sec\" -si 2 -sc 18 -y "
afterJob = "type out.txt"
newJob="netperf -H 138.91.159.43 -l 30"
restartNetperf="restart_aliprobe"
#print submitSTAFjob(host,service,jobCheckStaf)
#print submitSTAFjob(host,service,job1)
#submitSTAFjob(host,service,preJob)

time.sleep(2)

#submitSTAFjob(host,service,preJob)
#submitSTAFjob(host,service,afterJob)
submitSTAFjob(host,service,newJob)
