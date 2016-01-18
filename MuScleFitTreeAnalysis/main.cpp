#include "MuonPair.h"
#include "GenMuonPair.h"

#include "Helpers.h"
#include "CollinsSoperAnalysis.h"
// #include "GeneralizedEndPointAnalysisOld.h"
#include "GeneralizedEndPointAnalysis.h"

#include "LinkDef.h"
#include "TFile.h"
#include "TH1F.h"
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
  TH1F * h1_mLL = new TH1F ("h1_mLL", ";m(LL) [GeV];", 400., 0., 800);
  h1_mLL->Sumw2();
  
  // Afb
  const int nbins_mLL(11);
  double bins_mLL[nbins_mLL+1] = {60.,75.,85.,90.,95.,105.,120.,200.,300.,400.,600.,800.};
  TH1F * h1_AfbVsmLL            = new TH1F ("h1_AfbVsmLL",            ";m(LL) [GeV]; A_{FB}", nbins_mLL, bins_mLL);
  TH1F * h1_AfbVsmLL_cumulative = new TH1F ("h1_AfbVsmLL_cumulative", ";m(LL) [GeV]; A_{FB}", nbins_mLL, bins_mLL);

  // cosThetaCS (for reweighting events)
  TH1F * h1_cosThetaCS_tail = new TH1F("h1_cosThetaCS_tail", "; cos#theta_{CS};",50,-1.,+1.);
    
  CollinsSoperAnalysis * cpa = new CollinsSoperAnalysis(fout,bins_mLL[0],bins_mLL[nbins_mLL],"_all");
  // Afb differential in mLL
  vector<CollinsSoperAnalysis*> v_cpa;
  for (int i=0; i<nbins_mLL; i++){
    char append[20];
    sprintf(append,"mLL_bin%i",i);
    v_cpa.push_back(new CollinsSoperAnalysis(fout,bins_mLL[i],bins_mLL[i+1],append));
  }

  // Afb cumulative in mLL
  vector<CollinsSoperAnalysis*> v_cpa_cumulative;
  for (int i=0; i<nbins_mLL; i++){
    char append[20];
    sprintf(append,"cumulative_mLL_bin%i",i);
    v_cpa_cumulative.push_back(new CollinsSoperAnalysis(fout,bins_mLL[i],bins_mLL[nbins_mLL],append));
  }

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
      
      cpa->analyze(*muNegGen, *muPosGen, evtweight);
      for (int i=0; i<nbins_mLL; i++){
      	v_cpa[i]->analyze(*muNegGen, *muPosGen, evtweight);
	v_cpa_cumulative[i]->analyze(*muNegGen, *muPosGen, evtweight);
      }

      gepa->analyze(*muNegGen, *muPosGen, evtweight);
      
      double * angles = computeCollinsSoperAngles(*muNegGen, *muPosGen);
      double cosThetaCS = angles[0];
      if ( muNegGen->Pt()>global_parameters::pt_lep || muPosGen->Pt()>global_parameters::pt_lep ) 
	h1_cosThetaCS_tail->Fill(cosThetaCS, evtweight);    
      
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
  
  cpa->endjob();
  cout << cpa->getAfbRaw() << " " << cpa->getAfbErrorRaw() << endl;
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

  fout->cd();
  h1_mLL->Write();
  h1_AfbVsmLL->Write();
  h1_AfbVsmLL_cumulative->Write();
  h1_cosThetaCS_tail->Write();
  fout->Close();
  if ( fout !=0 ) delete fout;
  
  return 0;
  
} //main
