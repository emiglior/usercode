#!/usr/bin/env python
import sys
import ROOT
import math
import array
from optparse import OptionParser

###############
def setStyle():
###############
    ROOT.gStyle.SetTitleX(0.55)
    ROOT.gStyle.SetTitleAlign(23)
    #  TH1::StatOverflows(kTRUE)
    ROOT.gStyle.SetOptTitle(1)
    ROOT.gStyle.SetOptStat("e")
    ROOT.gStyle.SetPadTopMargin(0.08)
    ROOT.gStyle.SetPadBottomMargin(0.10)
    ROOT.gStyle.SetPadLeftMargin(0.18)
    ROOT.gStyle.SetPadRightMargin(0.05)
    ROOT.gStyle.SetPadBorderMode(0)
    ROOT.gStyle.SetTitleFillColor(10)
    ROOT.gStyle.SetTitleFont(42)
    ROOT.gStyle.SetTitleTextColor(ROOT.kBlue)
    ROOT.gStyle.SetTitleFontSize(0.06)
    ROOT.gStyle.SetTitleBorderSize(0)
    ROOT.gStyle.SetStatColor(ROOT.kWhite)
    ROOT.gStyle.SetStatFont(42)
    ROOT.gStyle.SetStatFontSize(0.05)
    ROOT.gStyle.SetStatTextColor(1)
    ROOT.gStyle.SetStatFormat("6.4g")
    ROOT.gStyle.SetStatBorderSize(1)
    ROOT.gStyle.SetPadTickX(1)  #To get tick marks on the opposite side of the frame
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetPadBorderMode(0)
    ROOT.gStyle.SetOptFit(1)
    ROOT.gStyle.SetNdivisions(510)

############################
def getExtrema(h1array):
############################
    the_max = 0.
    the_min =999.

    for h1 in h1array:
        this_max = h1.GetMaximum()
        this_min = h1.GetMinimum();
        if this_max>the_max:
            the_max = this_max
        if this_min<the_min:
            the_min = this_min
        
# print "Minimum: ", the_min ", Maximum: ", the_max
    return the_min, the_max

######################################################
def MakeNiceTrendPlotStyle( hist, color, the_extrema):
######################################################
    colors  = [ROOT.kRed,       ROOT.kRed,       ROOT.kBlue,      ROOT.kMagenta]
    markers = [ROOT.kOpenCircle,ROOT.kOpenCircle,ROOT.kFullCircle,ROOT.kOpenSquare]
    styles  = [ROOT.kSolid,     ROOT.kDashed,    ROOT.kSolid,     ROOT.kDotted]
    hist.SetStats(ROOT.kFALSE)  
    hist.GetXaxis().CenterTitle(ROOT.kTRUE)
    hist.GetYaxis().CenterTitle(ROOT.kTRUE)
    hist.GetXaxis().SetTitleFont(42) 
    hist.GetYaxis().SetTitleFont(42)  
    hist.GetXaxis().SetTitleSize(0.065)
    hist.GetYaxis().SetTitleSize(0.065)
    hist.GetXaxis().SetTitleOffset(0.75)
    hist.GetYaxis().SetTitleOffset(1.3)
    hist.GetXaxis().SetLabelFont(42)
    hist.GetYaxis().SetLabelFont(42)
    hist.GetYaxis().SetLabelSize(.06)
    hist.GetXaxis().SetLabelSize(.05)
    hist.SetMarkerSize(1.5)
#    if color == 0:
#        hist.SetMarkerStyle(markers[color])
    hist.SetLineColor(colors[color])
    hist.SetLineStyle(styles[color])
    hist.SetLineWidth(3)
    hist.SetMarkerColor(colors[color])
    hist.GetYaxis().SetRangeUser(the_extrema[0]*0.9,the_extrema[1]*1.1)

#####################
def getTH1cdf(h1_in):
#####################
# return c.d.f. of the input TH1
    h1_name = h1_in.GetName()+"_cdf"
    h1_title = h1_in.GetTitle()+" CDF"
    nbbin = h1_in.GetNbinsX()
    xmin = h1_in.GetNbinsX()
    cdf = ROOT.TH1F(h1_name, h1_title, nbbin, h1_in.GetXaxis().GetXmin(), h1_in.GetXaxis().GetXmax())

    total = 0
    for i in xrange(nbbin):    
        total += h1_in.GetBinContent(i)
        cdf.SetBinContent(i,total)

    integral = h1_in.Integral()
    cdf.Scale(1./integral)
    return cdf

#########################
def getTH1GausFit(h1_in, pad, gaussfit):
#######################
    pad.cd()
    pad.SetLogy()

    if gaussfit ==  True:
        # fit with gaussian (two-steps) and return mu and sigma
        xmin = h1_in.GetXaxis().GetXmin()
        xmax = h1_in.GetXaxis().GetXmax()

        # Start with a fit on +-1 RMS
        minfit = max(h1_in.GetMean() - h1_in.GetRMS(),xmin)
        maxfit = min(h1_in.GetMean() + h1_in.GetRMS(),xmax)

        # icnt is used to have a unique name for the TF1 
        getTH1GausFit.icnt += 1

        nameF1 = "g"+str(getTH1GausFit.icnt)
        g1 = ROOT.TF1(nameF1,"gaus",minfit,maxfit)
        g1.SetLineColor(ROOT.kRed)
        g1.SetLineWidth(2)
        h1_in.Fit(g1,"RQ")
  
        g1.SetRange(minfit,maxfit)
        h1_in.Fit(g1,"RQ")

        # One more iteration
        minfit = max(g1.GetParameter("Mean") - 2*g1.GetParameter("Sigma"),xmin)
        maxfit = min(g1.GetParameter("Mean") + 2*g1.GetParameter("Sigma"),xmax)
        g1.SetRange(minfit,maxfit)
        h1_in.Fit(g1,"RQ")

        mu = g1.GetParameter("Mean") 
        sigma = g1.GetParameter("Sigma")
    else:
        h1_in.Draw() 
        mu = h1_in.GetMean() 
        sigma = h1_in.GetRMS()

    return mu, sigma

