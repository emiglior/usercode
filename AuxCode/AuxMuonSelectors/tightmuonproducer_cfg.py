import FWCore.ParameterSet.Config as cms

process = cms.Process("OWNPARTICLES")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('file:/tmp/emiglior/B8DC1878-209A-E111-A03B-003048D2BC62.root')
)

process.TIGHTmuons = cms.EDProducer("TightMuonProducer",
                                    muonSrc  =cms.InputTag('muons'),
                                    vertexSrc=cms.InputTag('offlinePrimaryVertices')
)

process.VBTFmuons = cms.EDFilter("MuonSelector",
                                 src = cms.InputTag("muons"),                                 
                                 cut = cms.string('isGlobalMuon = 1 & isTrackerMuon = 1 & pt > 20 & abs(eta)<2.4 & abs(globalTrack().dxy)<0.2')
 )

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('/tmp/emiglior/myOutputFile.root'),
                               outputCommands=cms.untracked.vstring( 
    "keep *_*_*_*"
    )
)

  
process.p = cms.Path(process.VBTFmuons+process.TIGHTmuons)

process.e = cms.EndPath(process.out)
