#!/usr/bin/env python
import sys
import ROOT
import array
from optparse import OptionParser

#################
def argsort(seq):
################
    """ simplified version of the numpy.argsort() """
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key = seq.__getitem__)

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
    Float_t         hrow;\
    Float_t         hcol;\
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
    Int_t           nRowsInDet;\
    Int_t           nColsInDet;\
    Float_t         pitchx;\
    Float_t         pitchy;\
    Float_t         hx;\
    Float_t         hy;\
    Float_t         tx;\
    Float_t         ty;\
    Float_t         tz;\
    Float_t         theta;\
    Float_t         phi;\
    Int_t           DgN;\
    Int_t           DgRow[100];\
    Int_t           DgCol[100];\
    Int_t           DgDetId[100];\
    Float_t         DgAdc[100];\
    Float_t         DgCharge[100];\
    };" )

###############
def main():
###############

    parser = OptionParser()
    parser.add_option("-l", "--lego", 
                      action="store_true", dest="lego", default=False,
                      help="lego plots (default is no lego plots)")
    parser.add_option("-e", "--evts-to-dump",
                      action="store", type="int", dest="evts_to_dump", default=20,
                      help="max number of events to dump (for event display)")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="verbose output")

    (options, args) = parser.parse_args()

    max_evt_dumped = options.evts_to_dump
    max_evt_dumped+=1 # temporary fix.... should find a better way to dump "last" event

    # output ascii file
    output_ascii_file = file("test.txt", 'w')
    print >> output_ascii_file, "EventId ModuleId PixelRow PixelColumn pixelADC"

    # input root file
    try:
        input_root_file = ROOT.TFile.Open("stdgrechitfullph1g_ntuple_test.root")
    except:
        print "No input file specified"
        sys.exit()

    input_tree = input_root_file.Get("PixelNtuple")            
    if options.verbose: input_tree.Print()


    # sort the tree in case you want to display more than 1 cluster on the same module

    # variables evtnum and DgDetId stored in array fV1 (see TTree::Draw)
    # cf. http://root.cern.ch/root/roottalk/roottalk01/3646.html
    nentries = input_tree.GetEntries()
    input_tree.Draw("evt.evtnum*1000000000+DgDetId[0]","","goff")
    print "nentries", nentries
    # assign a "unique Id" to the cluster EEEMMMMMMMMM  
    # EEE = evt number  (assumption: only one run number)
    # MMMMMMMMM = detId number
    uniqueId = array.array('l')  
    for i in range(nentries):
        uniqueId.append(int(input_tree.GetV1()[i]))
    index_uniqueId = argsort(uniqueId)
    if options.verbose:
        for i in range(nentries):
            print i, index_uniqueId[i]


    # import the ROOT defined struct(s) in pyROOT
    declare_struct()
    from ROOT import evt_t, pixel_recHit_t

    # define the pyROOT classes and assign the address
    evt = evt_t()
    pixel_recHit = pixel_recHit_t()
    input_tree.SetBranchAddress("evt",ROOT.AddressOf(evt,"run"))        
    
    all_entries = input_tree.GetEntries()
    print "all_entries ", all_entries

    nR = 160  # rows or local_X
    nC = 8*52 # cols or local_Y
    h2_localXY_digi = []
    theRecHitPoints = []
    theSimHitPoints = []
    c_localXY_digi = []
    evt_dumped = 0
    recHitCount = 1
    uniqueId_old = -1

#    print len(h2_localXY_digi)

    for this_entry in xrange(all_entries):        

        if this_entry % 100 == 0:
            print "Processing rechit: ", this_entry

        input_tree.GetEntry(index_uniqueId[this_entry])

