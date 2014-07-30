#!/usr/bin/env python

from xml.dom.minidom import parse
from optparse import OptionParser
import ROOT

################################################
def getModifiedTH1Fs(file, color, canvas):
################################################
    """ main function to acces to the TGraphErrors and return them with a modified style """

#
    h1array=[]
# read-in canavas
    tFile = ROOT.TFile(file,'read')
    cIn = tFile.Get(canvas)
# 
    for ca in cIn.GetListOfPrimitives():
# Get TGraph from MultiGraph        
        if ca.InheritsFrom('TH1F') and ca.GetLineStyle() != ROOT.kDotted: 
#        if ca.InheritsFrom('TH1F'):
            ca.SetMarkerColor(color)
            ca.SetLineColor(color)
            ca.SetLineWidth(3)
            ca.GetXaxis().SetLabelSize(0.07)
            ca.GetYaxis().SetLabelSize(0.07)
            ca.GetXaxis().SetTitleSize(0.07)
            ca.GetYaxis().SetTitleSize(0.07)
            h1array.append(ca)
    return h1array

#############
class Sample:
#############
    """ class to map the Sample elements in the xml file """

    def __init__(self, is_rphi, root_file, label, color, marker_style):
        self.is_rphi       = is_rphi
        self.the_root_file = root_file
        self.the_label     = label

        if color == 'ROOT.kRed':
            self.the_color = ROOT.kRed
        elif color == 'ROOT.kGreen':
            self.the_color = ROOT.kGreen
        elif color == 'ROOT.kBlue':
            self.the_color = ROOT.kBlue
        elif color == 'ROOT.kBlack':
            self.the_color = ROOT.kBlack
        elif color == 'ROOT.kMagenta':
            self.the_color = ROOT.kMagenta
        elif color == 'ROOT.kCyan':
            self.the_color = ROOT.kCyan

        if marker_style == 'ROOT.kDot':
            self.the_marker_style = ROOT.kDot
        elif marker_style == 'ROOT.kOpenTriangleUp':
            self.the_marker_style = ROOT.kOpenTriangleUp
        elif marker_style == 'ROOT.kOpenTriangleDown':
            self.the_marker_style = ROOT.kOpenTriangleDown

 

############
def main():
############
    """ navigation through XML based on https://docs.python.org/2/library/xml.dom.minidom.html """

    ROOT.gROOT.SetBatch(ROOT.kTRUE) 
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetMarkerSize(1.2)
    
    parser = OptionParser()
    parser.add_option("-f", "--file",  
                      action="store", type="string", dest="input_xml_file",
                      help="input XML file")
    (options, args) = parser.parse_args()

    dom = parse(options.input_xml_file)

    def handleSampleList(samples, sample_list):
        for sample in samples:
            sample_list.append(handleSample(sample))


    def handleSample(sample):
        is_rphi = sample.getAttribute('Coordinate') == 'rphi'
        s = Sample(is_rphi, \
               handleInputRootFile(sample.getElementsByTagName("InputRootFile")[0]), \
               handleLabel(sample.getElementsByTagName("Label")[0]), \
               handleColor(sample.getElementsByTagName("Color")[0]), \
               handleMarkerStyle(sample.getElementsByTagName("MarkerStyle")[0]) \
           )
        return s

    def handleInputRootFile(input_root_file):
        return input_root_file.firstChild.nodeValue

    def handleLabel(label):
        return label.firstChild.nodeValue

    def handleColor(color):
        return color.firstChild.nodeValue

    def handleMarkerStyle(marker_style):
        return marker_style.firstChild.nodeValue

    SampleList = []
    handleSampleList(dom.getElementsByTagName('Sample'), SampleList)

    legRMS = ROOT.TLegend(0.18,0.15,0.48,0.33)
    legRMS.SetFillColor(0)
    legRMS.SetTextFont(42)
    legRMS.SetTextSize(0.02)
    legRMS.SetBorderSize(0)

    cRMSVsEta = ROOT.TCanvas('cRMSVsEta','cRMSVsEta',800,800)
    cRMSVsEta.SetLeftMargin(0.15)
    cRMSVsEta.SetBottomMargin(0.15)
    cRMSVsEta.SetGridy()
    
    first = True
    for aSample in SampleList:
        if aSample.is_rphi:
            h1array = getModifiedTH1Fs(aSample.the_root_file, aSample.the_color, 'cResVsEta_1')
        else:
            h1array = getModifiedTH1Fs(aSample.the_root_file, aSample.the_color, 'cResVsEta_2')

        for h1 in h1array:            
            cRMSVsEta.cd()
            if first: 
                first = False 
                h1.Draw("CP")
                
                h1.GetXaxis().SetTitle('|#eta|')
                h1.GetXaxis().CenterTitle(ROOT.kFALSE)
                h1.GetXaxis().SetTitleOffset(1.)

                if aSample.is_rphi:
                    h1.GetYaxis().SetRangeUser(0.,20.)
                    h1.GetYaxis().SetNdivisions(504,ROOT.kFALSE)
                else:
                    legRMS.SetX1(0.28)
                    legRMS.SetX2(0.58)
                    legRMS.SetY1(0.66)
                    legRMS.SetY2(0.86)
                    h1.GetYaxis().SetRangeUser(10.,40.)
                    h1.GetYaxis().SetNdivisions(506,ROOT.kFALSE)

                h1.GetYaxis().SetTitleOffset(1.)
                h1.GetYaxis().SetTitle('RMS [#mum]')
                h1.GetYaxis().CenterTitle(ROOT.kFALSE)
                legRMS.AddEntry(0,'CMSSW 620 SLHC11','')                 
            else:
                h1.Draw("CPsame")

            # extraLabel should be set to describe the input dataset
            extraLabel = aSample.the_label
            if h1.GetLineStyle() == ROOT.kSolid:
                legRMS.AddEntry(h1,'Q/Q_{av}<1; '+extraLabel,'LP') 
            elif h1.GetLineStyle() == ROOT.kDashed:
                legRMS.AddEntry(h1,'1<Q/Q_{av}<1.5; '+extraLabel,'LP')
            elif h1.GetLineStyle() == ROOT.kDotted:
                legRMS.AddEntry(h1,'Q/Q_{av}<1.5; '+extraLabel,'LP')
                
    legRMS.Draw('same')

    if SampleList[0].is_rphi:
        cRMSVsEta.SaveAs('RMS_rphi.pdf')
    else:
        cRMSVsEta.SaveAs('RMS_rz.pdf')

 
#             tpv1 = ROOT.TPaveText(0.65,0.92,0.95,0.99,"NDC")
#             #tpv1.SetFillColor(ROOT.kGray)
#             tpv1.SetFillColor(10)
#             tpv1.SetTextFont(72)
#             tpv1.SetTextAlign(11)
#             tpv1.SetTextColor(ROOT.kBlue)
#             tpv1.AddText("Barrel Pixel r-#Phi")
#             tpv1.Draw("same")






##################################
if __name__ == "__main__":        
    main()
