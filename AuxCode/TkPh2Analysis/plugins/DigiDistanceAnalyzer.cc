// -*- C++ -*-
//
// Package:    MyAnalyzer
// Class:      DigiDistanceAnalyzer
// 
/**\class DigiDistanceAnalyzer DigiDistanceAnalyzer.cc test/DigiDistanceAnalyzer.cc

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
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/TrackerNumberingBuilder/interface/GeometricDet.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"

#include "DataFormats/Common/interface/DetSetVector.h"
#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"
#include "DataFormats/SiPixelDetId/interface/PixelSubdetector.h"

#include "DataFormats/SiPixelDigi/interface/PixelDigi.h"
#include "DataFormats/SiPixelDigi/interface/PixelDigiCollection.h"

#include "SimDataFormats/TrackerDigiSimLink/interface/PixelDigiSimLink.h"

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

class DigiDistanceAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  DigiDistanceAnalyzer(const edm::ParameterSet& );
  ~DigiDistanceAnalyzer();
  void beginJob() override;
  void endJob() override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;
private:
      // ----------member data ---------------------------
  edm::ESGetToken<TrackerGeometry, TrackerDigiGeometryRecord> geom_esToken_;
  edm::ESGetToken<TrackerTopology, TrackerTopologyRcd> topo_esToken_;

  // edm::InputTag itPixelDigiSrc_;
  edm::EDGetTokenT<edm::DetSetVector<PixelDigi> > itPixelDigiToken_;

  // edm::InputTag itPixelDigiSimLinkSrc_;
  edm::EDGetTokenT<edm::DetSetVector<PixelDigiSimLink> > itPixelDigiSimLinkToken_;

  edm::InputTag hepMCSrc_;
  edm::EDGetTokenT<edm::HepMCProduct> hepMCToken_;

  // ROOT output
  // all IT

  // TBPX
   TFileDirectory tbpxDir_;

  // per TBPX layers
   std::map<uint32_t, TFileDirectory> tbpxLayerDirs_;
   std::map<uint32_t, TH1F*> map_h1_digi_n_;
   std::map<uint32_t, TH1F*> map_h1_digimatched_n_;
   std::map<uint32_t, TH1F*> map_h1_digi_ToT_; 

  unsigned int getSimTrackId(const edm::Handle<edm::DetSetVector<PixelDigiSimLink> >& simLinks,
			     const DetId& detId,
			     unsigned int& channel);
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
DigiDistanceAnalyzer::DigiDistanceAnalyzer( const edm::ParameterSet& pset ):
  geom_esToken_(esConsumes()),
  topo_esToken_(esConsumes()),

  // accessing the collection ("type", "module", "label", "process")
  // edm::DetSetVector<PixelDigi>          "simSiPixelDigis"           "Pixel"           "HLT"     
  // itPixelDigiSrc_("simSiPixelDigis","Pixel"),  
  // itPixelDigiToken_(consumes<edm::DetSetVector<PixelDigi> >(itPixelDigiSrc_)),
  itPixelDigiToken_(consumes<edm::DetSetVector<PixelDigi> >(pset.getParameter<edm::InputTag>("srcITPixelDigi"))),

  // accessing the collection ("type", "module", "label", "process")
  // edm::DetSetVector<PixelDigiSimLink>    "simSiPixelDigis"           "Pixel"           "HLT"     
  // itPixelDigiSimLinkSrc_("simSiPixelDigis","Pixel"),
  // itPixelDigiSimLinkToken_(consumes<edm::DetSetVector<PixelDigiSimLink> >(itPixelDigiSimLinkSrc_)),
  itPixelDigiSimLinkToken_(consumes<edm::DetSetVector<PixelDigiSimLink> >(pset.getParameter<edm::InputTag>("srcITPixelDigiSimLink"))),
  hepMCSrc_("generatorSmeared",""),
  hepMCToken_(consumes<edm::HepMCProduct>(hepMCSrc_))
{
  usesResource("TFileService:kSharedResource");
}

DigiDistanceAnalyzer::~DigiDistanceAnalyzer() {
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//
void DigiDistanceAnalyzer::beginJob() {
    edm::Service<TFileService> fs; 

// all IT

// TBPX
    tbpxDir_ = fs->mkdir("TBPX");

// per TBPX layer
    char subdirname[6];
    for ( unsigned int layer = 0; layer<4; layer++ ) {
       sprintf(subdirname, "layer%d", layer+1);   
       tbpxLayerDirs_[layer]        = tbpxDir_.mkdir(subdirname);
       map_h1_digi_n_[layer]        = tbpxLayerDirs_[layer].make<TH1F>("h1_digi_n",        "h1_digi_n",         10000, -0.5, 99999.5);
       map_h1_digimatched_n_[layer] = tbpxLayerDirs_[layer].make<TH1F>("h1_digimatched_n", "h1_digimatched_n",  10000, -0.5, 99999.5);
       map_h1_digi_ToT_[layer]      = tbpxLayerDirs_[layer].make<TH1F>("h1_digi_ToT",      "h1_digi_ToT",          16, -0.5,    15.5);
    }
}

void DigiDistanceAnalyzer::endJob() {}

// ------------ method called to produce the data  ------------
void
DigiDistanceAnalyzer::analyze( const edm::Event& iEvent, const edm::EventSetup& iSetup ) {
   const bool print = false;

   // geometry setup
   const TrackerGeometry* theGeometry = &iSetup.getData(geom_esToken_);
   // tracker topology from geometry
   const TrackerTopology* const tTopo = &iSetup.getData(topo_esToken_);

   // DigiSimLink
   auto itDigiSimLink = iEvent.getHandle(itPixelDigiSimLinkToken_);
   if ( !itDigiSimLink.isValid() ) {
     return;
     // add an exception if not valid ?
   }

   // analyze digi (per TBPX layer)
   int ndigi_tbpx[4] = {};
   int ndigimatched_tbpx[4] = {};

   auto itDigis = iEvent.getHandle(itPixelDigiToken_); 
   if ( itDigis.isValid() ) {

     edm::DetSetVector<PixelDigi>::const_iterator DSViter;
     for ( DSViter = itDigis->begin(); DSViter!= itDigis->end(); ++DSViter ) {
       uint32_t detid = DSViter->id;  
       DetId detId = DetId(detid);  // Get the Detid object
       if ( detId.subdetId() == PixelSubdetector::PixelBarrel ) {
   	 uint32_t layer = tTopo->pxbLayer(detId.rawId());
	 edm::DetSet<PixelDigi>::const_iterator DSiter_digi;
	 for ( DSiter_digi = DSViter->data.begin(); DSiter_digi != DSViter->data.end(); ++DSiter_digi ) {
	   ndigi_tbpx[layer-1]++;
	   map_h1_digi_ToT_[layer-1]->Fill(DSiter_digi->adc());
	   //  map_h1_digi_ToT_[layer-1]->Fill(DSiter_digi->row());
	   //  map_h1_digi_ToT_[layer-1]->Fill(DSiter_digi->column());

	   // Digi-SimTrack matching based on Validation/SiTrackerPhase2V Phase2TrackerValidateDigi 
	   // NB: SimTrack needed as inter-digi distance should be computed only for digis from different SimHits
	   int col = DSiter_digi->column();  // column
	   int row = DSiter_digi->row();     // row
	   unsigned int channel = PixelDigi::pixelToChannel(row, col);
	   unsigned int simTkId = getSimTrackId(itDigiSimLink, detId, channel);
	   if (simTkId != 0) ndigimatched_tbpx[layer-1]++;
	 }
       }      
     }
   }

   for ( int ll=0; ll<4; ll++){
     map_h1_digi_n_[ll]->Fill(ndigi_tbpx[ll]);
     map_h1_digimatched_n_[ll]->Fill(ndigimatched_tbpx[ll]);
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

}

//
// -- Get SimTrack Id
//
unsigned int DigiDistanceAnalyzer::getSimTrackId(const edm::Handle<edm::DetSetVector<PixelDigiSimLink> >& simLinks,
                                                 const DetId& detId,
                                                 unsigned int& channel) {

  unsigned int simTrkId(0);
  edm::DetSetVector<PixelDigiSimLink>::const_iterator DSViter(simLinks->find(detId));
  if ( DSViter == simLinks->end() )
    return simTrkId;

  // Loop over DigiSimLink in this det unit  
  edm::DetSet<PixelDigiSimLink>::const_iterator DSiter_digisim;
  for ( DSiter_digisim = DSViter->data.begin(); DSiter_digisim != DSViter->data.end(); ++DSiter_digisim ) {
    if (channel == DSiter_digisim->channel()) {
      simTrkId = DSiter_digisim->SimTrackId();
      break;
    }
  }
  return simTrkId;
}

//define this as a plug-in
DEFINE_FWK_MODULE(DigiDistanceAnalyzer);
