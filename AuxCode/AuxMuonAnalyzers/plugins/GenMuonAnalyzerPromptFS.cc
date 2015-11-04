// -*- C++ -*-
//
// Package:    AuxCode/AuxMuonAnalyzers
// Class:      GenMuonAnalyzerPromptFS
// 
/**\class GenMuonAnalyzerPromptFS GenMuonAnalyzerPromptFS.cc AuxCode/AuxMuonAnalyzers/plugins/GenMuonAnalyzerPromptFS.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Ernesto Migliore
//         Created:  Tue, 07 Jul 2015 14:55:09 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

// TFileService and ROOT
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1F.h"
#include "TTree.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenRunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

//
#include "MuonAnalysis/MomentumScaleCalibration/interface/Muon.h"
#include "MuonAnalysis/MomentumScaleCalibration/interface/GenMuonPair.h"

//
// class declaration
//

typedef reco::Particle::LorentzVector lorentzVector;
using namespace std;

class GenMuonAnalyzerPromptFS : public edm::EDAnalyzer {
   public:
      explicit GenMuonAnalyzerPromptFS(const edm::ParameterSet&);
      ~GenMuonAnalyzerPromptFS();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

      //Method to get the muon after FSR (old status 1 muon) starting from a muon which is daughter of the Z
      const reco::Candidate* getStatus1Muon(const reco::Candidate* status3Muon);  
      //Method to get the muon before FSR (old status 3 muon) starting from a muon which is daughter of the Z
      const reco::Candidate* getStatus3Muon(const reco::Candidate* status3Muon);  

   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      edm::InputTag genParticlesInputTag_;
      bool debug_;
      bool beforeFSR_;
      std::vector<int> resfind_;
      GenMuonPair * genMuonPair; 

  TH1F * h1_status;;
  TH1F * h1_nMu, * h1_nMuP, * h1_nMuN, * h1_MuMuMass_SD, * h1_MuMuMass_W;
  TTree * tree;
  int run_, evtnum_;
  double genweight_;
  double lheweight_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
GenMuonAnalyzerPromptFS::GenMuonAnalyzerPromptFS(const edm::ParameterSet& iConfig)

{
   //now do what ever initialization is needed
  genParticlesInputTag_       = iConfig.getParameter<edm::InputTag>                  ( "genParticlesInputTag" );
  debug_                      = iConfig.getUntrackedParameter<bool>                  ( "debugInfo" );
  beforeFSR_                  = iConfig.getUntrackedParameter<bool>                  ( "beforeFSR" );
  resfind_                    = iConfig.getParameter<std::vector<int> >              ( "resfind" );
}


GenMuonAnalyzerPromptFS::~GenMuonAnalyzerPromptFS()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

const reco::Candidate* 
GenMuonAnalyzerPromptFS::getStatus1Muon(const reco::Candidate* status3Muon){
  const reco::Candidate* tempMuon = status3Muon;
  //  bool lastCopy = ((reco::GenParticle*)tempMuon)->isLastCopy();           //  int status = tempStatus1Muon->status();
  bool isPromptFinalState = ((reco::GenParticle*)tempMuon)->isPromptFinalState();        //  int status = tempStatus1Muon->status();
  while(tempMuon == 0 || tempMuon->numberOfDaughters()!=0){
    if ( isPromptFinalState ) break;                              //    if (status == 1) break;
    //std::vector<const reco::Candidate*> daughters;
    for (unsigned int i=0; i<tempMuon->numberOfDaughters(); ++i){
      if ( tempMuon->daughter(i)->pdgId()==tempMuon->pdgId() ){
	tempMuon = tempMuon->daughter(i);
	isPromptFinalState = ((reco::GenParticle*)tempMuon)->isPromptFinalState(); 	//	status = tempStatus1Muon->status();
	break;
      }else continue;
    }//for loop
  }//while loop
  
  return tempMuon;
}

const reco::Candidate* 
GenMuonAnalyzerPromptFS::getStatus3Muon(const reco::Candidate* status3Muon){
  const reco::Candidate* tempMuon = status3Muon;
  bool lastCopy = ((reco::GenParticle*)tempMuon)->isLastCopyBeforeFSR();        //  int status = tempStatus1Muon->status();
  while(tempMuon == 0 || tempMuon->numberOfDaughters()!=0){
    if ( lastCopy ) break;                              //    if (status == 3) break;
    //std::vector<const reco::Candidate*> daughters;
    for (unsigned int i=0; i<tempMuon->numberOfDaughters(); ++i){
      if ( tempMuon->daughter(i)->pdgId()==tempMuon->pdgId() ){
	tempMuon = tempMuon->daughter(i);
	lastCopy = ((reco::GenParticle*)tempMuon)->isLastCopyBeforeFSR(); 	//	status = tempStatus1Muon->status();
	break;
      }else continue;
    }//for loop
  }//while loop
  
  return tempMuon;
}


// ------------ method called for each event  ------------
void
GenMuonAnalyzerPromptFS::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{


  using namespace edm;


  const unsigned int motherPdgIdArray[] = {21, 23, 100553, 100553, 553, 100443, 443}; // 21 (A) -> 23 (Z)
  // get MC particle collection
  edm::Handle<reco::GenParticleCollection> genParticlesHandle;
  iEvent.getByLabel(genParticlesInputTag_, genParticlesHandle);


  if( !genParticlesHandle.isValid() ) {
    edm::LogInfo("OutputInfo") << " failed to retrieve gen particle collection";
    edm::LogInfo("OutputInfo") << " GenMuonAnalyzerPromptFS cannot continue...!";
    std::cout << " GenMuonAnalyzerPromptFS cannot continue...!" <<  std::endl;
    return;
  }

  const vector<reco::GenParticle>* genParticles = genParticlesHandle.product();
  //get the signal processID
  edm::Handle<GenEventInfoProduct> genEvtInfo;
  iEvent.getByLabel("generator", genEvtInfo);
  double genEvt_weight = genEvtInfo->weight();

  // LHE weight
  edm::Handle<LHEEventProduct> lheEvent;
  iEvent.getByLabel("externalLHEProducer",lheEvent);
  double lheEvt_weight = lheEvent->originalXWGTUP();

  if ( debug_ ) std::cout << "Evt Weight: LHE = " << lheEvt_weight << " GEN = " << genEvt_weight<< std::endl;

  // loop on generated particles
  GenMuonPair muFromRes;
  int  nMuP(0), nMuN(0);

  //Loop on generated particles
  if( debug_ ) std::cout << "Starting loop on " << genParticles->size() << " genParticles" << std::endl;
  for( reco::GenParticleCollection::const_iterator part=genParticles->begin(); part!=genParticles->end(); ++part ) {
    if ( debug_ ) std::cout<<"genParticle has pdgId = "<<fabs(part->pdgId())<<" and status = "<<part->status()<<std::endl;
    if (fabs(part->pdgId())==13){// && part->status()==3) {
      bool fromRes = false;
      unsigned int motherPdgId = part->mother()->pdgId();
      if( debug_ ) {
	std::cout << "Found a muon with mother: " << motherPdgId << std::endl;
      }
      for( int ires = 0; ires < 7; ++ires ) {
	if( motherPdgId == motherPdgIdArray[ires] && resfind_[ires] ) fromRes = true;
      }
      if(fromRes){
	if (debug_ ) std::cout<<"fromRes = true, motherPdgId = "<<motherPdgId<<std::endl;
	// status1 or status3 are labels with no specific meaning anymore
	const reco::Candidate* status3Muon = &(*part);
	const reco::Candidate* status1Muon(0);	
	if ( beforeFSR_ ) { 
	  status1Muon = getStatus3Muon(status3Muon);
	 // status1Muon = status3Muon;
	} else {
	  status1Muon = getStatus1Muon(status3Muon);
	}
	if(part->pdgId()==13) {
	  if (status1Muon->p4().pt()!=0) muFromRes.mu1 = MuScleFitMuon(status1Muon->p4(),-1);
	  else muFromRes.mu1 = MuScleFitMuon(status3Muon->p4(),-1);
	  nMuN++;
	  if( debug_ ) std::cout << "Found a genMuon - : " << muFromRes.mu1 << std::endl;
	}
	else {
	  if (status1Muon->p4().pt()!=0) muFromRes.mu2 = MuScleFitMuon(status1Muon->p4(),+1);
	  else muFromRes.mu2 = MuScleFitMuon(status3Muon->p4(),+1);
	  nMuP++;
	  if( debug_ ) std::cout << "Found a genMuon + : " << muFromRes.mu2 << std::endl;
	}

      }// end if fromRes
    } // end if PDG ID=13
  } // end of loop

  if ( nMuP == 1 && nMuN == 1 ) {
    lorentzVector lv_MuMu = muFromRes.mu1.fP4 + muFromRes.mu2.fP4;
    //    h1_MuMuMass_SD->Fill(lv_MuMu.mass(),genEvt_weight);
    //    h1_MuMuMass_W->Fill(lv_MuMu.mass(),genEvt_weight);

    double pTmin = min(muFromRes.mu1.fP4.pt(), muFromRes.mu2.fP4.pt());
    double absEtaMax = max(fabs(muFromRes.mu1.fP4.eta()), fabs(muFromRes.mu2.fP4.eta())); 
    // @EM 2015.07.28: Horrible... same cuts as used by SD for the run1 calculation harcoded here....
    if ( pTmin > 18. && absEtaMax < 2.5 ) {
      if ( genEvt_weight < 0 ) {
	h1_MuMuMass_SD->Fill(lv_MuMu.mass(),-1.);
	h1_MuMuMass_W->Fill(lv_MuMu.mass() ,-1.);
      } else if ( genEvt_weight > 0 ) {
	h1_MuMuMass_SD->Fill(lv_MuMu.mass(),+1.);
	h1_MuMuMass_W->Fill(lv_MuMu.mass() ,+1.);
      }
    }
  }


  evtnum_ = iEvent.id().event();
  run_ = iEvent.id().run();
  genweight_ = genEvt_weight;
  lheweight_ = lheEvt_weight;
  genMuonPair->copy(muFromRes);
  tree->Fill();

    // //%
    // if( genps_it->pdgId() == 13 ) {
    //   muN = LorentzVector( genps_it->p4().x(),
    // 			   genps_it->p4().y(),
    // 			   genps_it->p4().z(),
    // 			   genps_it->p4().e() );
    //   h1_status->Fill(genps_it->status());

    //   if (genps_it->isLastCopy() ) {
    // 	nMuNLast++;
    //   }
    // } else if ( genps_it->pdgId() == -13 ) {
    //   muP = LorentzVector( genps_it->p4().x(),
    // 			   genps_it->p4().y(),
    // 			   genps_it->p4().z(),
    // 			   genps_it->p4().e() );
    //   h1_status->Fill(genps_it->status());

    //   if (genps_it->isLastCopy() ) { 
    // 	nMuPLast++;
    //   }
    // }


  h1_nMu->Fill(nMuP+nMuN);
  h1_nMuP->Fill(nMuP);
  h1_nMuN->Fill(nMuN);
 

}


// ------------ method called once each job just before starting event loop  ------------
void 
GenMuonAnalyzerPromptFS::beginJob()
{
  edm::Service<TFileService> fs;
  h1_nMu  = fs->make<TH1F>( "h1_nMu"   , "h1_nMu" , 11,  -0.5, 10.5 );
  h1_nMuP = fs->make<TH1F>( "h1_nMuP"  , "h1_nMuP", 11,  -0.5, 10.5 );
  h1_nMuN = fs->make<TH1F>( "h1_nMuN"  , "h1_nMuN", 11,  -0.5, 10.5 );
  h1_status = fs->make<TH1F>( "h1_status"  , "h1_status", 100,  -0.5, 99.5 );

  h1_MuMuMass_SD = fs->make<TH1F>( "h1_MuMuMass_SD", "h1_MuMuMass SDittmaier binning", 1001, 71.170,111.210);
  h1_MuMuMass_W  = fs->make<TH1F>( "h1_MuMuMass_W" , "h1_MuMuMass wide"              , 1701, 57.170,125.210);

  h1_MuMuMass_SD->Sumw2();  
  h1_MuMuMass_W->Sumw2();


  tree = fs->make<TTree>("T", "Gen Muon pairs");
  tree->Branch("run",    &run_   , "run/I");
  tree->Branch("evtnum", &evtnum_, "evtnum/I");
  tree->Branch("genweight", &genweight_, "genweight/D");
  tree->Branch("lheweight", &lheweight_, "lheweight/D");
  genMuonPair = new GenMuonPair;
  tree->Branch("GenMuons", "GenMuonPair", &genMuonPair);

}

// ------------ method called once each job just after ending the event loop  ------------
void 
GenMuonAnalyzerPromptFS::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
GenMuonAnalyzerPromptFS::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
GenMuonAnalyzerPromptFS::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
GenMuonAnalyzerPromptFS::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
GenMuonAnalyzerPromptFS::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
GenMuonAnalyzerPromptFS::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}





//define this as a plug-in
DEFINE_FWK_MODULE(GenMuonAnalyzerPromptFS);
