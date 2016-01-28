#include "MuonPair.h"
#include "GenMuonPair.h"

#include "Helpers.h"
#include "CollinsSoperAnalysis.h"
// #include "GeneralizedEndPointAnalysisOld.h"
#include "GeneralizedEndPointAnalysis.h"

#include "LinkDef.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TProfile.h"
#include "TTree.h"
#include "TLorentzVector.h"

#include <iostream>
#include <cmath>
#include <vector>

using namespace std;

int main(int argc, char *argv[]){

  // Parse arguments
  TString inputTree = argv[1];
  
  // input tree containing Generated events and Reco events  
  cout<<"Opening the file ..."<<endl;
  
  TFile *fin = TFile::Open(inputTree,"READ");
  fin->cd();

  cout<<"Getting the tree ..."<<endl;
  TTree *treeIN =(TTree*)fin->Get("demo/T"); //input tree named T
  
  TFile *fout = TFile::Open("TMP.root","RECREATE");

  // mLL
  TH1F * h1_mLL = new TH1F ("h1_mLL", ";m(LL) [GeV];", 700., 0., 1400);
  h1_mLL->Sumw2();

  // yLL
  TH1F * h1_yLL = new TH1F ("h1_yLL", ";y(LL);", 50., -5., +5.);
  h1_yLL->Sumw2();

  // yLL vs mLL
  TH2F * h2_yLLvsmLL = new TH2F ("h2_yLLvsmLL", ";m(LL) [GeV]; |y(LL)|", 140., 0., 1400, 50, 0., +5.);
  h2_yLLvsmLL->Sumw2();
  TProfile * hp_yLLvsmLL = new TProfile("hp_yLLvsmLL", ";m(LL) [GeV]; |y(LL)|", 140., 0., 1400, 0., +5.);
  hp_yLLvsmLL->Sumw2();
  
  // Afb
  const int nbins_mLL(13);
  double bins_mLL[nbins_mLL+1] = {50.,75.,85.,90.,95.,105.,120.,200.,300.,400.,600.,800.,1100.,1400.};
  TH1F * h1_AfbVsmLL            = new TH1F ("h1_AfbVsmLL",            ";m(LL) [GeV]; A_{FB}", nbins_mLL, bins_mLL);
  TH1F * h1_AfbVsmLL_cumulative = new TH1F ("h1_AfbVsmLL_cumulative", ";m(LL) [GeV]; A_{FB}", nbins_mLL, bins_mLL);
  TH1F * h1_AfbVsmLL_HPT            = new TH1F ("h1_AfbVsmLL_HPT",            ";m(LL) [GeV]; A_{FB}", nbins_mLL, bins_mLL);
  TH1F * h1_AfbVsmLL_cumulative_HPT = new TH1F ("h1_AfbVsmLL_cumulative_HPT", ";m(LL) [GeV]; A_{FB}", nbins_mLL, bins_mLL);


  // const int nbins_yLL(10);
  // double bins_yLL[nbins_yLL+1] = {-5.,-3.,-2.,-1.5,-0.75,0.,+0.75,+1.5,+2.,+3.,+5.};
  const int nbins_yLL(6);
  double bins_yLL[nbins_yLL+1] = {0.,+0.75,+1.5,+2.,+2.5,+3.,+5.};
  TH1F * h1_AfbVsyLL            = new TH1F ("h1_AfbVsyLL",     ";y(LL); A_{FB}", nbins_yLL, bins_yLL);
  TH1F * h1_AfbVsyLL_HPT        = new TH1F ("h1_AfbVsyLL_HPT", ";y(LL); A_{FB}", nbins_yLL, bins_yLL);

  // cosThetaCS (for reweighting events)
  TH1F * h1_cosThetaCS_tail = new TH1F("h1_cosThetaCS_tail", "; cos#theta_{CS};",50,-1.,+1.);

  double yLL_MAX(1000.);
  double mLL_MAX(100000.);
  
  //------- AFB ALL pTs  
  CollinsSoperAnalysis * cpa = new CollinsSoperAnalysis(fout,bins_mLL[0],bins_mLL[nbins_mLL],-yLL_MAX,+yLL_MAX,"_all");
  // Afb differential in mLL
  vector<CollinsSoperAnalysis*> v_cpa;
  for (int i=0; i<nbins_mLL; i++){
    char append[30];
    sprintf(append,"mLL_bin%i",i);
    v_cpa.push_back(new CollinsSoperAnalysis(fout,bins_mLL[i],bins_mLL[i+1],-yLL_MAX,+yLL_MAX,append));
  }
  // Afb cumulative in mLL
  vector<CollinsSoperAnalysis*> v_cpa_cumulative;
  for (int i=0; i<nbins_mLL; i++){
    char append[30];
    sprintf(append,"cumulative_mLL_bin%i",i);
    v_cpa_cumulative.push_back(new CollinsSoperAnalysis(fout,bins_mLL[0],bins_mLL[i+1],-yLL_MAX,+yLL_MAX,append));
  }
  // Afb differential in yLL
  vector<CollinsSoperAnalysis*> v_cpa_y;
  for (int i=0; i<nbins_yLL; i++){
    char append[30];
    sprintf(append,"yLL_bin%i",i);
    v_cpa_y.push_back(new CollinsSoperAnalysis(fout,-mLL_MAX,+mLL_MAX,bins_yLL[i],bins_yLL[i+1],append));
  }
  //-------
  
  //------- AFB HIGH pTs  
  CollinsSoperAnalysis * cpaHPT = new CollinsSoperAnalysis(fout,bins_mLL[0],bins_mLL[nbins_mLL],-yLL_MAX,+yLL_MAX,"_HPT_all");
  // Afb differential in mLL
  vector<CollinsSoperAnalysis*> v_cpaHPT;
  for (int i=0; i<nbins_mLL; i++){
    char append[30];
    sprintf(append,"HPT_mLL_bin%i",i);
    v_cpaHPT.push_back(new CollinsSoperAnalysis(fout,bins_mLL[i],bins_mLL[i+1],-yLL_MAX,+yLL_MAX,append));
  }
  // Afb cumulative in mLL
  vector<CollinsSoperAnalysis*> v_cpaHPT_cumulative;
  for (int i=0; i<nbins_mLL; i++){
    char append[30];
    sprintf(append,"HPT_cumulative_mLL_bin%i",i);
    v_cpaHPT_cumulative.push_back(new CollinsSoperAnalysis(fout,bins_mLL[0],bins_mLL[i+1],-yLL_MAX,+yLL_MAX,append));
  }
  // Afb differential in yLL
  vector<CollinsSoperAnalysis*> v_cpaHPT_y;
  for (int i=0; i<nbins_yLL; i++){
    char append[30];
    sprintf(append,"HPT_yLL_bin%i",i);
    v_cpaHPT_y.push_back(new CollinsSoperAnalysis(fout,-mLL_MAX,+mLL_MAX,bins_yLL[i],bins_yLL[i+1],append));
  }
  //-------
  
  // GeneralizedEndPoint
  GeneralizedEndPointAnalysis * gepa  = new GeneralizedEndPointAnalysis(fout);      
  //  GeneralizedEndPointAnalysis * gepaW = new GeneralizedEndPointAnalysis(fout,"ReWgt");
  if ( argc > 2 ) {
    gepa->set_delta_kappa(atof(argv[2]));
    //    gepaW->set_delta_kappa(atof(argv[2]));
  }
  // MuonPairs
  GenMuonPair *mupairGenIN_ = 0;
  double genweight_ = 0;
  double lheweight_ = 0;
  double evtweight;
  
  TLorentzVector* muNegGen=0;
  TLorentzVector* muPosGen=0;
  
  // Loop on input TTree
  if ( treeIN!=0 ) {              
    
    treeIN->SetBranchAddress("GenMuons",    &mupairGenIN_); //select generated event    
    treeIN->SetBranchAddress("genweight",   &genweight_);
    treeIN->SetBranchAddress("lheweight",   &lheweight_);
    
    int nentries=treeIN->GetEntries();

    //
    // First pass
    //
    int n_pt_gen_zero = 0;
    cout<<"Loop #1 over tree entries ...";
    for(int entry=0; entry<nentries;  entry++){ 

      treeIN->GetEntry(entry);
      if (entry%1000000==0)cout<<"Loop #1 Reading muon pair n. "<<entry<<endl;

      // if ( entry%4 != 0 ) continue; // to test scaling of dk_error with the size of the sample
      
      //      evtweight = (genweight_ > 0) ? +1. : -1.;  // temporary for aMC@NLO studies
      evtweight = genweight_;
      
      // cout<<"Pt1 = "<<mupairGenIN_->mu1.fP4.Pt()<<"; Pt2 = "<<mupairGenIN_->mu2.fP4.Pt()<<endl;

      // skip events where one of the pT gen is null 
      if ( mupairGenIN_->mu1.fP4.Pt() == 0 || mupairGenIN_->mu2.fP4.Pt() == 0 ) { 
	n_pt_gen_zero++;
	continue;
      }

      // fetch GEN muons from the input tree
      muNegGen = new TLorentzVector(mupairGenIN_->mu1.fP4.Px(), mupairGenIN_->mu1.fP4.Py(), mupairGenIN_->mu1.fP4.Pz(), mupairGenIN_->mu1.fP4.E());
      muPosGen = new TLorentzVector(mupairGenIN_->mu2.fP4.Px(), mupairGenIN_->mu2.fP4.Py(), mupairGenIN_->mu2.fP4.Pz(), mupairGenIN_->mu2.fP4.E());      

      double mLL = ((*muNegGen)+(*muPosGen)).M();
      h1_mLL->Fill(mLL, evtweight);    
      double yLL = ((*muNegGen)+(*muPosGen)).Rapidity();
      h1_yLL->Fill(yLL, evtweight);

      h2_yLLvsmLL->Fill(mLL, fabs(yLL), evtweight);
      hp_yLLvsmLL->Fill(mLL, fabs(yLL), evtweight);    

      // Afb done on all events 
      cpa->analyze(*muNegGen, *muPosGen, evtweight);
      for (int i=0; i<nbins_mLL; i++){
	v_cpa[i]->analyze(*muNegGen, *muPosGen, evtweight);
	v_cpa_cumulative[i]->analyze(*muNegGen, *muPosGen, evtweight);
      }
      for (int i=0; i<nbins_yLL; i++){
	v_cpa_y[i]->analyze(*muNegGen, *muPosGen, evtweight);
      }

      double * angles = computeCollinsSoperAngles(*muNegGen, *muPosGen);
      double cosThetaCS = angles[0];
      if ( muNegGen->Pt()>global_parameters::pt_lep || muPosGen->Pt()>global_parameters::pt_lep ) {	
	// fill th1 to be used for reweighting the events
	h1_cosThetaCS_tail->Fill(cosThetaCS, evtweight);    

	// Afb done only on events with at least one muon with pT>pt_lep (see definition in Helpers.h)
	cpaHPT->analyze(*muNegGen, *muPosGen, evtweight);
	for (int i=0; i<nbins_mLL; i++){
	  v_cpaHPT[i]->analyze(*muNegGen, *muPosGen, evtweight);
	  v_cpaHPT_cumulative[i]->analyze(*muNegGen, *muPosGen, evtweight);
	}
	for (int i=0; i<nbins_yLL; i++){
	  v_cpaHPT_y[i]->analyze(*muNegGen, *muPosGen, evtweight);
	}

	// Generalized EndPoint Analysis done only on events with at least one muon with pT>pt_lep (see definition in Helpers.h)
	gepa->analyze(*muNegGen, *muPosGen, evtweight);	
      }
      
      if ( muNegGen != 0 ) delete muNegGen; 
      if ( muPosGen != 0 ) delete muPosGen;      
    }
    cout << "entries with zero pTgen: " << n_pt_gen_zero << endl;

    //
    // Second pass (Generalized EndPoint analysis is performed here)
    //

    // // FIXME
    // // retrieve & normalize TH1F of cosThetaCS
    // TH1F * h_norm = (TH1F*)fout->Get("h1_cosThetaCS_tail");
    // double norm = h_norm->GetEntries();
    // h_norm->Scale(1/norm);

    // cout<<"Loop #2 over tree entries ...";    
    // for(int entry=0; entry<nentries;  entry++){ 

    //   treeIN->GetEntry(entry);
    //   if (entry%1000000==0)cout<<"Loop #2 Reading muon pair n. "<<entry<<endl;

    //   // skip events where one of the pT gen is null 
    //   if ( mupairGenIN_->mu1.fP4.Pt() == 0 || mupairGenIN_->mu2.fP4.Pt() == 0 ) { 
    // 	continue;
    //   }

    //   // fetch GEN muons from the input tree
    //   muNegGen = new TLorentzVector(mupairGenIN_->mu1.fP4.Px(), mupairGenIN_->mu1.fP4.Py(), mupairGenIN_->mu1.fP4.Pz(), mupairGenIN_->mu1.fP4.E());
    //   muPosGen = new TLorentzVector(mupairGenIN_->mu2.fP4.Px(), mupairGenIN_->mu2.fP4.Py(), mupairGenIN_->mu2.fP4.Pz(), mupairGenIN_->mu2.fP4.E());
      
    //   double * angles = computeCollinsSoperAngles(*muNegGen, *muPosGen);
    //   double cosThetaCS = angles[0];
    //   double weight = h_norm->GetBinContent(h_norm->FindBin(cosThetaCS));//FIXME check normalization
    //   weight = (3./8.*(1+cosThetaCS*cosThetaCS) + global_parameters::AfbFIXED*cosThetaCS) / weight;
    //   if ( weight > 0. ) {
    // 	gepaW->analyze(*muNegGen, *muPosGen, weight);
    //   }	else {
    // 	cout << "NEGATIVE WEIGHT "<< endl;
    //   }
    //   delete [] angles;
      
    //   if ( muNegGen != 0 ) delete muNegGen; 
    //   if ( muPosGen != 0 ) delete muPosGen;      
    // } // end of second pass

  }//check if tree has any entry
  
  //close & write 
  fin->Close();
  if ( fin!=0 ) delete fin;

  gepa->endjob();
  if ( gepa != 0 ) delete gepa;

  // gepaW->endjob();
  // if ( gepaW != 0 ) delete gepaW;
  
  // ----- ALL pTs
  cpa->endjob();
  cout << "Closing file ..." << endl;
  if ( cpa != 0 ) delete cpa;

  // summary histos
  for (int i=0; i<nbins_mLL; i++){
    v_cpa[i]->endjob();
    h1_AfbVsmLL->SetBinContent(i+1,v_cpa[i]->getAfbRaw());
    h1_AfbVsmLL->SetBinError(i+1,v_cpa[i]->getAfbErrorRaw());
    delete v_cpa[i];

    v_cpa_cumulative[i]->endjob();
    h1_AfbVsmLL_cumulative->SetBinContent(i+1,v_cpa_cumulative[i]->getAfbRaw());
    h1_AfbVsmLL_cumulative->SetBinError(i+1,v_cpa_cumulative[i]->getAfbErrorRaw());
    delete v_cpa_cumulative[i];    
  }
  for (int i=0; i<nbins_yLL; i++){
    v_cpa_y[i]->endjob();
    h1_AfbVsyLL->SetBinContent(i+1,v_cpa_y[i]->getAfbRaw());
    h1_AfbVsyLL->SetBinError(i+1,v_cpa_y[i]->getAfbErrorRaw());
    delete v_cpa_y[i];
  }
  // -----
  
  // ----- HIGH pTs
  cpaHPT->endjob();
  cout << "Closing file ..." << endl;
  if ( cpaHPT != 0 ) delete cpaHPT;

  // summary histos
  for (int i=0; i<nbins_mLL; i++){
    v_cpaHPT[i]->endjob();
    h1_AfbVsmLL_HPT->SetBinContent(i+1,v_cpaHPT[i]->getAfbRaw());
    h1_AfbVsmLL_HPT->SetBinError(i+1,v_cpaHPT[i]->getAfbErrorRaw());
    delete v_cpaHPT[i];

    v_cpaHPT_cumulative[i]->endjob();
    h1_AfbVsmLL_cumulative_HPT->SetBinContent(i+1,v_cpaHPT_cumulative[i]->getAfbRaw());
    h1_AfbVsmLL_cumulative_HPT->SetBinError(i+1,v_cpaHPT_cumulative[i]->getAfbErrorRaw());
    delete v_cpaHPT_cumulative[i];
  }
  for (int i=0; i<nbins_yLL; i++){
    v_cpaHPT_y[i]->endjob();
    h1_AfbVsyLL_HPT->SetBinContent(i+1,v_cpaHPT_y[i]->getAfbRaw());
    h1_AfbVsyLL_HPT->SetBinError(i+1,v_cpaHPT_y[i]->getAfbErrorRaw());
    delete v_cpaHPT_y[i];
  }
  // -----
  
  fout->cd();

  cout << "END-OF-JOB report for " << argv[1] << endl;
  cout << "Number of equivalent entries (before selection)" << (int)h1_mLL->GetEffectiveEntries() << endl;



  h1_mLL->Write();
  h1_AfbVsmLL->Write();
  h1_AfbVsmLL_cumulative->Write();
  h1_AfbVsmLL_HPT->Write();
  h1_AfbVsmLL_cumulative_HPT->Write();

  h1_yLL->Write();

  h2_yLLvsmLL->Write();
  hp_yLLvsmLL->Write();
      
  h1_AfbVsyLL->Write();
  h1_AfbVsyLL_HPT->Write();

  h1_cosThetaCS_tail->Write();
  fout->Close();
  if ( fout !=0 ) delete fout;
  
  return 0;
  
} //main
