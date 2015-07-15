#!/bin/bash

jobName=GenMuonAnalyzer_afterFSR
# Setup variables

LSF_DIR=/afs/cern.ch/user/e/emiglior/scratch0/jobs/lsf
LOG_DIR=/afs/cern.ch/user/e/emiglior/scratch0/jobs/log

OUT_DIR=/afs/cern.ch/user/e/emiglior/MyWorkSpace/public/MuScleFit/Run2/CMSSW_7_4_6_patch6/src/AuxCode/AuxMuonAnalyzers/test 

lsfname=${LSF_DIR}/${jobName}.lsf
logname=${jobName}.log

# 
# -- Clean lsf files
if [ -f $lsfname ]; then 
    rm  $lsfname
fi

if [ -f ${LOG_DIR}/${jobName}.log ]; then 
    rm ${LOG_DIR}/${jobName}.log
fi

# 
# -- Prepare the script to be submitted
touch $lsfname
echo '#!/bin/sh ' >> $lsfname
echo '#BSUB -L /bin/sh'       >> $lsfname
echo '#BSUB -J ' ${jobName}   >> $lsfname
echo '#BSUB -oo' ${LOG_DIR}/${jobName}.log >> $lsfname
echo '#BSUB -q 1nd'      >> $lsfname
echo 'jobName='$jobName  >> $lsfname
echo 'logname='$logname  >> $lsfname
echo 'OUT_DIR='$OUT_DIR  >> $lsfname

cat >>$lsfname <<"LSF"
echo  -----------------------
echo  Job started at `date`
echo  -----------------------


#Some variable definitions
echo "Defining variables ..."
cmssw_ver=CMSSW_7_4_6_patch6
CMSSW_DIR=/afs/cern.ch/user/e/emiglior/MyWorkSpace/public/MuScleFit/Run2/${cmssw_ver}/src

cd $CMSSW_DIR
eval `scram r -sh`

echo "Get into test directory ..."
#Go to the test directory and prepare to start the job
cd AuxCode/AuxMuonAnalyzers/test

echo "Issue cmsRun ..."
mkdir -p /tmp/emiglior
cmsRun genmuonanalyzer_afterFSR_cfg.py


echo "Inspecting test directory after cmsRun ..."
ls -lh . 


# Copy output files to EOS 
echo "Copy output files to EOS ..."
cd /tmp/emiglior
for RootOutputFile in $(ls *Gen*root ); do 
    echo " ... ${RootOutputFile}"
    cp -f ${RootOutputFile} $OUT_DIR/; 
done

echo  -----------------------
echo  Job ended at `date`
echo  -----------------------    
LSF

    
chmod u+x $lsfname    
bsub < $lsfname    