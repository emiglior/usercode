#include "TH1F.h"
#include "TProfile.h"
#include "TFile.h"
#include "TLorentzVector.h"

#include "RooDataSet.h"
#include "RooRealVar.h"

using namespace RooFit;

class CollinsSoperAnalysis {
public:
  CollinsSoperAnalysis(TFile *, double m1=50., double m2=150., const char * append="");
  ~CollinsSoperAnalysis();
  void analyze(const TLorentzVector & muNeg, const TLorentzVector & muPos, double weight=1.);
  void endjob();
  double getAfbRaw() {return AfbValRaw;}
  double getAfbErrorRaw() {return AfbErrorRaw;}
  double getAfbFit() {return AfbValFit;}
  double getAfbErrorFit() {return AfbErrorFit;}
    
private:
  TDirectory * the_dir;
  TH1F * h1_cosThetaCS;
  TH1F * h1_phiCS;  
  TProfile * hp_cosThetaCS;
  TProfile * hp_phiCS;

  double mLL_low, mLL_high;
  int nBelowZ, nAboveZ; 
  double AfbValRaw, AfbErrorRaw;
  double AfbValFit, AfbErrorFit;
  
  RooRealVar * rrv_c;  
  RooDataSet * rds_cosThetaCS;
};