#########################
class HistoStruct():
#########################
    """ container to store standard histos vs. a given variable V """

    def __init__(self, V_name, V_nbins, V_min, V_max, V_label, V_output_root_file, V_gaussfit):
    ###########################################################################################
        self.the_name = V_name
        self.the_nbins = V_nbins
        self.the_min = V_min
        self.the_max = V_max

        self.the_gaussfit = V_gaussfit

        self.the_output_root_file = V_output_root_file        
        current_dir = self.the_output_root_file.mkdir(V_name) 
        current_dir.cd()

        # define the data members not passed via the constructor
        self.the_xAxis = ROOT.TAxis(V_nbins,V_min,V_max) 

        self.h_V = ROOT.TH1F("h_%s" % V_name, str("monitor input variable; %s ;" % V_label) ,V_nbins, V_min, V_max)

        # list of TH1s
        self.q_inVBinTH1 = []
        self.q_secondaries_inVBinTH1 = []
        self.spreadX_inVBinTH1 = []
        self.spreadX_primaries_inVBinTH1 = []
        self.spreadY_inVBinTH1 = []
        self.spreadY_primaries_inVBinTH1 = []
        self.alpha_inVBinTH1 = []
        self.beta_inVBinTH1 = []

        V_span = (V_max-V_min)/V_nbins
        for i in xrange(V_nbins):
            V_low  = V_min+i*V_span
            V_high = V_low+V_span
        
            # Q cluster
            hname = "h1_q_%sBin%d" % (V_name ,i)
            htitle = "h1_q_%s bin %d (%.2f < %s < %.2f);Q_{uncorr} [ke];recHits" % (V_name, i, V_low, V_label, V_high)
            self.q_inVBinTH1.append( ROOT.TH1F(hname,htitle,80,0.,400.))

            # Q cluster (only secondaries)
            hname = "h1_q_secondaries_%sBin%d" % (V_name ,i)
            htitle = "h1_q_secondaries_%s bin %d (%.2f < %s < %.2f);Q_{uncorr} [ke];recHits" % (V_name, i, V_low, V_label, V_high)
            self.q_secondaries_inVBinTH1.append( ROOT.TH1F(hname,htitle,80,0.,400.))

            hname = "h1_spreadX_%sBin%d" % (V_name ,i)
            htitle = "h1_spreadX_%s bin %d (%.2f < %s < %.2f); spread;recHits" % (V_name, i, V_low, V_label, V_high)
            self.spreadX_inVBinTH1.append( ROOT.TH1F(hname,htitle,15,0.5,15.5))

            hname = "h1_spreadX_primaries_%sBin%d" % (V_name ,i)
            htitle = "h1_spreadX_primaries_%s bin %d (%.2f < %s < %.2f); spread;recHits" % (V_name, i, V_low, V_label, V_high)
            self.spreadX_primaries_inVBinTH1.append( ROOT.TH1F(hname,htitle,15,0.5,15.5))

            hname = "h1_spreadY_%sBin%d" % (V_name ,i)
            htitle = "h1_spreadY_%s bin %d (%.2f < %s < %.2f); spread;recHits" % (V_name, i, V_low, V_label, V_high)
            self.spreadY_inVBinTH1.append( ROOT.TH1F(hname,htitle,15,0.5,15.5))

            hname = "h1_spreadY_primaries_%sBin%d" % (V_name ,i)
            htitle = "h1_spreadY_primaries_%s bin %d (%.2f < %s < %.2f); spread;recHits" % (V_name, i, V_low, V_label, V_high)
            self.spreadY_primaries_inVBinTH1.append( ROOT.TH1F(hname,htitle,15,0.5,15.5))

            hname = "h1_alpha_%sBin%d" % (V_name ,i)
            htitle = "h1_alpha_%s bin %d (%.2f < %s < %.2f); #alpha;recHits" % (V_name, i, V_low, V_label, V_high)
            self.alpha_inVBinTH1.append( ROOT.TH1F(hname,htitle,80,0,1.6))

            hname = "h1_beta_%sBin%d" % (V_name ,i)
            htitle = "h1_beta_%s bin %d (%.2f < %s < %.2f); #beta;recHits" % (V_name, i, V_low, V_label, V_high)
            self.beta_inVBinTH1.append( ROOT.TH1F(hname,htitle,80,0,1.6))

        ### r-phi residuals
        current_subdir = current_dir.mkdir("residualsX")         
        current_subdir.cd()         

        self.resX_qall_inVBinTH1 = []
        self.resX_qlow_inVBinTH1 = []
        self.resX_qhigh_inVBinTH1 = []
        self.resX_qprimaries_inVBinTH1 = []

        for i in xrange(V_nbins):
            V_low  = V_min+i*V_span
            V_high = V_low+V_span
        
            hname = "h1_resX_qall_%sBin%d" % (V_name ,i)
            htitle = "h1_resX_qall_%s bin %d (%.2f < %s < %.2f);[#mum];recHits" % (V_name, i, V_low, V_label, V_high)
            self.resX_qall_inVBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))
            hname = "h1_resX_qlow_%sBin%d" % (V_name ,i)
            htitle = "h1_resX_qlow_%s bin %d (%.2f < %s < %.2f);[#mum];recHits" % (V_name, i, V_low, V_label, V_high)
            self.resX_qlow_inVBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))
            hname = "h1_resX_qhigh_%sBin%d" % (V_name ,i)
            htitle = "h1_resX_qhigh_%s bin %d (%.2f < %s < %.2f);[#mum];recHits" % (V_name, i, V_low, V_label, V_high)
            self.resX_qhigh_inVBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))
            hname = "h1_resX_qprimaries_%sBin%d" % (V_name ,i)
            htitle = "h1_resX_qprimaries_%s bin %d (%.2f < %s < %.2f);[#mum];recHits" % (V_name, i, V_low, V_label, V_high)
            self.resX_qprimaries_inVBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))        

        # final histograms
        if self.the_gaussfit == True:
            extra_ytitle_res  = "gaussian stdDev #sigma [#mum]" 
            extra_ytitle_bias = "gaussian #mu [#mum]"
        else:
            extra_ytitle_res  = "RMS [#mum]" 
            extra_ytitle_bias = "mean [#mum]"
            
        self.h_resRPhivsV_qall  = ROOT.TH1F("h_resRPhivs%s_qall" % V_name, str("Barrel #varphi-Hit Resolution; %s ;" % V_label)+extra_ytitle_res,V_nbins,V_min,V_max)
        self.h_resRPhivsV_qlow  = ROOT.TH1F("h_resRPhivs%s_qlow" % V_name, str("Barrel #varphi-Hit Resolution; %s ;" % V_label)+extra_ytitle_res,V_nbins,V_min,V_max)
        self.h_resRPhivsV_qhigh = ROOT.TH1F("h_resRPhivs%s_qhigh" % V_name,str("Barrel #varphi-Hit Resolution; %s ;" % V_label)+extra_ytitle_res,V_nbins,V_min,V_max)
        self.h_resRPhivsV_qprimaries = ROOT.TH1F("h_resRPhivs%s_qprimaries" % V_name,str("Barrel #varphi-Hit Resolution; %s ;" % V_label)+extra_ytitle_res,V_nbins,V_min,V_max)
    
        self.h_biasRPhivsV_qall  = ROOT.TH1F("h_biasRPhivs%s_qall" % V_name, str("Barrel #varphi-Hit Bias; %s ;" % V_label)+extra_ytitle_bias,V_nbins,V_min,V_max)
        self.h_biasRPhivsV_qlow  = ROOT.TH1F("h_biasRPhivs%s_qlow" % V_name, str("Barrel #varphi-Hit Bias; %s ;" % V_label)+extra_ytitle_bias,V_nbins,V_min,V_max)
        self.h_biasRPhivsV_qhigh = ROOT.TH1F("h_biasRPhivs%s_qhigh" % V_name,str("Barrel #varphi-Hit Bias; %s ;" % V_label)+extra_ytitle_bias,V_nbins,V_min,V_max)
        self.h_biasRPhivsV_qprimaries = ROOT.TH1F("h_biasRPhivs%s_qprimaries" % V_name,str("Barrel #varphi-Hit Bias; %s ;" % V_label)+extra_ytitle_bias,V_nbins,V_min,V_max)

        ### z residuals 
        current_subdir = current_dir.mkdir("residualsY")         
        current_subdir.cd()         

        self.resY_qall_inVBinTH1 = []
        self.resY_qlow_inVBinTH1 = []
        self.resY_qhigh_inVBinTH1 = []
        self.resY_qprimaries_inVBinTH1 = []

        for i in xrange(V_nbins):
            V_low  = V_min+i*V_span
            V_high = V_low+V_span
        
            hname = "h1_resY_qall_%sBin%d" % (V_name ,i)
            htitle = "h1_resY_qall_%s bin %d (%.2f < %s < %.2f);[#mum];recHits" % (V_name, i, V_low, V_label, V_high)
            self.resY_qall_inVBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))
            hname = "h1_resY_qlow_%sBin%d" % (V_name ,i)
            htitle = "h1_resY_qlow_%s bin %d (%.2f < %s < %.2f);[#mum];recHits" % (V_name, i, V_low, V_label, V_high)
            self.resY_qlow_inVBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))
            hname = "h1_resY_qhigh_%sBin%d" % (V_name ,i)
            htitle = "h1_resY_qhigh_%s bin %d (%.2f < %s < %.2f);[#mum];recHits" % (V_name, i, V_low, V_label, V_high)
            self.resY_qhigh_inVBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))
            hname = "h1_resY_qprimaries_%sBin%d" % (V_name ,i)
            htitle = "h1_resY_qprimaries_%s bin %d (%.2f < %s < %.2f);[#mum];recHits" % (V_name, i, V_low, V_label, V_high)
            self.resY_qprimaries_inVBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))        

        # final histograms
        if V_gaussfit == True:
            extra_ytitle_res  = "gaussian stdDev #sigma [#mum]" 
            extra_ytitle_bias = "gaussian #mu [#mum]"
        else:
            extra_ytitle_res  = "RMS [#mum]" 
            extra_ytitle_bias = "mean [#mum]"
            
        self.h_resZvsV_qall  = ROOT.TH1F("h_resZvs%s_qall" % V_name, str("Barrel z-Hit Resolution; %s ;" % V_label)+extra_ytitle_res,V_nbins,V_min,V_max)
        self.h_resZvsV_qlow  = ROOT.TH1F("h_resZvs%s_qlow" % V_name, str("Barrel z-Hit Resolution; %s ;" % V_label)+extra_ytitle_res,V_nbins,V_min,V_max)
        self.h_resZvsV_qhigh = ROOT.TH1F("h_resZvs%s_qhigh" % V_name,str("Barrel z-Hit Resolution; %s ;" % V_label)+extra_ytitle_res,V_nbins,V_min,V_max)
        self.h_resZvsV_qprimaries = ROOT.TH1F("h_resZvs%s_qprimaries" % V_name,str("Barrel z-Hit Resolution; %s ;" % V_label)+extra_ytitle_res,V_nbins,V_min,V_max)
    
        self.h_biasZvsV_qall  = ROOT.TH1F("h_biasZvs%s_qall" % V_name, str("Barrel z-Hit Bias; %s ;" % V_label)+extra_ytitle_bias,V_nbins,V_min,V_max)
        self.h_biasZvsV_qlow  = ROOT.TH1F("h_biasZvs%s_qlow" % V_name, str("Barrel z-Hit Bias; %s ;" % V_label)+extra_ytitle_bias,V_nbins,V_min,V_max)
        self.h_biasZvsV_qhigh = ROOT.TH1F("h_biasZvs%s_qhigh" % V_name,str("Barrel z-Hit Bias; %s ;" % V_label)+extra_ytitle_bias,V_nbins,V_min,V_max)
        self.h_biasZvsV_qprimaries = ROOT.TH1F("h_biasZvs%s_qprimaries" % V_name,str("Barrel z-Hit Bias; %s ;" % V_label)+extra_ytitle_bias,V_nbins,V_min,V_max)
        

    def FillFirstLoop(self, the_V, pixel_recHit):
    #############################################

