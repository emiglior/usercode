#!/usr/bin/python
import ROOT
import math

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
    colors = [4,2,2,6]
    markers = [20,24,24,25]
    styles = [1,2,1,9]
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
    if color == 0:
        hist.SetMarkerStyle(markers[color])
    hist.SetLineColor(colors[color])
    hist.SetLineStyle(styles[color])
    hist.SetLineWidth(3)
    hist.SetMarkerColor(colors[color])
    hist.GetYaxis().SetRangeUser(the_extrema[0]*0.9,the_extrema[1]*1.1)

##

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
def getTH1GausFit(h1_in, pad):
#######################
    pad.cd()
    pad.SetLogy()

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
    return mu, sigma

#####################
def declare_struct():
#####################
# ROOT defined struct(s) present in the input tree
    ROOT.gROOT.ProcessLine("struct evt_t {\
    Int_t           run;\
    Int_t           evtnum;\
    };" )

    ROOT.gROOT.ProcessLine("struct pixel_recHit_t {\
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


############
def main():
############
    # input root file
    input_root_file = ROOT.TFile('./stdgrechitfullph1g_ntuple_20kEvents.root')
    input_tree = input_root_file.Get('PixelNtuple')    
        
    # import the ROOT defined struct(s) in pyROOT
    declare_struct()
    from ROOT import evt_t, pixel_recHit_t

    # define the pyROOT classes and assign the address
    evt = evt_t()
    input_tree.SetBranchAddress("evt",ROOT.AddressOf(evt,'run'))
    pixel_recHit = pixel_recHit_t()
    input_tree.SetBranchAddress("pixel_recHit",ROOT.AddressOf(pixel_recHit,'q'))
    
    # TH1
    n_eta_bins = 25
    eta_min = 0.
    eta_max = 2.5
    eta_span = (eta_max-eta_min)/n_eta_bins
    output_root_file = ROOT.TFile('h1_out.root','RECREATE')

    ### hit maps
    output_root_file.mkdir('hitmaps') 
    output_root_file.cd('hitmaps') 
    h1_eta = ROOT.TH1F('h1_eta','h1eta_rechit',n_eta_bins,eta_min,eta_max)
    h2_rzhitmapSubId1 = ROOT.TH2F('h2_rzhitmapSubId1','rzhitmap_subid1; recHit z [cm]; recHit r [cm]',200,-300.,300.,150,0.,150.)
    h2_rzhitmapSubId2 = ROOT.TH2F('h2_rzhitmapSubId2','rzhitmap_subid2; recHit z [cm]; recHit r [cm]',200,-300.,300.,150,0.,150.)    
    h2_rzhitmap = ROOT.TH2F('h2_rzhitmap','rzhitmap; recHit z [cm]; recHit r [cm]',100,-50.,50.,100,2.5,5.)
    
    ### ionization
    output_root_file.cd() 
    output_root_file.mkdir('dEdx') 
    output_root_file.cd('dEdx') 
    hp_qvseta = ROOT.TProfile('hp_qvseta','hp_qvseta;#eta;Q [ke]',n_eta_bins,eta_min,eta_max)
    hp_qvseta_xAxis = hp_qvseta.GetXaxis() 
    
    h1_qcorr  = ROOT.TH1F('h1_qcorr','h1_qcorr;Q_{corr} [ke];recHits',80,0.,400.)

    q_inEtaBinTH1 = []
    nyVSq_inEtaBinTH2 = []
    for i in range(n_eta_bins):
        eta_low = 0.+i*eta_span
        eta_high = eta_low+eta_span
        
        hname = 'h1_q_EtaBin%d' % i
        htitle = 'h1_q_Eta bin %d (%.2f < #eta < %.2f);Q [ke];recHits' % (i, eta_low, eta_high)
        q_inEtaBinTH1.append( ROOT.TH1F(hname,htitle,80,0.,400.))
        
        hname = 'h2_nyVSq_EtaBin%d' % i
        htitle = 'h2_nyVSq_Eta bin %d (%.2f < #eta < %.2f);Q [ke]; spreadY; recHits' % (i, eta_low, eta_high)
        nyVSq_inEtaBinTH2.append( ROOT.TH2F(hname,htitle,80,0.,400.,11,-0.5,10.5))

    ### rPhi residuals 
    output_root_file.cd() 
    output_root_file.mkdir('residualsX')         
    output_root_file.cd('residualsX')         
    hp_resRPhivseta_qlow = ROOT.TProfile('hp_resRPhivseta_qlow','hp_resRPhivseta_qlow;#eta;#Delta(R#phi) [cm]',n_eta_bins,eta_min,eta_max,'s')
    hp_resRPhivseta_qhigh = ROOT.TProfile('hp_resRPhivseta_qhigh','hp_resRPhivseta_qhigh;#eta;#Delta(R#phi) [cm]',n_eta_bins,eta_min,eta_max,'s')

    resX_qall_inEtaBinTH1 = []
    resX_qlow_inEtaBinTH1 = []
    resX_qhigh_inEtaBinTH1 = []
    for i in range(n_eta_bins):
        eta_low = 0.+i*eta_span
        eta_high = eta_low+eta_span
        
        hname = 'h1_resX_qall_EtaBin%d' % i
        htitle = 'h1_resX_qall_Eta bin %d (%.2f < #eta < %.2f);[#mum];recHits' % (i, eta_low, eta_high)
        resX_qall_inEtaBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))
        hname = 'h1_resX_qlow_EtaBin%d' % i
        htitle = 'h1_resX_qlow_Eta bin %d (%.2f < #eta < %.2f);[#mum];recHits' % (i, eta_low, eta_high)
        resX_qlow_inEtaBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))
        hname = 'h1_resX_qhigh_EtaBin%d' % i
        htitle = 'h1_resX_qhigh_Eta bin %d (%.2f < #eta < %.2f);[#mum];recHits' % (i, eta_low, eta_high)
        resX_qhigh_inEtaBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))
        
    # final histograms
    h_resRPhivseta_qall  = ROOT.TH1F('h_resRPhivseta_qall','Barrel #varphi-Hit Resolution;|#eta|;gaussian standard deviation #sigma [#mum]',n_eta_bins,eta_min,eta_max)
    h_resRPhivseta_qlow  = ROOT.TH1F('h_resRPhivseta_qlow','Barrel #varphi-Hit Resolution;|#eta|;gaussian standard deviation #sigma [#mum]',n_eta_bins,eta_min,eta_max)
    h_resRPhivseta_qhigh = ROOT.TH1F('h_resRPhivseta_qhigh','Barrel #varphi-Hit Resolution;|#eta|;gaussian standard deviation #sigma [#mum]',n_eta_bins,eta_min,eta_max)
    
    h_biasRPhivseta_qall  = ROOT.TH1F('h_biasRPhivseta_qall','Barrel #varphi-Hit Bias;|#eta|;gaussian fit #mu [#mum]',n_eta_bins,eta_min,eta_max)
    h_biasRPhivseta_qlow  = ROOT.TH1F('h_biasRPhivseta_qlow','Barrel #varphi-Hit Bias;|#eta|;gaussian fit #mu [#mum]',n_eta_bins,eta_min,eta_max)
    h_biasRPhivseta_qhigh = ROOT.TH1F('h_biasRPhivseta_qhigh','Barrel #varphi-Hit Bias;|#eta|;gaussian fit #mu [#mum]',n_eta_bins,eta_min,eta_max)

    ### z residuals 
    output_root_file.cd() 
    output_root_file.mkdir('residualsY')         
    output_root_file.cd('residualsY')         
    hp_resZvseta_qlow = ROOT.TProfile('hp_resZvseta_qlow','hp_resZvseta_qlow;#eta;#Delta(Z) [cm]',n_eta_bins,eta_min,eta_max,'s')
    hp_resZvseta_qhigh = ROOT.TProfile('hp_resZvseta_qhigh','hp_resZvseta_qhigh;#eta;#Delta(Z) [cm]',n_eta_bins,eta_min,eta_max,'s')
    
    resY_qall_inEtaBinTH1 = []
    resY_qlow_inEtaBinTH1 = []
    resY_qhigh_inEtaBinTH1 = []
    for i in range(n_eta_bins):
        eta_low = 0.+i*eta_span
        eta_high = eta_low+eta_span
        
        hname = 'h1_resY_qall_EtaBin%d' % i
        htitle = 'h1_resY_qall_Eta bin %d (%.2f < #eta < %.2f);[#mum];recHits' % (i, eta_low, eta_high)
        resY_qall_inEtaBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))
        hname = 'h1_resY_qlow_EtaBin%d' % i
        htitle = 'h1_resY_qlow_Eta bin %d (%.2f < #eta < %.2f);[#mum];recHits' % (i, eta_low, eta_high)
        resY_qlow_inEtaBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))
        hname = 'h1_resY_qhigh_EtaBin%d' % i
        htitle = 'h1_resY_qhigh_Eta bin %d (%.2f < #eta < %.2f);[#mum];recHits' % (i, eta_low, eta_high)
        resY_qhigh_inEtaBinTH1.append( ROOT.TH1F(hname,htitle,100,-100.,100.))

    # final histograms
    
    h_resZvseta_qall = ROOT.TH1F('h_resZvseta_qall','Barrel z-Hit Resolution;|#eta|;gaussian standard deviation #sigma [#mum]',n_eta_bins,eta_min,eta_max) 
    h_resZvseta_qlow = ROOT.TH1F('h_resZvseta_qlow','Barrel z-Hit Resolution;|#eta|;gaussian standard deviation #sigma [#mum]',n_eta_bins,eta_min,eta_max) 
    h_resZvseta_qhigh= ROOT.TH1F('h_resZvseta_qhigh','Barrel z-Hit Resolution;|#eta|;gaussian standard deviation #sigma [#mum]',n_eta_bins,eta_min,eta_max)

    h_biasZvseta_qall = ROOT.TH1F('h_biasZvseta_qall','Barrel z-Hit Bias;|#eta|;gaussian fit #mu [#mum]',n_eta_bins,eta_min,eta_max) 
    h_biasZvseta_qlow = ROOT.TH1F('h_biasZvseta_qlow','Barrel z-Hit Bias;|#eta|;gaussian fit #mu [#mum]',n_eta_bins,eta_min,eta_max) 
    h_biasZvseta_qhigh= ROOT.TH1F('h_biasZvseta_qhigh','Barrel z-Hit Bias;|#eta|;gaussian fit #mu [#mum]',n_eta_bins,eta_min,eta_max)

    ######## 1st loop on the tree
    all_entries = input_tree.GetEntries()
    for this_entry in xrange(all_entries):
        input_tree.GetEntry(this_entry)

        # global position of the rechit
        # NB sin(theta) = tv3.Perp()/tv3.Mag()
        tv3 = ROOT.TVector3(pixel_recHit.gx, pixel_recHit.gy, pixel_recHit.gz)
    
        # hitmap dor sanity check (phase1 subid=1/2 -> BPIX/FPIX, phase2 subdi=1/2 barrel/endcap)
        if (pixel_recHit.subid==1):
            h2_rzhitmapSubId1.Fill(tv3.z(),tv3.Perp())
        elif (pixel_recHit.subid==2): 
            h2_rzhitmapSubId2.Fill(tv3.z(),tv3.Perp())

        # BPIX only (layer 1)
        if  (pixel_recHit.subid==1 and pixel_recHit.layer==1 ):
            h1_eta.Fill(abs(tv3.Eta()))
            h2_rzhitmap.Fill(tv3.z(),tv3.Perp())
            hp_qvseta.Fill(abs(tv3.Eta()),pixel_recHit.q*0.001)

            # ionization corrected for incident angle (only central) 
            if(abs(tv3.Eta())<0.25):
                h1_qcorr.Fill(pixel_recHit.q*0.001*tv3.Perp()/tv3.Mag())

            if(abs(tv3.Eta())<eta_max):
                index = hp_qvseta_xAxis.FindBin(abs(tv3.Eta()))
                q_inEtaBinTH1[index-1].Fill(pixel_recHit.q*0.001)
                nyVSq_inEtaBinTH2[index-1].Fill(pixel_recHit.q*0.001, min(pixel_recHit.spready,10.))

    # check where is the 70%/30% boundary in the distribution of the ionization corrected for incident angle
    output_root_file.cd() 
    output_root_file.cd('dEdx') 
    h1_qcorr_norm = getTH1cdf(h1_qcorr)
    Qave = h1_qcorr.GetMean()

    ######## 2nd loop on the tree
    for this_entry in xrange(all_entries):
        input_tree.GetEntry(this_entry)
        # BPIX only (layer 1)
        if (pixel_recHit.subid==1 and pixel_recHit.layer==1):

            tv3 = ROOT.TVector3(pixel_recHit.gx, pixel_recHit.gy, pixel_recHit.gz)

            # NB: at given eta   Qave -> Qave(eta=0)/sin(theta)
            if  pixel_recHit.q*0.001 < Qave*tv3.Mag()/tv3.Perp():
                hp_resRPhivseta_qlow.Fill(abs(tv3.Eta()),pixel_recHit.hx-pixel_recHit.x)
                hp_resZvseta_qlow.Fill(abs(tv3.Eta()),pixel_recHit.hy-pixel_recHit.y)
                if(abs(tv3.Eta())<eta_max):
                    index = hp_qvseta_xAxis.FindBin(abs(tv3.Eta()))
                    resX_qlow_inEtaBinTH1[index-1].Fill(10000.*(pixel_recHit.hx-pixel_recHit.x))
                    resY_qlow_inEtaBinTH1[index-1].Fill(10000.*(pixel_recHit.hy-pixel_recHit.y))
                    resX_qall_inEtaBinTH1[index-1].Fill(10000.*(pixel_recHit.hx-pixel_recHit.x))
                    resY_qall_inEtaBinTH1[index-1].Fill(10000.*(pixel_recHit.hy-pixel_recHit.y))

            elif  pixel_recHit.q*0.001 < 1.5*Qave*tv3.Mag()/tv3.Perp():
                hp_resRPhivseta_qhigh.Fill(abs(tv3.Eta()),pixel_recHit.hx-pixel_recHit.x)
                hp_resZvseta_qhigh.Fill(abs(tv3.Eta()),pixel_recHit.hy-pixel_recHit.y)
                if(abs(tv3.Eta())<eta_max):
                    index = hp_qvseta_xAxis.FindBin(abs(tv3.Eta()))
                    resX_qhigh_inEtaBinTH1[index-1].Fill(10000.*(pixel_recHit.hx-pixel_recHit.x))
                    resY_qhigh_inEtaBinTH1[index-1].Fill(10000.*(pixel_recHit.hy-pixel_recHit.y))
                    resX_qall_inEtaBinTH1[index-1].Fill(10000.*(pixel_recHit.hx-pixel_recHit.x))
                    resY_qall_inEtaBinTH1[index-1].Fill(10000.*(pixel_recHit.hy-pixel_recHit.y))

    ### fill the final histograms
    # ceil(x): the smallest integer value greater than or equal to x (NB return a float)
    w = math.ceil(math.sqrt(h1_eta.GetNbinsX()))
    h = math.ceil(n_eta_bins/w)
    #    print int(w), int(h)

    c1_rPhi_qall = ROOT.TCanvas("c1_rPhi_qall","c1_rPhi_qall",900,900)
    c1_rPhi_qall.SetFillColor(ROOT.kWhite)
    c1_rPhi_qall.Divide(int(w),int(h))
    c1_rPhi_qlow = ROOT.TCanvas("c1_rPhi_qlow","c1_rPhi_qlow",900,900)
    c1_rPhi_qlow.SetFillColor(ROOT.kWhite)
    c1_rPhi_qlow.Divide(int(w),int(h))
    c1_rPhi_qhigh = ROOT.TCanvas("c1_rPhi_qhigh","c1_rPhi_qhigh",900,900)
    c1_rPhi_qhigh.SetFillColor(ROOT.kWhite)
    c1_rPhi_qhigh.Divide(int(w),int(h))

    c1_z_qall = ROOT.TCanvas("c1_z_qall","c1_z_qall",900,900)
    c1_z_qall.SetFillColor(ROOT.kWhite)
    c1_z_qall.Divide(int(w),int(h))
    c1_z_qlow = ROOT.TCanvas("c1_z_qlow","c1_z_qlow",900,900)
    c1_z_qlow.SetFillColor(ROOT.kWhite)
    c1_z_qlow.Divide(int(w),int(h))
    c1_z_qhigh = ROOT.TCanvas("c1_z_qhigh","c1_z_qhigh",900,900)
    c1_z_qhigh.SetFillColor(ROOT.kWhite)
    c1_z_qhigh.Divide(int(w),int(h))

    # initialize the counter (there is only one instance of the function getTH1GausFit)
    getTH1GausFit.icnt = 0 
    for i in xrange(h1_eta.GetNbinsX()):
        c1_rPhi_qall.cd(i+1)
        mu, sigma = getTH1GausFit(resX_qall_inEtaBinTH1[i], c1_rPhi_qall.GetPad(i+1))
        h_resRPhivseta_qall.SetBinContent(i+1,sigma)
        h_biasRPhivseta_qall.SetBinContent(i+1,mu)

        c1_rPhi_qlow.cd(i+1)        
        mu, sigma = getTH1GausFit(resX_qlow_inEtaBinTH1[i], c1_rPhi_qlow.GetPad(i+1))
        h_resRPhivseta_qlow.SetBinContent(i+1,sigma)
        h_biasRPhivseta_qlow.SetBinContent(i+1,mu)

        c1_rPhi_qhigh.cd(i+1)        
        mu, sigma = getTH1GausFit(resX_qhigh_inEtaBinTH1[i], c1_rPhi_qhigh.GetPad(i+1))
        h_resRPhivseta_qhigh.SetBinContent(i+1,sigma)
        h_biasRPhivseta_qhigh.SetBinContent(i+1,mu)

        c1_z_qall.cd(i+1)
        mu, sigma = getTH1GausFit(resY_qall_inEtaBinTH1[i], c1_z_qall.GetPad(i+1))
        h_resZvseta_qall.SetBinContent(i+1,sigma)
        h_biasZvseta_qall.SetBinContent(i+1,mu)

        c1_z_qlow.cd(i+1)        
        mu, sigma = getTH1GausFit(resY_qlow_inEtaBinTH1[i], c1_z_qlow.GetPad(i+1))
        h_resZvseta_qlow.SetBinContent(i+1,sigma)
        h_biasZvseta_qlow.SetBinContent(i+1,mu)

        c1_z_qhigh.cd(i+1)        
        mu, sigma = getTH1GausFit(resY_qhigh_inEtaBinTH1[i], c1_z_qhigh.GetPad(i+1))
        h_resZvseta_qhigh.SetBinContent(i+1,sigma)
        h_biasZvseta_qhigh.SetBinContent(i+1,mu)


    c1_rPhi_qall.SaveAs ("c1_rPhi_qall.pdf")
    c1_rPhi_qlow.SaveAs ("c1_rPhi_qlow.pdf")
    c1_rPhi_qhigh.SaveAs("c1_rPhi_qhigh.pdf")

    c1_z_qall.SaveAs("c1_z_qall.pdf")
    c1_z_qlow.SaveAs("c1_z_qlow.pdf")
    c1_z_qhigh.SaveAs("c1_z_qhigh.pdf")

