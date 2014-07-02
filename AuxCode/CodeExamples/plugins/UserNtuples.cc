// -*- C++ -*-
//
// Package:    UserNtuples
// Class:      UserNtuples
// 
/**\class UserNtuples UserNtuples.cc AuxCode/CodeExamples/src/UserNtuples.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Ernesto Migliore,13 2-017,+41227672059,
//         Created:  Wed Jul  2 08:42:10 CEST 2014
// $Id$
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

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "AuxCode/CodeExamples/interface/MyObject.h"

#include <TTree.h>

//
// class declaration
//

class UserNtuples : public edm::EDAnalyzer {
   public:
      explicit UserNtuples(const edm::ParameterSet&);
      ~UserNtuples();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      virtual void endRun(edm::Run const&, edm::EventSetup const&);
      virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      // ----------member data ---------------------------
  edm::Service<TFileService> p_fileservice;

  MyObject * p_myobject;
  TTree * p_tree;
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
UserNtuples::UserNtuples(const edm::ParameterSet& iConfig)

{
   //now do what ever initialization is needed

}


UserNtuples::~UserNtuples()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
UserNtuples::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;


   p_myobject->set_run(iEvent.id().run());
   p_myobject->set_event(iEvent.id().event());
   p_tree->Fill();
}


// ------------ method called once each job just before starting event loop  ------------
void 
UserNtuples::beginJob()
{
  p_tree = p_fileservice->make<TTree>("UserObjectTree", "Example of tree with user-defined objects", 0);
  p_myobject = new MyObject;
  p_tree->Branch("MyObject", &p_myobject);  
}

// ------------ method called once each job just after ending the event loop  ------------
void 
UserNtuples::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
UserNtuples::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
UserNtuples::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
UserNtuples::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
UserNtuples::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
UserNtuples::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(UserNtuples);
