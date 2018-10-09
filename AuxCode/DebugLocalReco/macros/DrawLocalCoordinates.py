# pyROOT script to draw local coordinates frame(s)
# Input file: ascii file from "cout's" in DebugLocalCoordinates plugin

import ROOT
import array 
from optparse import OptionParser


def rotationY180(v3in):
    # 180deg rotation of input 3-vector around y-axis
    res = array.array('d',[0.,0.,0.])
    ROT180Y = [[-1., 0., 0.], [0., +1., 0], [0., 0., -1.]]
    for i in range(3):        
        for j in range(3):
            res[i] += ROT180Y[i][j] * v3in[j]
    return res


class LocalCoordinates:
    def __init__(self, ladder, gp0, gpX, gpY, gpZ, rotateY180):
        self.ladder = ladder
        self.gp0 = array.array('d',gp0)
        self.gpX = array.array('d',gpX)
        self.gpY = array.array('d',gpY)
        self.gpZ = array.array('d',gpZ)
        # in case a rotation of 180 deg around y-axis is required
        if rotateY180:
            self.gp0 = rotationY180(self.gp0)
            self.gpX = rotationY180(self.gpX)
            self.gpY = rotationY180(self.gpY)
            self.gpZ = rotationY180(self.gpZ)

        # local X 
        self.arrowX = ROOT.TArrow(self.gp0[0], self.gp0[1], self.gpX[0], self.gpX[1],0.02)
        self.arrowX.SetLineColor(ROOT.kRed)
        # local Z
        self.arrowZ = ROOT.TArrow(self.gp0[0], self.gp0[1], self.gpZ[0], self.gpZ[1],0.02)
        self.arrowZ.SetLineColor(ROOT.kBlue)
        
    def getArrowX(self):
        return self.arrowX
        
    def getArrowZ(self):
        return self.arrowZ

 
def main():

    desc   = """ This is a description of %prog."""
    parser = OptionParser(description=desc,version='%prog version 0.1') 
    parser.add_option('--rotateY180',  help='perform a rotation of 180 deg around y-axis (to match cmsShow images)', dest='rotateY180',  action='store_true')
    (opts, args) = parser.parse_args()

    local_coordinates_list = []
    with open('LocalCoordinates.2023D17.txt', 'r') as input_file: # 'r' = read
        # Example of the format
        # layer=1 ladder=1 module=5 rawId=303042580 (2.94592,0.789964,-1.02228e-16)   (3.20493,-0.175912,-1.38125e-16)   (2.94592,0.789964,-1)   (3.9118,1.04897,-7.30634e-18) 
        for line in input_file:
            ladder, gp0_str, gpX_str, gpY_str, gpZ_str = line.split()[1],\
                                                         line.split()[4],\
                                                         line.split()[5],\
                                                         line.split()[6],\
                                                         line.split()[7]
            # convert the string "(2.94592,0.789964,-1.02228e-16)" in a tuples of 3 floats
            gp0 = array.array('d',[float(gp0_str[1:-1].split(',')[0]), float(gp0_str[1:-1].split(',')[1]), float(gp0_str[1:-1].split(',')[2])])
            gpX = array.array('d',[float(gpX_str[1:-1].split(',')[0]), float(gpX_str[1:-1].split(',')[1]), float(gpX_str[1:-1].split(',')[2])])
            gpY = array.array('d',[float(gpY_str[1:-1].split(',')[0]), float(gpY_str[1:-1].split(',')[1]), float(gpY_str[1:-1].split(',')[2])])
            gpZ = array.array('d',[float(gpZ_str[1:-1].split(',')[0]), float(gpZ_str[1:-1].split(',')[1]), float(gpZ_str[1:-1].split(',')[2])])
        
            local_coordinates_list.append(LocalCoordinates(ladder, gp0, gpX, gpY, gpZ, opts.rotateY180))

    c1 = ROOT.TCanvas('c1',',c1',600,600)
    c1.Range(-5,-5,+5,+5)
    # global X
    xdir = array.array('d',[1.,0.,0.])
    if opts.rotateY180:
        xdir = rotationY180(xdir)
    globalX = ROOT.TArrow(0.,0.,xdir[0],xdir[1],0.02)
    globalX.SetLineColor(ROOT.kRed)
    globalX.SetLineWidth(5)
    globalX.Draw()
    # global Y
    ydir = array.array('d',[0.,1.,0.])
    if opts.rotateY180:
        ydir = rotationY180(ydir)
    globalY = ROOT.TArrow(0.,0.,ydir[0],ydir[1],0.02)
    globalY.SetLineColor(ROOT.kGreen)
    globalY.SetLineWidth(5)
    globalY.Draw()
    
    for lc in local_coordinates_list:
        lc.getArrowX().Draw()
        lc.getArrowZ().Draw()
    c1.SaveAs('/tmp/c1.pdf')
        
if __name__ == '__main__':  
   main()
    



