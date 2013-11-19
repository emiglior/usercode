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

    USER = os.environ.get('USER')
    HOME = os.environ.get('HOME')
    PBS_DIR = os.getcwd()+os.path.join("/PBS") 
    LOG_DIR = os.getcwd()+os.path.join("/log")
    SCRAM_ARCH = "slc5_amd64_gcc472"
    CMSSW_VER="CMSSW_6_1_2_SLHC8_patch3"
        
###########################################################################
class Job:
    """Main class to create and submit PBS jobs"""
###########################################################################

    def __init__(self, job_id, maxevents, ageing, pixelrocrows, pixelroccols, bpixthr, bpixl0thickness):
############################################################################################################################
        
        # store the job-ID (since it is created in a for loop)
        self.job_id=job_id
        
        # max event used in this job
        self.maxevents=maxevents

        ## FIXME: always check that these are specified
        
        # parameters of the pixel digitizer 
        self.pixelrocrows=pixelrocrows
        self.pixelroccols=pixelroccols
        self.bpixl0thickness=bpixl0thickness
        
        self.bpixthr=bpixthr
        self.ageing=ageing
        
        self.out_dir=os.path.join("/lustre/cms/store/user",USER,"SLHCSimPhase2/out","PixelROCRows_" +pixelrocrows+"_PixelROCCols_"+pixelroccols,"L0Thick_"+self.bpixl0thickness,"BPixThr_"+bpixthr)
        os.system("mkdir -p "+self.out_dir)

        self.job_basename= 'pixelCPE_age' + self.ageing + '_PixelROCRows' + self.pixelrocrows + "_PixelROCCols" + self.pixelroccols +"_L0Thick" + self.bpixl0thickness + "_BPixThr" + self.bpixthr
        
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
        fout.write("#PBS -S /bin/sh\n")       
        fout.write("#PBS -N "+self.job_basename+"\n")
        fout.write("#PBS -j oe \n")
        fout.write("#PBS -o "+os.path.join(LOG_DIR,self.job_basename)+".log"+"\n")
        fout.write("#PBS -q local \n")
        fout.write("### Auto-Generated Script by LoopCMSSWBuildAndRunFromTarBall.py ### \n")
        fout.write("JobName="+self.job_basename+" \n")
        fout.write("OUT_DIR="+self.out_dir+" \n")
        fout.write("maxevents="+str(self.maxevents)+" \n")
        fout.write("pixelroccols="+self.pixelroccols+" \n")
        fout.write("pixelrocrows="+self.pixelrocrows+" \n")
        fout.write("ageing="+self.ageing+" \n")
        fout.write("bpixthr="+self.bpixthr+" \n")
        
        # specific for cmssusy.ba.infn.it
        # https://www.ba.infn.it/pagine-utenti.html?task=viewpage&user_id=111&pageid=96
        fout.write("if [ \"$PBS_ENVIRONMENT\" == \"PBS_BATCH\" ]; then \n")
        fout.write("echo \"I AM IN BATCH\" \n")
        fout.write("mkdir -p /home/tmp/$USER/$PBS_JOBID \n")
        fout.write("export HOME=/home/tmp/$USER/$PBS_JOBID \n")
        fout.write("cd \n")
        fout.write("export PBS_O_WORKDIR=$HOME \n")
        fout.write("fi \n")
        fout.write("export SCRAM_ARCH=slc5_amd64_gcc472 \n")
        fout.write("# Save current dir on batch machine  \n")
        fout.write("BATCH_DIR=`pwd` \n")
        fout.write("echo '$HOSTNAME is '$HOSTNAME \n")
        fout.write("echo '$BATCH_DIR is '$BATCH_DIR\n")
        fout.write("echo '$PBS_ENVIRONMENT is ' $PBS_ENVIRONMENT \n")
        fout.write("# Setup variables   \n")
        fout.write("VO_CMS_SW_DIR=/cvmfs/cms.cern.ch \n")
        fout.write("source $VO_CMS_SW_DIR/cmsset_default.sh \n")
        fout.write("cmssw_ver="+CMSSW_VER+" \n")
        fout.write("# Install and Compile CMSSW on batch node  \n")

        # ugly alternative for SLC6
        fout.write("# start here ugly recipe for SLC6 since git doesn't work after scram \n")
        fout.write("cp -pr /lustre/cms/store/user/musich/612SLHC8_fromRecipe.tgz . \n")
        fout.write("tar xf 612SLHC8_fromRecipe.tgz \n")
        fout.write("cd ${cmssw_ver}/src \n")
        fout.write("scramv1 b ProjectRename \n")        

#         fout.write("scram p CMSSW $cmssw_ver  \n")
#         fout.write("cd ${cmssw_ver}/src \n")
#         fout.write("eval `scram r -sh` \n")

