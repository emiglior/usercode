#ifndef HELPERS_H
#define HELPERS_H

#include "TLorentzVector.h"
#include "TH1F.h"

double * computeCollinsSoperAngles(const TLorentzVector & muNeg, const TLorentzVector & muPos); 

// collection of user defined parameters of the analysis

namespace global_parameters{
  // GeV -> TeV conversion
  const double GeVToTeV = 0.001;
  
  // PDG
  const double mass_Z(91.188);  
  
  // analysis is limited in [-cosThetaCS_max,+cosThetaCS_max] range
  // static const double cosThetaCS_max(0.5);
  const double cosThetaCS_max(1.);
  
  // min pT for GeneralizedEndPoint analysis
  const double pt_lep = 50.;
  const double up_limit = 1./pt_lep;
  
  const int binning = 40;
  const float dk_step = 0.00005; // dk_step = 0.000004; // original
  
  // target Afb
  const double AfbFIXED = 0.05;
}

#endif
