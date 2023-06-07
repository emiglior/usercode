/*
 *

 * 
 */
// -*- C++ -*-
//
// Package:    SimHitDistanceAnalyzer
// Class:      SimHitDistanceAnalyzer
// 
/**\class SimHitDistanceAnalyzer SimHitDistanceAnalyzer.cc test/SimHitDistanceAnalyzer.cc

 Description: <one line class summary>

**/

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "Geometry/CommonDetUnit/interface/GeomDetType.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"
#include "Geometry/CommonTopologies/interface/PixelGeomDetUnit.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/TrackerNumberingBuilder/interface/GeometricDet.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"

#include "DataFormats/Common/interface/DetSetVector.h"
#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"
#include "DataFormats/SiPixelDetId/interface/PixelSubdetector.h"

#include "SimDataFormats/TrackingHit/interface/PSimHit.h"
#include "SimDataFormats/TrackingHit/interface/PSimHitContainer.h"
 
//#include "SimDataFormats/CrossingFrame/interface/CrossingFrame.h"
#include "SimDataFormats/CrossingFrame/interface/MixCollection.h"

#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#define HEPMC // look at generator output
#ifdef HEPMC
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenRunInfoProduct.h"
#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"
#include "HepPDT/ParticleDataTable.hh"
#endif

// TFileService stuff
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/TFileDirectory.h"

// For ROOT
#include <TROOT.h>
#include <TFile.h>

#include <TH1.h>
//#include <TH2.h>

// CLHEP (for speed of light)
#include "CLHEP/Units/PhysicalConstants.h"
#include "CLHEP/Units/SystemOfUnits.h"

using namespace std;
//using namespace edm;

//
//
// class declaration
//
using Phase2TrackerGeomDetUnit = PixelGeomDetUnit;

constexpr double c_cm_ns = CLHEP::c_light * CLHEP::ns / CLHEP::cm;
constexpr double c_inv = 1.0 / c_cm_ns;
constexpr double GeVperkElectron = 3.61E-06;

class SimHitDistanceAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  SimHitDistanceAnalyzer(const edm::ParameterSet& );
  ~SimHitDistanceAnalyzer();
  void beginJob() override;
  void endJob() override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;
private:
  // ----------member data ---------------------------


  edm::ESGetToken<TrackerGeometry, TrackerDigiGeometryRecord> geom_esToken_;
  edm::ESGetToken<TrackerTopology, TrackerTopologyRcd> topo_esToken_;

  typedef vector<edm::InputTag> vInputTag;

  vInputTag vitSimHitSrc_;
  vector<edm::EDGetTokenT<edm::PSimHitContainer> > vsimHitToken_;

  vInputTag vitMixSimHitSrc_;
  vector<edm::EDGetTokenT<CrossingFrame<PSimHit> > > vmixsimHitToken_;

  edm::InputTag hepMCSrc_;
  edm::EDGetTokenT<edm::HepMCProduct> hepMCToken_;

  // ROOT output
  // all IT

  // TBPX
  TFileDirectory tbpxDir_;

  // per TBPX layers
  std::map<uint32_t, TFileDirectory> tbpxLayerDirs_;
  // standard SimHit
  std::map<uint32_t, TH1F*> map_h1_simhit_time_; 
  std::map<uint32_t, TH1F*> map_h1_simhit_n_;
  std::map<uint32_t, TH1F*> map_h1_simhit_charge_; 
  // SimHit from MixingModule
  std::map<uint32_t, TH1F*> map_h1_mixsimhit_time_; 
  std::map<uint32_t, TH1F*> map_h1_mixsimhit_n_;
  std::map<uint32_t, TH1F*> map_h1_mixsimhit_charge_; 
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
SimHitDistanceAnalyzer::SimHitDistanceAnalyzer( const edm::ParameterSet& pset ):
  geom_esToken_(esConsumes()),
  topo_esToken_(esConsumes()),
  hepMCSrc_("generatorSmeared",""),
  hepMCToken_(consumes<edm::HepMCProduct>(hepMCSrc_))
{
  usesResource("TFileService:kSharedResource");

  // accessing the collection ("type", "module", "label", "process")
  // vector<PSimHit>                       "g4SimHits"                 "TrackerHitsPixelBarrelHighTof"  "SIM"     
  // vector<PSimHit>                       "g4SimHits"                 "TrackerHitsPixelBarrelLowTof"   "SIM"     
  // vector<PSimHit>                       "g4SimHits"                 "TrackerHitsPixelEndcapHighTof"  "SIM"     
  // vector<PSimHit>                       "g4SimHits"                 "TrackerHitsPixelEndcapLowTof"   "SIM"     

  // SimHit 
  vitSimHitSrc_ = pset.getParameter<vInputTag>("srcPSimHit");
  for (const auto& itag : vitSimHitSrc_) 
    vsimHitToken_.push_back(consumes<edm::PSimHitContainer>(itag));

  vitMixSimHitSrc_ = pset.getParameter<vInputTag>("srcMixPSimHit");
  for (const auto& itag : vitMixSimHitSrc_) 
    vmixsimHitToken_.push_back(consumes<CrossingFrame<PSimHit> >(itag));

}

