#!/usr/bin/env python

import datetime,time
import os,sys
import string, re
import subprocess
# generic  python modules
from optparse import OptionParser

###### method to define global variable instead of export #############

def set_global_var(sample):
    global USER
    global HOME
    global PBS_DIR
    global LOG_DIR
    
    global SCRAM_ARCH
    global CMSSW_VER

    global GENSIM_FILE

    USER = os.environ.get('USER')
    HOME = os.environ.get('HOME')
    PBS_DIR = os.getcwd()+os.path.join("/PBS") 
    LOG_DIR = os.getcwd()+os.path.join("/log")
    SCRAM_ARCH = "slc5_amd64_gcc472"
    CMSSW_VER="CMSSW_6_1_2_SLHC8_patch3"
    
    if (sample=="TTbar") | (sample=="ttbar") | (sample=="TTBar") :
        GENSIM_FILE = "file:/lustre/cms/store/user/musich/SLHCSimPhase2/Samples/612_slhc8/RelVals/TTbar/2E905DB0-012F-E311-830A-0025905964C4.root"
    elif (sample=="MinBias") | (sample=="minbias") :
        GENSIM_FILE = "file:/lustre/cms/store/user/musich/SLHCSimPhase2/Samples/612_slhc8/RelVals/MinBias/D0C92216-F62E-E311-A76C-0026189437E8.root"
    elif (sample=="IsoMuons") | (sample=="muons") | (sample=="Muons") :
        GENSIM_FILE = "file:/lustre/cms/store/user/musich/SLHCSimPhase2/Samples/ParticleGun/step1_FourMuPartGun_100kEvents.root"
    else :
        print "unrecongnize input sample, using default (=TTbar)"
        GENSIM_FILE = "file:/lustre/cms/store/user/musich/SLHCSimPhase2/Samples/612_slhc8/RelVals/TTbar/2E905DB0-012F-E311-830A-0025905964C4.root"
    
###########################################################################
class Job:
    """Main class to create and submit PBS jobs"""
###########################################################################

    def __init__(self, job_id,firstevent,maxevents, sample, pu, ageing, pixelrocrows, pixelroccols, bpixthr):
