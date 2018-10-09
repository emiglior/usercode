# for phase2
import FWCore.ParameterSet.Config as cms

#from Configuration.StandardSequences.Eras import eras
process = cms.Process("DegugLocalCoordinates")

process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023D17_cff')

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = cms.untracked.vstring("cout")
process.MessageLogger.cout = cms.untracked.PSet(threshold = cms.untracked.string("ERROR"))

process.source = cms.Source("EmptySource",
                            firstRun = cms.untracked.uint32(1)
                            )

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
    )

process.DebugLocalCoordinates = cms.EDAnalyzer("DebugLocalCoordinates")


process.p = cms.Path(
    process.DebugLocalCoordinates
)

