import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.TFileService = cms.Service("TFileService", fileName = cms.string("UserNtuples.root") )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
    '/store/data/Run2012B/DoubleMu/AOD/PromptReco-v1/000/193/752/504D95A3-789B-E111-9B6C-003048D3C944.root'
    )
)

process.demo = cms.EDAnalyzer('UserNtuples'
)


process.p = cms.Path(process.demo)