# To access the events in a tree no variables need to be assigned to the different branches. Instead the leaves are available as properties of the tree, returning the values of the present event. 
        pixel_recHit.pdgid      = input_tree.pdgid
        pixel_recHit.process    = input_tree.process
        pixel_recHit.q          = input_tree.q
        pixel_recHit.x          = input_tree.x
        pixel_recHit.y          = input_tree.y
        pixel_recHit.xx         = input_tree.xx
        pixel_recHit.xy         = input_tree.xy
        pixel_recHit.yy         = input_tree.yy
        pixel_recHit.row        = input_tree.row
        pixel_recHit.col        = input_tree.col
        pixel_recHit.hrow       = input_tree.hrow
        pixel_recHit.hcol       = input_tree.hcol
        pixel_recHit.gx         = input_tree.gx
        pixel_recHit.gy         = input_tree.gy
        pixel_recHit.gz         = input_tree.gz
        pixel_recHit.subid      = input_tree.subid
        pixel_recHit.module     = input_tree.module
        pixel_recHit.layer      = input_tree.layer
        pixel_recHit.ladder     = input_tree.ladder
        pixel_recHit.disk       = input_tree.disk
        pixel_recHit.blade      = input_tree.blade
        pixel_recHit.panel      = input_tree.panel
        pixel_recHit.side       = input_tree.side
        pixel_recHit.nsimhit    = input_tree.nsimhit
        pixel_recHit.spreadx    = input_tree.spreadx
        pixel_recHit.spready    = input_tree.spready
        pixel_recHit.pitchx     = input_tree.pitchx
        pixel_recHit.pitchy     = input_tree.pitchy
        pixel_recHit.nColsInDet = input_tree.nColsInDet
        pixel_recHit.nRowsInDet = input_tree.nRowsInDet
        pixel_recHit.hx         = input_tree.hx
        pixel_recHit.hy         = input_tree.hy
        pixel_recHit.tx         = input_tree.tx
        pixel_recHit.ty         = input_tree.ty
        pixel_recHit.tz         = input_tree.tz
        pixel_recHit.theta      = input_tree.theta
        pixel_recHit.phi        = input_tree.phi
        pixel_recHit.DgN        = input_tree.DgN

        pixel_recHit.DgRow = array.array('i',[0]*100)
        pixel_recHit.DgCol = array.array('i',[0]*100)
        pixel_recHit.DgDetId = array.array('i',[0]*100)
        pixel_recHit.DgAdc = array.array('f',[0]*100)
        pixel_recHit.DgCharge = array.array('f',[0]*100)

        for iDg in range(pixel_recHit.DgN):
            pixel_recHit.DgRow[iDg] = input_tree.DgRow[iDg]
            pixel_recHit.DgCol[iDg] = input_tree.DgCol[iDg]
            pixel_recHit.DgDetId[iDg] = input_tree.DgDetId[iDg]
            pixel_recHit.DgAdc[iDg] = input_tree.DgAdc[iDg]
            pixel_recHit.DgCharge[iDg] =input_tree.DgCharge[iDg]
       
        # BPIX layer 1 only 
        if pixel_recHit.subid==1 and pixel_recHit.layer==1:     

            if options.verbose: 
                print  "spread X, spread Y, DgN", pixel_recHit.spreadx, pixel_recHit.spready, pixel_recHit.DgN
                print  "nColsInDet: ",pixel_recHit.nColsInDet," nRowInDet: ",pixel_recHit.nRowsInDet," pitchx: ",pixel_recHit.pitchx," pitchy: ",pixel_recHit.pitchy         
            for iDg in range(pixel_recHit.DgN):
                if options.verbose: print iDg, pixel_recHit.DgDetId[iDg], pixel_recHit.DgRow[iDg], pixel_recHit.DgCol[iDg]
                print >> output_ascii_file, evt.evtnum,  pixel_recHit.DgDetId[iDg], pixel_recHit.DgRow[iDg], pixel_recHit.DgCol[iDg], int(pixel_recHit.DgCharge[iDg]*1000) # ADC (in ke) converted to int
            print >> output_ascii_file, "--> next rechit"

            # straw man event display
            if evt_dumped < max_evt_dumped:

                if evt.evtnum*1000000000+pixel_recHit.DgDetId[0] > uniqueId_old: 

                    if evt_dumped > 0:
                        c_localXY_digi[-1].cd()
                        h2_localXY_digi[-1].SetTitle("Evt: "+str(uniqueId_old/1000000000)+" Mod: "+str(uniqueId_old % 1000000000))

                        if options.lego:
                            h2_localXY_digi[-1].Draw("LEGOcolz")
                        else:
                            h2_localXY_digi[-1].Draw("colz")

                        theRecHitPoints[-1].SetMarkerStyle(20)    
                        theSimHitPoints[-1].SetMarkerStyle(3)

                        theRecHitPoints[-1].SetMarkerSize(1.)
                        theSimHitPoints[-1].SetMarkerSize(1.)
                        
                        theRecHitPoints[-1].SetMarkerColor(ROOT.kBlack)
                        theSimHitPoints[-1].SetMarkerColor(ROOT.kRed)
                        
                        #print "theRecHitPoints[-1].GetN() :", theRecHitPoints[-1].GetN(), "recHitCount :", recHitCount

                        theRecHitPoints[-1].Set(recHitCount)
                        theSimHitPoints[-1].Set(recHitCount)
                        theRecHitPoints[-1].RemovePoint(0)
                        theSimHitPoints[-1].RemovePoint(0)

                        #print "theRecHitPoints[-1].GetN() :", theRecHitPoints[-1].GetN()

                        theRecHitPoints[-1].Draw("Psame")
                        theSimHitPoints[-1].Draw("Psame")

                        h2_localXY_digi[-1].SetMaximum(40.)
                        c_localXY_digi[-1].SaveAs("c_localXY_digi_"+str(evt_dumped)+".png")
                        #c_localXY_digi[-1].SaveAs("c_localXY_digi_"+str(evt_dumped)+".root")

                        recHitCount=1

                    h2_localXY_digi.append(ROOT.TH2F("h2_localXY_digi"+str(evt_dumped),"h2_localXY_digi",nR,-0.5,-0.5+nR,nC,-0.5,-0.5+nC))
                    h2_localXY_digi[-1].SetStats(ROOT.kFALSE)  

                    theRecHitPoints.append(ROOT.TGraph(100))
                    theSimHitPoints.append(ROOT.TGraph(100))

                    if options.lego:
                        c_localXY_digi.append(ROOT.TCanvas("c_localXY_digi"+str(evt_dumped),"c_localXY_digi"))
                    else:
                        c_localXY_digi.append(ROOT.TCanvas("c_localXY_digi"+str(evt_dumped),"c_localXY_digi",nR*2,nC*2)) # size of the canvas with the same aspect ratio of the module

                    uniqueId_old = evt.evtnum*1000000000+pixel_recHit.DgDetId[0]
                    evt_dumped += 1

                for iDg in range(pixel_recHit.DgN):
                    h2_localXY_digi[-1].SetBinContent(pixel_recHit.DgRow[iDg], pixel_recHit.DgCol[iDg],pixel_recHit.DgCharge[iDg])
         
                theRecHitPoints[-1].SetPoint(recHitCount,pixel_recHit.row,pixel_recHit.col)
                theSimHitPoints[-1].SetPoint(recHitCount,pixel_recHit.hrow,pixel_recHit.hcol) 
                recHitCount +=1

# close ascii output
    output_ascii_file.close()

##################################
if __name__ == "__main__":        
    main()