SimHitDistanceAnalyzer::~SimHitDistanceAnalyzer() {
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//
void SimHitDistanceAnalyzer::beginJob() {
    edm::Service<TFileService> fs; 

// all IT

// TBPX
    tbpxDir_ = fs->mkdir("TBPX");

// per TBPX layer
    char subdirname[6];
    for ( unsigned int layer = 0; layer<4; layer++ ) {
       sprintf(subdirname, "layer%d", layer+1);   
       tbpxLayerDirs_[layer]           = tbpxDir_.mkdir(subdirname);
       map_h1_simhit_time_[layer]      = tbpxLayerDirs_[layer].make<TH1F>("h1_simhit_time",      "h1_simhit_time",           60, -150, 150.);
       map_h1_simhit_n_[layer]         = tbpxLayerDirs_[layer].make<TH1F>("h1_simhit_n",         "h1_simhit_n",           10000, -0.5, 999999.5);
       map_h1_simhit_charge_[layer]    = tbpxLayerDirs_[layer].make<TH1F>("h1_simhit_charge",    "h1_simhit_charge",         32, -0.1, 31.9);
       map_h1_mixsimhit_time_[layer]   = tbpxLayerDirs_[layer].make<TH1F>("h1_mixsimhit_time",   "h1_mixsimhit_time",        60, -150, 150.);
       map_h1_mixsimhit_n_[layer]      = tbpxLayerDirs_[layer].make<TH1F>("h1_mixsimhit_n",      "h1_mixsimhit_n",        10000, -0.5, 999999.5);
       map_h1_mixsimhit_charge_[layer] = tbpxLayerDirs_[layer].make<TH1F>("h1_mixsimhit_charge", "h1_mixsimhit_charge",      32, -0.1, 31.9);
    }
}

void SimHitDistanceAnalyzer::endJob() {}

// ------------ method called to produce the data  ------------
void
SimHitDistanceAnalyzer::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup ) {
   const bool print = false;

   // geometry setup
   const TrackerGeometry* tkGeom = &iSetup.getData(geom_esToken_);
   // tracker topology from geometry
   const TrackerTopology* const tkTopo = &iSetup.getData(topo_esToken_);

   // analyze SimHit (per TBPX layer)
   int nsimhit_tbpx[4] = {};

   std::vector<PSimHit> itSimHits;

   for (const auto& itoken : vsimHitToken_) {
     auto itSimHitHandle = iEvent.getHandle(itoken);
     if (!itSimHitHandle.isValid())
       continue;
     const edm::PSimHitContainer& tmpSimHits = (*itSimHitHandle.product());
     itSimHits.insert(itSimHits.end(), tmpSimHits.begin(), tmpSimHits.end());      
   } 

   for (const auto& iSimHit : itSimHits) {
     if (print) cout << "SimHit charge: " << iSimHit.energyLoss() << endl;
     uint32_t detid = iSimHit.detUnitId();  
     DetId detId = DetId(detid);  // Get the Detid object
     if ( detId.subdetId() == PixelSubdetector::PixelBarrel ) {
       const Phase2TrackerGeomDetUnit* tkDetUnit = dynamic_cast<const Phase2TrackerGeomDetUnit*>(tkGeom->idToDetUnit(detId));
       uint32_t layer = tkTopo->pxbLayer(detId.rawId());
       double tofCorr = iSimHit.tof() - tkDetUnit->surface().toGlobal(iSimHit.localPosition()).mag() * c_inv;
       map_h1_simhit_time_[layer-1]->Fill(tofCorr); 
       if ( -5.<=tofCorr && tofCorr < +20. ) { // define the current BX as [-5ns,+20ns]
	 nsimhit_tbpx[layer-1]++;
	 map_h1_simhit_charge_[layer-1]->Fill(iSimHit.energyLoss()/GeVperkElectron );  //convert GeV to ke 
       }
     }
   }
  
   for ( int ll=0; ll<4; ll++){
     map_h1_simhit_n_[ll]->Fill(nsimhit_tbpx[ll]);
   }

   // analyze MixingModule SimHit (per TBPX layer)
   int nmixsimhit_tbpx[4] = {};

   //$  next section requires to be cleaned up 
   for (const auto& itoken : vmixsimHitToken_) {
     edm::Handle<CrossingFrame<PSimHit> > cf_simhit_H;
     
     bool found = iEvent.getByToken(itoken, cf_simhit_H);
     if (!found || !cf_simhit_H.isValid()) continue;

     std::unique_ptr<MixCollection<PSimHit> > coll(new MixCollection<PSimHit>(cf_simhit_H.product()));
     for(MixCollection<PSimHit>::iterator isim = coll->begin(); isim != coll->end(); ++isim){
       //if (print) cout << "MixSimHit charge: " <<  (*isim).energyLoss() << endl;
       // int tkid = (*isim).trackId();
       // if (tkid <= 0) continue;
       
       const PSimHit& iSimHit = (*isim);
       uint32_t detid = iSimHit.detUnitId();  
       DetId detId = DetId(detid);  // Get the Detid object
       if ( detId.subdetId() == PixelSubdetector::PixelBarrel ) {
	 const Phase2TrackerGeomDetUnit* tkDetUnit = dynamic_cast<const Phase2TrackerGeomDetUnit*>(tkGeom->idToDetUnit(detId));
	 uint32_t layer = tkTopo->pxbLayer(detId.rawId());
	 double tofCorr = iSimHit.tof() - tkDetUnit->surface().toGlobal(iSimHit.localPosition()).mag() * c_inv;
	 map_h1_mixsimhit_time_[layer-1]->Fill(tofCorr); 
	 if ( -5.<=tofCorr && tofCorr < +20. ) { // define the current BX as [-5ns,+20ns]
	   nmixsimhit_tbpx[layer-1]++;
	   map_h1_mixsimhit_charge_[layer-1]->Fill(iSimHit.energyLoss()/GeVperkElectron );  //convert GeV to ke 	   
	 }
       }
     }
     //$
   } 
   for ( int ll=0; ll<4; ll++){
     map_h1_mixsimhit_n_[ll]->Fill(nmixsimhit_tbpx[ll]);
   }

// #ifdef HEPMC
//    const bool printGenParticles = false;
//    if(printGenParticles) {
//      const HepMC::GenEvent* myGenEvent = MCEvt->GetEvent() ;
//      if(print) cout<<" Print HepMC "<<endl;
//      int i=0;
//      for ( HepMC::GenEvent::particle_const_iterator p = myGenEvent->particles_begin();
// 	   p != myGenEvent->particles_end(); ++p, ++i ) {
//        if(print) 
// 	 cout<< "Particle from MC = "<<(i+1)<<" type "<< abs((*p)->pdg_id())<<" status "<< (*p)->status()
// 	     << " ,Pt/Eta = "<< (*p)->momentum().perp()<<" "<< (*p)->momentum().eta()<<endl;  
//      }   
//    }

// #endif // HEPMC


/*
    std::unique_ptr<MixCollection<PSimHit>> col( new MixCollection<PSimHit>(cf_simhit.product(), std::pair<int, int>(-1, 1)) );
    std::cout << *(col.get()) << std::endl;
    MixCollection<PSimHit>::iterator cfi;
    for (cfi = col->begin(); cfi != col->end(); cfi++) {
      std::cout << " Hit " << count << " has tof " << cfi->timeOfFlight() << " trackid " << cfi->trackId()
                << " bunchcr " << cfi.bunch() << " trigger " << cfi.getTrigger()
                << ", from EncodedEventId: " << cfi->eventId().bunchCrossing() << " " << cfi->eventId().event()
                << "  bcr from MixCol " << cfi.bunch() << std::endl;
      //      std::cout<<" Hit: "<<(*cfi)<<std::endl;
      count++;
    }
*/

}

//define this as a plug-in
DEFINE_FWK_MODULE(SimHitDistanceAnalyzer);