############################################################################################################################
        
        # store the job-ID (since it is created in a for loop)
        self.job_id=job_id
        
        # first/max event used in this job
        self.firstevent=firstevent
        self.maxevents=maxevents

        ## FIXME: always check that these are specified
        self.sample=sample
        self.pu=pu
        
        # parameters of the pixel digitizer 
        self.pixelrocrows=pixelrocrows
        self.pixelroccols=pixelroccols
        self.bpixthr=bpixthr
        self.ageing=ageing
        
        self.out_dir=os.path.join("/lustre/cms/store/user",USER,"SLHCSimPhase2/out","sample_"+sample,"pu_"+pu,"PixelROCRows_" +pixelrocrows+"_PixelROCCols_"+pixelroccols,"BPixThr_"+bpixthr)
        os.system("mkdir -p "+self.out_dir)

        self.job_basename= 'step_digitodqm_' +self.sample+ '_pu' + self.pu + '_age' + self.ageing + '_' + str(self.firstevent)+ "_PixelROCRows" + self.pixelrocrows + "_PixelROCCols" + self.pixelroccols + "_BPixThr" + self.bpixthr
        
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
        fout.write("#PBS -o "+os.path.join(LOG_DIR,self.job_basename)+".out"+"\n")
        fout.write("#PBS -e "+os.path.join(LOG_DIR,self.job_basename)+".err"+"\n")
        fout.write("#PBS -q local \n")
        fout.write("#PBS -l mem=5gb \n")
        fout.write("### Auto-Generated Script by LoopCMSSWBuildAndRunFromTarBall.py ### \n")
        fout.write("JobName="+self.job_basename+" \n")
        fout.write("outfilename="+self.job_basename+".root"+" \n")
        fout.write("OUT_DIR="+self.out_dir+" \n")
        fout.write("firstevent="+str(self.firstevent)+" \n")
        fout.write("maxevents="+str(self.maxevents)+" \n")
        fout.write("pixelroccols="+self.pixelroccols+" \n")
        fout.write("pixelrocrows="+self.pixelrocrows+" \n")
        fout.write("puscenario="+self.pu+" \n")
        fout.write("ageing="+self.ageing+" \n")
        fout.write("bpixthr="+self.bpixthr+" \n")
        fout.write("inputgensimfilename="+GENSIM_FILE+" \n")
        
        # specific for cmssusy.ba.infn.it
        # https://www.ba.infn.it/pagine-utenti.html?task=viewpage&user_id=111&pageid=96
        fout.write("if [ \"$PBS_ENVIRONMENT\" == \"PBS_BATCH\" ]; then \n")
        fout.write("echo \"I AM IN BATCH\" \n")
        fout.write("mkdir -p /home/tmp/$USER/$PBS_JOBID \n")
        fout.write("export HOME=/home/tmp/$USER/$PBS_JOBID \n")
        fout.write("cd \n")
        fout.write("export PBS_O_WORKDIR=$HOME \n")
        fout.write("fi \n")
        fout.write("# Save current dir on batch machine  \n")
        fout.write("BATCH_DIR='pwd' \n")
        fout.write("echo '$HOSTNAME is '$HOSTNAME \n")
        fout.write("echo '$BATCH_DIR is '$BATCH_DIR\n")
        fout.write("echo '$CVSROOT is '$CVSROOT \n")
        fout.write("echo '$SCRAM_ARCH is '$SCRAM_ARCH \n")
        fout.write("echo '$PBS_ENVIRONMENT is ' $PBS_ENVIRONMENT \n")
        fout.write("# Setup variables   \n")
        fout.write("source /opt/exp_soft/cms/cmsset_default.sh \n")
        fout.write("export SCRAM_ARCH=slc5_amd64_gcc472 \n")
        fout.write("cmssw_ver="+CMSSW_VER+" \n")
        fout.write("# Install and Compile CMSSW on batch node  \n")
        fout.write("scram p CMSSW $cmssw_ver  \n")
        fout.write("cd ${cmssw_ver}/src \n")
        fout.write("eval `scram r -sh` \n")
        # fout.write("# this is needed to change the size of the pixels \n")
        # fout.write("# addpkg CalibTracker/SiPixelESProducers V50-00-02 \n")
        # fout.write("# addpkg CondFormats/SiPixelObjects V50-00-03 \n")
        # fout.write("# addpkg Geometry/TrackerCommonData \n")
        # fout.write("# addpkg SLHCUpgradeSimulations/Geometry \n")
        # fout.write("# checkdeps -a \n")
        # fout.write("# copy a templated version of trackerStructureTopology.xml and set the pixel size \n")
        # fout.write("# trackerStructureTopology_template_L0.xml   -> L0    BPIX is changed \n")
        # fout.write("# trackerStructureTopology_template_L1.xml   -> L1    BPIX is changed \n")
        # fout.write("# trackerStructureTopology_template_L0L1.xml -> L0+L1 BPIX is changed \n")
        # fout.write("# cp -v /cmshome/traverso/AuxFiles/trackerStructureTopology_template_L0.xml ${BATCH_DIR}/trackerStructureTopology_template.xml \n")
        # fout.write("#sed -e \"s%PIXELROCROWS%$PixelROCRows%g\" -e \"s%PIXELROCCOLS%$PixelROCCols%g\" ${BATCH_DIR}/trackerStructureTopology_template.xml > Geometry/TrackerCommonData/data/PhaseI/trackerStructureTopology.xml \n")
        # fout.write("# showtags -r \n")
        fout.write("git clone -b 612_slhc8 git://github.com/emiglior/usercode.git . \n")
        fout.write("scram b -j 8 \n")
        fout.write("# Run CMSSW to complete the recipe for changing the size of the pixels \n")
        fout.write("# cd SLHCUpgradeSimulations/Geometry/test \n")
        fout.write("# cmsRun writeFile_phase1_cfg.py \n")
        fout.write("# mv PixelSkimmedGeometry_phase1.txt ${CMSSW_BASE}/src/SLHCUpgradeSimulations/Geometry/data/PhaseI \n")
        fout.write("# Run CMSSW for DIGI-to-DQM steps \n")
        fout.write("cd "+os.path.join("AuxCode","SLHCSimPhase2","test")+"\n")  
        fout.write("cmsRun step_digitodqmvalidation_PUandAge.py maxEvents=${maxevents} firstEvent=${firstevent} BPixThr=${bpixthr} InputFileName=${inputgensimfilename} OutFileName=${outfilename} PUScenario=${puscenario} AgeingScenario=${ageing} \n")
        fout.write("ls -lh . \n")
        fout.write(" # retrieve the outputs \n")
        fout.write("for RootOutputFile in $(ls *root ); do rfcp  ${RootOutputFile}  ${OUT_DIR}/${RootOutputFile} ; done \n")
        fout.write("rfcp step_digitodqmvalidation_PUandAge.py ${OUT_DIR} \n")
        fout.write("# rfcp ${CMSSW_BASE}/src/SLHCUpgradeSimulations/Geometry/data/PhaseI/PixelSkimmedGeometry_phase1.txt ${OUT_DIR} \n")
        fout.write("# rfcp ${CMSSW_BASE}/src/Geometry/TrackerCommonData/data/PhaseI/trackerStructureTopology.xml ${OUT_DIR} \n")
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
    parser.add_option('-n','--numberofjobs',    help='number of splitted jobs', dest='numberofjobs', action='store',  default=1)
    parser.add_option('-j','--jobname', help='task name', dest='jobname', action='store', default='myjob')
    parser.add_option('-r','--ROCRows',help='ROC Rows (default 80 -> du=100 um)', dest='rocrows', action='store', default='80')
    parser.add_option('-c','--ROCCols',help='ROC Cols (default 52 -> dv=150 um)', dest='roccols', action='store', default='52')
    parser.add_option('-t','--BPixThr',help='BPix Threshold', dest='bpixthr', action='store', default='2000')
    parser.add_option('-p','--pileup',help='set pileup',dest='pu',action='store',default='NoPU')
    parser.add_option('-S','--sample',help='set sample name',dest='sample',action='store',default='TTbar')
    parser.add_option('-a','--ageing',help='set ageing',dest='ageing',action='store',default='NoAgeing')
    (opts, args) = parser.parse_args()

