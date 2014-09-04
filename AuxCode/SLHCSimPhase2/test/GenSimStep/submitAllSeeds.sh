#!/bin/bash

CMSSW_DIR=${CMSSW_BASE}/src/AuxCode/SLHCSimPhase2/test/GenSimStep
cd $CMSSW_DIR

for i in {0..159}; do   
    echo "------ submitting job with seed = $i"
    bsub -o tmp.tmp -q 1nd MinBias_TuneZ2star_14TeV_pythia6_cff_py_GEN_SIM_forPhaseI_TEMPL.lsf $i 300
done

for i in {0..39}; do   
    echo "------ submitting job with seed = $i"
    bsub -o tmp.tmp -q 1nd FourMuPt_1_200_cfi_GEN_SIM_forPhaseI_TEMPL.lsf $i 2500
    bsub -o tmp.tmp -q 1nd TTtoAnything_14TeV_pythia6_cff_py_GEN_SIM_forPhaseI_TEMPL.lsf $i 300
done

