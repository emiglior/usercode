import FWCore.ParameterSet.Config as cms
matchmuonsbytrackerhits = cms.EDProducer("MatchMuonsByTrackerHits",
    # module label
    muonSrc1 = cms.InputTag(''),
    # module label 
    muonsSrc2 = cms.InputTag(''),
    # minimum shared fraction to be called duplicate
    ShareFrac = cms.double(0.19),
    # best track chosen by chi2 modified by parameters below:
    FoundHitBonus = cms.double(5.0),
    LostHitPenalty = cms.double(20.0),
    # minimum difference in rechit position in cm
    # negative Epsilon uses sharedInput for comparison
    Epsilon = cms.double(-0.001),
    allowFirstHitShare = cms.bool(True)
)


