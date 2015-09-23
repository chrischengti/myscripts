__author__ = 'ziguang'

from scheduleJobsStaf import *
import argparse

if __name__ == "__main__":

        parser = argparse.ArgumentParser()
        help_tMessage= "the type of link test to perform, below typse are supported %s" % str(allTestType)
        parser.add_argument("-t", type=str, help=help_tMessage )
        parser.add_argument("-f", type=str, help="folder to save log file")
        parser.add_argument("-c", type=str, help="the cloud info file")
        args = parser.parse_args()
        print args
        logger.info(str(args))
        testBothInAndOutRegion(args.c,args.t,args.f)