# conversion factors
        CmToUm = 10000. # length -> from cm to um
        ToKe = 0.001    # charge -> from e to ke
##################################################

        if self.the_min<=the_V and the_V<=self.the_max:
            index = self.the_xAxis.FindBin(the_V)
            self.q_inVBinTH1[index-1].Fill(pixel_recHit.q*ToKe)

            # Q cluster (only secondaries)
            if pixel_recHit.process != 2:
                self.q_secondaries_inVBinTH1[index-1].Fill(pixel_recHit.q*ToKe)

            self.spreadX_inVBinTH1[index-1].Fill(min(pixel_recHit.spreadx, 15))
            self.spreadY_inVBinTH1[index-1].Fill(min(pixel_recHit.spready, 15))

            if pixel_recHit.process == 2:
                self.spreadX_primaries_inVBinTH1[index-1].Fill(min(pixel_recHit.spreadx, 15))
                self.spreadY_primaries_inVBinTH1[index-1].Fill(min(pixel_recHit.spready, 15))

                self.alpha_inVBinTH1[index-1].Fill(math.atan(math.fabs(pixel_recHit.tz/pixel_recHit.tx)))
                self.beta_inVBinTH1[index-1].Fill(math.atan(math.fabs(pixel_recHit.tz/pixel_recHit.ty)))
                

    def FillSecondLoop(self, the_V, pixel_recHit, QaveCorr):
    ####################################################

