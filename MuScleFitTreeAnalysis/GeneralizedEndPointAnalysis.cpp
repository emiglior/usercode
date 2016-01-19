#include "GeneralizedEndPointAnalysis.h"
#include "Helpers.h"

#include "TF1.h"
#include "TH1F.h"
#include "TCanvas.h"
#include "TPaveText.h"
#include "Rtypes.h"
#include "TGraph.h"
//#include "TLegend.h"
#include "TFitResultPtr.h"

#include "TGaxis.h"
#include "TFrame.h"

#include <sys/stat.h>
#include <iostream>

using namespace std;

GeneralizedEndPointAnalysis::GeneralizedEndPointAnalysis(TFile * fout, const char * append) :
  the_dir(0), delta_kappa(0), HList_pos(0), HList_neg(0), HListKS_pos(0), HListKS_neg(0), Canvas(0), dk(0), chi2(0), ks(0) {

  // create the dir on local filesystem where output canvas are saved
  if (strcmp(append, "") == 0) {
    sprintf(dirname,"./mc_pt_%i/",(int)global_parameters::pt_lep);
  } else {
    sprintf(dirname,"./mc_pt_%i_%s/",(int)global_parameters::pt_lep,append);
  }
  mkdir(dirname,0775);
  
  if ( fout != 0 ) {
    fout->cd();
    
    char dir_title[40];
    sprintf(dir_title,"GeneralizedEndPointAnalysis%s",append);
    the_dir = fout->mkdir(dir_title);
    the_dir->cd();

    // --- defining the nr. of delta_k to inject
    // float global_parameters::dk_step = 0.000004; // original
    // for(float f =-0.0002; f<0.0002; f+= dk_step ) 
    //   delta_k.push_back(f);
    
    for(double f =-0.5; f<0.5; f+=global_parameters::dk_step )  // range in [c/TeV]
      delta_k.push_back(f);
    
    n_Dk = delta_k.size();
    dk = new double [n_Dk];
    chi2 = new double[n_Dk];
    ks = new double[n_Dk];

    // --- creating the array of histograms
    char name_p[10], title_p[30], name_n[10], title_n[30],  name_can[100], title_can[100];
    // create the pointers to the histograms
    TH1F *h_pos, *h_KSpos;
    TH1F *h_neg, *h_KSneg; 
    TCanvas * c_temp;

    vector<double> vK_bins = computeCurvatureVariableBins(global_parameters::pt_lep*global_parameters::GeVToTeV);
    int binning = (int)vK_bins.size()-1;
    double k_bins[binning+1];
    copy(vK_bins.begin(), vK_bins.end(), k_bins);
    
    for (int i = 0; i < n_Dk; i++) {
      if (strcmp(append, "") == 0) {
	sprintf(name_can,"canvas_Dkappa%d", i);
      } else {
	sprintf(name_can,"canvas_Dkappa%d_%s", i, append);
      }
      sprintf(title_can,"canvas Dkappa=%.5lf for pos. vs neg. curvature",delta_k[i]);
      sprintf(name_p,"h_pos_%d",i);
      sprintf(title_p,"histo %d curvature",i);
      sprintf(name_n,"h_neg_%d",i);
      sprintf(title_n,"histo %d curvature",i);

      //      h_pos = new TH1F(name_p,title_p,global_parameters::binning,0.,global_parameters::up_limit); // was 50
      //      h_neg = new TH1F(name_n,title_n,global_parameters::binning,0.,global_parameters::up_limit); // revert later to positive values for comparison
      
      h_pos = new TH1F(name_p,title_p,binning,k_bins); 
      h_neg = new TH1F(name_n,title_n,binning,k_bins); 
      h_pos->SetTitle("Leading pos muon curvature q/p_{T};#kappa [c/TeV];Entries");
      h_neg->SetTitle("Leading neg muon curvature q/p_{T};#kappa [c/TeV];Entries");

      h_pos->Sumw2();
      h_neg->Sumw2();

      HList_pos.Add(h_pos);
      HList_neg.Add(h_neg);

      // book TH1 with finer binning histos for K-S test
      sprintf(name_p,"h_KSpos_%d",i);
      sprintf(title_p,"histo %d curvature (for KS test)",i);
      sprintf(name_n,"h_KSneg_%d",i);
      sprintf(title_n,"histo %d curvature (for KS test)",i);

      h_KSpos = new TH1F(name_p,title_p,global_parameters::binningKS,0.,global_parameters::up_limit); // was 50
      h_KSneg = new TH1F(name_n,title_n,global_parameters::binningKS,0.,global_parameters::up_limit); // revert later to positive values for comparison      
      // h_KSpos->Sumw2();
      // h_KSneg->Sumw2();

      HListKS_pos.Add(h_KSpos);
      HListKS_neg.Add(h_KSneg);

      c_temp = new TCanvas(name_can,title_can,800,800);
      Canvas.Add(c_temp);

    }
 
  }
}

