import FWCore.ParameterSet.Config as cms


simHitDistanceAnalyzer = cms.EDAnalyzer( "SimHitDistanceAnalyzer", 
                                         # SimHits
                                         srcPSimHit  = cms.VInputTag(('g4SimHits:TrackerHitsPixelBarrelLowTof'),
                                                                     ('g4SimHits:TrackerHitsPixelBarrelHighTof'),
                                                                     ('g4SimHits:TrackerHitsPixelEndcapLowTof'),
                                                                     ('g4SimHits:TrackerHitsPixelEndcapHighTof')),
                                         # SimHits from MixingModule
                                         srcMixPSimHit  = cms.VInputTag(('mix:g4SimHitsTrackerHitsPixelBarrelLowTof'),
                                                                        ('mix:g4SimHitsTrackerHitsPixelBarrelHighTof'),
                                                                        ('mix:g4SimHitsTrackerHitsPixelEndcapLowTof'),
                                                                        ('mix:g4SimHitsTrackerHitsPixelEndcapHighTof'))

                                     ) 
