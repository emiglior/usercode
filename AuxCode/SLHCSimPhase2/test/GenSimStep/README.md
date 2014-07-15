GEN-SIM step for Extended2017 geometry

Parameters as obtained from
runTheMatrix.py --what upgrade -l 10000

cmsDriver.py FourMuPt_1_200_cfi  --conditions auto:upgrade2017 -n 10 --eventcontent FEVTDEBUG --relval 10000,100 -s GEN,SIM --datatier GEN-SIM --beamspot Gauss --customise SLHCUpgradeSimulations/Configuration/combinedCustoms.cust_2017 --geometry Extended2017 --magField 38T_PostLS1 --fileout file:step1.root  > step1_FourMuPt1_200+FourMuPt_1_200_2017_GenSimFull+DigiFull_2017+RecoFull_2017+HARVESTFull_2017.log  2>&1
 
 
cmsDriver.py step2  --conditions auto:upgrade2017 -n 10 --eventcontent FEVTDEBUGHLT -s DIGI:pdigi_valid,L1,DIGI2RAW --datatier GEN-SIM-DIGI-RAW --customise SLHCUpgradeSimulations/Configuration/combinedCustoms.cust_2017 --geometry Extended2017 --magField 38T_PostLS1 --filein file:step1.root  --fileout file:step2.root  > step2_FourMuPt1_200+FourMuPt_1_200_2017_GenSimFull+DigiFull_2017+RecoFull_2017+HARVESTFull_2017.log  2>&1
 
cmsDriver.py step3  --conditions auto:upgrade2017 -n 10 --eventcontent FEVTDEBUGHLT,DQM -s RAW2DIGI,L1Reco,RECO,VALIDATION,DQM --datatier GEN-SIM-RECO,DQM --customise SLHCUpgradeSimulations/Configuration/combinedCustoms.cust_2017 --geometry Extended2017 --magField 38T_PostLS1 --filein file:step2.root  --fileout file:step3.root  > step3_FourMuPt1_200+FourMuPt_1_200_2017_GenSimFull+DigiFull_2017+RecoFull_2017+HARVESTFull_2017.log  2>&1