# conversion factors
        CmToUm = 10000. # length -> from cm to um
        ToKe = 0.001    # charge -> from e to ke
##################################################

        # monitor input variable
        self.h_V.Fill(the_V)

        if self.the_min<=the_V and the_V<=self.the_max:
            index = self.the_xAxis.FindBin(the_V)
        
            self.resX_qprimaries_inVBinTH1[index-1].Fill((pixel_recHit.hx-pixel_recHit.x)*CmToUm)
            self.resY_qprimaries_inVBinTH1[index-1].Fill((pixel_recHit.hy-pixel_recHit.y)*CmToUm)

            if  pixel_recHit.q*math.fabs(pixel_recHit.tz)*ToKe < QaveCorr:
                self.resX_qlow_inVBinTH1[index-1].Fill((pixel_recHit.hx-pixel_recHit.x)*CmToUm)
                self.resY_qlow_inVBinTH1[index-1].Fill((pixel_recHit.hy-pixel_recHit.y)*CmToUm)
                self.resX_qall_inVBinTH1[index-1].Fill((pixel_recHit.hx-pixel_recHit.x)*CmToUm)
                self.resY_qall_inVBinTH1[index-1].Fill((pixel_recHit.hy-pixel_recHit.y)*CmToUm)
                
            elif  pixel_recHit.q*math.fabs(pixel_recHit.tz)*ToKe < 1.5*QaveCorr:
                self.resX_qhigh_inVBinTH1[index-1].Fill((pixel_recHit.hx-pixel_recHit.x)*CmToUm)
                self.resY_qhigh_inVBinTH1[index-1].Fill((pixel_recHit.hy-pixel_recHit.y)*CmToUm)
                self.resX_qall_inVBinTH1[index-1].Fill((pixel_recHit.hx-pixel_recHit.x)*CmToUm)
                self.resY_qall_inVBinTH1[index-1].Fill((pixel_recHit.hy-pixel_recHit.y)*CmToUm)
                
        
    def DrawAllCanvas(self, Qave):
    ##############################
        
        ### fill the final histograms
        # ceil(x): the smallest integer value greater than or equal to x (NB return a float)
        w = math.ceil(math.sqrt(self.the_nbins))
        h = math.ceil(self.the_nbins/w)
        #    print int(w), int(h)
                      
        c1_qclus = ROOT.TCanvas("c1_qclus","c1_qclus",900,900)
        c1_qclus.SetFillColor(ROOT.kWhite)
        c1_qclus.Divide(int(w),int(h))
        
        c1_spreadXY = ROOT.TCanvas("c1_spreadXY","c1_spreadXY",900,900)
        c1_spreadXY.SetFillColor(ROOT.kWhite)
        c1_spreadXY.Divide(int(w),int(h))
        
        c1_primaries_spreadXY = ROOT.TCanvas("c1_primaries_spreadXY","c1_primaries_spreadXY",900,900)
        c1_primaries_spreadXY.SetFillColor(ROOT.kWhite)
        c1_primaries_spreadXY.Divide(int(w),int(h))
        
        c1_alphabeta = ROOT.TCanvas("c1_alphabeta","c1_alphabeta",900,900)
        c1_alphabeta.SetFillColor(ROOT.kWhite)
        c1_alphabeta.Divide(int(w),int(h))

        # need to store TLines in a list otherwise only the lines for the last pad are kept on the canvas
        line1 = []
        line2 = []
        line3 = []
        line1s = []
        line2s = []

        for i in xrange(self.the_nbins):

            ### charge distribution (not normalized)
            # vertical lines are Qave/sin(theta) for the low/up edge of the bin (NB: Qave is normalized)
            c1_qclus.cd(i+1)
            self.q_inVBinTH1[i].Draw()
            self.q_inVBinTH1[i].SetMaximum(self.q_inVBinTH1[i].GetMaximum()*1.1)
            ymax = self.q_inVBinTH1[i].GetMaximum()

            xlow = self.the_xAxis.GetBinLowEdge(i+1)
            tmp1 = math.exp(-xlow)               # t=tg(theta/2) = exp(-eta)  
            tmp2 = (1.0+tmp1*tmp1)/(2.0*tmp1)    # 1/sin(theta)=(1+t^2)/(2*t)
            line1.append(ROOT.TLine(Qave*tmp2,0.6*ymax,Qave*tmp2,ymax))
            line1[i].SetLineColor(ROOT.kMagenta)
            line1[i].Draw("same")

            xup = self.the_xAxis.GetBinUpEdge(i+1)
            tmp1 = math.exp(-xup)               # t=tg(theta/2) = exp(-eta)  
            tmp2 = (1.0+tmp1*tmp1)/(2.0*tmp1)   # 1/sin(theta)=(1+t^2)/(2*t)
            line2.append(ROOT.TLine(Qave*tmp2,0.6*ymax,Qave*tmp2,ymax))
            line2[i].SetLineColor(ROOT.kMagenta)
            line2[i].Draw("same")
            
            line3.append(ROOT.TLine(self.q_inVBinTH1[i].GetMean(),0,self.q_inVBinTH1[i].GetMean(),0.4*ymax))
            line3[i].SetLineColor(ROOT.kRed)
            line3[i].Draw("same")
            
            # draw Q_cluster for particle from secondry interactions
            self.q_secondaries_inVBinTH1[i].SetLineColor(ROOT.kGreen)
            self.q_secondaries_inVBinTH1[i].Draw("same")

            ###
            c1_spreadXY.cd(i+1)
            self.spreadY_inVBinTH1[i].SetLineColor(ROOT.kBlue)
            self.spreadY_inVBinTH1[i].Draw()
            self.spreadX_inVBinTH1[i].SetLineColor(ROOT.kRed)
            self.spreadX_inVBinTH1[i].Draw("same")

            ymax = self.spreadY_inVBinTH1[i].GetMaximum()
        
            line1s.append(ROOT.TLine(self.spreadX_inVBinTH1[i].GetMean(),0,self.spreadX_inVBinTH1[i].GetMean(),0.4*ymax))
            line1s[i].SetLineStyle(ROOT.kDotted)
            line1s[i].SetLineColor(ROOT.kRed)
            line1s[i].Draw("same")
            line2s.append(ROOT.TLine(self.spreadY_inVBinTH1[i].GetMean(),0,self.spreadY_inVBinTH1[i].GetMean(),0.4*ymax))
            line2s[i].SetLineStyle(ROOT.kDotted)
            line2s[i].SetLineColor(ROOT.kBlue)
            line2s[i].Draw("same")
            
            ###
            c1_primaries_spreadXY.cd(i+1)
            self.spreadY_primaries_inVBinTH1[i].SetLineColor(ROOT.kBlue)
            self.spreadY_primaries_inVBinTH1[i].Draw()
            self.spreadX_primaries_inVBinTH1[i].SetLineColor(ROOT.kRed)
            self.spreadX_primaries_inVBinTH1[i].Draw("same")
        
            ###
            c1_alphabeta.cd(i+1)
            self.beta_inVBinTH1[i].SetLineColor(ROOT.kBlue)
            self.beta_inVBinTH1[i].Draw()
            self.alpha_inVBinTH1[i].SetLineColor(ROOT.kRed)
            self.alpha_inVBinTH1[i].Draw("same")


        # save the canvas
        c1_qclus.SaveAs("c1_qclus_in%sBin.pdf" % self.the_name)
        c1_spreadXY.SaveAs("c1_spreadXY_in%sBin.pdf" % self.the_name)
        c1_primaries_spreadXY.SaveAs("c1_primaries_spreadXY_in%sBin.pdf" % self.the_name)
        c1_alphabeta.SaveAs("c1_alphabeta_in%sBin.pdf" % self.the_name)


        # residuals
        c1_rPhi_qall = ROOT.TCanvas("c1_rPhi_qall","c1_rPhi_qall",900,900)
        c1_rPhi_qall.SetFillColor(ROOT.kWhite)
        c1_rPhi_qall.Divide(int(w),int(h))
        c1_rPhi_qlow = ROOT.TCanvas("c1_rPhi_qlow","c1_rPhi_qlow",900,900)
        c1_rPhi_qlow.SetFillColor(ROOT.kWhite)
        c1_rPhi_qlow.Divide(int(w),int(h))
        c1_rPhi_qhigh = ROOT.TCanvas("c1_rPhi_qhigh","c1_rPhi_qhigh",900,900)
        c1_rPhi_qhigh.SetFillColor(ROOT.kWhite)
        c1_rPhi_qhigh.Divide(int(w),int(h))
        c1_rPhi_qprimaries = ROOT.TCanvas("c1_rPhi_qprimaries","c1_rPhi_qprimaries",900,900)
        c1_rPhi_qprimaries.SetFillColor(ROOT.kWhite)
        c1_rPhi_qprimaries.Divide(int(w),int(h))
        
        c1_z_qall = ROOT.TCanvas("c1_z_qall","c1_z_qall",900,900)
        c1_z_qall.SetFillColor(ROOT.kWhite)
        c1_z_qall.Divide(int(w),int(h))
        c1_z_qlow = ROOT.TCanvas("c1_z_qlow","c1_z_qlow",900,900)
        c1_z_qlow.SetFillColor(ROOT.kWhite)
        c1_z_qlow.Divide(int(w),int(h))
        c1_z_qhigh = ROOT.TCanvas("c1_z_qhigh","c1_z_qhigh",900,900)
        c1_z_qhigh.SetFillColor(ROOT.kWhite)
        c1_z_qhigh.Divide(int(w),int(h))
        c1_z_qprimaries = ROOT.TCanvas("c1_z_qprimaries","c1_z_qprimaries",900,900)
        c1_z_qprimaries.SetFillColor(ROOT.kWhite)
        c1_z_qprimaries.Divide(int(w),int(h))

        # initialize the counter (there is only one instance of the function getTH1GausFit)
        getTH1GausFit.icnt = 0 
        for i in xrange(self.the_nbins):

            c1_rPhi_qall.cd(i+1)
            mu, sigma = getTH1GausFit(self.resX_qall_inVBinTH1[i], c1_rPhi_qall.GetPad(i+1), self.the_gaussfit)
            self.h_resRPhivsV_qall.SetBinContent(i+1,sigma)
            self.h_biasRPhivsV_qall.SetBinContent(i+1,mu)
            
            c1_rPhi_qlow.cd(i+1)        
            mu, sigma = getTH1GausFit(self.resX_qlow_inVBinTH1[i], c1_rPhi_qlow.GetPad(i+1), self.the_gaussfit)
            self.h_resRPhivsV_qlow.SetBinContent(i+1,sigma)
            self.h_biasRPhivsV_qlow.SetBinContent(i+1,mu)

            c1_rPhi_qhigh.cd(i+1)        
            mu, sigma = getTH1GausFit(self.resX_qhigh_inVBinTH1[i], c1_rPhi_qhigh.GetPad(i+1), self.the_gaussfit)
            self.h_resRPhivsV_qhigh.SetBinContent(i+1,sigma)
            self.h_biasRPhivsV_qhigh.SetBinContent(i+1,mu)
            
            c1_rPhi_qprimaries.cd(i+1)        
            mu, sigma = getTH1GausFit(self.resX_qprimaries_inVBinTH1[i], c1_rPhi_qprimaries.GetPad(i+1), self.the_gaussfit)
            self.h_resRPhivsV_qprimaries.SetBinContent(i+1,sigma)
            self.h_biasRPhivsV_qprimaries.SetBinContent(i+1,mu)
            
            c1_z_qall.cd(i+1)
            mu, sigma = getTH1GausFit(self.resY_qall_inVBinTH1[i], c1_z_qall.GetPad(i+1), self.the_gaussfit)
            self.h_resZvsV_qall.SetBinContent(i+1,sigma)
            self.h_biasZvsV_qall.SetBinContent(i+1,mu)
            
            c1_z_qlow.cd(i+1)        
            mu, sigma = getTH1GausFit(self.resY_qlow_inVBinTH1[i], c1_z_qlow.GetPad(i+1), self.the_gaussfit)
            self.h_resZvsV_qlow.SetBinContent(i+1,sigma)
            self.h_biasZvsV_qlow.SetBinContent(i+1,mu)
            
            c1_z_qhigh.cd(i+1)        
            mu, sigma = getTH1GausFit(self.resY_qhigh_inVBinTH1[i], c1_z_qhigh.GetPad(i+1), self.the_gaussfit)
            self.h_resZvsV_qhigh.SetBinContent(i+1,sigma)
            self.h_biasZvsV_qhigh.SetBinContent(i+1,mu)
            
            c1_z_qprimaries.cd(i+1)        
            mu, sigma = getTH1GausFit(self.resY_qprimaries_inVBinTH1[i], c1_z_qprimaries.GetPad(i+1), self.the_gaussfit)
            self.h_resZvsV_qprimaries.SetBinContent(i+1,sigma)
            self.h_biasZvsV_qprimaries.SetBinContent(i+1,mu)

        c1_rPhi_qall.SaveAs ("c1_rPhi_qall_in%sBin.pdf" % self.the_name)
        c1_rPhi_qlow.SaveAs ("c1_rPhi_qlow_in%sBin.pdf" % self.the_name)
        c1_rPhi_qhigh.SaveAs("c1_rPhi_qhigh_in%sBin.pdf" % self.the_name)
        c1_rPhi_qprimaries.SaveAs("c1_rPhi_qprimaries_in%sBin.pdf" % self.the_name)
        
        c1_z_qall.SaveAs("c1_z_qall_in%sBin.pdf" % self.the_name)
        c1_z_qlow.SaveAs("c1_z_qlow_in%sBin.pdf" % self.the_name)
        c1_z_qhigh.SaveAs("c1_z_qhigh_in%sBin.pdf" % self.the_name)
        c1_z_qprimaries.SaveAs("c1_z_qprimaries_in%sBin.pdf" % self.the_name)


        # draw nice trend plots
        setStyle()

        lego = ROOT.TLegend(0.35,0.75,0.75,0.88)
        lego.SetFillColor(10)
        lego.SetTextSize(0.05)
        lego.SetTextFont(42)
        lego.SetFillColor(10)
        lego.SetLineColor(10)
        lego.SetShadowColor(10)
        
        cResVsV_1 = ROOT.TCanvas("cResVs%s_1" % self.the_name,"cResVs%s_1" % self.the_name,500,700)
        rphi_arr = []
        rphi_arr.append(self.h_resRPhivsV_qlow)
        rphi_arr.append(self.h_resRPhivsV_qhigh)
        rphi_arr.append(self.h_resRPhivsV_qprimaries)
  
        the_extrema = getExtrema(rphi_arr)
        MakeNiceTrendPlotStyle(self.h_resRPhivsV_qlow,0,the_extrema)
        self.h_resRPhivsV_qlow.Draw("C")
        MakeNiceTrendPlotStyle(self.h_resRPhivsV_qhigh,1,the_extrema)
        self.h_resRPhivsV_qhigh.Draw("Csame")
        MakeNiceTrendPlotStyle(self.h_resRPhivsV_qprimaries,3,the_extrema)
        self.h_resRPhivsV_qprimaries.Draw("Csame")
        
        lego.AddEntry(self.h_resRPhivsV_qlow,"primaries Q/#LTQ#GT<1") 
        lego.AddEntry(self.h_resRPhivsV_qhigh,"primaries 1<Q/#LTQ#GT<1.5")
        lego.AddEntry(self.h_resRPhivsV_qprimaries,"primaries Q/#LTQ#GT<1.5")
        
        lego.Draw("same")
        cResVsV_1.SaveAs("rmsVs%s_rphi.root" % self.the_name)
        
        cResVsV_2 = ROOT.TCanvas("cResVs%s_2" % self.the_name,"cResVs%s_2" % self.the_name,500,700)
        z_arr = []
        z_arr.append(self.h_resZvsV_qlow)
        z_arr.append(self.h_resZvsV_qhigh)
        z_arr.append(self.h_resZvsV_qprimaries)
        
        the_extrema = getExtrema(z_arr)        
        MakeNiceTrendPlotStyle(self.h_resZvsV_qlow,0,the_extrema)
        self.h_resZvsV_qlow.Draw("C")
        MakeNiceTrendPlotStyle(self.h_resZvsV_qhigh,1,the_extrema)
        self.h_resZvsV_qhigh.Draw("Csame")
        MakeNiceTrendPlotStyle(self.h_resZvsV_qprimaries,3,the_extrema)
        self.h_resZvsV_qprimaries.Draw("Csame")
        
        lego.Draw("same")
        cResVsV_2.SaveAs("rmsVs%s_rz.root" % self.the_name)