# check that chosen pixel size matches what is currently available in the trackerStructureTopology
# https://twiki.cern.ch/twiki/bin/view/CMS/ExamplePhaseI#Changing_the_Pixel_Size
    if int(opts.rocrows) % 80:
        print 'illegal value for PixelROCRows' 
    exit

    if int(opts.roccols) % 52:
        print "illegal value for PixelROCCols"
    exit

    # Set global variables
    set_global_var(opts.sample)
 
    print "********************************************************"
    print "*                 Configuration info                   *"
    print "********************************************************"
    print "  Launching this script from : ",os.getcwd()
    print "- submitted                  : ",opts.submit
    print "- Jobname                    : ",opts.jobname
    print "- Sample                     : ",opts.sample
    print "- Input generated sample     : ",GENSIM_FILE
    print "- PileUp Scenario            : ",opts.pu
    print "- ROCRows                    : ",opts.rocrows
    print "- ROCCols                    : ",opts.roccols
    print "- Clusterizer Threshold      : ",opts.bpixthr
    print "- Ageing Scenario            : ",opts.ageing
    
    # Setup CMSSW variables
    os.system("source /opt/exp_soft/cms/cmsset_default.sh")
    os.chdir(os.path.join(HOME,"SLHCSimPhase2",CMSSW_VER,"src"))
    os.system("eval `scram r -sh`")

    # Split and submit
    child_edm = subprocess.Popen(["edmEventSize","-v",GENSIM_FILE],stdout=subprocess.PIPE)
    (out,err) = child_edm.communicate()

    ### uncomment next to debug the script on 50 events
    # nEvents=50 # this line should be commented for running on the full GEN-SIM sample
    nEvents = int((out.split("\n")[1]).split()[3])
    
    eventsPerJob = nEvents/int(opts.numberofjobs)

    print "********************************************************"
    print "*                 Job submission pattern               *"
    print "********************************************************"    
    print "- Total events to run       : ",nEvents," in ",opts.numberofjobs," jobs" 
    print "- Total events/job          : ",eventsPerJob
    
    remainder=nEvents
    firstEvent=1
    jobIndex=0
    
    #prepare the list of the DQM files for the harvesting
    DQMFileList=""

    #############################################
    # prepare the log folder
    #############################################
    #AUX_DIR = os.path.join(HOME,"SLHCSimPhase2","AuxFiles")
    #if not os.path.exists(AUX_DIR):
    #    os.makedirs(AUX_DIR)
    #os.chdir(AUX_DIR)
    
    out_dir = None

    #############################################
    # loop on the jobs
    #############################################
    
    while remainder>0:

        print "- Job n. ",jobIndex," will process events from: ",firstEvent," to ",firstEvent+eventsPerJob-1
        
        ajob=Job(opts.jobname, firstEvent, eventsPerJob, opts.sample, opts.pu, opts.ageing, opts.rocrows, opts.roccols, opts.bpixthr)
        ajob.createThePBSFile()

        dqmoutput=ajob.job_basename+".root"
        dqmoutput.replace("digitodqm_","digitodqm_inDQM")        
        # this is needed for the script doing the harvesting
        DQMFileList+="file:"+os.path.join(ajob.out_dir,dqmoutput)+","

        out_dir = ajob.out_dir # save for later usage
        
        if opts.submit:
            ajob.submit()
            del ajob

        remainder -= eventsPerJob
        firstEvent += eventsPerJob
        jobIndex+=1
        
    #############################################
    # link the output folder
    #############################################
    
    link_name="sample_"+opts.sample+"_pu"+opts.pu+"_PixelROCRows_"+opts.rocrows+"_PixelROCCols_"+opts.roccols+"_BPixThr_"+opts.bpixthr
    linkthedir="ln -fs "+out_dir+" "+os.path.join(LOG_DIR,link_name)     
    os.system(linkthedir)    

    print "- Output will be saved in   :",out_dir
    print "********************************************************"

    #############################################
    # prepare the script for the harvesting step
    #############################################
    
    harvestingname = PBS_DIR + "/jobs/"+opts.jobname+"_sample_"+opts.sample+"_pu"+opts.pu+"_PixelRocRows"+ opts.rocrows+"_PixelROCCols_"+opts.roccols+"_BPixThr"+ opts.bpixthr+".sh"
    fout=open(harvestingname,"w")
    fout.write("#!/bin/sh \n")
    fout.write("source /opt/exp_soft/cms/cmsset_default.sh \n")
    fout.write("cmssw_ver="+CMSSW_VER+" \n")
    fout.write("cd "+os.path.join(HOME,"SLHCSimPhase2","${cmssw_ver}","src")+"\n")
    fout.write("eval `scram r -sh`\n")
    fout.write("DQMFileList="+DQMFileList[:-1]+" \n")
    fout.write("cmsDriver.py step4 --geometry ExtendedPhase2TkBE --magField 38T_PostLS1 --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1,SLHCUpgradeSimulations/Configuration/phase2TkCustomsBE.customise,SLHCUpgradeSimulations/Configuration/phase2TkCustomsBE.l1EventContent,AuxCode/SLHCSimPhase2/TkOnlyValidationCustoms.customise_tkonly --conditions auto:upgradePLS3 --mc -s HARVESTING:validationHarvesting+dqmHarvesting --filein $DQMFileList --fileout file:step4_sample_"+opts.sample+"_pu"+opts.pu+"_PixelRocRows"+ opts.rocrows+"_PixelROCCols_"+opts.roccols+"_BPixThr"+ opts.bpixthr+".root > step4_sample_"+opts.sample+"_pu"+opts.pu+"_PixelRocRows"+ opts.rocrows+"_PixelROCCols_"+opts.roccols+"_BPixThr"+ opts.bpixthr+".log \n")
    fout.write("mv DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root AuxCode/SLCHSimPhase2/test/step4_sample_"+opts.sample+"_pu"+opts.pu+"_PixelRocRows"+ opts.rocrows+"_PixelROCCols_"+opts.roccols+"_BPixThr"+ opts.bpixthr+".root")
    fout.close()

if __name__ == "__main__":        
    main()

    