#         # implement in the PBS script E.Brownson's recipe for changing the size of the pixels / part #1
#         fout.write("# Eric Brownson's recipe to change the size of the pixels \n")
#         fout.write("### 1: checkout CMSSW patches \n")
#         fout.write("if [ \"$PBS_ENVIRONMENT\" == \"PBS_BATCH\" ]; then \n")
#         fout.write("cd $HOME \n")
#         fout.write("# git config needed to avoid \n")
#         fout.write("# error: SSL certificate problem: unable to get local issuer certificate while accessing \n")
#         fout.write("ln -fs "+os.path.join(HOME,".gitconfig")+ " .\n")        
#         fout.write("# since /cmshome/emiglior is mounted on the batch node \n")
#         fout.write("eval `ssh-agent -s` \n")
#         fout.write("ssh-add "+os.path.join(HOME,".ssh","id_rsa")+"\n")
#         fout.write("# checkpoint: test that ssh connection is ok \n")
#         fout.write("ssh -T git@github.com \n")
#         fout.write("git clone https://github.com/fwyzard/cms-git-tools \n")
#         fout.write("ls -l ${PWD}/cms-git-tools \n")
#         fout.write("PATH=$PATH:${PWD}/cms-git-tools\n")
#         fout.write("git cms-init -y --ssh \n")
#         fout.write("echo \"List the content of HOME\" \n")
#         fout.write("ls -la $HOME \n")
#         fout.write("cd $HOME/${cmssw_ver}/src  \n")
#         fout.write("fi \n")
#         fout.write("git cms-addpkg CalibTracker/SiPixelESProducers \n")
#         fout.write("git cms-addpkg CondFormats/SiPixelObjects \n")
#         fout.write("git cms-addpkg CondTools/SiPixel \n")
#         fout.write("git cms-addpkg Geometry/TrackerCommonData \n")
#         fout.write("git cms-addpkg SLHCUpgradeSimulations/Geometry \n")
#         fout.write("git cms-addpkg SLHCUpgradeSimulations/Configuration \n")
#         fout.write("echo \"After git cms-addpkg\" \n")
#         fout.write("pwd \n")
#         fout.write("ls -l . \n")
#         fout.write("git pull https://github.com/brownsonian/cmssw SmallPitch_on612 \n")
#         fout.write("### 1 ended  \n")
        
#         fout.write("git clone -b 612_slhc8 git://github.com/emiglior/usercode.git \n")
#         fout.write("mv usercode/AuxCode .\n")
#         fout.write("rm -fr usercode \n")
#         fout.write("git cms-checkdeps -a \n")

        fout.write("# compile \n")
        fout.write("scram b -j 8 \n")
        fout.write("eval `scram r -sh` \n")

        # implement in the PBS script E.Brownson's recipe for changing the size of the pixels / part #2
        fout.write("# Eric Brownson's recipe to change the size of the pixels \n")
        fout.write("### 2: modify the topology \n")
        fout.write("# trackerStructureTopology_template_L0.xml   -> L0    BPIX is changed \n")
        fout.write("sed -e \"s%PIXELROCROWS%"+self.pixelrocrows+"%g\" -e \"s%PIXELROCCOLS%"+self.pixelroccols+"%g\" AuxCode/SLHCSimPhase2/test/trackerStructureTopology_template_L0.xml > Geometry/TrackerCommonData/data/PhaseII/BarrelEndcap/trackerStructureTopology.xml \n")
        fout.write("# Run CMSSW to complete the recipe for changing the size of the pixels \n")
        fout.write("cmsRun SLHCUpgradeSimulations/Geometry/test/writeFile_phase2BE_cfg.py \n")
        fout.write("mv PixelSkimmedGeometry_phase2BE.txt ${CMSSW_BASE}/src/SLHCUpgradeSimulations/Geometry/data/PhaseII/BarrelEndcap/PixelSkimmedGeometry.txt \n")        
        fout.write("### 2 ended  \n")

        # implement the recipe for changing the bpix sensor thickness from A. Tricomi
        fout.write("# A Tricomi's recipe to change the sensors thickness \n")
        fout.write("sed -e \"s%BPIXLAYER0THICKNESS%"+self.bpixl0thickness+"%g\" AuxCode/SLHCSimPhase2/test/pixbarladderfull0_template.xml > Geometry/TrackerCommonData/data/PhaseI/pixbarladderfull0.xml \n")
        
        fout.write("# Run CMSSW for GEN-NTUPLE steps \n")
        fout.write("cd "+os.path.join("AuxCode","SLHCSimPhase2","test")+"\n")  
        fout.write("cmsRun TenMuE_0_200_cff_py_GEN_TO_RECO_TO_PixelCPE_NTUPLE.py maxEvents=${maxevents} BPixThr=${bpixthr} AgeingScenario=${ageing} \n")
        fout.write("ls -lh . \n")
        fout.write("cd Brownson \n")
        fout.write("make \n")
        fout.write("ln -fs ../stdgrechitfullph1g_ntuple.root . \n")
        fout.write("./res \n")        
        fout.write(" # retrieve the outputs \n")
        fout.write("for RootOutputFile in $(ls *root ); do rfcp  ${RootOutputFile}  ${OUT_DIR}/${RootOutputFile} ; done \n")
        fout.write("for EpsOutputFile in $(ls *eps ); do rfcp  ${EpsOutputFile}  ${OUT_DIR}/${EpsOutputFile} ; done \n")
        fout.write("rfcp TenMuE_0_200_cff_py_GEN_TO_RECO_TO_PixelCPE_NTUPLE.py ${OUT_DIR} \n")
        fout.close()

