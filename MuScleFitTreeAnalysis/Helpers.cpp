//
// Module containing helper functions
//
#include "Helpers.h"

#include "TVector3.h"

#include <cmath>
#include <algorithm>

#include <iostream>

using namespace std;

vector<double> computeCurvatureVariableBins(const double pT_ini) {
  // Parametrization of pT resolution based on MuScleFit studies
  const double q0=2.5e-4/global_parameters::GeVToTeV; // Hit Resoultion
  const double qk=1e-2;                               // MS

  vector<double> k_bins;
  
  double k = 1./pT_ini;
  double sigma_k;
  
  while (k > 0) {
    sigma_k = q0 + qk*k;
    k_bins.push_back(k);
    k -= 3*sigma_k;
  }
  k_bins.push_back(0);

  // since its curvature, revert the order
  reverse(k_bins.begin(),k_bins.end());

  return k_bins;
}


double * computeCollinsSoperAngles(const TLorentzVector & muNeg, const TLorentzVector & muPos){
// John C. Collins and Davison E. Soper
// Phys. Rev. D 16, 2219 – Published 1 October 1977
// http://dx.doi.org/10.1103/PhysRevD.16.2219
  
  TLorentzVector Q = muNeg+muPos;

  double muNegplus  = 1.0/sqrt(2.0) * (muNeg.E() + muNeg.Pz());
  double muNegminus = 1.0/sqrt(2.0) * (muNeg.E() - muNeg.Pz());
  double muPosplus  = 1.0/sqrt(2.0) * (muPos.E() + muPos.Pz());
  double muPosminus = 1.0/sqrt(2.0) * (muPos.E() - muPos.Pz()); 

  /************************************************************************
   *
   * cos(theta_CS) = 2 Q^-1 (Q^2+Qt^2)^-(1/2) (mu^+ mu^- - mu^- mu^+)
   *
   ************************************************************************/
  double costhetaCS = 2.0 / Q.Mag() / sqrt(pow(Q.Mag(), 2) + pow(Q.Perp(), 2)) * (muNegplus * muPosminus - muNegminus * muPosplus);
  if (Q.Rapidity()<0) costhetaCS = -costhetaCS;

  /************************************************************************
   *
   * tan(phi_CS) = (Q^2 + Qt^2)^1/2 / Q (Dt dot R unit) /(Dt dot Qt unit)
   *
   ************************************************************************/
  // unit vector on R direction
  TLorentzVector Pbeam(0.,0.,1.,1.);
  TVector3 R = (Pbeam.Vect()).Cross(Q.Vect());
  TVector3 Runit = R.Unit();  

  // unit vector on Qt
  TVector3 Qt = Q.Vect(); Qt.SetZ(0.0);
  TVector3 Qtunit = Qt.Unit();
    
  TLorentzVector D(muPos-muNeg);
  TVector3 Dt = D.Vect(); Dt.SetZ(0.0);
  double tanphi = (sqrt(pow(Q.Mag(), 2) + pow(Q.Perp(), 2)) / Q.Mag()) * (Dt.Dot(Runit) / Dt.Dot(Qtunit));
  if (Q.Rapidity()<0) tanphi = -tanphi;
  double phiCS = atan(tanphi); 
  
  double *angles = new double[2];
  angles[0] = costhetaCS;
  angles[1] = phiCS;
  return angles;
  
}
