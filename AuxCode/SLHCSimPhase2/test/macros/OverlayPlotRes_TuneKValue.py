#!/usr/bin/env python
import ROOT
import math
from optparse import OptionParser

##########################
def drawTicks(h1_in, line):
##########################
    # Draw "ticks" in eta correponding to the borders of the pixels
    yL = 8100.
    zL =  285. # 220.
    ROC_cols = 52 #81 
    for iL in xrange(ROC_cols):
        eta = math.asinh((iL*yL/ROC_cols)/zL)
        if eta<h1_in.GetXaxis().GetXmax():
            line.append(ROOT.TLine(eta, 10., eta, 15.))
            line[iL].Draw("same")

################################################
def getModifiedTH1Fs(file, color, canvas):
################################################
    """ main function to acces to the TGraphErrors and return them with a modified style """

#
    h1array=[]
# read-in canavas
    tFile = ROOT.TFile(file+'.root','read')
    cIn = tFile.Get(canvas)
# 
    for ca in cIn.GetListOfPrimitives():
# Get TGraph from MultiGraph        
        if ca.InheritsFrom('TH1F') and ca.GetLineStyle() != ROOT.kDotted: 
#         if ca.InheritsFrom('TH1F'):
            ca.SetMarkerStyle(color[1])                
            ca.SetMarkerColor(color[0])
            ca.SetLineColor(color[0])
            ca.SetLineWidth(3)
            ca.GetXaxis().SetLabelSize(0.05)
            ca.GetYaxis().SetLabelSize(0.05)
            ca.GetXaxis().SetTitleSize(0.07)
            ca.GetYaxis().SetTitleSize(0.07)
            h1array.append(ca)

    return h1array


### python implementation of "enum" type for the different options
# http://stackoverflow.com/questions/3248851/pythons-enum-equivalent
class Scenario: pass
class Default  (Scenario): pass
class Tune300  (Scenario): pass
class Tune500  (Scenario): pass
class KScan    (Scenario): pass
###

############
def main():
############
    ROOT.gROOT.SetBatch(ROOT.kTRUE) 
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetMarkerSize(1.2)


    parser = OptionParser()
    parser.add_option("-w", "--what",  
                      action="store", type="int", dest="what", default=1,
                      help="1 (CMSSW_620_SLHC11), 2 (300/fb new tune), 3 (500/fb new tune), 4 (k-scan)")

    (options, args) = parser.parse_args()
    if options.what == 1:
        scenario = Default
    elif options.what == 2:
        scenario = Tune300
    elif options.what == 3:
        scenario = Tune500
    elif options.what == 4:
        scenario = KScan

