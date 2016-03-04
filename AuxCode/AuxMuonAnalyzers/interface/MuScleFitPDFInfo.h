#ifndef MuScleFitPDFInfo_h
#define MuScleFitPDFInfo_h

#include <TObject.h>

class MuScleFitPDFInfo : public TObject
{
 public:
 MuScleFitPDFInfo() : Q(0), id1(0), x1(0), pdf1(0), id2(0), x2(0), pdf2() {}     
 MuScleFitPDFInfo(const double& Q_, 
		   const int& id1_, const double& x1_, const double& pdf1_,
		  const int& id2_, const double& x2_, const double& pdf2_) :
  Q(Q_), id1(id1_), x1(x1_), pdf1(pdf1_), id2(id2_), x2(x2_), pdf2(pdf2_) {}         
  double Q;
  int id1;
  double x1;
  double pdf1;
  int id2;
  double x2;
  double pdf2;
  ClassDef(MuScleFitPDFInfo, 1)    
    };
ClassImp(MuScleFitPDFInfo)

#endif

