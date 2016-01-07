#include "TLorentzVector.h"
#include "TFile.h"

#include "TObjArray.h"

#include <vector>

using namespace std;

class DkScanAnalysis {
public:
  DkScanAnalysis(TFile *, const char * append="");
  ~DkScanAnalysis();
  void analyze(const TLorentzVector & muNeg, const TLorentzVector & muPos, double weight=1.);
  void endjob(); 
    
private:
  TDirectory * the_dir;

  TObjArray HList_pos, HList_neg, Canvas;
  vector <float> delta_k;

  vector <float> dk_68;
  vector <float> dk_95;

  int n_Dk;
  double *dk, *chi2, *ks;

  char dirname[200];
};
