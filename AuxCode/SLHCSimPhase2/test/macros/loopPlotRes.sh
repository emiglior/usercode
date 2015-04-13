#!/bin/sh

function run_PlotRes {
    python PlotRes.py -f $1 -L $3 -S $4 
    ext=$TMPDIR/$2
    mkdir -p $ext

    mv *.root    ${ext}
    mv *.png     ${ext}
    mv *.pdf     ${ext}
    mv *.txt     ${ext}
    }

DATA=/tmp/emiglior
        

#run_PlotRes ${DATA}/OccupancyPlotTest_TenMuE_ntuple_age_NoAgeing_PixDigiThr_1500_100_evts_seed_1.root  TestBPIX_Layer1 1 1
run_PlotRes ${DATA}/OccupancyPlotTest_TenMuE_ntuple_age_NoAgeing_PixDigiThr_1500_100_evts_seed_1.root  TestBPIX_Layer3 3 1
#run_PlotRes ${DATA}/OccupancyPlotTest_TenMuE_ntuple_age_NoAgeing_PixDigiThr_1500_100_evts_seed_1.root  TestFPIX_Disk1  1 2
#run_PlotRes ${DATA}/OccupancyPlotTest_TenMuE_ntuple_age_NoAgeing_PixDigiThr_1500_100_evts_seed_1.root  TestFPIX_Disk3  3 2
#run_PlotRes ${DATA}/OccupancyPlotTest_TenMuE_ntuple_age_NoAgeing_PixDigiThr_1500_100_evts_seed_1.root  TestFPIX_Disk5  5 2


