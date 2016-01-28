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


CollinsSoperAnalysis::CollinsSoperAnalysis(TFile * fout, double m1, double m2, double y1, double y2, const char * append)
  : mLL_low(m1), mLL_high(m2), yLL_low(y1), yLL_high(y2), AfbValRaw(0), AfbErrorRaw(0), AfbValFit(0), AfbErrorFit(0)  {
 
  if ( fout != 0 ) {
    fout->cd();
    
    char dir_title[50];
    sprintf(dir_title,"CollinsSoperAnalysis%s",append);
    the_dir = fout->mkdir(dir_title);
    the_dir->cd();

    char h_title[50];
    sprintf(h_title,"h1_cosThetaCS%s",append);
    h1_cosThetaCS = new TH1F(h_title,"; cos#theta_{CS}^{*};",50,-1.  ,+1.);

    sprintf(h_title,"h1_cosThetaCS_pos%s",append);
    h1_cosThetaCS_pos = new TH1F(h_title,"; cos#theta_{CS}^{*};",50,-1.  ,+1.);
    h1_cosThetaCS_pos->Sumw2();
	
    sprintf(h_title,"h1_cosThetaCS_neg%s",append);
    h1_cosThetaCS_neg = new TH1F(h_title,"; cos#theta_{CS}^{*};",50,-1.  ,+1.);
    h1_cosThetaCS_neg->Sumw2();
    
    sprintf(h_title,"h1_PhiCS%s",append);
    h1_phiCS      = new TH1F(h_title,"; #phi_{CS}^{*};"     ,50,-3.15/2,+3.15/2);

    sprintf(h_title,"hp_cosThetaCS%s",append);
    hp_cosThetaCS = new TProfile(h_title,"; cos#theta_{CS}^{*};",50,-1.    ,+1.    ,60.,120.);
    sprintf(h_title,"hp_PhiCS%s",append);
    hp_phiCS      = new TProfile(h_title,"; #phi_{CS}^{*};"     ,50,-3.15/2,+3.15/2,60.,120.);

    char rf_title[40];
    sprintf(rf_title,"rrv_c%s",append);
    rrv_c = new RooRealVar(rf_title,"rrv_c",-global_parameters::cosThetaCS_max,+global_parameters::cosThetaCS_max);
    // sprintf(rf_title,"rrv_w%s",append);
    // rrv_w = new RooRealVar(rf_title,"rrv_w");
    sprintf(rf_title,"cosThetaCS%s",append);
    rds_cosThetaCS = new RooDataSet(rf_title,"cosThetaCS dataset", RooArgSet(*rrv_c));
  }
}

CollinsSoperAnalysis::~CollinsSoperAnalysis(){  
  the_dir->cd();
  h1_cosThetaCS->Write();
  h1_cosThetaCS_pos->Write();
  h1_cosThetaCS_neg->Write();
  h1_phiCS->Write();
  hp_cosThetaCS->Write();
  hp_phiCS->Write();

  if ( h1_cosThetaCS  != 0 ) delete h1_cosThetaCS  ;
  if ( h1_cosThetaCS_pos  != 0 ) delete h1_cosThetaCS_pos  ;
  if ( h1_cosThetaCS_neg  != 0 ) delete h1_cosThetaCS_neg  ;
  if ( h1_phiCS       != 0 ) delete h1_phiCS       ; 
  if ( hp_cosThetaCS  != 0 ) delete hp_cosThetaCS  ; 
  if ( hp_phiCS       != 0 ) delete hp_phiCS       ;                        
  if ( rrv_c          != 0 ) delete rrv_c          ;
  //  if ( rrv_w          != 0 ) delete rrv_w          ; 
  if ( rds_cosThetaCS != 0 ) delete rds_cosThetaCS ;
}

void CollinsSoperAnalysis::analyze(const TLorentzVector & muNeg, const TLorentzVector & muPos, double weight){

  TLorentzVector Q = muNeg+muPos;
  if ( Q.M()<mLL_low || Q.M()>mLL_high ) return;
  if ( fabs(Q.Rapidity())<yLL_low || fabs(Q.Rapidity())>yLL_high ) return;
 
  double * angles = computeCollinsSoperAngles(muNeg, muPos);
  double cosThetaCS = angles[0];
  double phiCS = angles[1];
  
  if ( fabs(cosThetaCS)>global_parameters::cosThetaCS_max ) return; 
  h1_cosThetaCS->Fill(cosThetaCS, weight);
  cosThetaCS > 0 ? h1_cosThetaCS_pos->Fill(cosThetaCS, weight) : h1_cosThetaCS_neg->Fill(cosThetaCS, weight);
  
  hp_cosThetaCS->Fill(cosThetaCS, Q.M(), weight);

  // add cosThetaCS to RooDataSet
  // TODO: usage weighted in events in RooDataSet ?
  // https://root.cern.ch/root/html/tutorials/roofit/rf403_weightedevts.C.html
  rrv_c->setVal(cosThetaCS);
  //  rrv_w->setVal(weight);
  rds_cosThetaCS->add(RooArgSet(*rrv_c));

  h1_phiCS->Fill(phiCS, weight);
  hp_phiCS->Fill(phiCS, Q.M(), weight);  

  delete [] angles;
  return;
}

void CollinsSoperAnalysis::endjob(){

  // compute RAW Afb
  // char cut_title[40];
  // sprintf(cut_title,"%s>0",rrv_c->GetName());
  double nF = h1_cosThetaCS_pos->GetSumOfWeights(); //rds_cosThetaCS->sumEntries(cut_title);  
  double nB = h1_cosThetaCS_neg->GetSumOfWeights(); //rds_cosThetaCS->sumEntries() - nF; 
  if ( (nF+nB) > 0 ) {
    AfbValRaw = (nF-nB)/(nF+nB);
    AfbErrorRaw= 2./(nF+nB)*sqrt(nF*nB/(nF+nB));
  } else {
    AfbValRaw = 0;
    AfbErrorRaw= 2;
  }
      
  cout << "CPA::endjob() nF " << nF << " nB " << nB << " AFB "<< AfbValRaw << endl;
  
  // NB: the parametrization is such that Afb=(F-B)/(F+B)
  // "forward event" -> direction of mu- along the direction of the Z 
  RooRealVar Afb("Afb","Afb variable",0.,-1.,1.);
  RooGenericPdf rf_pdf("pdf","pdf","3/8*(1+@0*@0)+@1*@0",RooArgSet(*rrv_c, Afb));
  rf_pdf.fitTo(*rds_cosThetaCS);

  // dummy pdf with Afb=0 (just for illustration)
  RooRealVar Afb_null("Afb_null","Afb_null variable",0.);
  RooGenericPdf rf_pdf_null("pdf_null","pdf_null","3/8*(1+@0*@0)+@1*@0",RooArgSet(*rrv_c, Afb_null));

  AfbValFit = Afb.getValV();
  AfbErrorFit = Afb.getError();
  
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