#####################
def declare_struct():
#####################
# ROOT defined struct(s) present in the input tree
    ROOT.gROOT.ProcessLine("struct evt_t {\
    Int_t           run;\
    Int_t           evtnum;\
    };" )

    ROOT.gROOT.ProcessLine("struct pixel_recHit_t {\
    Int_t       pdgid;\
    Int_t     process;\
    Float_t         q;\
    Float_t         x;\
    Float_t         y;\
    Float_t         xx;\
    Float_t         xy;\
    Float_t         yy;\
    Float_t         row;\
    Float_t         col;\
    Float_t         gx;\
    Float_t         gy;\
    Float_t         gz;\
    Int_t           subid;\
    Int_t           module;\
    Int_t           layer;\
    Int_t           ladder;\
    Int_t           disk;\
    Int_t           blade;\
    Int_t           panel;\
    Int_t           side;\
    Int_t           nsimhit;\
    Int_t           spreadx;\
    Int_t           spready;\
    Float_t         hx;\
    Float_t         hy;\
    Float_t         tx;\
    Float_t         ty;\
    Float_t         tz;\
    Float_t         theta;\
    Float_t         phi;\
    };" )


###############
def main():
###############

# conversion factors
    CmToUm = 10000. # length -> from cm to um
    ToKe = 0.001    # charge -> from e to ke
