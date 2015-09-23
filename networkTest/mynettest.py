__author__ = 'ziguang'

from scheduleJobsStaf import *

if __name__ == "__main__":
    logger.info('starting test ')
    cloudInfo = "region_ipnew"
    infos = parseCloudhostInfo(cloudInfo)
    detectAgent(infos)