# draw nice trend plots
    setStyle()
    cResVsEta = ROOT.TCanvas("cResVsEta","cResVsEta",1000,700)
    cResVsEta.Divide(2,1)

    lego = ROOT.TLegend(0.35,0.75,0.75,0.88)
    lego.SetFillColor(10)
    lego.SetTextSize(0.05)
    lego.SetTextFont(42)
    lego.SetFillColor(10)
    lego.SetLineColor(10)
    lego.SetShadowColor(10)
    
    cResVsEta.cd(1)
    rphi_arr = []
    rphi_arr.append(h_resRPhivseta_qall)
    rphi_arr.append(h_resRPhivseta_qlow)
    rphi_arr.append(h_resRPhivseta_qhigh)
  
    the_extrema = getExtrema(rphi_arr)

    MakeNiceTrendPlotStyle(h_resRPhivseta_qall,0,the_extrema)
    h_resRPhivseta_qall.Draw("C")
    h_resRPhivseta_qall.Draw("Psame")
    MakeNiceTrendPlotStyle(h_resRPhivseta_qhigh,1,the_extrema)
    h_resRPhivseta_qlow.Draw("Csame")
    MakeNiceTrendPlotStyle(h_resRPhivseta_qlow,2,the_extrema)
    h_resRPhivseta_qhigh.Draw("Csame")

    lego.AddEntry(h_resRPhivseta_qall,"Q/#LTQ#GT<1.5") 
    lego.AddEntry(h_resRPhivseta_qlow,"Q/#LTQ#GT<1.") 
    lego.AddEntry(h_resRPhivseta_qhigh,"1.<Q/#LTQ#GT<1.5")
    lego.Draw("same")
    
    cResVsEta.cd(2)
    z_arr = []
    z_arr.append(h_resZvseta_qall)
    z_arr.append(h_resZvseta_qlow)
    z_arr.append(h_resZvseta_qhigh)
    
    the_extrema = getExtrema(z_arr)
  
    MakeNiceTrendPlotStyle(h_resZvseta_qall,0,the_extrema)
    h_resZvseta_qall.Draw("C")
    h_resZvseta_qall.Draw("Psame")
    MakeNiceTrendPlotStyle(h_resZvseta_qhigh,1,the_extrema)
    h_resZvseta_qlow.Draw("Csame")
    MakeNiceTrendPlotStyle(h_resZvseta_qlow,2,the_extrema)
    h_resZvseta_qhigh.Draw("Csame")

    
    lego.Draw("same")
    cResVsEta.SaveAs("rmsVsEta.root")
    cResVsEta.SaveAs("rmsVsEta.pdf")
    
    #    
    output_root_file.Write()
    output_root_file.Close()

##################################
if __name__ == "__main__":        
    main()
