#!/bin/sh

function run_PlotRes {
    python PlotRes.py -f $1 -L $3 -S $4 -e 300000
    ext=$2
    mkdir -p $ext

    mv *.root    ${ext}
    mv *.png     ${ext}
    mv *.pdf     ${ext}
    mv *.txt     ${ext}
    }

DATA=/tmp/emiglior
         
python SkimTree.py -f ${DATA}/pixellocalreco_ntuple_test0TPGun_PixelROCRows_80_80_PixelROCCols_52_52_Thick_0.285_0.285_BPixThr_3000.root 

run_PlotRes ${DATA}/pixellocalreco_ntuple_test0TPGun_PixelROCRows_80_80_PixelROCCols_52_52_Thick_0.285_0.285_BPixThr_3000_Skimmed.root  TestBPIX_Layer1 1 1
run_PlotRes ${DATA}/pixellocalreco_ntuple_test0TPGun_PixelROCRows_80_80_PixelROCCols_52_52_Thick_0.285_0.285_BPixThr_3000_Skimmed.root  TestFPIX_Disk1  1 2
run_PlotRes ${DATA}/pixellocalreco_ntuple_test0TPGun_PixelROCRows_80_80_PixelROCCols_52_52_Thick_0.285_0.285_BPixThr_3000_Skimmed.root  TestFPIX_Disk3  3 2
run_PlotRes ${DATA}/pixellocalreco_ntuple_test0TPGun_PixelROCRows_80_80_PixelROCCols_52_52_Thick_0.285_0.285_BPixThr_3000_Skimmed.root  TestFPIX_Disk5  5 2


