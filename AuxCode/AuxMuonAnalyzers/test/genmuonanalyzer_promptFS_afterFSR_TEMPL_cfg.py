# This pset is a templated version to submit jobs with different jobId on different input files
# quick-and-dirt way to by-pass crab3 (at least for the moment...)
import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 50000


import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing()
options.register('jobId',
                 1, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "job ID")
options.parseArguments()

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.TFileService = cms.Service("TFileService", fileName = cms.string("/tmp/emiglior/GenMuonAnalyzerHistos_PFS_afterFSR_jobId"+str(options.jobId)+".root") )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(50000) )

# aMC@NLO /DYJetsToLL
#from AuxCode.AuxMuonAnalyzers.DYJetsToLL_M_50_TuneCUETP8M1_13TeV_amcatnloFXFX_pythia8_cfi import readFiles
#numOfFilesPerJob=50 # -> 40kEvts/file -> 2MEvts/job

# POWHEG
#from AuxCode.AuxMuonAnalyzers.ZToMuMu_NNPDF30_13TeVpowheg_M_50_120_cfi import readFiles
#numOfFilesPerJob=68 # 
#from AuxCode.AuxMuonAnalyzers.ZToMuMu_NNPDF30_13TeVpowheg_M_120_200_cfi import readFiles
#numOfFilesPerJob=5 # 
#from AuxCode.AuxMuonAnalyzers.ZToMuMu_NNPDF30_13TeVpowheg_M_200_400_cfi import readFiles
#numOfFilesPerJob=4 # 
#from AuxCode.AuxMuonAnalyzers.ZToMuMu_NNPDF30_13TeVpowheg_M_400_800_cfi import readFiles
#numOfFilesPerJob=9 # 
from AuxCode.AuxMuonAnalyzers.ZToMuMu_NNPDF30_13TeVpowheg_M_800_1400_cfi import readFiles
numOfFilesPerJob=3 #

# MadGraph high pT(Z)
from AuxCode.AuxMuonAnalyzers.DYJetsToLL_M_50_Zpt_150toInf_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_cfi import readFiles
numOfFilesPerJob=60 #

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(readFiles[(options.jobId-1)*numOfFilesPerJob:options.jobId*numOfFilesPerJob-1])  #readFilesSlimmed
)

process.demo = cms.EDAnalyzer('GenMuonAnalyzerPromptFS',
                              # The resonances are to be specified in this order:
                              # A0, Z0, Y(3S), Y(2S), Y(1S), Psi(2S), J/Psi
                              resfind = cms.vint32(1, 1, 0, 0, 0, 0, 0),
                              genParticlesInputTag = cms.InputTag("prunedGenParticles" ),
                              beforeFSR = cms.untracked.bool(False),
                              debugInfo = cms.untracked.bool(False),
)


process.p = cms.Path(process.demo)
#print process.dumpPython()
