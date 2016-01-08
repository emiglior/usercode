#include "TH1F.h"
#include "TFile.h"
#include "TLorentzVector.h"

#include <iostream>
#include <fstream>

using namespace std;

class GeneralizedEndPointAnalysisOld {
public:
  GeneralizedEndPointAnalysisOld(TFile *, const char * append="");
  ~GeneralizedEndPointAnalysisOld();
  void analyze(const TLorentzVector & muNeg, const TLorentzVector & muPos, double weight=1.);
  void endjob() {;} 
    
private:
  TDirectory * the_dir;

  TH1F * h_pt_neg; 
  TH1F * h_pt_pos; 
  TH1F * h_ptinv_neg; 
  TH1F * h_ptinv_pos; 
  TH1F * h_cosThetaCS;
  TH1F * h_cosThetaCS_tail;
  TH1F * h_mLL;
  TH1F * h_mLL_tail;
  
  ofstream outfile;
};



