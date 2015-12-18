#include "CollinsSoperAnalysis.h"
#include "Helpers.h"

#include "TCanvas.h"

#include "RooArgSet.h"
#include "RooGenericPdf.h"
#include "RooPlot.h"

#include <iostream>
#include <cmath>

using namespace std;
using namespace RooFit;

// PDG
static const double mass_Z(91.188);

// analysis is limitied in [-0.5,+0.5] range
//static const double cosThetaCS_max(0.5);

static const double cosThetaCS_max(1.);

CollinsSoperAnalysis::CollinsSoperAnalysis(TFile * fout, double m1, double m2, const char * append)
  : mLL_low(m1), mLL_high(m2), AfbVal(0), AfbError(0)  {
 
  nBelowZ=0; nAboveZ=0; 
  if ( fout != 0 ) {
    fout->cd();
    
    char dir_title[40];
    sprintf(dir_title,"CollinsSoperAnalysis%s",append);
    the_dir = fout->mkdir(dir_title);
    the_dir->cd();

    char h_title[40];
    sprintf(h_title,"h1_cosThetaCS%s",append);
    h1_cosThetaCS = new TH1F(h_title,"; cos#theta_{CS}^{*};",50,-1.  ,+1.);
    sprintf(h_title,"h1_PhiCS%s",append);
    h1_phiCS      = new TH1F(h_title,"; #phi_{CS}^{*};"     ,50,-3.15/2,+3.15/2);

    sprintf(h_title,"hp_cosThetaCS%s",append);
    hp_cosThetaCS = new TProfile(h_title,"; cos#theta_{CS}^{*};",50,-1.    ,+1.    ,60.,120.);
    sprintf(h_title,"hp_PhiCS%s",append);
    hp_phiCS      = new TProfile(h_title,"; #phi_{CS}^{*};"     ,50,-3.15/2,+3.15/2,60.,120.);

    char rf_title[40];
    sprintf(rf_title,"rrv_c%s",append);
    rrv_c = new RooRealVar(rf_title,"rrv_c",-cosThetaCS_max,+cosThetaCS_max);
    sprintf(rf_title,"cosThetaCS%s",append);
    rds_cosThetaCS = new RooDataSet(rf_title,"cosThetaCS dataset", RooArgSet(*rrv_c));
  }
}

CollinsSoperAnalysis::~CollinsSoperAnalysis(){  
  the_dir->cd();
  h1_cosThetaCS->Write();
  h1_phiCS->Write();
  hp_cosThetaCS->Write();
  hp_phiCS->Write();

  if ( h1_cosThetaCS  != 0 ) delete h1_cosThetaCS  ;
  if ( h1_phiCS       != 0 ) delete h1_phiCS       ; 
  if ( hp_cosThetaCS  != 0 ) delete hp_cosThetaCS  ; 
  if ( hp_phiCS       != 0 ) delete hp_phiCS       ;                        
  if ( rrv_c          != 0 ) delete rrv_c          ; 
  if ( rds_cosThetaCS != 0 ) delete rds_cosThetaCS ;

  return;
}

void CollinsSoperAnalysis::analyze(const TLorentzVector & muNeg, const TLorentzVector & muPos, double weight){

  TLorentzVector Q = muNeg+muPos;
  if ( Q.M()<mLL_low || Q.M()>mLL_high ) return;
  Q.M() < mass_Z ? nBelowZ++ : nAboveZ++;
 
  double * angles = computeCollinsSoperAngles(muNeg, muPos);
  double cosThetaCS = angles[0];
  double phiCS = angles[1];
  
  if ( fabs(cosThetaCS)>cosThetaCS_max ) return; 
  h1_cosThetaCS->Fill(cosThetaCS, weight);
  hp_cosThetaCS->Fill(cosThetaCS, Q.M(), weight);

  // add cosThetaCS to RooDataSet
  // TODO: usage weighted in events in RooDataSet ?
  rrv_c->setVal(cosThetaCS);
  rds_cosThetaCS->add(RooArgSet(*rrv_c));

  h1_phiCS->Fill(phiCS, weight);
  hp_phiCS->Fill(phiCS, Q.M(), weight);  

  delete [] angles;
  return;
}

void CollinsSoperAnalysis::endjob(){

  cout << "nBelow/nAbove " << nBelowZ << " / " << nAboveZ << endl;
  // NB: the parametrization is such that Afb=(F-B)/(F+B)
  // "forward event" -> direction of mu- along the direction of the Z 
  RooRealVar Afb("Afb","Afb variable",0.,-1.,1.);
  RooGenericPdf rf_pdf("pdf","pdf","3/8*(1+@0*@0)+@1*@0",RooArgSet(*rrv_c, Afb));
  rf_pdf.fitTo(*rds_cosThetaCS);

  // dummy pdf with Afb=0 (just for illustration)
  RooRealVar Afb_null("Afb_null","Afb_null variable",0.);
  RooGenericPdf rf_pdf_null("pdf_null","pdf_null","3/8*(1+@0*@0)+@1*@0",RooArgSet(*rrv_c, Afb_null));

  AfbVal = Afb.getValV();
  AfbError = Afb.getError();
  
  // plot result
  TCanvas * c = new TCanvas("CollinsSopherAnalysis","CollinsSopherAnalysis",600,600);
  c->cd();
  RooPlot* mframe = rrv_c->frame();
  // original dataset
  rds_cosThetaCS->plotOn(mframe);  
  // pdf with Afb
  rf_pdf.plotOn(mframe);
  // pdf without Afb
  rf_pdf_null.plotOn(mframe,LineStyle(kDashed));
  mframe->Draw() ;
  //  c->SaveAs("CollinsSoperAnalysis.pdf");
  
  return;
}