GeneralizedEndPointAnalysis::~GeneralizedEndPointAnalysis() {
  
  the_dir->cd();

  for(int j=0;j<n_Dk;j++){    
    TObject* h_pos_temp = HList_pos.At(j);
    TObject* h_neg_temp = HList_neg.At(j);    
    h_pos_temp->Write(); 
    h_neg_temp->Write(); 

    TObject* h_KSpos_temp = HListKS_pos.At(j);
    TObject* h_KSneg_temp = HListKS_neg.At(j);    
    h_KSpos_temp->Write(); 
    h_KSneg_temp->Write(); 
}

  if (HList_pos.GetSize()!=0 && HList_neg.GetSize()!=0) {
    //cout<< "Yes, the size is different from zero"<< endl;
    HList_pos.SetOwner(kTRUE);
    HList_neg.SetOwner(kTRUE);
    HList_pos.Clear();
    HList_neg.Clear();
  }
  
  if (HListKS_pos.GetSize()!=0 && HListKS_neg.GetSize()!=0) {
    //cout<< "Yes, the size is different from zero"<< endl;
    HListKS_pos.SetOwner(kTRUE);
    HListKS_neg.SetOwner(kTRUE);
    HListKS_pos.Clear();
    HListKS_neg.Clear();
  }
  
  if ( dk != 0 ) delete[] dk;
  if ( chi2 != 0 ) delete[] chi2;
  if ( ks != 0 ) delete[] ks;
}

void GeneralizedEndPointAnalysis::analyze(const TLorentzVector & muNeg, const TLorentzVector & muPos, double weight){

  the_dir->cd();
  double k_prime;
  
  //-- Injecting  the Dk  
  for(int j=0;j<n_Dk;j++){
    
    TObject* h_pos_temp = HList_pos.At(j);
    TObject* h_neg_temp = HList_neg.At(j);

    TObject* h_KSpos_temp = HListKS_pos.At(j);
    TObject* h_KSneg_temp = HListKS_neg.At(j);

    // EM 2016.01.10
    // if the injected bias flips the sign of the curvature then skip this muon pair
    if  (( (+1./(muPos.Pt()*global_parameters::GeVToTeV) + delta_kappa) < 0 ) ||
	 ( (-1./(muNeg.Pt()*global_parameters::GeVToTeV) + delta_kappa) > 0 ) ) continue;

    // EM 2016.01.11 not sure if next "continue" should be active or not. To be investigated...
    if  (( (+1./(muPos.Pt()*global_parameters::GeVToTeV) + delta_kappa - delta_k[j]) < 0 ) ||
    	 ( (-1./(muNeg.Pt()*global_parameters::GeVToTeV) + delta_kappa - delta_k[j]) > 0 ) ) continue;

    // EM 2016.01.11
    // define delta_k[j] as "negative" to compensate the "additive" delta_kappa
    // -- positively charged
    k_prime = +1./(muPos.Pt()*global_parameters::GeVToTeV) + delta_kappa - delta_k[j]; 
    if(k_prime>0){
      ((TH1F*)h_pos_temp)->Fill(k_prime,weight);
      ((TH1F*)h_KSpos_temp)->Fill(k_prime,weight);
    }
    else{
      ((TH1F*)h_neg_temp)->Fill(k_prime*(-1),weight); //filling with the negative to have the same histogram range for the chi2 comparison
      ((TH1F*)h_KSneg_temp)->Fill(k_prime*(-1),weight); //filling with the negative to have the same histogram range for the chi2 comparison
    }	

    // -- negatively charged
    k_prime = -1./(muNeg.Pt()*global_parameters::GeVToTeV) + delta_kappa - delta_k[j];
    if(k_prime<0){
      ((TH1F*)h_neg_temp)->Fill(k_prime*(-1),weight); //filling with the negative to have the same histogram range for the chi2 comparison
      ((TH1F*)h_KSneg_temp)->Fill(k_prime*(-1),weight); //filling with the negative to have the same histogram range for the chi2 comparison
    }
    else{
      ((TH1F*)h_pos_temp)->Fill(k_prime,weight);
      ((TH1F*)h_KSpos_temp)->Fill(k_prime,weight);
    }
  }

}

