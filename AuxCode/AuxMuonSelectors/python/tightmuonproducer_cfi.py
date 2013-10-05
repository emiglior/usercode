import FWCore.ParameterSet.Config as cms

demo = cms.EDProducer('TightMuonProducer',
                      muonSrc=cms.InputTag('muons'),
                      vertexSrc=cms.InputTag('offlinePrimaryVertices'),
                      isPF=cms.bool(True)
)
