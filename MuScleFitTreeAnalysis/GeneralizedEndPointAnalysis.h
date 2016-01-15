#include "TLorentzVector.h"
#include "TFile.h"

#include "TObjArray.h"

#include <vector>

using namespace std;

class GeneralizedEndPointAnalysis {
public:
  GeneralizedEndPointAnalysis(TFile *, const char * append="");
  ~GeneralizedEndPointAnalysis();
  void analyze(const TLorentzVector & muNeg, const TLorentzVector & muPos, double weight=1.);
  void endjob(); 
    
private:
  TDirectory * the_dir;

  TObjArray HList_pos, HList_neg;
  TObjArray HListKS_pos, HListKS_neg;
  TObjArray Canvas;
  vector <float> delta_k;

  /* vector <float> dk_68; */
  /* vector <float> dk_95; */

  int n_Dk;
  double *dk, *chi2, *ks;
  
  char dirname[200];
};
