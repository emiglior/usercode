#include "TH1F.h"
#include "TProfile.h"
#include "TFile.h"
#include "TLorentzVector.h"

#include "RooDataSet.h"
#include "RooRealVar.h"

using namespace RooFit;

class CollinsSoperAnalysis {
public:
  // default values for mLL and yLL range correspond essentially to no cuts
  CollinsSoperAnalysis(TFile *, double m1=0., double m2=10000., double y1=-1000., double y2=+1000., const char * append="");
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
  TH1F * h1_cosThetaCS_pos;
  TH1F * h1_cosThetaCS_neg;
  TH1F * h1_phiCS;  
  TProfile * hp_cosThetaCS;
  TProfile * hp_phiCS;

  double mLL_low, mLL_high;
  double yLL_low, yLL_high;
  double AfbValRaw, AfbErrorRaw;
  double AfbValFit, AfbErrorFit;
  
  RooRealVar * rrv_c;
  //  RooRealVar * rrv_w;  
  RooDataSet * rds_cosThetaCS;
};


