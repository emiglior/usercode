import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.Geometry.GeometryExtended2023Muon_cff')
process.load('Configuration.Geometry.GeometryExtended2023MuonReco_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:upgradePLS3', '')

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('/store/caf/user/emiglior/SLHCSimPhase2/620_slhc17_patch1/Extended2023Muon/GEN-SIM/Thick_BPIX_0.150_FPIX_0.285/step1_MinBias_TuneZ2star_14TeV_pythia6_50kEvts.root')
                            )

process.TFileService = cms.Service('TFileService',
                                   fileName = cms.string("myChecks.root")
                                   )

process.demo = cms.EDAnalyzer('SimTruthChecks',
                              verbose = cms.untracked.bool(True)
                              )


process.p = cms.Path(process.demo)

# customisation of the process.

# Automatic addition of the customisation function from SLHCUpgradeSimulations.Configuration.combinedCustoms
from SLHCUpgradeSimulations.Configuration.combinedCustoms import cust_2023Muon 

#call to customisation function cust_2023Muon imported from SLHCUpgradeSimulations.Configuration.combinedCustoms
process = cust_2023Muon(process)

# End of customisation functions
