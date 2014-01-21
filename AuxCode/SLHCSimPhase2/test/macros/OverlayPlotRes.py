import ROOT

#h_resRPhivseta_qhigh,

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
        if ca.InheritsFrom('TH1F'):
            ca.SetMarkerColor(color)
            ca.SetLineColor(color)
            h1array.append(ca)

    return h1array


############
def main():
############
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetMarkerSize(1.2)

### overlay residuals in rphi
    # dictionary 
    dict_rphi = {'rmsVsEta_rphi_A':ROOT.kBlack,\
               'rmsVsEta_rphi_B':ROOT.kRed}
    
    legRMS_rphi = ROOT.TLegend(0.12,0.13,0.47,0.26)
    legRMS_rphi.SetFillColor(0)
    legRMS_rphi.SetTextFont(42)
    legRMS_rphi.SetTextSize(0.03)
    legRMS_rphi.SetBorderSize(0)

    cRMSVsEta_rphi = ROOT.TCanvas('cRMSVsEta_rphi','cRMSVsEta_rphi',500,500)
    cRMSVsEta_rphi.SetGridy()
    
    first = True
    for kName, vColor in dict_rphi.items():
#        print kName
        h1array = getModifiedTH1Fs(kName, vColor, 'cResVsEta_1')
        for h1 in h1array:            
            cRMSVsEta_rphi.cd()
            if first: 
                first = False 
                h1.Draw("C")
                h1.Draw("Psame")

                h1.GetXaxis().SetTitle('|#eta|')
                h1.GetXaxis().CenterTitle(ROOT.kFALSE)

                h1.GetYaxis().SetRangeUser(0,30)
                h1.GetYaxis().SetTitleOffset(0.7)
                h1.GetYaxis().SetTitle('[#mum]')
                h1.GetYaxis().CenterTitle(ROOT.kFALSE)
            else:
                h1.Draw("Csame")
                h1.Draw("Psame")
                
            # extraLabel should be set to describe the input dataset
            extraLabel = ' ' 
            if h1.GetLineColor() == ROOT.kBlack:
                extraLabel += 'Text A '         
            elif h1.GetLineColor() == ROOT.kRed:
                extraLabel += 'Text B '         

            if h1.GetLineStyle() == ROOT.kSolid:
                legRMS_rphi.AddEntry(h1,'Q/Q_{av}<1'+extraLabel,'L') 
            elif h1.GetLineStyle() == ROOT.kDashed:
                legRMS_rphi.AddEntry(h1,'1<Q/Q_{av}<1.5'+extraLabel,'L')


    legRMS_rphi.Draw('same');
    cRMSVsEta_rphi.SaveAs('foo_rphi.png')

### overlay residuals in rz
    # dictionary 
    dict_rz = {'rmsVsEta_rz_A':ROOT.kBlack,\
               'rmsVsEta_rz_B':ROOT.kRed}
    
    legRMS_rz = ROOT.TLegend(0.12,0.13,0.47,0.26)
    legRMS_rz.SetFillColor(0)
    legRMS_rz.SetTextFont(42)
    legRMS_rz.SetTextSize(0.03)
    legRMS_rz.SetBorderSize(0)

    cRMSVsEta_rz = ROOT.TCanvas('cRMSVsEta_rz','cRMSVsEta_rz',500,500)
    cRMSVsEta_rz.SetGridy()
    
    first = True
    for kName, vColor in dict_rz.items():
#        print kName
        h1array = getModifiedTH1Fs(kName, vColor, 'cResVsEta_2')
        for h1 in h1array:            
            cRMSVsEta_rz.cd()
            if first: 
                first = False 
                h1.Draw("C")
                h1.Draw("Psame")

                h1.GetXaxis().SetTitle('|#eta|')
                h1.GetXaxis().CenterTitle(ROOT.kFALSE)

                h1.GetYaxis().SetRangeUser(0,30)
                h1.GetYaxis().SetTitleOffset(0.7)
                h1.GetYaxis().SetTitle('[#mum]')
                h1.GetYaxis().CenterTitle(ROOT.kFALSE)
            else:
                h1.Draw("Csame")
                h1.Draw("Psame")
                
            # extraLabel should be set to describe the input dataset
            extraLabel = ' ' 
            if h1.GetLineColor() == ROOT.kBlack:
                extraLabel += 'Text A '         
            elif h1.GetLineColor() == ROOT.kRed:
                extraLabel += 'Text B '         

            if h1.GetLineStyle() == ROOT.kSolid:
                legRMS_rz.AddEntry(h1,'Q/Q_{av}<1'+extraLabel,'L') 
            elif h1.GetLineStyle() == ROOT.kDashed:
                legRMS_rz.AddEntry(h1,'1<Q/Q_{av}<1.5'+extraLabel,'L')


    legRMS_rz.Draw('same');
    cRMSVsEta_rz.SaveAs('foo_rz.png')


##################################
if __name__ == "__main__":        
    main()