############################################
    def submit(self):
############################################
        os.system("chmod u+x " + os.path.join(self.pbs_dir,'jobs',self.output_PBS_name))
        os.system("qsub < "+os.path.join(self.pbs_dir,'jobs',self.output_PBS_name))

#################
def main():            
### MAIN LOOP ###

    desc="""This is a description of %prog."""
    parser = OptionParser(description=desc,version='%prog version 0.1')
    parser.add_option('-s','--submit',  help='job submitted', dest='submit', action='store_true', default=False)
    parser.add_option('-n','--numberofevents',    help='number of events', dest='numberofevents', action='store',  default=1)
    parser.add_option('-j','--jobname', help='task name', dest='jobname', action='store', default='myjob')
    parser.add_option('-r','--ROCRows',help='ROC Rows (default 80 -> du=100 um)', dest='rocrows', action='store', default='80')
    parser.add_option('-c','--ROCCols',help='ROC Cols (default 52 -> dv=150 um)', dest='roccols', action='store', default='52')
    parser.add_option('-t','--Layer0Thick',help='BPix L0 sensor thickness', dest='layer0thick', action='store', default='285')
    parser.add_option('-T','--BPixThr',help='BPix Threshold', dest='bpixthr', action='store', default='2000')
    parser.add_option('-a','--ageing',help='set ageing',dest='ageing',action='store',default='NoAgeing')
    parser.add_option('-i','--input',help='set input configuration (overrides default)',dest='inputconfig',action='store',default=None)
    (opts, args) = parser.parse_args()

    # initialize needed input 
    mRocRows = None
    mRocCols = None
    mBPixthr = None
    mL0Thick = None
    mAgeing  = None

    ConfigFile = opts.inputconfig
    
    if ConfigFile is not None:

        print "********************************************************"
        print "*         Parsing from input file:", ConfigFile,"    "
        
        config = ConfigParser.ConfigParser()
        config.read(ConfigFile)
        
        mRocRows   = ConfigSectionMap(config,"PixelConfiguration")['rocrows']   
        mRocCols   = ConfigSectionMap(config,"PixelConfiguration")['roccols']   
        mL0Thick   = ConfigSectionMap(config,"PixelConfiguration")['layer0thickness']
        mBPixThr   = ConfigSectionMap(config,"PixelConfiguration")['bpixthr']   
        mAgeing    = ConfigSectionMap(config,"PixelConfiguration")['ageing']    
        mNOfEvents = ConfigSectionMap(config,"JobConfiguration")['numberofevents']

    else :

        print "********************************************************"
        print "*             Parsing from command line                *"
        print "********************************************************"
        
        mRocRows   = opts.rocrows
        mRocCols   = opts.roccols
        mL0Thick   = opts.layer0thick
        mBPixThr   = opts.bpixthr
        mAgeing    = opts.ageing
        mNOfEvents = opts.numberofevents


# check that chosen pixel size matches what is currently available in the trackerStructureTopology
# https://twiki.cern.ch/twiki/bin/view/CMS/ExamplePhaseI#Changing_the_Pixel_Size
    if int(mRocRows) % 80:
        print 'illegal value for PixelROCRows' 
    exit

    if int(mRocCols) % 52:
        print "illegal value for PixelROCCols"
    exit

    # Set global variables
    set_global_var()
 
    print "********************************************************"
    print "*                 Configuration info                   *"
    print "********************************************************"
    print "  Launching this script from : ",os.getcwd()
    print "- submitted                  : ",opts.submit
    print "- Jobname                    : ",opts.jobname
    print "- ROCRows                    : ",mRocRows
    print "- ROCCols                    : ",mRocCols
    print "- L0 Thickness               : ",mL0Thick
    print "- Clusterizer Threshold      : ",mBPixThr
    print "- Ageing Scenario            : ",mAgeing
    print "- Total events to run        : ",mNOfEvents     

    nEvents=int(mNOfEvents)
    
    jobIndex=0

    ajob=Job(opts.jobname, nEvents, mAgeing, mRocRows, mRocCols, mBPixThr, mL0Thick)
    ajob.createThePBSFile()        

    out_dir = ajob.out_dir # save for later usage
    
    if opts.submit:
        ajob.submit()
        del ajob
            
        
    #############################################
    # link the output folder
    #############################################
    
    link_name="PixelROCRows_"+mRocRows+"_PixelROCCols_"+mRocCols+"_L0Thick"+mL0Thick+"_BPixThr_"+mBPixThr
    linkthedir="ln -fs "+out_dir+" "+os.path.join(LOG_DIR,link_name)     
    os.system(linkthedir)    

    print "- Output will be saved in   :",out_dir
    print "********************************************************"

if __name__ == "__main__":        
    main()

    


