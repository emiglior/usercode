#include "GeneralizedEndPointAnalysis.h"
#include "Helpers.h"

#include <cmath>
#include <iomanip>


using namespace std;

static const double GeVToTeV = 0.001;

GeneralizedEndPointAnalysis::GeneralizedEndPointAnalysis(TFile * fout, const char * append) {

  if ( fout != 0 ) {
    fout->cd();
    
    char dir_title[40];
    sprintf(dir_title,"GeneralizedEndPointAnalysis%s",append);
    the_dir = fout->mkdir(dir_title);
    the_dir->cd();

    char h_title[40];
    sprintf(h_title,"h_pt_neg%s",append);
    h_pt_neg = new TH1F(h_title,"pT neg; pT (#mu^{-}) [GeV/c];"   ,500, 5.,505.);
    sprintf(h_title,"h_pt_pos%s",append);
    h_pt_pos = new TH1F(h_title,"pT pos; pT (#mu^{+}) [GeV/c];"   ,500, 5.,505.);
    sprintf(h_title,"h_ptinv_neg%s",append);
    h_ptinv_neg = new TH1F(h_title,"pTinv neg; 1/pT (#mu^{-}) [c/TeV];"   ,2000, 0.,200.);
    sprintf(h_title,"h_ptinv_pos%s",append);
    h_ptinv_pos = new TH1F(h_title,"pTinv pos; 1/pT (#mu^{+}) [c/TeV];"   ,2000, 0.,200.);

    h_pt_neg->StatOverflows(kTRUE); 
    h_pt_pos->StatOverflows(kTRUE); 
    h_ptinv_neg->StatOverflows(kTRUE); 
    h_ptinv_pos->StatOverflows(kTRUE); 

    sprintf(h_title,"h_cosThetaCS%s",append);
    h_cosThetaCS = new TH1F(h_title," ; cos#theta_{CS};",50,-1.,+1.);
    sprintf(h_title,"h_cosThetaCS_tail%s",append);
    h_cosThetaCS_tail = new TH1F(h_title," ; cos#theta_{CS};",50,-1.,+1.);

    sprintf(h_title,"h_mLL%s",append);
    h_mLL = new TH1F(h_title," ; m_{LL} [GeV];",50,50.,150.);
    sprintf(h_title,"h_mLL_tail%s",append);
    h_mLL_tail = new TH1F(h_title," ; m_{LL} [GeV];",50,50.,150.);

  }
  
  char f_title[40];
  sprintf(f_title,"GeneralizedEndPoint%s.txt",append);
  outfile.open(f_title);
  outfile << "p" << '\t' << "pT" << '\t' << "eta" << '\t' << "p" << '\t' << "pT" << '\t' << "eta" << endl;
}

GeneralizedEndPointAnalysis::~GeneralizedEndPointAnalysis(){
  outfile.close();
  
  the_dir->cd();
  h_pt_neg->Write(); 
  h_pt_pos->Write(); 
  h_ptinv_neg->Write(); 
  h_ptinv_pos->Write();
  h_cosThetaCS->Write();
  h_cosThetaCS_tail->Write();
  h_mLL->Write();
  h_mLL_tail->Write();

  if ( h_pt_neg     != 0 ) delete h_pt_neg;
  if ( h_pt_pos	    != 0 ) delete h_pt_pos;
  if ( h_ptinv_neg  != 0 ) delete h_ptinv_neg;
  if ( h_ptinv_pos  != 0 ) delete h_ptinv_pos;
  if ( h_cosThetaCS != 0 ) delete h_cosThetaCS;
  if ( h_cosThetaCS_tail != 0 ) delete h_cosThetaCS_tail;
  if ( h_mLL      != 0 ) delete h_mLL;
  if ( h_mLL_tail != 0 ) delete h_mLL_tail;

  return;
}

void GeneralizedEndPointAnalysis::analyze(const TLorentzVector & muNeg, const TLorentzVector & muPos, double weight){
    
  the_dir->cd();
  
  double pt1_gen = muNeg.Pt(); double eta1_gen = muNeg.Eta(); double p1_gen = muNeg.P();
  double pt2_gen = muPos.Pt(); double eta2_gen = muPos.Eta(); double p2_gen = muPos.P();

  h_pt_neg->Fill(pt1_gen, weight); 
  h_pt_pos->Fill(pt2_gen, weight); 

  // Get curvatures in c/TeV
  double k1_gen = -1/(pt1_gen*GeVToTeV);
  double k2_gen =  1/(pt2_gen*GeVToTeV);      
  
  h_ptinv_neg->Fill(fabs(k1_gen), weight); 
  h_ptinv_pos->Fill(fabs(k2_gen), weight); 

  double mLL = (muNeg+muPos).M();
  h_mLL->Fill(mLL, weight);
  
  // cosThetaCS analysis
  double * angles = computeCollinsSoperAngles(muNeg, muPos);
  double cosThetaCS = angles[0];
  h_cosThetaCS->Fill(cosThetaCS, weight);

  // debug end-point events (pT>100 GeV)
  if ( pt1_gen>100 || pt2_gen>100 ) {
    h_cosThetaCS_tail->Fill(cosThetaCS, weight);    
    h_mLL_tail->Fill(mLL, weight);
    outfile << setprecision(4) << p1_gen << '\t' << pt1_gen << '\t' << eta1_gen << '\t' << p2_gen << '\t' << pt2_gen << '\t' << eta2_gen << endl;
  }
  delete [] angles;

  return;
}

// void computeVariableBins(const double& pT_ini, const double& pT_max, vector<double>& bins) {

//   const double q0(2.5e-4); // Hit Resoultion
//   const double qk(1e-2);   // MS

//   for (double pT = pT_ini; pT<pT_max; pT += (q0*pT + qk)*pT) {
//     bins.push_back(pT);
//   }

// }






//     // Get pts and etas

  //   }
  //   cout << "entries with zero pTgen: " << n_pt_gen_zero << endl;
      
  // }//check if tree has any entry

  // cout << "Closing file ..." << endl;
  // //close & write 
  // fin->Close();
  // if ( fin!=0 ) delete fin;

  // fout->cd();

  // // perform K-S test
  // double ks = h_ptinv_neg->KolmogorovTest(h_ptinv_pos,"UOD");  // "UO" undeflows/overflows included in the KS test
  //                                                              // "D" debug info
  // cout << "KS prob "<< ks << endl;


  // // perform chi2 test
  // double chi2prob = h_ptinv_neg->Chi2Test(h_ptinv_pos,"UUP");  // "UU" unweighted/unweighted
  //                                                              // "P" debug info
  // cout << "chi2 prob "<< chi2prob << endl;