##################################################

    parser = OptionParser()
    parser.add_option("-f", "--file",  
                      action="store", type="string", dest="input_root_filename",
                      help="input root file")
    parser.add_option("-o", "--on-track",
                      action="store_true", dest="ontrack", default=False,
                      help="use on track clusters (default is all clusters)")
    parser.add_option("-g", "--gauss",
                      action="store_true", dest="gaussfit", default=False,
                      help="gaussian fit of residuals (default is RMS)")
    parser.add_option("-e", "--entries",
                      action="store", type="int", dest="entries", default=-1,
                      help="number of entries")
    
    (options, args) = parser.parse_args()

# do not pop-up canvases as they are drawn
    ROOT.gROOT.SetBatch(ROOT.kTRUE) 

    # input root file
    try:
        input_root_file = ROOT.TFile.Open(options.input_root_filename)
    except:
        print "No input file specified"
        sys.exit()
        
    output_root_filename = "PlotResHistos"
    if options.ontrack == False: 
        input_tree = input_root_file.Get("PixelNtuple")
        output_root_filename += "_All"
    else:
        input_tree = input_root_file.Get("Pixel2Ntuple")            
        output_root_filename += "_OnTrack"

    if options.gaussfit == False: 
        output_root_filename += "_RMS"
    else:
        output_root_filename += "_Sigma"

    output_root_filename += ".root"

    input_tree.Print()
        
    # import the ROOT defined struct(s) in pyROOT
    declare_struct()
    from ROOT import evt_t, pixel_recHit_t

    # define the pyROOT classes and assign the address
    evt = evt_t()
    pixel_recHit = pixel_recHit_t()
    input_tree.SetBranchAddress("evt",ROOT.AddressOf(evt,"run"))        
    input_tree.SetBranchAddress("pixel_recHit",ROOT.AddressOf(pixel_recHit,"pdgid"))
    
    output_root_file = ROOT.TFile(output_root_filename,"RECREATE")

    ### HIT POSITIONS
    output_root_file.mkdir("hitmapsAndCharge") 
    output_root_file.cd("hitmapsAndCharge") 

    ### hit maps
    h2_rzhitmapSubId1 = ROOT.TH2F("h2_rzhitmapSubId1","rzhitmap_subid1; recHit z [cm]; recHit r [cm]",200,-300.,300.,150,0.,150.)
    h2_rzhitmapSubId2 = ROOT.TH2F("h2_rzhitmapSubId2","rzhitmap_subid2; recHit z [cm]; recHit r [cm]",200,-300.,300.,150,0.,150.)    
    h2_rzhitmapSelected = ROOT.TH2F("h2_rzhitmapSelected","rzhitmap; recHit z [cm]; recHit r [cm]",100,-50.,50.,100,2.5,5.)

    ### simhit and rechit local positions
    h1_localX_witdh1_simHit = ROOT.TH1F("h1_localX_witdh1_simHit","h1_localX_witdh1_simHit",2000,-10000,+10000)
    h1_localX_witdh1_recHit = ROOT.TH1F("h1_localX_witdh1_recHit","h1_localX_witdh1_recHit",2000,-10000,+10000)
    h1_localX_witdh1_delta = ROOT.TH1F("h1_localX_witdh1_delta","h1_localX_witdh1_delta",80,-400,+400)

    h1_localY_witdh1_simHit = ROOT.TH1F("h1_localY_witdh1_simHit","h1_localY_witdh1_simHit",7000,-35000,+35000)
    h1_localY_witdh1_recHit = ROOT.TH1F("h1_localY_witdh1_recHit","h1_localY_witdh1_recHit",7000,-35000,+35000)
    h1_localY_witdh1_delta = ROOT.TH1F("h1_localY_witdh1_delta","h1_localY_witdh1_delta",80,-400,+400)    

    # size of the bin is dXxdY um^2
    dX = 100
    dY = 100 
    nX = (8200*2)/dX
    nY = (33000*2)/dY
    print "Local HitMaps nX, nY: ", nX, nY
    h2_localXY_simHit = ROOT.TH2F("h2_localXY_simHit","h2_localXY_simHit",nX,-8200,+8200,nY,-33000,33000) 
    h2_localXY_recHit = ROOT.TH2F("h2_localXY_recHit","h2_localXY_recHit",nX,-8200,+8200,nY,-33000,33000)

    ### 
    h1_qcorr  = ROOT.TH1F("h1_qcorr","h1_qcorr primaries;Q_{corr} [ke]; recHits",200,0.,400.)

    ### histo containers
    hsEta  = HistoStruct("Eta" ,25, 0.,2.5, "|#eta|", output_root_file, options.gaussfit)
    hsZeta = HistoStruct("Zeta",50, 0.,25., "|z|"   , output_root_file, options.gaussfit)
    hsCotgBeta  = HistoStruct("CotgBeta" ,30,0.,6., "|cotg(#beta)|", output_root_file, options.gaussfit)

    all_entries = input_tree.GetEntries()
    if options.entries != -1:
        all_entries = options.entries
    print "all_entries ", all_entries        

    ######## 1st loop on the tree
    for this_entry in xrange(all_entries):
        input_tree.GetEntry(this_entry)

        if this_entry % 100000 == 0:
            print "Loop #1 Procesing Event: ", this_entry

        # global position of the rechit
        # NB sin(theta) = tv3.Perp()/tv3.Mag()
        tv3 = ROOT.TVector3(pixel_recHit.gx, pixel_recHit.gy, pixel_recHit.gz)
    
        # hitmap for sanity check (phase1 subid=1/2 -> BPIX/FPIX, phase2 subid=1/2 barrel/endcap)
        if (pixel_recHit.subid==1):
            h2_rzhitmapSubId1.Fill(tv3.z(),tv3.Perp())
        elif (pixel_recHit.subid==2): 
            h2_rzhitmapSubId2.Fill(tv3.z(),tv3.Perp())

        # BPIX only (layer 1)
        if pixel_recHit.subid==1 and pixel_recHit.layer==1:
            h2_rzhitmapSelected.Fill(tv3.z(),tv3.Perp())

            # map of local positions 
            h2_localXY_simHit.Fill(pixel_recHit.hx*CmToUm,pixel_recHit.hy*CmToUm) 
            h2_localXY_recHit.Fill(pixel_recHit.x*CmToUm ,pixel_recHit.y*CmToUm) 

            # map of local positions for clusters with projected width=1 ("pettine")
            if pixel_recHit.spreadx == 1:
                h1_localX_witdh1_simHit.Fill(pixel_recHit.hx*CmToUm) 
                h1_localX_witdh1_recHit.Fill(pixel_recHit.x*CmToUm) 
                h1_localX_witdh1_delta.Fill((pixel_recHit.hx-pixel_recHit.x)*CmToUm)
            if pixel_recHit.spready == 1:
                h1_localY_witdh1_simHit.Fill(pixel_recHit.hy*CmToUm)                 
                h1_localY_witdh1_recHit.Fill(pixel_recHit.y*CmToUm) 
                h1_localY_witdh1_delta.Fill((pixel_recHit.hy-pixel_recHit.y)*CmToUm)
