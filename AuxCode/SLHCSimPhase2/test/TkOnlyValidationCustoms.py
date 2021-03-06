import FWCore.ParameterSet.Config as cms
def customise_tkonly(process):
    # keeping only tracker validation sequences
    process.validation_step.remove(process.globaldigisanalyze)                               
    process.validation_step.remove(process.ecalSimHitsValidationSequence)                    
    process.validation_step.remove(process.ecalDigisValidationSequence)                      
    process.validation_step.remove(process.ecalRecHitsValidationSequence)                    
    process.validation_step.remove(process.ecalClustersValidationSequence)                   
    process.validation_step.remove(process.hcalSimHitsValidationSequence)                    
    process.validation_step.remove(process.hcaldigisValidationSequence)                      
    process.validation_step.remove(process.hcalSimHitStudy)                                  
    process.validation_step.remove(process.hcalRecHitsValidationSequence)                    
    process.validation_step.remove(process.calotowersValidationSequence)                     
    process.validation_step.remove(process.validSimHit)                                      
    process.validation_step.remove(process.muondtdigianalyzer)                               
    process.validation_step.remove(process.cscDigiValidation)                                
    process.validation_step.remove(process.validationMuonRPCDigis)                           
    process.validation_step.remove(process.recoMuonValidation)                               
    process.validation_step.remove(process.muIsoVal_seq)                                     
    process.validation_step.remove(process.muonIdValDQMSeq)                                  
    process.validation_step.remove(process.mixCollectionValidation)                          
    process.validation_step.remove(process.JetValidation)                                    
    process.validation_step.remove(process.METValidation)                                    
    process.validation_step.remove(process.egammaValidation)                                 
    process.validation_step.remove(process.pfJetValidationSequence)                          
    process.validation_step.remove(process.pfMETValidationSequence)                          
    process.validation_step.remove(process.rpcRecHitValidation_step)                         
    process.validation_step.remove(process.dtLocalRecoValidation_no2D)                       
    process.validation_step.remove(process.TauValNumeratorAndDenominatorQCD)                 
    process.validation_step.remove(process.TauValNumeratorAndDenominatorRealData)            
    process.validation_step.remove(process.TauValNumeratorAndDenominatorRealElectronsData)   
    process.validation_step.remove(process.TauValNumeratorAndDenominatorRealMuonsData)       
    process.validation_step.remove(process.TauValNumeratorAndDenominatorZEE)                 
    process.validation_step.remove(process.TauValNumeratorAndDenominatorZMM)                 
    process.validation_step.remove(process.TauValNumeratorAndDenominatorZTT)                 
    process.validation_step.remove(process.recoMuonValidationHLT_seq)                        
    process.validation_step.remove(process.hltMuonValidator)                                 
    process.validation_step.remove(process.HLTTauVal)                                        
    process.validation_step.remove(process.egammaValidationSequence)                         
    process.validation_step.remove(process.HLTTopVal)                                        
    process.validation_step.remove(process.HLTFourVector)                                    
    process.validation_step.remove(process.heavyFlavorValidationSequence)                    
    process.validation_step.remove(process.HLTJetMETValSeq)
    # removing additional track collections from trackValidation input
    process.trackValidator.label = cms.VInputTag(cms.InputTag("generalTracks"))   
    return(process)




                                      
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                                   
                                  
                                  
                                  
                                  
                                  
                                  
                                  
                                  