### overlay residuals in rphi
    # dictionary 
    dict_rphi = {}

    if scenario is Default:  # 620_SLHC11 default
        dict_rphi.update(
            {'RadDamage/phase1_ageingMark0_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rphi':[ROOT.kBlack,ROOT.kDot]\
            ,'RadDamage/phase1_300fb_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rphi':[ROOT.kMagenta,ROOT.kDot]\
            ,'RadDamage/phase1_500fb_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rphi':[ROOT.kRed,ROOT.kDot]}
        )
    elif scenario is Tune300: # 300/fb new tune (by layer)
        dict_rphi.update(
            {'RadDamage/phase1_300fbAllLayers_NoNoise_NoIneff_NoEdges/Layer1/All/rmsVsEta_rphi':[ROOT.kMagenta,ROOT.kDot]\
            ,'RadDamage/phase1_300fbAllLayers_NoNoise_NoIneff_NoEdges/Layer2/All/rmsVsEta_rphi':[ROOT.kBlue,ROOT.kDot]\
            ,'RadDamage/phase1_300fbAllLayers_NoNoise_NoIneff_NoEdges/Layer3/All/rmsVsEta_rphi':[ROOT.kBlack,ROOT.kDot]\
            ,'RadDamage/phase1_300fbAllLayers_NoNoise_NoIneff_NoEdges/Layer4/All/rmsVsEta_rphi':[ROOT.kBlack,ROOT.kDot]}
        )
    elif scenario is Tune500: # 500/fb new tune (by layer)
        dict_rphi.update(
            {'Raddamage/phase1_500fbAllLayers_NoNoise_NoIneff_NoEdges/Layer1/All/rmsVsEta_rphi':[ROOT.kRed,ROOT.kDot]\
            ,'RadDamage/phase1_500fbAllLayers_NoNoise_NoIneff_NoEdges/Layer2/All/rmsVsEta_rphi':[ROOT.kGreen,ROOT.kDot]\
            ,'RadDamage/phase1_500fbAllLayers_NoNoise_NoIneff_NoEdges/Layer3/All/rmsVsEta_rphi':[ROOT.kBlue,ROOT.kDot]\
            ,'RadDamage/phase1_500fbAllLayers_NoNoise_NoIneff_NoEdges/Layer4/All/rmsVsEta_rphi':[ROOT.kBlack,ROOT.kDot]}
        )
    elif scenario is KScan:# k-scan
        dict_rphi.update(
            {'RadDamage/phase1_ageingMark70_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rphi':[ROOT.kRed,ROOT.kDot]\
            ,'RadDamage/phase1_ageingMark40_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rphi':[ROOT.kMagenta,ROOT.kDot]\
            ,'RadDamage/phase1_ageingMark35_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rphi':[ROOT.kGreen,ROOT.kDot]\
            ,'RadDamage/phase1_ageingMark30_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rphi':[ROOT.kBlue,ROOT.kDot]\
            ,'RadDamage/phase1_ageingMark0_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rphi':[ROOT.kBlack,ROOT.kDot]}
        )
    
    legRMS_rphi = ROOT.TLegend(0.18,0.15,0.48,0.33)
    legRMS_rphi.SetFillColor(0)
    legRMS_rphi.SetTextFont(42)
    legRMS_rphi.SetTextSize(0.02)
    legRMS_rphi.SetBorderSize(0)

    cRMSVsEta_rphi = ROOT.TCanvas('cRMSVsEta_rphi','cRMSVsEta_rphi',800,800)
    cRMSVsEta_rphi.SetLeftMargin(0.15)
    cRMSVsEta_rphi.SetBottomMargin(0.15)
    cRMSVsEta_rphi.SetGridy()
    
    first = True
    for kName, vColor in dict_rphi.items():
        print kName
        h1array = getModifiedTH1Fs(kName, vColor, 'cResVsEta_1')
        for h1 in h1array:            
            cRMSVsEta_rphi.cd()
            if first: 
                first = False 
                h1.Draw("CP")

                h1.GetXaxis().SetTitle('|#eta|')
                h1.GetXaxis().CenterTitle(ROOT.kFALSE)
                h1.GetXaxis().SetTitleOffset(1.)
                h1.GetYaxis().SetRangeUser(0.,20.)
                h1.GetYaxis().SetNdivisions(504,ROOT.kFALSE)
                h1.GetYaxis().SetTitleOffset(1.)
                h1.GetYaxis().SetTitle('RMS [#mum]')
                h1.GetYaxis().CenterTitle(ROOT.kFALSE)
                
                if scenario is Default:  # 620_SLHC11 default
                    legRMS_rphi.AddEntry(0,'CMSSW 620 SLHC11','')                 
                elif scenario is Tune300: # 300/fb new tune (by layer)
                    legRMS_rphi.AddEntry(0,'New 150/fb (aka CMS 300/fb)','')                 
                elif scenario is Tune500: # 500/fb new tune (by layer)
                    legRMS_rphi.AddEntry(0,'New 300/fb (aka CMS 500/fb)','')                 

            else:
                h1.Draw("CPsame")
                
            # extraLabel should be set to describe the input dataset
            extraLabel = ' ' 

            if scenario is Default:  # 620_SLHC11 default
                if h1.GetLineColor() == ROOT.kRed:
                    extraLabel += ' k = 1.5 (aka CMS 500/fb)'
                elif h1.GetLineColor() == ROOT.kMagenta:
                    extraLabel += ' k = 1.0 (aka CMS 300/fb)'

            elif scenario is Tune300: # 300/fb new tune (by layer)
                if h1.GetLineColor() == ROOT.kMagenta:
                    extraLabel += ' BPIX L1'
                elif h1.GetLineColor() == ROOT.kBlue:
                    extraLabel += ' BPIX L2'
                elif h1.GetLineColor() == ROOT.kBlack:
                    extraLabel += ' BPIX L3/L4'

            elif scenario is Tune500: # 500/fb new tune (by layer)
                if h1.GetLineColor() == ROOT.kRed:
                    extraLabel += ' BPIX L1'
                elif h1.GetLineColor() == ROOT.kGreen:
                    extraLabel += ' BPIX L2'
                elif h1.GetLineColor() == ROOT.kBlue:
                    extraLabel += ' BPIX L3'
                elif h1.GetLineColor() == ROOT.kBlack:
                    extraLabel += ' BPIX L4'

            elif scenario is KScan: # k-scan
                if h1.GetLineColor() == ROOT.kRed:
                    extraLabel += 'k = 0.70'
                elif h1.GetLineColor() == ROOT.kMagenta:
                    extraLabel += 'k = 0.40'
                elif h1.GetLineColor() == ROOT.kBlue:
                    extraLabel += 'k = 0.30'
                elif h1.GetLineColor() == ROOT.kGreen:
                    extraLabel += 'k = 0.35'
                elif h1.GetLineColor() == ROOT.kBlack:
                    extraLabel += 'k = 0.00'

            if h1.GetLineStyle() == ROOT.kSolid:
                legRMS_rphi.AddEntry(h1,'Q/Q_{av}<1'+extraLabel,'LP') 
            elif h1.GetLineStyle() == ROOT.kDashed:
                legRMS_rphi.AddEntry(h1,'1<Q/Q_{av}<1.5'+extraLabel,'LP')
            elif h1.GetLineStyle() == ROOT.kDotted:
                legRMS_rphi.AddEntry(h1,'Q/Q_{av}<1.5'+extraLabel,'LP')

            bv1 = ROOT.TBox(1.5,0.,2.5,30.)
            bv1.SetFillColor(1)
            bv1.SetFillColor(ROOT.kGray)
            # bv1.SetFillStyle(3144)
            # bv1.Draw()       
 
            tpv1 = ROOT.TPaveText(0.65,0.92,0.95,0.99,"NDC")
            #tpv1.SetFillColor(ROOT.kGray)
            tpv1.SetFillColor(10)
            tpv1.SetTextFont(72)
            tpv1.SetTextAlign(11)
            tpv1.SetTextColor(ROOT.kBlue)
            tpv1.AddText("Barrel Pixel r-#Phi")
            tpv1.Draw("same")

