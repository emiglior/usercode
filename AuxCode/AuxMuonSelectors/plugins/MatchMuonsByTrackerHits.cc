// -*- C++ -*-
//
// Package:    MatchMuonsByTrackerHits
// Class:      MatchMuonsByTrackerHits
// 
/**\class MatchMuonsByTrackerHits MatchMuonsByTrackerHits.cc AuuCode/MatchMuonsByTrackerHits/src/MatchMuonsByTrackerHits.cc

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

#include "DataFormats/TrackerRecHit2D/interface/SiStripMatchedRecHit2DCollection.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripRecHit2DCollection.h"
#include "DataFormats/TrackerRecHit2D/interface/SiStripRecHit1DCollection.h"


#include "Geometry/CommonDetUnit/interface/GeomDetUnit.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"

//
// class declaration
//

class MatchMuonsByTrackerHits : public edm::EDProducer {
public:
  explicit MatchMuonsByTrackerHits(const edm::ParameterSet&);
  ~MatchMuonsByTrackerHits();
  
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
  edm::InputTag muonCollectionTag1_;
  edm::InputTag muonCollectionTag2_;

  double epsilon_;
  bool use_sharesInput_;
  double shareFrac_;
  double foundHitBonus_;
  double lostHitPenalty_;
  bool allowFirstHitShare_;
  //

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
MatchMuonsByTrackerHits::MatchMuonsByTrackerHits(const edm::ParameterSet& iConfig):
muonCollectionTag1_(iConfig.getParameter<edm::InputTag>("muonSrc1")),
muonCollectionTag2_(iConfig.getParameter<edm::InputTag>("muonSrc2")),
epsilon_(iConfig.getParameter<double>("Epsilon")),
shareFrac_(iConfig.getParameter<double>("ShareFrac")),
foundHitBonus_(iConfig.getParameter<double>("FoundHitBonus")),
lostHitPenalty_(iConfig.getParameter<double>("LostHitPenalty")),
allowFirstHitShare_(iConfig.getParameter<bool>("allowFirstHitShare"))
{
  produces<std::vector<reco::Muon> >();  
  use_sharesInput_ = true;
  if ( epsilon_ > 0.0 ) use_sharesInput_ = false;

}


MatchMuonsByTrackerHits::~MatchMuonsByTrackerHits()
{
}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
MatchMuonsByTrackerHits::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
 
   edm::Handle<std::vector<reco::Muon> > mC1;
   iEvent.getByLabel(muonCollectionTag1_,mC1);

   edm::Handle<std::vector<reco::Muon> > mC2;
   iEvent.getByLabel(muonCollectionTag2_,mC2);

   std::map<reco::MuonCollection::const_iterator, std::vector<const TrackingRecHit*> > rh1;
   std::map<reco::MuonCollection::const_iterator, std::vector<const TrackingRecHit*> > rh2;

   std::vector<int> selected1; for (unsigned int i=0; i<mC1->size(); ++i){selected1.push_back(1);}
   std::vector<int> selected2; for (unsigned int i=0; i<mC2->size(); ++i){selected2.push_back(1);}

   // fill a map of the rechit associated to the inner tracks of the muons in the first collection
   int iMu1=0;
   for(std::vector<reco::Muon>::const_iterator recomuon_it=mC1->begin(); recomuon_it!=mC1->end(); ++recomuon_it, ++iMu1){
     if (recomuon_it->isAValidMuonTrack(reco::Muon::InnerTrack)){
       const reco::Track & track = *(recomuon_it->innerTrack());
       trackingRecHit_iterator itB = track.recHitsBegin();
       trackingRecHit_iterator itE = track.recHitsEnd();
       for (trackingRecHit_iterator it = itB;  it != itE; ++it) { 
	 const TrackingRecHit* hit = &(**it);
	 rh1[recomuon_it].push_back(hit);
       }
     } else {
       rh1[recomuon_it].clear();
     }

   }
   // fill a map of the rechit associated to the inner tracks of the muons in the second collection
   int iMu2=0;
   for(std::vector<reco::Muon>::const_iterator recomuon_it=mC2->begin(); recomuon_it!=mC2->end(); ++recomuon_it, ++iMu2){
     if (recomuon_it->isAValidMuonTrack(reco::Muon::InnerTrack)){
       const reco::Track & track = *(recomuon_it->innerTrack());
       trackingRecHit_iterator itB = track.recHitsBegin();
       trackingRecHit_iterator itE = track.recHitsEnd();
       for (trackingRecHit_iterator it = itB;  it != itE; ++it) { 
	 const TrackingRecHit* hit = &(**it);
	 rh2[recomuon_it].push_back(hit);
       }
     } else {
       rh2[recomuon_it].clear();
     }
   }

   
   if ( (0<mC1->size()) && (0<mC2->size()) ){
     int i=-1;
     for (reco::MuonCollection::const_iterator muon1=mC1->begin(); muon1!=mC1->end(); ++muon1){
       i++; 
       std::vector<const TrackingRecHit*>& iHits = rh1[muon1]; 
       unsigned nh1 = iHits.size();
       if (nh1==0) {selected1[i]=1; continue;}
       int j=-1;
       for (reco::MuonCollection::const_iterator muon2=mC2->begin(); muon2!=mC2->end(); ++muon2){
	 j++;
	 std::vector<const TrackingRecHit*>& jHits = rh2[muon2]; 
	 unsigned nh2 = jHits.size();
	 if (nh2==0) {selected2[j]=1; continue;}
	 int noverlap=0;
	 int firstoverlap=0;
	 for ( unsigned ih=0; ih<nh1; ++ih ) { 
	   const TrackingRecHit* it = iHits[ih];
	   if (it->isValid()){
	     int jj=-1;
	     for ( unsigned jh=0; jh<nh2; ++jh ) { 
	       const TrackingRecHit* jt = jHits[jh];
	       jj++;
	       if (jt->isValid()){
		 if (!use_sharesInput_){
		   float delta = fabs ( it->localPosition().x()-jt->localPosition().x() ); 
		   if ((it->geographicalId()==jt->geographicalId())&&(delta<epsilon_)) {
		     noverlap++;
		     if ( allowFirstHitShare_ && ( ih == 0 ) && ( jh == 0 ) ) firstoverlap=1;
		   }
		 }else{
		   if ( it->sharesInput(jt,TrackingRecHit::some) ) {
		     noverlap++;
		     if ( allowFirstHitShare_ && ( ih == 0 ) && ( jh == 0 ) ) firstoverlap=1;
		   }
		 }
	       }
	     }
	   }
	 }
	 //

	 int newQualityMask =( muon1->innerTrack()->qualityMask() | muon2->innerTrack()->qualityMask() ); // take OR of trackQuality 
	 int nhit1 = muon1->innerTrack()->numberOfValidHits();
	 int nhit2 = muon2->innerTrack()->numberOfValidHits();
	 if ( (noverlap-firstoverlap) > (std::min(nhit1,nhit2)-firstoverlap)*shareFrac_ ) {
	   double score1 = foundHitBonus_*nhit1 - lostHitPenalty_*muon1->innerTrack()->numberOfLostHits() - muon1->innerTrack()->chi2();
	   double score2 = foundHitBonus_*nhit2 - lostHitPenalty_*muon2->innerTrack()->numberOfLostHits() - muon2->innerTrack()->chi2();
	   const double almostSame = 1.001;
	   if ( score1 > almostSame * score2 ){
	     selected2[j]=0; 
	     selected1[i]=10+newQualityMask; // add 10 to avoid the case where mask = 1
	   }else if ( score2 > almostSame * score1 ){
	     selected1[i]=0; 
	     selected2[j]=10+newQualityMask;  // add 10 to avoid the case where mask = 1
	   }else{
	     if ( muon1->innerTrack()->algo() <= muon2->innerTrack()->algo()) {
	       selected2[j]=0;
	       selected1[i]=10+newQualityMask; // add 10 to avoid the case where mask = 1
	     }else{
	       selected1[i]=0;
	       selected2[j]=10+newQualityMask; // add 10 to avoid the case where mask = 1
	     }
	   }
	 }//end got a duplicate
       }//end track2 loop
     }//end track loop
   }//end more than 1 track
   
  //
  //  output selected muons - if any
  //
   // the output
   std::vector<reco::Muon> matchedMuons;
   //   std::vector<reco::Track> matchedMuonTracks;
   //   std::vector<reco::TrackExtra> matchedMuonsTrackExtras;
     

   if ( 0<mC1->size()) {
     int i=0;
     for (reco::MuonCollection::const_iterator muon=mC1->begin(); muon!=mC1->end(); 
	  ++muon, ++i){
       // debug
       if ( false ) std::cout<<"MU1 pT/sel " << muon->innerTrack()->pt() << " " <<
	 muon->innerTrack()->innerDetId() << " " << 
	 muon->innerTrack()->outerDetId() << " " << 
	 selected1[i] << std::endl;
     }
   }
   
   if ( 0<mC2->size()) {
     int i=0;
     for (reco::MuonCollection::const_iterator muon=mC2->begin(); muon!=mC2->end(); 
	  ++muon, ++i){
 // debug 
      if ( false ) std::cout<<"MU2 pT/sel " << muon->innerTrack()->pt() << " " << 
	 muon->innerTrack()->innerDetId() << " " << 
	 muon->innerTrack()->outerDetId() << " " << 
	 selected2[i] << std::endl;

       //--------------------- TO BE CHECKED --------------------------//
       if ( selected2[i]!=1 ) matchedMuons.push_back(*muon);
       //--------------------------------------------------------------//

     }
   }

   
   // the output
   std::auto_ptr<std::vector<reco::Muon> > matchedMuonCollection( new std::vector<reco::Muon> (matchedMuons) );
   iEvent.put(matchedMuonCollection);

}

// ------------ method called once each job just before starting event loop  ------------
void 
MatchMuonsByTrackerHits::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MatchMuonsByTrackerHits::endJob() {
}

// ------------ method called when starting to processes a run  ------------
void 
MatchMuonsByTrackerHits::beginRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
MatchMuonsByTrackerHits::endRun(edm::Run&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
MatchMuonsByTrackerHits::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
MatchMuonsByTrackerHits::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MatchMuonsByTrackerHits::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MatchMuonsByTrackerHits);
