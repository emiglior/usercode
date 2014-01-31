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
    global PBS_DIR
    global LOG_DIR
    
    global SCRAM_ARCH
    global CMSSW_VER
    global LAUNCH_BASE

    USER = os.environ.get('USER')
    HOME = os.environ.get('HOME')
    LAUNCH_BASE = os.environ.get('CMSSW_BASE')
    PBS_DIR = os.path.join(os.getcwd(),"PBS")
    LOG_DIR = os.path.join(os.getcwd(),"log")
    SCRAM_ARCH = "slc5_amd64_gcc472"
    CMSSW_VER="CMSSW_5_3_3"
    
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
    """Main class to create and submit PBS jobs"""
###########################################################################

    def __init__(self, job_id, maxevents, bpixthr, myseed, islocal):
############################################################################################################################
        
        # store the job-ID (since it is created in a for loop)
        self.job_id=job_id
        
        # max event used in this job
        self.maxevents=maxevents

        ## FIXME: always check that these are specified
        
        # parameters of the pixel digitizer 
        self.bpixthr=bpixthr
        self.myseed=myseed
        self.islocal=islocal
        self.launch_dir=LAUNCH_BASE

        self.out_dir=os.path.join("/store/caf/user",USER,"SLHCSimPhase2/out","BPixThr_"+bpixthr)

        if(self.job_id==1):
            mkdir_eos(self.out_dir)

        self.job_basename= 'pixelCPE_BPixThr' + self.bpixthr +"_seed" +str(self.myseed)
        
        self.cfg_dir=None
        self.outputPSetName=None

# PBS variables        
        self.output_PBS_name=None

###############################
    def createThePBSFile(self):
###############################

# directory to store the PBS to be submitted
        self.pbs_dir = PBS_DIR
        if not os.path.exists(self.pbs_dir):
            os.makedirs(self.pbs_dir)

        jobs_dir = os.path.join(PBS_DIR,"jobs")
        if not os.path.exists(jobs_dir):
            os.makedirs(jobs_dir)

        self.output_PBS_name=self.job_basename+".pbs"
        fout=open(os.path.join(self.pbs_dir,'jobs',self.output_PBS_name),'w')
    
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        fout.write("#!/bin/sh \n") 

        fout.write("#BSUB -L /bin/sh \n")       
        fout.write("#BSUB -J "+self.job_basename+"\n")
        fout.write("#BSUB -oo "+os.path.join(LOG_DIR,self.job_basename)+".log \n") # LXBATCH
        fout.write("#BSUB -q cmscaf1nd \n")                                        # LXBATCH      
        fout.write("### Auto-Generated Script by LoopCMSSWBuildAndRun.py ### \n")
        fout.write("JobName="+self.job_basename+" \n")
        fout.write("OUT_DIR="+self.out_dir+" \n")
        fout.write("islocal="+str(self.islocal)+" \n")

        if(self.islocal):
            fout.write("echo \"I AM IN LOCAL MODE\" \n")
            fout.write("export PKG_DIR="+self.launch_dir+"/src/AuxCode/NewStdHitNtuplizer/test \n")
        else:
            fout.write("echo \"I AM NOT IN LOCAL MODE\" \n")
            fout.write("export PKG_DIR=AuxCode/NewStdHitNtuplizer/test \n")

        fout.write("maxevents="+str(self.maxevents)+" \n")
        fout.write("bpixthr="+self.bpixthr+" \n")
        fout.write("myseed="+str(self.myseed)+" \n")
        
        fout.write("if [ ! \"$LSB_JOBID\" = \"\" ]; then \n")
        fout.write("echo \"I AM IN BATCH\" \n")
        fout.write("export HOME=$WORKDIR \n") # LXBATCH
        fout.write("cd \n")
        fout.write("fi \n")
                   
        fout.write("export SCRAM_ARCH=slc5_amd64_gcc472 \n")
        fout.write("# Setup variables   \n")
                                      
        fout.write("cmssw_ver="+CMSSW_VER+" \n")
        fout.write("# Install and Compile CMSSW on batch node  \n")
        fout.write("scram p CMSSW $cmssw_ver  \n")
        fout.write("cd ${cmssw_ver}/src \n")
        fout.write("eval `scram r -sh` \n")

         # implement in the PBS script E.Brownson's recipe for changing the size of the pixels / part #1
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
        fout.write("git clone https://github.com/fwyzard/cms-git-tools \n")
        fout.write("PATH=$PWD/cms-git-tools:$PATH \n")
        fout.write("git cms-init -y --ssh \n")
        fout.write("cd $HOME/${cmssw_ver}/src  \n")
        fout.write("fi \n")
    
        fout.write("git clone -b 53X_phase0 git://github.com/emiglior/usercode.git \n")
        fout.write("mv usercode/AuxCode .\n")
        fout.write("rm -fr usercode \n")
   
        fout.write("# compile \n")
        fout.write("scram b -j 8 \n")
        fout.write("eval `scram r -sh` \n")
        
        fout.write("# Run CMSSW for GEN-NTUPLE steps \n")
        fout.write("cd "+os.path.join("AuxCode","NewStdHitNtuplize","test")+"\n")  
        fout.write("cmsRun ${PKG_DIR}/test_PixelCPE_NTUPLE.py maxEvents=${maxevents} BPixThr=${bpixthr} MySeed=${myseed} \n")
        fout.write("ls -lh . \n")
        fout.write("cmsStage -f ${PKG_DIR}/test_PixelCPE_NTUPLE.py ${OUT_DIR}/test_PixelCPE_NTUPLE.py \n")
      
        fout.write(" # retrieve the outputs \n")
        fout.write("for RootOutputFile in $(ls *root ); do cmsStage -f  ${RootOutputFile}  ${OUT_DIR}/${RootOutputFile} ; done \n")
        fout.close()

