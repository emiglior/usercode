// -*- C++ -*-
//
// Package:    SimTruthChecks
// Class:      SimTruthChecks
// 
/**\class SimTruthChecks SimTruthChecks.cc AuxCode/SLCHSimPhase2/plugins/SimTruthChecks.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Marco Musich
//         Created:  Wed, 25 Mar 2015 08:46:08 GMT
// $Id$
//
//


// system include files
#include <memory>
#include <iomanip>      // std::setw

// ROOT
#include "TH2D.h"
#include "TProfile.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "SimDataFormats/TrackingHit/interface/PSimHit.h"
#include "SimDataFormats/TrackingHit/interface/PSimHitContainer.h"
#include "DataFormats/SiPixelDetId/interface/PixelSubdetector.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

// DataFormats
#include "DataFormats/DetId/interface/DetId.h"
#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"

// Geometry
#include "MagneticField/Engine/interface/MagneticField.h"
#include "Geometry/CommonDetUnit/interface/GeomDetType.h"
#include "Geometry/CommonDetUnit/interface/GeomDetUnit.h"
#include "Geometry/Records/interface/IdealGeometryRecord.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "Geometry/TrackerGeometryBuilder/interface/PixelGeomDetUnit.h"
#include "Geometry/TrackerGeometryBuilder/interface/PixelGeomDetType.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"

// 20/Jul/2014 Mark Grimes - temporary hack to remap the DetIds from old SLHC11 input
// files. As soon as this functionality is no longer needed this should be taken out.
#include <FWCore/ServiceRegistry/interface/Service.h>
#include <SimTracker/SiPixelDigitizer/interface/RemapDetIdService.h>

//
// class declaration
//

class SimTruthChecks : public edm::EDAnalyzer {
   public:
      explicit SimTruthChecks(const edm::ParameterSet&);
      ~SimTruthChecks();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
 
      // ----------member data ---------------------------
      typedef std::vector<std::string> vstring;
      vstring trackerContainers;
      bool debug_;
      TH2D *h2_HitMapRZ;
      TH2D *h2_HitMapRPhi; 
      TProfile *p_ThicknessVsRho;
};

//
// constructors and destructor
//
SimTruthChecks::SimTruthChecks(const edm::ParameterSet& iConfig):
  debug_(iConfig.getUntrackedParameter<bool>("verbose",false))
{
   //now do what ever initialization is needed
   //
   // Take by default all tracker SimHits
   //
 
  trackerContainers.push_back("TrackerHitsPixelBarrelLowTof");
  trackerContainers.push_back("TrackerHitsPixelBarrelHighTof");
  trackerContainers.push_back("TrackerHitsPixelEndcapLowTof");
  trackerContainers.push_back("TrackerHitsPixelEndcapHighTof");
  
}


SimTruthChecks::~SimTruthChecks(){}

//
// member functions
//

// ------------ method called for each event  ------------
void
SimTruthChecks::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
 
   //Retrieve tracker topology from geometry
   edm::ESHandle<TrackerTopology> tTopoHandle;
   iSetup.get<IdealGeometryRecord>().get(tTopoHandle);
   const TrackerTopology* const tTopo = tTopoHandle.product();

   // geometry setup
   edm::ESHandle<TrackerGeometry> geometry;
   iSetup.get<TrackerDigiGeometryRecord>().get(geometry);
   const TrackerGeometry* theGeometry = &(*geometry);

   // 20/Jul/2014 Mark Grimes - temporary hack to remap the DetIds from old SLHC11 input
   // files. As soon as this functionality is no longer needed this should be taken out.
   edm::Service<simtracker::services::RemapDetIdService> detIdRemapService;

   for(auto const& trackerContainer : trackerContainers) {
     //Retrieve the simhit vector
     edm::Handle<std::vector<PSimHit> > simHits;
     edm::InputTag tag_hits("g4SimHits", trackerContainer);
     detIdRemapService->getByLabel(iEvent,tag_hits,simHits);
     for (std::vector<PSimHit>::const_iterator isim = simHits->begin(); isim != simHits->end(); isim++) {
       DetId detId((*isim).detUnitId());

       unsigned int subid = detId.subdetId();
       int detid_db = detId.rawId();

       int layer_num = -99;
       //int ladder_num=-99,module_num=-99,disk_num=-99,blade_num=-99,panel_num=-99,side_num=-99;
       if ( ( subid == PixelSubdetector::PixelBarrel ) || ( subid == PixelSubdetector::PixelEndcap ) ) {
	 // 1 = PXB, 2 = PXF
	 if ( subid == PixelSubdetector::PixelBarrel ) {
	   layer_num = tTopo->pxbLayer(detId.rawId());

	   //ladder_num = tTopo->pxbLadder(detId.rawId());
	   //module_num = tTopo->pxbModule(detId.rawId());
	   // std::cout <<"\ndetId = "<<subid<<" : "<<tTopo->pxbLayer(detId.rawId())<<" , "<<tTopo->pxbLadder(detId.rawId())<<" , "<< tTopo->pxbModule(detId.rawId());

	 } else if ( subid == PixelSubdetector::PixelEndcap ) {
	   
	   //module_num = tTopo->pxfModule(detId());
	   //disk_num = tTopo->pxfDisk(detId());
	   //blade_num = tTopo->pxfBlade(detId());
	   //panel_num = tTopo->pxfPanel(detId());
	   //side_num = tTopo->pxfSide(detId());
	   
	 }
	 
	 if( (subid == PixelSubdetector::PixelBarrel) && (layer_num<=4) ){

	   float sim_z1 = (*isim).entryPoint().z();
	   float sim_z2 = (*isim).exitPoint().z();
	   float sim_zpos = 0.5*(sim_z1+sim_z2);

	   int pdgid  = (*isim).particleType();
	   int process= (*isim).processType();

	   float sim_x1 = (*isim).entryPoint().x();
	   float sim_x2 = (*isim).exitPoint().x();
	   float sim_xpos = 0.5*(sim_x1+sim_x2);
	   float sim_y1 = (*isim).entryPoint().y();
	   float sim_y2 = (*isim).exitPoint().y();
	   float sim_ypos = 0.5*(sim_y1+sim_y2);
	    
	   LocalPoint lp = LocalPoint(sim_xpos,sim_ypos,sim_zpos);

	   const GeomDet* geomDet( theGeometry->idToDet(detId) );
	   GlobalPoint GP0 = geomDet->surface().toGlobal(lp);

	   float thickness = fabs(sim_z2-sim_z1)*10000;

	   if(process==2){
	     if(debug_) {std::cout<< "simHit pdgId: " << std::setw(5) << pdgid << "| process: " << std::setw(3) << process 
				  << "| detId: "<< detid_db <<"| subid: "<<subid<<"| layer:"<<layer_num << "| thickness [um]: "<<thickness<<std::endl;}
	     
	     h2_HitMapRZ->Fill(GP0.z(),GP0.perp());        
	     h2_HitMapRPhi->Fill(GP0.x(),GP0.y());    
	     p_ThicknessVsRho->Fill(GP0.perp(),thickness);
	   }
	 }
       }
     }  
   }
}


// ------------ method called once each job just before starting event loop  ------------
void 
SimTruthChecks::beginJob()
{
 
  edm::Service<TFileService> fs;
 
  h2_HitMapRZ        = fs->make<TH2D>("h2_HitMapRZ"," HitMap (r-z) view; global r [cm]; global z [cm]",120,-60,60,180,0.,18);	     
  h2_HitMapRPhi      = fs->make<TH2D>("h2_HitMapRPhi"," HitMap (r-#phi) view; global x [cm]; global y [cm]",360,-18,18,360,-18,18);	     
  p_ThicknessVsRho   = fs->make<TProfile>("p_ThicknessVsRho","Sensor thickness vs SimHit #rho [cm];SimHit #rho [cm]; sensor thickness [#mum]",1000,0,100);

}

// ------------ method called once each job just after ending the event loop  ------------
void 
SimTruthChecks::endJob() {}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
SimTruthChecks::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(SimTruthChecks);
