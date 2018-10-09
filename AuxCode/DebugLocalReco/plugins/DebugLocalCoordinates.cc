// -*- C++ -*-
//
// Package:    AuxCode/DebugLocalReco
// Class:      DebugLocalCoordinates
//
/**\class DebugLocalCoordinates DebugLocalCoordinates.cc AuxCode/DebugLocalReco/plugins/DebugLocalCoordinates.cc

 Description: print out direction of local-detId (x,y,z) into global-CMS (x,y,z) coordinates

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Ernesto Migliore
//         Created:  Tue, 25 Sep 2018 08:36:33 GMT
//
//


// system include files
#include <memory>
#include <iostream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/GeometryVector/interface/LocalPoint.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"
#include "DataFormats/SiPixelDetId/interface/PixelSubdetector.h"

#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h" 

#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/TrackerGeometryBuilder/interface/PixelGeomDetUnit.h"


//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<>
// This will improve performance in multithreaded jobs.


class DebugLocalCoordinates : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit DebugLocalCoordinates(const edm::ParameterSet&);
      ~DebugLocalCoordinates();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

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
DebugLocalCoordinates::DebugLocalCoordinates(const edm::ParameterSet& iConfig)
{
   //now do what ever initialization is needed

}


DebugLocalCoordinates::~DebugLocalCoordinates()
{

   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
DebugLocalCoordinates::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   //Retrieve tracker topology from geometry
   edm::ESHandle<TrackerTopology> tTopoHandle;
   iSetup.get<TrackerTopologyRcd>().get(tTopoHandle);
   const TrackerTopology* const tTopo = tTopoHandle.product();
 
   //Retrieve old style tracker geometry from geometry
   edm::ESHandle<TrackerGeometry> tGeometryHandle;
   iSetup.get<TrackerDigiGeometryRecord>().get(tGeometryHandle);
   const TrackerGeometry* const tGeometry = tGeometryHandle.product();
   std::cout<<" There are "<< tGeometry->detUnits().size() << " detectors"<< std::endl;
   
   LocalPoint lp0(0.,0.,0.), lpX(1.,0.,0.), lpY(0.,1.,0.), lpZ(0.,0.,1.);

   //for(TrackerGeometry::DetContainer::const_iterator it = tGeometry->detUnits().begin(); 
   for(auto it = tGeometry->detUnits().begin(); it != tGeometry->detUnits().end(); it++){
       
     // for phase2 this does not select the inner tracker module but all modules 
     const PixelGeomDetUnit * pixelGeomDetUnit = dynamic_cast<PixelGeomDetUnit const*>(*it);
     if( pixelGeomDetUnit!=0 ) {
       const DetId detId = (*it)->geographicalId();
       //       auto detType= detid.det(); // det type, tracker=1
       auto rawId = detId.rawId();

       // cout<<detType<<endl;
       // fill bpix values for LA 
       if( detId.subdetId() == static_cast<int>(PixelSubdetector::PixelBarrel) ) {
	       
	 // 
	 // std::cout <<" pixel barrel:" 
	 // 	   <<" layer=" << tTopo->pxbLayer(rawId) << " ladder=" << tTopo->pxbLadder(rawId) << " module=" << tTopo->pxbModule(rawId)
	 // 	   <<" rawId=" << rawId << std::endl;

	 if ( tTopo->pxbLayer(rawId) == 1 && tTopo->pxbModule(rawId) == 5 ) { // select module in mid-barrel

	   const GeomDet * geomDet( tGeometry->idToDet(detId) );
	   GlobalPoint gp0 = geomDet->surface().toGlobal(lp0);
	   GlobalPoint gpX = geomDet->surface().toGlobal(lpX);
	   GlobalPoint gpY = geomDet->surface().toGlobal(lpY);
	   GlobalPoint gpZ = geomDet->surface().toGlobal(lpZ);

	   std::cout <<" pixel barrel:" 
		     <<" layer=" << tTopo->pxbLayer(rawId) << " ladder="<< tTopo->pxbLadder(rawId) << " module="<< tTopo->pxbModule(rawId)
	     	     <<" rawId=" << rawId 
		     << gp0 << " " << gpX << " " << gpY << " " << gpZ << std::endl;

	 }



	       
	 // fill fpix values for LA (for phase2 fpix & epix)
       } else if( detId.subdetId() == static_cast<int>(PixelSubdetector::PixelEndcap )) {

	 // // for phase2: ring=blade, panel==1 
	 // std::cout << " pixel endcap:" 
	 // 	   << " side=" << tTopo->pxfSide(detId) << " disk=" <<  tTopo->pxfDisk(detId) << " blade(ring)=" <<  tTopo->pxfBlade(detId) << " panel="<<  tTopo->pxfPanel(detId) << "  module=" << tTopo->pxfModule(detId) << "  rawId=" << rawId << std::endl;
	       
       }
     }
   }

}


// ------------ method called once each job just before starting event loop  ------------
void
DebugLocalCoordinates::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
DebugLocalCoordinates::endJob()
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
DebugLocalCoordinates::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

  //Specify that only 'tracks' is allowed
  //To use, remove the default given above and uncomment below
  //ParameterSetDescription desc;
  //desc.addUntracked<edm::InputTag>("tracks","ctfWithMaterialTracks");
  //descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(DebugLocalCoordinates);
