#ifndef HELPERS_H
#define HELPERS_H

#include "TLorentzVector.h"
#include "TH1F.h"

#include<vector>

double * computeCollinsSoperAngles(const TLorentzVector & muNeg, const TLorentzVector & muPos); 

std::vector<double> computeCurvatureVariableBins(const double pT_ini);
  
// collection of user defined parameters of the analysis

namespace global_parameters{
  // GeV -> TeV conversion
  const double GeVToTeV = 0.001;
  
  // PDG
  const double mass_Z = 91.188;  // [GeV/c**2]
  
  // analysis is limited in [-cosThetaCS_max,+cosThetaCS_max] range
  // static const double cosThetaCS_max(0.5);
  const double cosThetaCS_max(1.);
  
  // min pT for GeneralizedEndPoint analysis
  const double pt_lep = 100.; // [GeV/c]
  const double up_limit = 1./(pt_lep*GeVToTeV); // [c/TeV]
  
  const int binningKS = 200;
  const double dk_step = 0.01; // [c/TeV]
  
  // target Afb
  const double AfbFIXED = 0.05;
}

#endif