#                print "SimHitY: ", pixel_recHit.hy*CmToUm, " RecHitY: ", pixel_recHit.y*CmToUm, " DeltaY: ", 

#            print "cos^2(a)+cos^2(b)+cos^2(g)=", pixel_recHit.tx*pixel_recHit.tx+pixel_recHit.ty*pixel_recHit.ty+pixel_recHit.tz*pixel_recHit.tz # debug

            if pixel_recHit.tz >= 0:
                beta = math.atan(-pixel_recHit.tz/pixel_recHit.ty)
            else:
                beta = math.atan(pixel_recHit.tz/pixel_recHit.ty)
            if beta<0: 
                beta = math.pi+beta                                

            # your preferred definition of eta
            the_eta = tv3.Eta()
#            the_eta = -math.log(math.tan(0.5*beta))

            # ionization corrected for incident angle (only primaries at central eta) 
            if math.fabs(the_eta)<0.20 and pixel_recHit.process == 2:
                h1_qcorr.Fill(pixel_recHit.q*ToKe*math.fabs(pixel_recHit.tz))
                # effective thickness estimated from eta of recHit
#                h1_qcorr.Fill(pixel_recHit.q*ToKe*tv3.Perp()/tv3.Mag())

            hsEta.FillFirstLoop(math.fabs(the_eta), pixel_recHit)
            hsZeta.FillFirstLoop(math.fabs(tv3.z()), pixel_recHit)
            hsCotgBeta.FillFirstLoop(math.fabs(1./math.tan(beta)), pixel_recHit)

    ### Compute the Q averaged in the central eta-bin
    output_root_file.cd("hitmapsAndCharge") 
    h1_qcorr_norm = getTH1cdf(h1_qcorr)
    Qave = h1_qcorr.GetMean()
    print "Average Corrected Q cluster [ke]: ", Qave


    ######## 2nd loop on the tree (required when selections based Qave are used)
    for this_entry in xrange(all_entries):
        input_tree.GetEntry(this_entry)

        if this_entry % 100000 == 0:
            print "Loop #2 Procesing Event: ", this_entry

        # BPIX only (layer 1)
        if pixel_recHit.subid==1 and pixel_recHit.layer==1:

            # global position of the rechit
            # NB sin(theta) = tv3.Perp()/tv3.Mag()
            tv3 = ROOT.TVector3(pixel_recHit.gx, pixel_recHit.gy, pixel_recHit.gz)

            if pixel_recHit.tz >= 0:
                beta = math.atan(-pixel_recHit.tz/pixel_recHit.ty)
            else:
                beta = math.atan(pixel_recHit.tz/pixel_recHit.ty)
            if beta<0: 
                beta = math.pi+beta

            # residuals for clusters Q<1.5*Q_ave from primaries only (same selection as Morris Swartz)
            if pixel_recHit.q*ToKe < 1.5*Qave/math.fabs(pixel_recHit.tz) and pixel_recHit.process == 2:
               hsEta.FillSecondLoop(math.fabs(tv3.Eta()), pixel_recHit, Qave)
               hsZeta.FillSecondLoop(math.fabs(tv3.z()), pixel_recHit, Qave)
               hsCotgBeta.FillSecondLoop(math.fabs(1./math.tan(beta)), pixel_recHit, Qave)
            # effective thickness estimated from eta of recHit
            # the_eta = tv3.Eta()
            # if pixel_recHit.q*ToKe < 1.5*Qave*tv3.Mag()/tv3.Perp():
            #     hsEta.FillSecondLoop(math.fabs(the_eta), pixel_recHit, Qave*tv3.Mag()/tv3.Perp())
            #     hsZeta.FillSecondLoop(math.fabs(tv3.z()), pixel_recHit, Qave*tv3.Mag()/tv3.Perp())
            #     hsCotgBeta.FillSecondLoop(math.fabs(1./math.tan(beta)), pixel_recHit, Qave*tv3.Mag()/tv3.Perp())


    ########################
    ### SUMMARY CANVASES ###
    ########################

    ### local position 
    c1_localXY = ROOT.TCanvas("c1_localXY","c1_localXY",600,900)
    c1_localXY.SetFillColor(ROOT.kWhite)