void GeneralizedEndPointAnalysis::endjob(){
  // counters
  float nsel_pos=0.; 
  float nsel_neg=0.; 
  float nsel2_pos=0.;
  float nsel2_neg=0.;


  // === THE BULK: chi2 and Kolmogorov tests
   for(int i=0;i<n_Dk ;i++){
     TObject* h_pos_temp = HList_pos.At(i);
     TObject* h_neg_temp = HList_neg.At(i);

     TObject* h_KSpos_temp = HListKS_pos.At(i);
     TObject* h_KSneg_temp = HListKS_neg.At(i);

     // cout << "POS --> "<< ((TH1F*)h_pos_temp)->GetXaxis()->GetXmin()<< "/" <<((TH1F*)h_pos_temp)->GetXaxis()->GetXmax() << endl;
     // cout << "NEG --> "<< ((TH1F*)h_neg_temp)->GetXaxis()->GetXmin()<< "/" <<((TH1F*)h_neg_temp)->GetXaxis()->GetXmax() << endl;
    
     nsel_pos = ((TH1F*)h_pos_temp)->Integral();
     nsel_neg = ((TH1F*)h_neg_temp)->Integral();
    
    // --- normalization 
    ((TH1F*)h_pos_temp)->Scale(((TH1F*)h_neg_temp)->Integral()/((TH1F*)h_pos_temp)->Integral());
    ((TH1F*)h_KSpos_temp)->Scale(((TH1F*)h_KSneg_temp)->Integral()/((TH1F*)h_KSpos_temp)->Integral());

    nsel2_pos = ((TH1F*)h_pos_temp)->Integral();
    nsel2_neg = ((TH1F*)h_neg_temp)->Integral();

    cout << "\n";
    cout << "========================================================="<< endl; 
    cout<< "Printing few informations for the delta_k= "<< delta_k[i] << " c/TeV "<<endl; 
    cout<< "* Histogram for k>0 -- "<<endl;
    ((TH1F*)h_pos_temp)->Print();
    cout<< "*  Histogram for k<0 -- "<<endl;
    ((TH1F*)h_neg_temp)->Print();
    cout << " Positive histo --> selected (before normalization) =  "<< nsel_pos << " / (after normalization) = " << nsel2_pos << endl;
    cout << " Negative histo --> selected (before normalization) =  "<< nsel_neg << " / (after normalization) = " << nsel2_neg << endl;
    cout << "\n";
    //double chi2= ((TH1F*)h_pos_temp)->Chi2Test(((TH1F*)h_neg_temp),"UU,CHI2,P");
    //hChi2->Fill(delta_k[i],chi2);
        
    dk[i]= delta_k[i];

    // EM 2016.01.07 Chi2Test changed from "WW" to "UU" to avoid a warning from ROOT
    // chi2[i]= ((TH1F*)h_pos_temp)->Chi2Test(((TH1F*)h_neg_temp),"WW,NORM,CHI2,P"); //CHI2
    // Info in <TH1F::Chi2TestX>: NORM option should be used together with UU option. It is ignored
    //    chi2[i]= ((TH1F*)h_pos_temp)->Chi2Test(((TH1F*)h_neg_temp),"UU,NORM,CHI2,P"); //CHI2

    chi2[i]= ((TH1F*)h_pos_temp)->Chi2Test(((TH1F*)h_neg_temp),"WW,CHI2,P"); //CHI2 

    // sanity check: when using weighted events check that there is no bin with a negative number of entries    
    for (int i=0; i<global_parameters::binningKS; i++) {
      if ( ((TH1F*)h_KSpos_temp)->GetBinContent(i+1) < 0  ||
	   ((TH1F*)h_KSneg_temp)->GetBinContent(i+1) < 0  ) {
	cout << "WARNING in KS test: at least one bin with negative content for dk=" << dk[i] << endl;
      }
    }

    cout << "\n";
    cout<< "* KS Histogram for k>0 -- "<<endl;
    ((TH1F*)h_KSpos_temp)->Print();
    cout<< "*  KS Histogram for k<0 -- "<<endl;
    ((TH1F*)h_KSneg_temp)->Print();

    ks[i] = ((TH1F*)h_KSpos_temp)->KolmogorovTest(((TH1F*)h_KSneg_temp),"D"); 
    
    // --- evaluating the p-value for the 68% CL (--> p-value > 0.32)
    double chisq;
    int ndf, igood;
    double p_value = 0;

    // EM 2016.01.07 Chi2TestX changed from "WW" to "UU" to avoid a warning from ROOT
    // p_value = ((TH1F*)h_pos_temp)->Chi2TestX(((TH1F*)h_neg_temp),chisq,ndf,igood,"WW,NORM,P");

    // EM 2016.01.11 ->
    // p_value = ((TH1F*)h_pos_temp)->Chi2TestX(((TH1F*)h_neg_temp),chisq,ndf,igood,"UU,NORM,P");   
    // if(p_value>=0.32){
    //   dk_68.push_back(delta_k[i]);
    // }    
    // if(p_value>=0.05){ // this is for 2-sigma!
    //   dk_95.push_back(delta_k[i]);
    // }
    // <- EM 2016.01.11 

    // --- Draw them on canvas 

    TObject* canv= Canvas.At(0);
    ((TCanvas*)canv)->cd();
    //((TCanvas*)canv)->SetLogy();

    /// -------------------------
    TPad *pad1 = new TPad("pad1", "pad1", 0, 0.3, 1, 0.985);
    // pad1->SetTopMargin(0.05); 
    pad1->SetBottomMargin(0.08); // Upper and lower plot are joined
    pad1->Draw();             // Draw the upper pad: pad1
    pad1->cd();               // pad1 becomes the current pad
    //pad1->SetLogy();
    // -------------------------

    // set TH1 max for pretty printing
    double h_pos_temp_max = ((TH1F*)h_pos_temp)->GetBinContent(((TH1F*)h_pos_temp)->GetMaximumBin());
    double h_neg_temp_max = ((TH1F*)h_neg_temp)->GetBinContent(((TH1F*)h_neg_temp)->GetMaximumBin());

    ((TH1F*)h_pos_temp)->SetMaximum(1.1*max(h_pos_temp_max,h_neg_temp_max));
    ((TH1F*)h_neg_temp)->SetMaximum(1.1*max(h_pos_temp_max,h_neg_temp_max));
      
    // ((TH1F*)h_pos_temp)->Sumw2(); // EM 2016.01.08 SumW2 already set
    // ((TH1F*)h_neg_temp)->Sumw2(); // EM 2016.01.08 SumW2 already set
    ((TH1F*)h_pos_temp)->SetStats(0);
    ((TH1F*)h_neg_temp)->SetStats(0);
    
    ((TH1F*)h_pos_temp)->SetTitle(""); 
    ((TH1F*)h_neg_temp)->SetTitle(""); 

    ((TH1F*)h_pos_temp)->Draw("E0L");
    ((TH1F*)h_neg_temp)->SetLineColor(kRed);  
    ((TH1F*)h_neg_temp)->SetMarkerColor(kRed);  
    ((TH1F*)h_pos_temp)->SetLineWidth(2);
    ((TH1F*)h_neg_temp)->SetLineWidth(2);
    ((TH1F*)h_neg_temp)->Draw("SAME,E0L");

    char entries_text_pos [200];
    char entries_text_neg [200];
    char entries_text_dk [200];
    char canvas_name_png[200];
    char canvas_name_pdf[200];

    TPaveText *entries_text = new TPaveText(.7,.12,.85,.25,"brNDC");
    sprintf(entries_text_dk,"Injected #Delta#kappa = %.3f c/TeV",delta_k[i]);
    sprintf(entries_text_pos,"Entries #kappa_{pos} = %.0f",nsel_pos);
    sprintf(entries_text_neg,"Entries #kappa_{neg} = %.0f",nsel_neg);
    entries_text->SetFillColor(kWhite);
    entries_text->SetBorderSize(0);
    entries_text->AddText(entries_text_dk);
    entries_text->AddText(entries_text_pos);
    entries_text->AddText(entries_text_neg);
    (entries_text->GetLineWith("neg"))->SetTextColor(kRed);
    entries_text->SetTextSize(0.028);
    entries_text->Draw();

    // -------------
    ((TCanvas*)canv)->cd(); // Go back to the main canvas before defining pad2
    // CMS_lumi(((TCanvas*)canv) , iPeriod, 11 );
    // ((TCanvas*)canv)->Update();
    // ((TCanvas*)canv)->RedrawAxis();

    TPad *pad2 = new TPad("pad2", "pad2", 0, 0.05, 1, 0.3);
    // pad2->SetTopMargin(0.1);
    pad2->SetBottomMargin(0.2);
    pad2->SetGridx(); // vertical grid
    pad2->SetGridy(); 
    pad2->Draw();
    pad2->cd();       // pad2 becomes the current pad

    // Define the ratio plot
    TH1F *h3 = (TH1F*)h_pos_temp->Clone("h3");
    h3->SetLineColor(kBlack);
    h3->SetMinimum(0.0);  // Define Y ..
    h3->SetMaximum(2.0);  // .. range
    //    h3->Sumw2();          // EM 2016.01.08 Sumw2 already set
    h3->SetStats(0);      // No statistics on lower plot
    h3->Divide((TH1F*)h_neg_temp);
    h3->SetMarkerStyle(kFullTriangleUp);
    h3->Draw("ep");       // Draw the ratio plot
    
    //((TH1F*)h_pos_temp)->GetYaxis()->SetTitleSize(20);
    //((TH1F*)h_pos_temp)->GetYaxis()->SetTitleFont(43);
    //((TH1F*)h_pos_temp)->GetYaxis()->SetTitleOffset(1.55);

    // Ratio plot (h3) settings
    h3->SetTitle(""); // Remove the ratio title

    // Y axis ratio plot settings
    h3->GetYaxis()->SetTitle("Ratio pos/neg ");
    h3->GetYaxis()->SetNdivisions(505);
    h3->GetYaxis()->SetTitleSize(18);//was 20
    h3->GetYaxis()->SetTitleFont(43);
    h3->GetYaxis()->SetTitleOffset(1.55);
    h3->GetYaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
    h3->GetYaxis()->SetLabelSize(13); //was 15
    
    // X axis ratio plot settings
    h3->GetXaxis()->SetTitleSize(18);//was 20
    h3->GetXaxis()->SetTitleFont(43);
    h3->GetXaxis()->SetTitleOffset(4.);
    h3->GetXaxis()->SetLabelFont(43); // Absolute font size in pixel (precision 3)
    h3->GetXaxis()->SetLabelSize(13);//was 15

    // ==============

    ((TCanvas*)canv)->Draw(); 

    sprintf(canvas_name_png,"dk_%i.png",i);
    sprintf(canvas_name_pdf,"dk_%i.pdf",i);
    ((TCanvas*)canv)->SaveAs(Form("%s%s",dirname, canvas_name_png));
    ((TCanvas*)canv)->SaveAs(Form("%s%s",dirname, canvas_name_pdf)); 

    // canvas and th1 are saved in ROOT file the original macro....
    // outFile->cd("extra_plots");
    // ((TCanvas*)canv)->Write();  
    // ((TH1F*)h_pos_temp)->Write();
    // ((TH1F*)h_neg_temp)->Write();

    entries_text->Clear();
    pad1->Clear();
    pad2->Clear();

    
   } // end of loop on dK

   the_dir->cd();
  
   TGraph *grChi2 = new TGraph(n_Dk,dk,chi2);
   grChi2->SetMarkerColor(kBlue);
   
   TGraph *grKS = new TGraph(n_Dk,dk,ks);
   grKS->SetMarkerColor(kRed);
   grKS->SetLineColor(kRed);  

   // EM 2016.01.08 next Write() statements likely not needed
   // mg->Write();
   // grChi2->Write();
   // grKS->Write();
   
   // --- opening canvas

   //   TCanvas *c1 = new TCanvas("c1","curvature",800,800);

   //   TLegend * legend = new TLegend(.4,.6 + 0.07,.6,.6 + 0.18 + 0.09);

   // === Writing on the canvas
   // c1->cd();
   // //c1->SetLogy();
   // legend->SetTextFont(42);
   // legend->SetTextSize(0.028);
   // legend->SetFillColor(kWhite); 
   // legend->SetBorderSize(0); 
   // legend->SetHeader("#eta ranges:"); 
   // hcurv->SetStats(kFALSE);
   // hcurv->SetLineWidth(2);
   // hcurv->Draw();
   // hcurv->SetTitle(";#kappa [c/GeV];Entries");//muon q/p_{T} curvature (for different #eta ranges)
   
   // legend->AddEntry(hcurv, " full #eta ", "L");
   // legend->Draw("SAME");
      
   TFitResultPtr r = grChi2->Fit("pol2","RSV","",-30*global_parameters::dk_step,+30*global_parameters::dk_step);
   TF1 *myFunc = grChi2->GetFunction("pol2");
   myFunc->SetLineWidth(1);
   myFunc->SetLineColor(kBlue);
   
   grChi2->SetMarkerStyle(kFullDotMedium);
   grChi2->SetTitle("#chi^{2} minimization vs. #Delta#kappa; #Delta#kappa [c/TeV];#chi^{2}");
   grKS->SetMarkerStyle(kFullDotMedium);
   grKS->SetTitle("Kolmogorov test probability vs. #Delta#kappa; #Delta#kappa [c/TeV]; KS prob.");

   // --- CHI2 TEST
   
   // --- calculating the minimum chi2 and its uncertainty (assuming parabolic beahviour in the minimum)   
   double dk_minChi2 = myFunc->GetMinimumX(-0.5,+0.5); // careful [-0.5,+0.5] hardcoded !!!
   double chi2plusone = myFunc->Eval(dk_minChi2)+1;
   double dk_minChi2_uncert = TMath::Abs(dk_minChi2 - (myFunc->GetX(chi2plusone,-0.5,+0.5)));

   char result_text[200];      
   sprintf(result_text,"#Delta#kappa = %.3f +/- %.3f c/TeV",dk_minChi2,dk_minChi2_uncert);
   TPaveText *ptext_chi2 = new TPaveText(.4,.72,.65,.78,"brNDC"); 
   ptext_chi2->SetFillColor(kWhite);
   //ptext->SetTextSize(0.04);
   
   // chi2 graph
   TCanvas *c2 = new TCanvas("c2","Chi2",800,800);
   c2->cd();  
   grChi2->Draw("AP");
   ptext_chi2->AddText(result_text);
   ptext_chi2->Draw();
   c2->Update();
   
   c2->SaveAs(Form("%schi2.png",dirname));
   c2->SaveAs(Form("%schi2.pdf",dirname));
   c2->Write();

   // --- K-S TEST

   // --- calculating the max K-S 
   double maxKS = 0;
   double dk_maxKS;
   for(int i=0;i<n_Dk;i++) {
     if(ks[i]>maxKS) {
       maxKS=ks[i];
       dk_maxKS=dk[i];
     }
   }
   
   sprintf(result_text,"#Delta#kappa = %.3f c/TeV",dk_maxKS);
   TPaveText *ptext_KS = new TPaveText(.15,.72,.40,.78,"brNDC"); 
   ptext_KS->SetFillColor(kWhite);

   // KS graph
   TCanvas *c3 = new TCanvas("c3","Kolmogorov",800,800);
   c3->cd();  
   grKS->Draw("ACP");
   ptext_KS->AddText(result_text);
   ptext_KS->Draw();
   c3->Update();
   
   c3->SaveAs(Form("%sKS.png",dirname));
   c3->SaveAs(Form("%sKS.pdf",dirname));
   c3->Write();
   
   TCanvas *c4 = new TCanvas("c4","KolmogorovAndChi2",0,0,800,800);
   TPad *pad = new TPad("pad","",0,0,1,1);
   pad->Draw();
   pad->cd();

   // draw a frame to define the range
   TH1F *hr = c4->DrawFrame(-0.5,0,+0.5,chi2[0]);
   hr->SetXTitle("#Delta #kappa");
   hr->SetYTitle("#chi^{2}");
   pad->GetFrame()->SetBorderSize(12);
   
   grChi2->Draw("P");
      
   //create a transparent pad drawn on top of the main pad
   c4->cd();   
   TPad *overlay = new TPad("overlay","",0,0,1,1);
   overlay->SetFillStyle(4000);
   overlay->SetFillColor(kWhite);
   overlay->SetFrameFillStyle(4000);
   overlay->Draw();
   overlay->cd();
      
   Double_t xmin = pad->GetUxmin();
   Double_t ymin = 0;
   Double_t xmax = pad->GetUxmax();
   Double_t ymax = maxKS*1.1;

   TH1F *hframe = overlay->DrawFrame(xmin,ymin,xmax,ymax);
   hframe->GetXaxis()->SetLabelOffset(99);
   hframe->GetYaxis()->SetLabelOffset(99);
   hframe->GetYaxis()->SetTickLength(0);
   grKS->Draw("PC");
      
   //Draw an axis on the right side
   TGaxis *axis = new TGaxis(xmax,ymin,xmax, ymax,ymin,ymax,510,"+L");
   axis->SetLineColor(kRed);
   axis->SetLabelColor(kRed);
   axis->Draw();

   TPaveText *ptext = new TPaveText(.10,.10,.30,.20,"brNDC");
   ptext->SetFillColor(kWhite);
   sprintf(result_text,"IN: #Delta#kappa = %.3f c/TeV",delta_kappa);
   ptext->AddText(result_text);
   sprintf(result_text,"OUT (#chi^{2}): #Delta#kappa = %.3f +/- %.3f c/TeV",dk_minChi2,dk_minChi2_uncert);
   ptext->AddText(result_text);
   sprintf(result_text,"OUT (K-S): #Delta#kappa = %.3f c/TeV",dk_maxKS);
   ptext->AddText(result_text);
   ptext->Draw();

   c4->SaveAs(Form("%schi2_KS.png",dirname));
   c4->SaveAs(Form("%schi2_KS.pdf",dirname));  
   c4->Write();   

   // c4->SetFillStyle(4000);
   // c4->SetFillColor(0);
   // c4->SetFrameFillStyle(4000);
   // c4->Draw();
   // c4->cd();
   // c4->Update();
  
  // c1->SaveAs(Form("%scurvature.png",dirname));
  // c1->SaveAs(Form("%scurvature.pdf",dirname));

   
  return;
 }

  
