
import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 50000

process.TFileService = cms.Service("TFileService", fileName = cms.string("/tmp/emiglior/GenMuonAnalyzerHistos_afterFSR.root") )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

from AuxCode.AuxMuonAnalyzers.DYJetsToLL_M_50_TuneCUETP8M1_13TeV_amcatnloFXFX_pythia8_cfi import readFiles

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = readFiles
)

process.demo = cms.EDAnalyzer('GenMuonAnalyzer',
                              # The resonances are to be specified in this order:
                              # A0, Z0, Y(3S), Y(2S), Y(1S), Psi(2S), J/Psi
                              resfind = cms.vint32(0, 1, 0, 0, 0, 0, 0),
                              genParticlesInputTag = cms.InputTag("prunedGenParticles" ),
                              beforeFSR = cms.untracked.bool(False),
                              debugInfo = cms.untracked.bool(False),
)


process.p = cms.Path(process.demo)

