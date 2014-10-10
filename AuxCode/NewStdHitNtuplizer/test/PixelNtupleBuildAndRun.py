#!/usr/bin/env python

import datetime,time
import os,sys
import string, re
import subprocess
import ConfigParser
from optparse import OptionParser

##### method to parse the input file ################################

def ConfigSectionMap(config, section):
    the_dict = {}
    options = config.options(section)
    for option in options:
        try:
            the_dict[option] = config.get(section, option)
            if the_dict[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            the_dict[option] = None
    return the_dict

###### method to define global variable instead of export #############

def set_global_var():
    global USER
    global HOME
    global LSF_DIR
    global LOG_DIR
    
    global SCRAM_ARCH
    global CMSSW_VER
    global LAUNCH_BASE

    USER = os.environ.get('USER')
    HOME = os.environ.get('HOME')
    LAUNCH_BASE = os.environ.get('CMSSW_BASE')
    LSF_DIR = os.path.join(os.getcwd(),"LSF")
    LOG_DIR = os.path.join(os.getcwd(),"log")
    SCRAM_ARCH = "slc6_amd64_gcc472"
    CMSSW_VER="CMSSW_5_3_21"
    
###### method to create recursively directories on EOS  #############
    
def mkdir_eos(out_path):
    newpath='/'
    for dir in out_path.split('/'):
        newpath=os.path.join(newpath,dir)
        # do not issue mkdir from very top of the tree
        if newpath.find('SLHCSimPhase2') > 0:
            p = subprocess.Popen(["cmsMkdir",newpath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out, err) = p.communicate()
            p.wait()

    # now check that the directory exists
    p = subprocess.Popen(["cmsLs",out_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    p.wait()
    if p.returncode !=0:
        print out

###########################################################################
class Job:
    """Main class to create and submit LSF jobs"""
###########################################################################

    def __init__(self, job_id, maxevents, myseed, islocal, queue, task_name):
############################################################################################################################
        
        # store the job-ID (since it is created in a for loop)
        self.job_id=job_id
        self.task_name=task_name
        self.queue=queue

        # max event used in this job
        self.maxevents=maxevents

        ## FIXME: always check that these are specified
        
        # parameters of the pixel digitizer 
        self.myseed=myseed
        self.islocal=islocal
        self.launch_dir=LAUNCH_BASE

        self.out_dir=os.path.join("/store/caf/user",USER,"SLHCSimPhase2/out53X","53X_phase0")

        if(self.job_id==1):
            mkdir_eos(self.out_dir)

        self.job_basename  = self.task_name + "_pixelCPE_53X_phase0_seed" +str(self.myseed)
        self.task_basename  = self.task_name + "_pixelCPE_53X_phase0"

        self.cfg_dir=None
        self.outputPSetName=None

        # LSF variables        
        self.output_LSF_name=None

###############################
    def createTheLSFFile(self):
###############################

        # directory to store the LSF to be submitted
        self.lsf_dir = LSF_DIR
        if not os.path.exists(self.lsf_dir):
            os.makedirs(self.lsf_dir)

        jobs_dir = os.path.join(LSF_DIR,"jobs")
        if not os.path.exists(jobs_dir):
            os.makedirs(jobs_dir)

        self.output_LSF_name=self.job_basename+".lsf"
        fout=open(os.path.join(self.lsf_dir,'jobs',self.output_LSF_name),'w')
    
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        fout.write("#!/bin/sh \n") 

        fout.write("#BSUB -L /bin/sh \n")       
        fout.write("#BSUB -J "+self.job_basename+"\n")
        fout.write("#BSUB -oo "+os.path.join(LOG_DIR,self.job_basename)+".log \n") # LXBATCH
        fout.write("#BSUB -q "+self.queue+" \n")                                   # LXBATCH
        fout.write("### Auto-Generated Script by LoopCMSSWBuildAndRun.py ### \n")
        fout.write("JobName="+self.job_basename+" \n")
        fout.write("OUT_DIR="+self.out_dir+" \n")
        fout.write("islocal="+str(self.islocal)+" \n")
        fout.write("maxevents="+str(self.maxevents)+" \n")
        fout.write("myseed="+str(self.myseed)+" \n")
        
        fout.write("if [ ! \"$LSB_JOBID\" = \"\" ]; then \n")
        fout.write("echo \"I AM IN BATCH\" \n")
        fout.write("export HOME=$WORKDIR \n") # LXBATCH
        fout.write("cd \n")
        fout.write("fi \n")
                   
        fout.write("export SCRAM_ARCH=slc6_amd64_gcc472 \n")
        fout.write("# Setup variables   \n")
                                      
        fout.write("cmssw_ver="+CMSSW_VER+" \n")
        fout.write("# Install and Compile CMSSW on batch node  \n")
        fout.write("scram p CMSSW $cmssw_ver  \n")
        fout.write("cd ${cmssw_ver}/src \n")
        fout.write("eval `scram r -sh` \n")

        if(self.islocal):
            fout.write("echo \"I AM IN LOCAL MODE\" \n")
            fout.write("export PKG_DIR="+self.launch_dir+"/src/AuxCode/NewStdHitNtuplizer/test \n")
        else:
            fout.write("echo \"I AM NOT IN LOCAL MODE\" \n")
            fout.write("export PKG_DIR=${CMSSW_BASE}/src/AuxCode/NewStdHitNtuplizer/test \n")

        # implement in the LSF script E.Brownson's recipe for changing the size of the pixels / part #1
        fout.write("# Eric Brownson's recipe to change the size of the pixels \n")
        fout.write("### 1: checkout CMSSW patches \n")

        fout.write("if [ ! \"$LSB_JOBID\" = \"\" ]; then \n")

        fout.write("cd \n")
        fout.write("# git config needed to avoid \n")
        fout.write("# error: SSL certificate problem: unable to get local issuer certificate while accessing \n")
        fout.write("ln -fs "+os.path.join(HOME,".gitconfig")+ " .\n")        
        fout.write("# since /cmshome/emiglior is mounted on the batch node \n")
        fout.write("eval `ssh-agent -s` \n")
        fout.write("ssh-add "+os.path.join(HOME,".ssh","id_rsa")+"\n")
        fout.write("# checkpoint: test that ssh connection is ok \n")
        fout.write("ssh -T git@github.com \n")
        fout.write("cd $HOME/${cmssw_ver}/src  \n")
        fout.write("fi \n")
    
        fout.write("git clone -b 53X_phase0 git://github.com/emiglior/usercode.git \n")
        fout.write("mv usercode/AuxCode .\n")
        fout.write("rm -fr usercode \n")
   
        fout.write("# compile \n")
        fout.write("scram b -j 8 \n")
        fout.write("eval `scram r -sh` \n")
        
        fout.write("# Run CMSSW for GEN-NTUPLE steps \n")
        fout.write("cd "+os.path.join("AuxCode","NewStdHitNtuplizer","test")+"\n")  
        fout.write("cmsRun ${PKG_DIR}/test_PixelCPE_NTUPLE.py maxEvents=${maxevents} MySeed=${myseed} \n")
        fout.write("ls -lh . \n")
        fout.write("cmsStage -f ${PKG_DIR}/test_PixelCPE_NTUPLE.py ${OUT_DIR}/test_PixelCPE_NTUPLE.py \n")
      
        fout.write(" # retrieve the outputs \n")
        fout.write("for RootOutputFile in $(ls *root ); do cmsStage -f  ${RootOutputFile}  ${OUT_DIR}/${RootOutputFile} ; done \n")
        fout.close()

############################################
    def submit(self):
############################################
        os.system("chmod u+x " + os.path.join(self.lsf_dir,'jobs',self.output_LSF_name))
        os.system("bsub < "+os.path.join(self.lsf_dir,'jobs',self.output_LSF_name)) #LXBATCH

#################
def main():            
### MAIN LOOP ###

    desc="""This is a description of %prog."""
    parser = OptionParser(description=desc,version='%prog version 0.1')
    parser.add_option('-s','--submit',  help='job submitted', dest='submit', action='store_true', default=False)
    parser.add_option('-q','--queue',help='lxbatch queue for submission', dest='queue',action='store',default='cmscaf1nd')
    parser.add_option('-l','--local', help='reads local branch',dest='localmode',action='store_true', default=False)
    parser.add_option('-n','--numberofevents', help='number of events', dest='numberofevents', action='store', default='1')
    parser.add_option('-N','--jobsInTask', help='number of jobs in this task', dest='jobsInTask', action='store',default='500')  
    parser.add_option('-j','--jobname', help='task name', dest='jobname', action='store', default='myjob')   

    parser.add_option('-i','--input',help='set input configuration (overrides default)',dest='inputconfig',action='store',default=None)
    (opts, args) = parser.parse_args()

    # initialize needed input 
    mQueue      = None
    mJobsInTask = None
 
    ConfigFile = opts.inputconfig
    
    if ConfigFile is not None:

        print "********************************************************"
        print "*         Parsing from input file:", ConfigFile,"    "
        
        config = ConfigParser.ConfigParser()
        config.read(ConfigFile)
         
        mNOfEvents  = ConfigSectionMap(config,"JobConfiguration")['numberofevents']
        mJobsInTask = ConfigSectionMap(config,"JobConfiguration")['numberofjobs']
        mQueue      = ConfigSectionMap(config,"JobConfiguration")['queue']
    else :

        print "********************************************************"
        print "*             Parsing from command line                *"
        print "********************************************************"
 
        mNOfEvents = opts.numberofevents
        mJobsInTask= opts.jobsInTask
        mQueue      = opts.queue
     
# check that chosen pixel size matches what is currently available in the trackerStructureTopology
# https://twiki.cern.ch/twiki/bin/view/CMS/ExamplePhaseI#Changing_the_Pixel_Size
   

    # Set global variables
    set_global_var()
 
    print "********************************************************"
    print "*                 Configuration info                   *"
    print "********************************************************"
    print "  Launching this script from : ",os.getcwd()
    print "- submitted                  : ",opts.submit
    print "- isLocal version            : ",opts.localmode
    print "- Jobs in Task               : ",mJobsInTask
    print "- Jobname                    : ",opts.jobname
    print "- Events/Job                 : ",mNOfEvents
    print "- Total events to run        : ",int(mNOfEvents)*int(mJobsInTask)     

    nEvents=int(mNOfEvents)
    
    jobIndex=0

    for theseed in range(1,int(mJobsInTask)+1):

        ajob=Job(theseed, nEvents, theseed, opts.localmode, mQueue, opts.jobname)
        ajob.createTheLSFFile()        

        out_dir = ajob.out_dir # save for later usage
    
        if opts.submit:
            ajob.submit()
            del ajob

        jobIndex+=1       
            
        
    #############################################
    # link the output folder
    #############################################
    
    link_name="53Xjobs"
    linkthedir="ln -fs "+out_dir+" "+os.path.join(LOG_DIR,link_name)     
    os.system(linkthedir)    

    print "- Output will be saved in   :",out_dir
    print "********************************************************"

    #############################################
    # prepare the script for the harvesting step
    #############################################

    harvestingname = LSF_DIR + "/jobs/PixelCPENtuple_"+opts.jobname+".sh"
    fout=open(harvestingname,"w")

    fout.write("#!/bin/bash \n")
    fout.write("OUT_DIR="+out_dir+" \n")
    fout.write("cd "+os.path.join(LAUNCH_BASE,"src","AuxCode","SLHCSimPhase2","test")+"\n")
    fout.write("eval `scram r -sh` \n")
    fout.write("mkdir -p /tmp/$USER/"+link_name+" \n")
    fout.write("for inputfile in `cmsLs "+out_dir+" |grep seed | grep root`; do \n")
    fout.write("   namebase=`echo $inputfile |awk '{split($0,b,\"/\"); print b[15]}'` \n")
    fout.write("   cmsStage -f $OUT_DIR/$namebase /tmp/$USER/"+link_name+" \n")
    fout.write("# Uncomment next line to clean up EOS space \n")
    fout.write("#  cmsRm $OUT_DIR/$namebase \n")
    fout.write("done \n")
    fout.write("cd /tmp/$USER/"+link_name+" \n")
    fout.write("hadd /tmp/$USER/stdgrechitfullph1g_ntuple_"+link_name+".root /tmp/$USER/"+link_name+"/stdgrechitfullph1g_ntuple_*.root \n")
    fout.write("cmsStage -f /tmp/$USER/stdgrechitfullph1g_ntuple_"+link_name+".root $OUT_DIR \n")
    os.system("chmod u+x "+harvestingname)
    
if __name__ == "__main__":        
    main()

    