#    legRMS_rphi.Draw('same');
    cRMSVsEta_rphi.SaveAs('foo_rphi_ageing.pdf')
    cRMSVsEta_rphi.SaveAs('foo_rphi_ageing.root')

# draw rphi resolution with y-axis range (0,100) um 
    cRMSVsEta_rphi_extY = cRMSVsEta_rphi.DrawClone()    
    for ca in cRMSVsEta_rphi_extY.GetListOfPrimitives():
         if ca.InheritsFrom('TH1F'):
             ca.GetYaxis().SetRangeUser(0.,100.)
             ca.GetYaxis().SetNdivisions(510,ROOT.kTRUE)
                
    cRMSVsEta_rphi_extY.Update()
#    cRMSVsEta_rphi_extY.SaveAs('foo_rphi_extY_ageing.png')
    cRMSVsEta_rphi_extY.SaveAs('foo_rphi_extY_ageing.pdf')

### overlay residuals in rz
    # dictionary 
    dict_rz = {}

    if scenario is Default:  # 620_SLHC11 default
        dict_rz.update(
            {'RadDamage/phase1_ageingMark0_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rz':[ROOT.kBlack,ROOT.kDot]\
            ,'RadDamage/phase1_300fb_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rz':[ROOT.kMagenta,ROOT.kDot]\
            ,'RadDamage/phase1_500fb_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rz':[ROOT.kRed,ROOT.kDot]}
        )
    elif scenario is Tune300: # 300/fb new tune (by layer)
        dict_rz.update(
            {'RadDamage/phase1_300fbAllLayers_NoNoise_NoIneff_NoEdges/Layer1/All/rmsVsEta_rz':[ROOT.kMagenta,ROOT.kDot]\
            ,'RadDamage/phase1_300fbAllLayers_NoNoise_NoIneff_NoEdges/Layer2/All/rmsVsEta_rz':[ROOT.kBlue,ROOT.kDot]\
            ,'RadDamage/phase1_300fbAllLayers_NoNoise_NoIneff_NoEdges/Layer3/All/rmsVsEta_rz':[ROOT.kBlack,ROOT.kDot]\
            ,'RadDamage/phase1_300fbAllLayers_NoNoise_NoIneff_NoEdges/Layer4/All/rmsVsEta_rz':[ROOT.kBlack,ROOT.kDot]}
        )
    elif scenario is Tune500: # 500/fb new tune (by layer)
        dict_rz.update(
            {'Raddamage/phase1_500fbAllLayers_NoNoise_NoIneff_NoEdges/Layer1/All/rmsVsEta_rz':[ROOT.kRed,ROOT.kDot]\
            ,'RadDamage/phase1_500fbAllLayers_NoNoise_NoIneff_NoEdges/Layer2/All/rmsVsEta_rz':[ROOT.kGreen,ROOT.kDot]\
            ,'RadDamage/phase1_500fbAllLayers_NoNoise_NoIneff_NoEdges/Layer3/All/rmsVsEta_rz':[ROOT.kBlue,ROOT.kDot]\
            ,'RadDamage/phase1_500fbAllLayers_NoNoise_NoIneff_NoEdges/Layer4/All/rmsVsEta_rz':[ROOT.kBlack,ROOT.kDot]}
        )
    elif scenario is KScan:# k-scan
        dict_rz.update(
            {'RadDamage/phase1_ageingMark70_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rz':[ROOT.kRed,ROOT.kDot]\
            ,'RadDamage/phase1_ageingMark40_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rz':[ROOT.kMagenta,ROOT.kDot]\
            ,'RadDamage/phase1_ageingMark35_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rz':[ROOT.kGreen,ROOT.kDot]\
            ,'RadDamage/phase1_ageingMark30_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rz':[ROOT.kBlue,ROOT.kDot]\
            ,'RadDamage/phase1_ageingMark0_NoNoise_NoIneff_NoEdges/All/rmsVsEta_rz':[ROOT.kBlack,ROOT.kDot]}
        )
    
    legRMS_rz = ROOT.TLegend(0.28,0.66,0.58,0.86)
