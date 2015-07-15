//Roofit classes
#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooAddPdf.h"
#include "RooGenericPdf.h"
#include "RooPlot.h"
#include "RooDataHist.h"
#include "RooExponential.h"
#include "RooAbsData.h"
#include "RooBreitWigner.h"
#include "RooPolynomial.h"
//non Roofit classes
#include "TCanvas.h"
#include <iostream>
#include <fstream>
#include <TMath.h>
#include <TH1F.h>
#include <TF1.h>
#include <TFile.h>
#include <TCanvas.h>
#include <TString.h>
#include <TLegend.h>
#include <TPaveText.h>
using namespace std;
using namespace RooFit;

void LineshapeAnalyser(){

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  //          Initialization
  //

  //Set input files 
  TString filename1=    "../test/input/GenMuonAnalyzerHistos_beforeFSR.root";
  TString filename2=    "../test/input/GenMuonAnalyzerHistos_afterFSR.root";
  //Fast rename tool, rename just these lines when you change input files
  TString EnergyFile1="13";       //insert "Sqrt(s)" of the filename1
  TString EnergyFile2="13";       //insert "Sqrt(s)" of the filename2
  TString VersionFile1="beforeISR";     //insert "v" of the filename1
  TString VersionFile2="afterISR";      //insert "v" of the filename2
  TString CutFile1="";
  TString CutFile2="";

  //Labels and titles used below 
  TString TitleLineshape1 = "Z Lineshape #sqrt{s} = "+EnergyFile1+" TeV ("+VersionFile1+" "+CutFile1+")";
  TString TitleLineshape2 = "Z Lineshape #sqrt{s} = "+EnergyFile2+" TeV ("+VersionFile2+" "+CutFile2+")";
  TString TitleRatio = "Z Lineshape Ratio #sqrt{s} = "+EnergyFile1+" TeV ("+VersionFile1+" "+CutFile1+")  /  #sqrt{s} = "+EnergyFile2+" TeV ("+VersionFile2+" "+CutFile2+")";
  TString TitleFit1 = "Z Lineshape Fit #sqrt{s} = "+EnergyFile1+" TeV ("+VersionFile1+" "+CutFile1+") ";
  TString TitleFit2= "Z Lineshape Fit #sqrt{s} = "+EnergyFile2+" TeV ("+VersionFile2+" "+CutFile2+")";
  TString LabelData1="#sqrt{s}= "+EnergyFile1+" TeV ("+VersionFile1+" "+CutFile1+") Data";//legend title h1 blue
  TString LabelData2="#sqrt{s}= "+EnergyFile2+" TeV ("+VersionFile2+" "+CutFile2+") Data";//legend title h1 blue
  TString LabelFit1="#sqrt{s}= "+EnergyFile2+" TeV ("+VersionFile2+" "+CutFile2+") Fit";//legend title h2 red
  TString LabelFit2="#sqrt{s}= "+EnergyFile2+" TeV ("+VersionFile2+" "+CutFile2+") Fit";//legend title h2 red
  TString LabelRatio="Ratio";//legend title h2 red
  
  //Png files output saves
  TString OutputComparisonPng="../test/output/"+EnergyFile1+"TeV("+VersionFile1+CutFile1+")_vs_ "+EnergyFile2+"Tev("+VersionFile2+CutFile2+")_Comparison.png";
  TString OutputFitPng="../test/output/"+EnergyFile1+"TeV("+VersionFile1+CutFile1+")_vs_ "+EnergyFile2+"Tev("+VersionFile2+CutFile2+")_Fit.png";
   
    
   /////////////////////////////////RootFit Initialization
  //Variables (name, title, initial value, allowed range)
  //  RooRealVar x("x","x",71.1888,111.19) ; //we use this to fit
  RooRealVar x("x","x",81.,101.) ; //we use this to fit
  RooRealVar mean("Mean","mean of BW",91,89,92,"GeV") ;// to set a good start value is very important
  RooRealVar width("Width","width of BW",2.5,1,5,"GeV");
  RooRealVar lambda1("Exp. lambda1","Exponential constant",1,-10,10,"GeV");
  RooRealVar lambda2("Exp. lambda2","Exponential constant",1,-10,10,"GeV");
  RooRealVar k0("a0","0th order linear coefficient",71.1888,111.19,"Gev") ;
  RooRealVar k1("a1","1th order linear coefficient",71.1888,111.19) ;

  // Build pdfs
  RooBreitWigner BW("BW","Breit-Wigner PDF",x,mean,width) ;  
  RooExponential Exp1("Exp1","Exponential PDF",x,lambda1);
  RooExponential Exp2("Exp2","Exponential PDF",x,lambda2);
  RooPolynomial Linear("Linear","Linear PDF",x,RooArgList(k0,k1),1);
 
  //User defined pdf  
  RooGenericPdf RBW("Relativistic Breit-Wigner","RBW","@0/(pow(@0*@0 - @1*@1,2) + @2*@2*@0*@0*@0*@0/(@1*@1))",RooArgList(x,mean,width));
  
  // Sum of pdfs, fraction is the weight of the second pdf wrt to the first
  RooRealVar fraction("Fraction","Weight of the second pdf",0.5,0.,1.) ;
  RooAddPdf  Sum_ExpRBW("Exp+RBW","Exp+RBW",RooArgList(Exp1,RBW),fraction) ;
  RooAddPdf  Sum_LinearRBW("Linear+RBW","Linear+RBW",RooArgList(Linear,RBW),fraction) ;
  RooAddPdf  Sum_ExpBW("Exp+BW","Exp+BW",RooArgList(Exp1,BW),fraction) ;
  RooAddPdf  Sum_LinearBW("Linear+BW","Linear+BW",RooArgList(Linear,BW),fraction) ;

  // Construct plot frame in 'x' first canvas
  RooPlot* xframe11 = x.frame(Title(TitleLineshape1)) ;
  RooPlot* xframe12 = x.frame(Title(TitleLineshape2)) ;
  RooPlot* xframe13 = x.frame(Title(TitleRatio)) ;
  // Construct plot frame in 'x' second canvas
  RooPlot* xframe21 = x.frame(Title(TitleFit1)) ;
  RooPlot* xframe22 = x.frame(Title(TitleFit2)) ;
  RooPlot* xframe23 = x.frame(Title(TitleRatio)) ;

  ////////////////////////////////End RootFit initialization
  //Histograms
  TFile f1(filename1);
  TH1F *h1 = (TH1F*)f1.Get("demo/h1_MuMuMass");
  TFile f2(filename2);   
  TH1F *h2 = (TH1F*)f2.Get("demo/h1_MuMuMass");
  
  //        END Initialization
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////












  
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////






  
  
  






  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  /////////      Event representation

  
  //Create RooDataHist needed in frame 11,12,21,22
  RooDataHist DataLineshape1("h1data","h1 data",RooArgList(x),h1);
  RooDataHist DataLineshape2("h2data","h2 data",RooArgList(x),h2); //1.black 2.red 3.green 4.blue
  TCanvas *Canvas1 = new TCanvas("Comparison","Comparison",0,0,700,1000); 
  TCanvas *Canvas2 = new TCanvas("Fit","Fit",0,0,700,1000); 
  Canvas1->Divide(1,3);
  Canvas2->Divide(1,3);
  
  

  // FRAME 11
  DataLineshape1.plotOn(xframe11,
			MarkerStyle(1),MarkerColor(kRed),
			LineStyle(1),LineColor(kRed),LineWidth(2),
			DataError(RooAbsData::None),
			Binning(1001,71.1888,111.19 ),
			DrawOption("PEX0C"));
  //Set up a legend for Canvas1 frame11
  TLegend *leg11=0; 
  leg11 = new TLegend(0.76,0.55,0.99,0.7,"Z Lineshape");  
  leg11->SetBorderSize(1);
  leg11->SetFillColor(0);
  leg11->SetTextFont(42);
  h1->SetLineColor(kRed);
  leg11->AddEntry(h1,LabelData1,"L");
  Canvas1->cd(1); xframe11->Draw(); leg11->Draw("same");
  


  
  // FRAME 12
  DataLineshape2.plotOn(xframe12,
			MarkerStyle(1),MarkerColor(kBlue),
			LineStyle(1),LineColor(kBlue),LineWidth(2),
			DataError(RooAbsData::None), 
			Binning(1001, 71.1888,111.19) ,
			DrawOption("PEX0C"));
  //Set up a legend for Canvas1 frame12
  TLegend *leg12=0; 
  leg12 = new TLegend(0.76,0.55,0.99,0.7,"Z Lineshape");  
  leg12->SetBorderSize(1);
  leg12->SetFillColor(0);
  leg12->SetTextFont(42);
  h2->SetLineColor(kBlue);
  leg12->AddEntry(h2,LabelData2,"L");
  Canvas1->cd(2); xframe12->Draw(); leg12->Draw("same");
  
  
  
  // FRAME 21
  DataLineshape1.plotOn(xframe21,
			MarkerStyle(1),MarkerColor(kRed),
			LineStyle(1),LineColor(kRed),LineWidth(2),
			DataError(RooAbsData::None),
			Binning(1001,71.1888,111.19 ),
			DrawOption("PEX0C"));
  //Fit data lineshape 1 and plot on frame
  Sum_ExpBW.fitTo(DataLineshape1,Range(86.5,96.5)); //fit in this range
  Sum_ExpBW.plotOn(xframe21,LineColor(kBlack),LineWidth(2));
  Sum_ExpBW.paramOn(xframe21,Layout(0.65));//,RooArgSet(mean,width,lambda1,fraction),kFALSE,"",2,"NELU",0.73, 0.99,0.55,0) ;//xmin,xmax,ymax
  /* here some functions easy to copy and paste 
  //-----------LINEAR + BW
  Sum_LinearBW.fitTo(DataLineshape1);
  Sum_LinearBW.plotOn(xframe21,LineColor(kBlack),LineWidth(2));
  Sum_LinearBW.paramOn(xframe21,RooArgSet(mean,width,k0,k1,fraction),kFALSE,"",2,"NELU",0.73, 0.99,0.55,0) ;//xmin,xmax,ymax
  //-----------LINEAR + RBW
  Sum_LinearRBW.fitTo(DataLineshape1);
  Sum_LinearRBW.plotOn(xframe21,LineColor(kBlack),LineWidth(2));
  Sum_LinearRBW.paramOn(xframe21,RooArgSet(mean,width,k0,k1,fraction),kFALSE,"",2,"NELU",0.73, 0.99,0.55,0) ;//xmin,xmax,ymax
  //-----------EXPONENTIAL + RBW
  Sum_ExpRBW.fitTo(DataLineshape1);
  Sum_ExpRBW.plotOn(xframe21,LineColor(kBlack),LineWidth(2));
  Sum_ExpRBW.paramOn(xframe21,RooArgSet(mean,width,c,fraction),kFALSE,"",2,"NELU",0.73, 0.99,0.55,0) ;//xmin,xmax,ymax
  //-----------EXPONENTIAL + BW
  Sum_ExpBW.fitTo(DataLineshape1);
  Sum_ExpBW.plotOn(xframe21,LineColor(kBlack),LineWidth(2));
  Sum_ExpBW.paramOn(xframe21,RooArgSet(mean,width,c,fraction),kFALSE,"",2,"NELU",0.73, 0.99,0.55,0) ;//xmin,xmax,ymax
  */
  //Set up a legend for Canvas2 frame21 (Fit1)
  h1->SetLineColor(kRed);
  TLegend *leg21=0; 
  leg21 = new TLegend(0.73,0.55,0.99,0.7,"Fit");  
  leg21->SetBorderSize(1);
  leg21->SetFillColor(0);
  leg21->SetTextFont(42);
  leg21->AddEntry(h1,LabelData1,"L");
  leg21->AddEntry(&RBW,"Fit","L");
  Canvas2->cd(1); xframe21->Draw(); leg21->Draw("same");



  // FRAME 22
  DataLineshape2.plotOn(xframe22,
		       	MarkerStyle(1),MarkerColor(kBlue),
			LineStyle(1),LineColor(kBlue),LineWidth(2),
			DataError(RooAbsData::None), 
			Binning(1001, 71.1888,111.19),
			DrawOption("PEX0C"));

  //Fit data lineshape 2 and plot on frame
  Sum_ExpBW.fitTo(DataLineshape2,Range(83.,95.5));
  Sum_ExpBW.plotOn(xframe22,LineColor(kBlack),LineWidth(2));
  Sum_ExpBW.paramOn(xframe22,Layout(0.65));//,RooArgSet(mean,width,lambda1,fraction),kFALSE,"",2,"NELU",0.73, 0.99,0.55,0) ;//xmin,xmax,ymax
  /* here some functions easy to copy and paste 
  //-----------LINEAR + BW
  Sum_LinearBW.fitTo(DataLineshape2);
  Sum_LinearBW.plotOn(xframe22,LineColor(kBlack),LineWidth(2));
  Sum_LinearBW.paramOn(xframe22,RooArgSet(mean,width,k0,k1,fraction),kFALSE,"",2,"NELU",0.73, 0.99,0.55,0) ;//xmin,xmax,ymax
  //-----------LINEAR + RBW
  Sum_LinearRBW.fitTo(DataLineshape2);
  Sum_LinearRBW.plotOn(xframe22,LineColor(kBlack),LineWidth(2));
  Sum_LinearRBW.paramOn(xframe22,RooArgSet(mean,width,k0,k1,fraction),kFALSE,"",2,"NELU",0.73, 0.99,0.55,0) ;//xmin,xmax,ymax
  //-----------EXPONENTIAL + BW
  Sum_ExpBW.fitTo(DataLineshape2);
  Sum_ExpBW.plotOn(xframe22,LineColor(kBlack),LineWidth(2));
  Sum_ExpBW.paramOn(xframe22,RooArgSet(mean,width,c,fraction),kFALSE,"",2,"NELU",0.73, 0.99,0.55,0) ;//xmin,xmax,ymax
  //-----------EXPONENTIAL + RBW
  Sum_ExpRBW.fitTo(DataLineshape2);
  Sum_ExpRBW.plotOn(xframe22,LineColor(kBlack),LineWidth(2));
  Sum_ExpRBW.paramOn(xframe22,RooArgSet(mean,width,c,fraction),kFALSE,"",2,"NELU",0.73, 0.99,0.55,0) ;//xmin,xmax,ymax
 */
  //Set up a legend for Canvas2 frame22 (Fit1)
  TLegend *leg22=0; 
  leg22 = new TLegend(0.73,0.55,0.99,0.7,"Fit ");  
  leg22->SetBorderSize(1);
  leg22->SetFillColor(0);
  leg22->SetTextFont(42);
  // h2->SetLineColor(kBlue);
  leg22->AddEntry(h2,LabelData2,"L");
  leg22->AddEntry(&RBW,"Fit","L");
  Canvas2->cd(2); xframe22->Draw(); leg22->Draw("same");
  
  
  
  
  //Create RooDataHist needed in frame 13,23
  h1->Divide(h2); //create Ratio h1/h2
  RooDataHist Ratio("ratio","Ratio",RooArgList(x),h1);




  // FRAME 13
  Ratio.plotOn(xframe13,
	       MarkerStyle(1),MarkerColor(kMagenta),
	       LineStyle(1),LineColor(kMagenta),LineWidth(2),
	       DataError(RooAbsData::None), 
	       Binning(1001, 71.1888,111.19),
	       DrawOption("PEX0C"));
  //Set up a legend for Canvas1 frame13
  TLegend *leg13=0; 
  leg13 = new TLegend(0.76,0.55,0.99,0.7,"Ratio file1/file2");  
  leg13->SetBorderSize(1);
  leg13->SetFillColor(0);
  leg13->SetTextFont(42);
  Canvas1->cd(3); xframe13->Draw(); xframe13->GetYaxis()->SetRangeUser(0.75,1.25);
  h1->SetLineColor(kMagenta);
  leg13->AddEntry(h1,LabelRatio,"PL");
  leg13->Draw("same");
  




  // FRAME 23
  Ratio.plotOn(xframe23,
	       MarkerStyle(1),MarkerColor(kMagenta),
	       LineStyle(1),LineColor(kMagenta),LineWidth(2),
	       DataError(RooAbsData::None), 
	       Binning(1001, 71.1888,111.19),
	       DrawOption("PEX0C"));
  //the legend for this frame is already defined as leg13
  Canvas2->cd(3); xframe23->Draw(); xframe23->GetYaxis()->SetRangeUser(0.75,1.25);
  h1->SetLineColor(kMagenta);
  leg13->Draw("same");
  
 
  /////////      END Event representation
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  

  Canvas1->Update();
  Canvas2->Update();
  Canvas1->SaveAs(OutputComparisonPng);
  Canvas2->SaveAs(OutputFitPng);
  
  f1.Close();
  f2.Close();
  
}




/*//////////// MORE..

  ///////// ricetta per sommare due pdf
  RooAddPdf  Bgd_ExpExp("Exp1+Exp2","Exp1+Exp2",RooArgList(Exp1,Exp2),fraction);
  RooAddPdf  Sum_BgdRBW("Exp1+RBW","Exp1+RBW",RooArgList(RBW,Exp1),sigfraction );
  RooAddPdf  Sum_BgdRBW("Exp1+Exp2+RBW","Exp1+Exp2+RBW",RooArgList(RBW,Bgd_ExpExp),sigfraction );
  
*/
