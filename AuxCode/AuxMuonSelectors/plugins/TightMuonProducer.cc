// -*- C++ -*-
//
// Package:    TightMuonProducer
// Class:      TightMuonProducer
// 
/**\class TightMuonProducer TightMuonProducer.cc AuuCode/TightMuonProducer/src/TightMuonProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Ernesto Migliore,13 2-017,+41227672059,
//         Created:  Wed Jun 20 12:27:19 CEST 2012
// $Id$
//
//


// system include files
#include <memory>
#include <iostream>

// user include files
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"

#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "DataFormats/TrackReco/interface/TrackExtra.h"
#include "DataFormats/TrackingRecHit/interface/TrackingRecHit.h"
//
// class declaration
//

class TightMuonProducer : public edm::EDProducer {
public:
  explicit TightMuonProducer(const edm::ParameterSet&);
  ~TightMuonProducer();
  
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  
private:
  virtual void beginJob() ;
  virtual void produce(edm::Event&, const edm::EventSetup&);
  virtual void endJob() ;
  
  virtual void beginRun(edm::Run&, edm::EventSetup const&);
  virtual void endRun(edm::Run&, edm::EventSetup const&);
  virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
  virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
  
  // ----------member data ---------------------------
  edm::InputTag muonCollectionTag_;
  edm::InputTag vertexCollectionTag_;
  bool isPF_;

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
TightMuonProducer::TightMuonProducer(const edm::ParameterSet& iConfig):
muonCollectionTag_(iConfig.getParameter<edm::InputTag>("muonSrc")),
vertexCollectionTag_(iConfig.getParameter<edm::InputTag>("vertexSrc")),
isPF_(iConfig.getUntrackedParameter<bool>("isPF"))
{
  //now do what ever other initialization is needed
  produces<std::vector<reco::Muon> >();  

}


TightMuonProducer::~TightMuonProducer()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
TightMuonProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
 
   edm::Handle<std::vector<reco::Muon> > muons;
   iEvent.getByLabel(muonCollectionTag_,muons);

   edm::Handle<std::vector<reco::Vertex> > vtx;
   iEvent.getByLabel(vertexCollectionTag_, vtx);
   const reco::Vertex pv = vtx.product()->operator[](0);

   std::vector<reco::Muon> tightMuons;

   for(std::vector<reco::Muon>::const_iterator recomuon_it=muons->begin(); recomuon_it!=muons->end(); ++recomuon_it){
     
     bool ISGLOB = (recomuon_it->isGlobalMuon());
     bool ID = (muon::isGoodMuon(*recomuon_it,muon::GlobalMuonPromptTight) && (recomuon_it->numberOfMatchedStations()>1) );
     bool HITS = (recomuon_it->innerTrack()->hitPattern().trackerLayersWithMeasurement() > 5 && recomuon_it->innerTrack()->hitPattern().numberOfValidPixelHits() > 0);
     bool IP = (fabs(recomuon_it->muonBestTrack()->dxy(pv.position())) < 0.2 && fabs(recomuon_it->muonBestTrack()->dz(pv.position())) < 0.5);

     if ( isPF_ ) {
        if ( muon::isTightMuon(*recomuon_it,pv)  ) tightMuons.push_back(*recomuon_it);
     } else {
       if (ISGLOB && ID && HITS && IP) tightMuons.push_back(*recomuon_it);
     }
   }      
   // the output
   std::auto_ptr<std::vector<reco::Muon> > tightMuonCollection( new std::vector<reco::Muon> (tightMuons) );
   iEvent.put(tightMuonCollection);

}

// ------------ method called once each job just before starting event loop  ------------
void 
TightMuonProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TightMuonProducer::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
TightMuonProducer::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
TightMuonProducer::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
TightMuonProducer::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
TightMuonProducer::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TightMuonProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TightMuonProducer);