#    legRMS_rz = ROOT.TLegend(0.48,0.48,0.78,0.68)
    legRMS_rz.SetFillColor(0)
    legRMS_rz.SetTextFont(42)
    legRMS_rz.SetTextSize(0.02)
    legRMS_rz.SetBorderSize(0)

    cRMSVsEta_rz = ROOT.TCanvas('cRMSVsEta_rz','cRMSVsEta_rz',800,800)
    cRMSVsEta_rz.SetLeftMargin(0.15)
    cRMSVsEta_rz.SetBottomMargin(0.15)
    cRMSVsEta_rz.SetGridy()
    
    first = True
    line1  = []
    for kName, vColor in dict_rz.items():
#        print kName
        h1array = getModifiedTH1Fs(kName, vColor, 'cResVsEta_2')
        for h1 in h1array:            
            cRMSVsEta_rz.cd()
            if first: 
                first = False 
                h1.Draw("CP")

                h1.GetXaxis().SetTitle('|#eta|')
                h1.GetXaxis().CenterTitle(ROOT.kFALSE)
                h1.GetXaxis().SetTitleOffset(1.)
                h1.GetYaxis().SetRangeUser(10.,40.)
                h1.GetYaxis().SetNdivisions(506,ROOT.kFALSE)
                h1.GetYaxis().SetTitleOffset(1.)
                h1.GetYaxis().SetTitle('RMS [#mum]')
                h1.GetYaxis().CenterTitle(ROOT.kFALSE)
                
                drawTicks(h1, line1)
                if scenario is Default:  # 620_SLHC11 default
                    legRMS_rz.AddEntry(0,'CMSSW 620 SLHC11','')                 
                elif scenario is Tune300: # 300/fb new tune (by layer)
                    legRMS_rz.AddEntry(0,'New 150/fb (aka CMS 300/fb)','')                 
                elif scenario is Tune500: # 500/fb new tune (by layer)
                    legRMS_rz.AddEntry(0,'New 300/fb (aka CMS 500/fb)','')                 

            else:
                h1.Draw("CPsame")
                
            # extraLabel should be set to describe the input dataset
            extraLabel = ' ' 

            if scenario is Default:  # 620_SLHC11 default
                if h1.GetLineColor() == ROOT.kRed:
                    extraLabel += ' k = 1.5 (aka CMS 500/fb)'
                elif h1.GetLineColor() == ROOT.kMagenta:
                    extraLabel += ' k = 1.0 (aka CMS 300/fb)'

            elif scenario is Tune300: # 300/fb new tune (by layer)
                if h1.GetLineColor() == ROOT.kMagenta:
                    extraLabel += ' BPIX L1'
                elif h1.GetLineColor() == ROOT.kBlue:
                    extraLabel += ' BPIX L2'
                elif h1.GetLineColor() == ROOT.kBlack:
                    extraLabel += ' BPIX L3/L4'

            elif scenario is Tune500: # 500/fb new tune (by layer)
                if h1.GetLineColor() == ROOT.kRed:
                    extraLabel += ' BPIX L1'
                elif h1.GetLineColor() == ROOT.kGreen:
                    extraLabel += ' BPIX L2'
                elif h1.GetLineColor() == ROOT.kBlue:
                    extraLabel += ' BPIX L3'
                elif h1.GetLineColor() == ROOT.kBlack:
                    extraLabel += ' BPIX L4'

            elif scenario is KScan: # k-scan
                if h1.GetLineColor() == ROOT.kRed:
                    extraLabel += 'k = 0.70'
                elif h1.GetLineColor() == ROOT.kMagenta:
                    extraLabel += 'k = 0.40'
                elif h1.GetLineColor() == ROOT.kBlue:
                    extraLabel += 'k = 0.30'
                elif h1.GetLineColor() == ROOT.kGreen:
                    extraLabel += 'k = 0.35'
                elif h1.GetLineColor() == ROOT.kBlack:
                    extraLabel += 'k = 0.00'

            if h1.GetLineStyle() == ROOT.kSolid:
                legRMS_rz.AddEntry(h1,'Q/Q_{av}<1'+extraLabel,'LP') 
            elif h1.GetLineStyle() == ROOT.kDashed:
                legRMS_rz.AddEntry(h1,'1<Q/Q_{av}<1.5'+extraLabel,'LP')
            elif h1.GetLineStyle() == ROOT.kDotted:
                legRMS_rz.AddEntry(h1,'Q/Q_{av}<1.5'+extraLabel,'LP')


            # xl = 0.2 # "left" line
            # xm = 0.4 # "middle" line
            # xr = 0.6 # "right" line
            # x1 = h1.GetXaxis().GetXmin()
            # #y1 = h1.GetYaxis().GetXmin()
            # y1 = cRMSVsEta_rz.GetUymin()
            # x2 = h1.GetXaxis().GetXmax()
            # #y2 = h1.GetYaxis().GetXmax()
            # y2 = cRMSVsEta_rz.GetUymax()

            bv = ROOT.TBox(1.5,10.,2.5,40.)
            bv.SetFillColor(ROOT.kGray)
            # bv.SetFillStyle(3005)
            # bv.Draw()    

            tpv1 = ROOT.TPaveText(0.65,0.92,0.95,0.99,"NDC")
            #tpv1.SetFillColor(ROOT.kGray)
            tpv1.SetFillColor(10)
            tpv1.SetTextFont(72)
            tpv1.SetTextAlign(11)
            tpv1.SetTextColor(ROOT.kBlue)
            tpv1.AddText("Barrel Pixel r-z")
            tpv1.Draw("same")

    legRMS_rz.Draw('same')        
    cRMSVsEta_rz.SaveAs('foo_rz_ageing.pdf')
#    cRMSVsEta_rz.SaveAs('foo_rz_ageing.png')


# draw rz resolution with y-axis range (0,100) um 
    cRMSVsEta_rz_extY = cRMSVsEta_rz.DrawClone()    
    for ca in cRMSVsEta_rz_extY.GetListOfPrimitives():
         if ca.InheritsFrom('TH1F'):
# phase2             ca.GetYaxis().SetRangeUser(0.,40.)
             ca.GetYaxis().SetRangeUser(0.,100.)
             ca.GetYaxis().SetNdivisions(510,ROOT.kTRUE)
                
    cRMSVsEta_rz_extY.Update()
#    cRMSVsEta_rz_extY.SaveAs('foo_rz_extY_ageing.png')
    cRMSVsEta_rz_extY.SaveAs('foo_rz_extY_ageing.pdf')


##################################
if __name__ == "__main__":        
    main()