############################################
    def submit(self):
############################################
        os.system("chmod u+x " + os.path.join(self.pbs_dir,'jobs',self.output_PBS_name))
        os.system("bsub < "+os.path.join(self.pbs_dir,'jobs',self.output_PBS_name)) #LXBATCH

#################
def main():            
### MAIN LOOP ###

    desc="""This is a description of %prog."""
    parser = OptionParser(description=desc,version='%prog version 0.1')
    parser.add_option('-s','--submit',  help='job submitted', dest='submit', action='store_true', default=False)
    parser.add_option('-l','--local', help='reads local branch',dest='localmode',action='store_true', default=False)
    parser.add_option('-n','--numberofevents', help='number of events', dest='numberofevents', action='store', default='1')
    parser.add_option('-N','--jobsInTask', help='number of jobs in this task', dest='jobsInTask', action='store',default='500')  
    parser.add_option('-j','--jobname', help='task name', dest='jobname', action='store', default='myjob')
    parser.add_option('-T','--BPixThr',help='BPix Threshold', dest='bpixthr', action='store', default='3500')
 
    parser.add_option('-i','--input',help='set input configuration (overrides default)',dest='inputconfig',action='store',default=None)
    (opts, args) = parser.parse_args()

    # initialize needed input 
   
    mBPixthr = None
    mJobsInTask=None
 
    ConfigFile = opts.inputconfig
    
    if ConfigFile is not None:

        print "********************************************************"
        print "*         Parsing from input file:", ConfigFile,"    "
        
        config = ConfigParser.ConfigParser()
        config.read(ConfigFile)
        
        mBPixThr   = ConfigSectionMap(config,"PixelConfiguration")['bpixthr']   
      
        mNOfEvents = ConfigSectionMap(config,"JobConfiguration")['numberofevents']
        mJobsInTask= opts.jobsInTask

    else :

        print "********************************************************"
        print "*             Parsing from command line                *"
        print "********************************************************"

        mBPixThr   = opts.bpixthr
     
        mNOfEvents = opts.numberofevents
        mJobsInTask= opts.jobsInTask
     
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
    print "- Clusterizer Threshold      : ",mBPixThr
    print "- Total events to run        : ",mNOfEvents     

    nEvents=int(mNOfEvents)
    
    jobIndex=0

    for theseed in range(1,int(mJobsInTask)+1):

        #ajob=Job(opts.jobname, nEvents, mAgeing, mRocRows, mRocCols, mBPixThr, mL0Thick,theseed)
        #ajob=Job(theseed, nEvents, mAgeing, mRocRows, mRocCols, mBPixThr, mL0Thick,theseed)
        ajob=Job(theseed, nEvents, mBPixThr, theseed, opts.localmode)
        ajob.createThePBSFile()        

        out_dir = ajob.out_dir # save for later usage
    
        if opts.submit:
            ajob.submit()
            del ajob

        jobIndex+=1       
            
        
    #############################################
    # link the output folder
    #############################################
    
    link_name="BPixThr_"+mBPixThr
    linkthedir="ln -fs "+out_dir+" "+os.path.join(LOG_DIR,link_name)     
    os.system(linkthedir)    

    print "- Output will be saved in   :",out_dir
    print "********************************************************"

    #############################################
    # prepare the script for the harvesting step
    #############################################

    harvestingname = PBS_DIR + "/jobs/PixelCPENtuple_"+opts.jobname+"_BPixThr"+mBPixThr+".csh"
    fout=open(harvestingname,"w")

    fout.write("#!/bin/tcsh \n")
    fout.write("OUT_DIR="+out_dir+" \n")
    fout.write("mkdir /tmp/$USER/"+link_name+" \n")
    fout.write("foreach inputfile (`cmsLs "+out_dir+"`) \n")
    fout.write("set namebase=`echo $inputfile |awk '{split($0,b,\"/\"); print b[11]}'` \n")
    fout.write("if (\"$namebase\" =~ *\"stdgrechitfullph1g\"*) then \n")
    fout.write("echo \"copying: $COUNT $myDir/$namebase\" \n") 
    fout.write("cmsStage $myDir/$namebase /tmp/$USER/"+link_name+" \n")
    fout.write("@ COUNT+=1 \n")
    fout.write("if ($COUNT == "+mJobsInTask+") then \n")
    fout.write("break \n")
    fout.write("endif \n")
    fout.write("endif \n") 
    fout.write("end \n")
    fout.write("echo \"copied $COUNT files\" \n")
    fout.write("cd /tmp/$USER/"+link_name+" \n")
    fout.write("hadd stdgrechitfullph1g_ntuple_"+link_name+"*.root \n")
    fout.write("cmsStage stdgrechitfullph1g_ntuple_"+link_name+"*.root /store/caf/user/$USER/SLHCSimPhase2/PixelNtuples \n")
    fout.write("cd "+os.path.join("${CMSSW_BASE}","src","AuxCode","SLHCSimPhase2","test","Brownson")+"\n") 
    fout.write("make \n")
    fout.write("ln -fs /tmp/$USER/"+link_name+"/stdgrechitfullph1g_ntuple_"+link_name+"*.root ./stdgrechitfullph1g_ntuple.root \n")
    fout.write("./res \n")
    #fout.write("for RootOutputFile in $(ls *pdf ); do cp  ${RootOutputFile}  ${OUT_DIR}/${RootOutputFile} ; done \n")
    fout.write("for EpsOutputFile in $(ls *eps ); do cp  ${EpsOutputFile}    ${OUT_DIR}/${EpsOutputFile} ; done \n")
      
if __name__ == "__main__":        
    main()

    


