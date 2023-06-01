import FWCore.ParameterSet.Config as cms

# Configured for 2026D98
from Configuration.Eras.Era_Phase2C17I13M9_cff import Phase2C17I13M9
process = cms.Process('USER',Phase2C17I13M9)

# run the input file through the end;
# for a limited number of events, replace -1 with the desired number 
#
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(5) )

process.load('Configuration.Geometry.GeometryExtended2026D98Reco_cff')
#process.load('Configuration.StandardSequences.MagneticField_cff')

process.source = cms.Source( "PoolSource",
                             fileNames = cms.untracked.vstring(
                                 'file:/tmp/emiglior/step2_PU20.root'
                                 # MinBias: /RelValMinBias_14TeV/CMSSW_13_1_0_pre1-130X_mcRun4_realistic_v2_2026D98noPU-v1/GEN-SIM-DIGI-RAW
                                 # '/store/relval/CMSSW_13_1_0_pre1/RelValMinBias_14TeV/GEN-SIM-DIGI-RAW/130X_mcRun4_realistic_v2_2026D98noPU-v1/00000/00b94927-8b55-4543-b652-7af9c216411f.root'
                                 # NoPU: /RelValQCD_FlatPt_15_3000HS_14/CMSSW_13_1_0_pre1-130X_mcRun4_realistic_v2_2026D98noPU-v1/GEN-SIM-DIGI-RAW 
                                 # '/store/relval/CMSSW_13_1_0_pre1/RelValQCD_FlatPt_15_3000HS_14/GEN-SIM-DIGI-RAW/130X_mcRun4_realistic_v2_2026D98noPU-v1/00000/0db2a284-263a-4cb3-8304-deafc1ae4956.root'
                                 # PU200: /RelValQCD_FlatPt_15_3000HS_14/PU_130X_mcRun4_realistic_v2_2026D98PU200-v1/GEN-SIM-DIGI-RAW
                                 # '/store/relval/CMSSW_13_1_0_pre1/RelValQCD_FlatPt_15_3000HS_14/GEN-SIM-DIGI-RAW/PU_130X_mcRun4_realistic_v2_2026D98PU200-v1/00000/017b660f-bb4e-4b00-825c-5574204c3416.root',
                                 # '/store/relval/CMSSW_13_1_0_pre1/RelValQCD_FlatPt_15_3000HS_14/GEN-SIM-DIGI-RAW/PU_130X_mcRun4_realistic_v2_2026D98PU200-v1/00000/0302edf9-7e88-466d-894b-a8b5e4159e5e.root'
			     )
                           )

# FileService is mandatory, as the following analyzer module 
# will want it, to create output histogram file
# 
process.TFileService = cms.Service("TFileService",
        fileName = cms.string("SimHitDistanceAnalyzer.root")
)


process.load('FWCore.Modules.printContent_cfi')
process.load('AuxCode.TkPh2Analysis.SimHitDistanceAnalyzer_cfi')

process.p1 = cms.Path( process.simHitDistanceAnalyzer ) #* process.printContent )

