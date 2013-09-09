/** \class ImpactParameterCuts
 *  No description available.
 *
 *  $Date: 2012/02/08 15:24:51 $
 *  $Revision: 1.2 $
 *  \author R. Bellan - UCSB <riccardo.bellan@cern.ch>
 */

#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/EgammaCandidates/interface/Electron.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/Math/interface/Vector3D.h"

namespace reco{
  typedef edm::Ref<std::vector<Muon> > MuonRef;
}

class ImpactParameterCuts: public edm::EDFilter {

public:

  enum LeptonType {Muon,Electron};

  /// Constructor
  ImpactParameterCuts(const edm::ParameterSet& pset);

  /// Destructor
  virtual ~ImpactParameterCuts(){};

  // Operations
  virtual bool filter(edm::Event &, const edm::EventSetup&);

  bool checkMuons(edm::Event &event, const edm::EventSetup&eSetup);
  bool checkElectrons(edm::Event &event, const edm::EventSetup&eSetup);

protected:

private:
  edm::InputTag theInputLabel;
  edm::InputTag theVtxLabel;

  LeptonType type_;

  
  double theDxyCut;
  double theZCut;
  int minNum_;
  int filter_;

};


ImpactParameterCuts::ImpactParameterCuts(const edm::ParameterSet& pset)
  : theInputLabel(pset.getParameter<edm::InputTag>("Input"))
  , theVtxLabel(pset.getParameter<edm::InputTag>("VtxCollection"))
  , theDxyCut(pset.getParameter<double>("dXYcut"))
  , theZCut(pset.getParameter<double>("dZcut"))
  , minNum_(pset.getParameter<int>("MinNum"))
  , filter_(pset.getParameter<bool>("filter")){

  std::string type = pset.getParameter<std::string>("TypeOfInput");
  if(type == "muon"){
    type_ = ImpactParameterCuts::Muon;
    produces<std::vector<reco::Muon> >();
  }
  if(type == "electron"){
    type_ = ImpactParameterCuts::Electron;
    produces<std::vector<reco::Electron> >();
  }
}

bool ImpactParameterCuts::checkMuons(edm::Event &event, const edm::EventSetup&eSetup){

  edm::Handle<std::vector<reco::Muon> > muons;
  event.getByLabel(theInputLabel, muons);

  edm::Handle<std::vector<reco::Vertex> > vertices;
  event.getByLabel(theVtxLabel, vertices);
  
  if (vertices->empty() || vertices->front().isFake()) return false;

  reco::MuonRef::key_type muIndex = 0;
  
  std::auto_ptr<std::vector<reco::Muon> >    output(new std::vector<reco::Muon>());
  std::auto_ptr<std::vector<reco::MuonRef> > outputRef(new std::vector<reco::MuonRef>());

  int count = 0;
  for(std::vector<reco::Muon>::const_iterator muon = muons->begin(); muon != muons->end(); ++muon, ++muIndex){
    if (muon->innerTrack().isNonnull()){
      if(fabs(muon->innerTrack()->dxy(vertices->front().position())) >= theDxyCut) continue;
      if(fabs(muon->innerTrack()->dz(vertices->front().position())) >= theZCut) continue;
    }
    output->push_back(reco::Muon(*muon));

    outputRef->push_back(reco::MuonRef(muons, muIndex));
    
    ++count;

  }

  event.put(output);
  //event.put(outputRef);
  return filter_ ? count >= minNum_ : true;


}


bool ImpactParameterCuts::checkElectrons(edm::Event &event, const edm::EventSetup&eSetup){

  edm::Handle<std::vector<reco::Electron> > electrons;
  event.getByLabel(theInputLabel, electrons);

  edm::Handle<std::vector<reco::Vertex> > vertices;
  event.getByLabel(theVtxLabel, vertices);
  
  if (vertices->empty() || vertices->front().isFake()) return false;

  std::auto_ptr<std::vector<reco::Electron> >    output(new std::vector<reco::Electron>());

  int count = 0;
  for(std::vector<reco::Electron>::const_iterator electron = electrons->begin(); electron != electrons->end(); ++electron){
    if(fabs(electron->gsfTrack()->dxy(vertices->front().position()))       >= theDxyCut) continue;
    if(fabs(electron->gsfTrack()->vz() - vertices->front().position().z()) >= theZCut) continue;
    
    output->push_back(reco::Electron(*electron));

    ++count;

  }

  event.put(output);
  //event.put(outputRef);
  return filter_ ? count >= minNum_ : true;


}


bool ImpactParameterCuts::filter(edm::Event &event, const edm::EventSetup&eSetup){
 
  if(type_ == ImpactParameterCuts::Muon)
    return checkMuons(event, eSetup);
  else if(type_ == ImpactParameterCuts::Electron)
    return checkElectrons(event, eSetup);
  else
    return !filter_;
      

}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(ImpactParameterCuts);