#    c1_localXY.Divide(2,2)
    c1_localXY.Divide(1,2)

    c1_localXY.cd(1)
    h1_localX_witdh1_recHit.SetLineColor(ROOT.kRed) 
    h1_localX_witdh1_recHit.Draw() 
    h1_localX_witdh1_simHit.Draw("same") 

    c1_localXY.cd(2)
    h1_localY_witdh1_recHit.SetLineColor(ROOT.kRed) 
    h1_localY_witdh1_recHit.Draw() 
    h1_localY_witdh1_simHit.Draw("same") 

#    c1_localXY.cd(3)
#    h1_localX_witdh1_delta.Draw() 
#
#    c1_localXY.cd(4)
#    h1_localY_witdh1_delta.Draw() 

    c1_localXY.SaveAs("c1_localXY.root")

    ### local position 
    c1_localXY_hitmap = ROOT.TCanvas("c1_localXY_hitmap","c1_localXY_hitmap",164*3,330*3) # size of the canvas has the same aspect ratio of the module 
    c1_localXY_hitmap.SetFillColor(ROOT.kWhite)
    c1_localXY_hitmap.Divide(2,1)
    
    # # red-blue
    # stops = [ 0.00, 0.50, 1.00]
    # red   = [ 0.00, 0.50, 1.00]
    # green = [ 0.00, 0.00, 0.00]
    # blue  = [ 1.00, 0.50, 0.00]

    # s = array.array('d', stops)
    # r = array.array('d', red)
    # g = array.array('d', green)
    # b = array.array('d', blue)
    
    # npoints = len(s)
    # ncontours = 8
    # ROOT.TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
    # ROOT.gStyle.SetNumberContours(ncontours)
    # 
    
    c1_localXY_hitmap.cd(1)
    h2_localXY_simHit.Draw("boxcolz")     
    c1_localXY_hitmap.cd(2)
    h2_localXY_recHit.Draw("boxcolz") 
    
    c1_localXY_hitmap.SaveAs("c1_localXY_hitmap.root")
    
    hsEta.DrawAllCanvas(Qave)
    hsZeta.DrawAllCanvas(Qave)
    hsCotgBeta.DrawAllCanvas(Qave)

    output_root_file.Write()
    output_root_file.Close()

##################################
if __name__ == "__main__":        
    main()
