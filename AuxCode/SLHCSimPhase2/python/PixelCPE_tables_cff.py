import FWCore.ParameterSet.Config as cms

# taken from https://github.com/cms-sw/cmssw/blob/CMSSW_6_1_2_SLHC8_patch3/RecoLocalTracker/SiPixelRecHits/src/PixelCPEGeneric.cc

#Pixel CPE for default pixel cell (100um x 150um)
pixel_CPE_100x150_default = cms.PSet(
    xerr_barrel_l1_= cms.untracked.vdouble(0.00115, 0.00120, 0.00088),
    xerr_barrel_l1_def_=cms.untracked.double(0.01030),
    yerr_barrel_l1_= cms.untracked.vdouble(0.00375,0.00230,0.00250,0.00250,0.00230,0.00230,0.00210,0.00210,0.00240),
    yerr_barrel_l1_def_=cms.untracked.double(0.00210),
    xerr_barrel_ln_= cms.untracked.vdouble(0.00115, 0.00120, 0.00088),
    xerr_barrel_ln_def_=cms.untracked.double(0.01030),
    yerr_barrel_ln_= cms.untracked.vdouble(0.00375,0.00230,0.00250,0.00250,0.00230,0.00230,0.00210,0.00210,0.00240),
    yerr_barrel_ln_def_=cms.untracked.double(0.00210),
    xerr_endcap_= cms.untracked.vdouble(0.0020, 0.0020),
    xerr_endcap_def_=cms.untracked.double(0.0020),
    yerr_endcap_= cms.untracked.double(0.00210),
    yerr_endcap_def_=cms.untracked.double(0.00075)
    )

#Pixel CPE for upgrade pixel cell (100um x 150um) 
pixel_CPE_100x150_upgrade = cms.PSet(
    xerr_barrel_l1_= cms.untracked.vdouble(0.00114,0.00104,0.00214),
    xerr_barrel_l1_def_= cms.untracked.double(0.00425),
    yerr_barrel_l1_= cms.untracked.vdouble(0.00299,0.00203,0.0023,0.00237,0.00233,0.00243,0.00232,0.00259,0.00176),
    yerr_barrel_l1_def_=cms.untracked.double(0.00245),
    xerr_barrel_ln_= cms.untracked.vdouble(0.00114,0.00104,0.00214),
    xerr_barrel_ln_def_=cms.untracked.double(0.00425),
    yerr_barrel_ln_= cms.untracked.vdouble(0.00299,0.00203,0.0023,0.00237,0.00233,0.00243,0.00232,0.00259,0.00176),
    yerr_barrel_ln_def_=cms.untracked.double(0.00245),
    xerr_endcap_= cms.untracked.vdouble(0.00151,0.000813,0.00221),
    xerr_endcap_def_=cms.untracked.double(0.00218),
    yerr_endcap_= cms.untracked.vdouble(0.00261,0.00107,0.00264),
    yerr_endcap_def_=cms.untracked.double(0.00357)
    )

#Pixel CPE for upgrade pixel cell (75um x 100um) 
pixel_CPE_75x100_upgrade = cms.PSet(
    xerr_barrel_l1_= cms.untracked.vdouble(0.00104, 0.000691, 0.00122),
    xerr_barrel_l1_def_=cms.untracked.double(0.00321),
    yerr_barrel_l1_= cms.untracked.vdouble(0.00199,0.00136,0.0015,0.00153,0.00152,0.00171,0.00154,0.00157,0.00154),
    yerr_barrel_l1_def_=cms.untracked.double(0.00164),
    xerr_barrel_ln_= cms.untracked.vdouble(0.00114,0.00104,0.00214),
    xerr_barrel_ln_def_=cms.untracked.double(0.00425),
    yerr_barrel_ln_= cms.untracked.vdouble(0.00299,0.00203,0.0023,0.00237,0.00233,0.00243,0.00232,0.00259,0.00176),
    yerr_barrel_ln_def_=cms.untracked.double(0.00245),
    xerr_endcap_= cms.untracked.vdouble(0.00151,0.000813,0.00221),
    xerr_endcap_def_=cms.untracked.double(0.00218),
    yerr_endcap_= cms.untracked.vdouble(0.00261,0.00107,0.00264),
    yerr_endcap_def_=cms.untracked.double(0.00357)
    )

#Pixel CPE for upgrade pixel cell (50um x 75um)
# DUMMY VALUES TO TEST THE WORKFLOW
pixel_CPE_50x75_upgrade = cms.PSet(
    xerr_barrel_l1_= cms.untracked.vdouble(0.00104, 0.000691, 0.00122),
    xerr_barrel_l1_def_=cms.untracked.double(0.00321),
    yerr_barrel_l1_= cms.untracked.vdouble(0.00199,0.00136,0.0015,0.00153,0.00152,0.00171,0.00154,0.00157,0.00154),
    yerr_barrel_l1_def_=cms.untracked.double(0.00164),
    xerr_barrel_ln_= cms.untracked.vdouble(0.00114,0.00104,0.00214),
    xerr_barrel_ln_def_=cms.untracked.double(0.00425),
    yerr_barrel_ln_= cms.untracked.vdouble(0.00299,0.00203,0.0023,0.00237,0.00233,0.00243,0.00232,0.00259,0.00176),
    yerr_barrel_ln_def_=cms.untracked.double(0.00245),
    xerr_endcap_= cms.untracked.vdouble(0.00151,0.000813,0.00221),
    xerr_endcap_def_=cms.untracked.double(0.00218),
    yerr_endcap_= cms.untracked.vdouble(0.00261,0.00107,0.00264),
    yerr_endcap_def_=cms.untracked.double(0.00357)
    )


#Dummy Pixel CPE (for test purposes)  
pixel_CPE_dummy= cms.PSet(
    xerr_barrel_l1_=cms.untracked.vdouble(0.00415,0.0042,0.00388),
    xerr_barrel_l1_def_=cms.untracked.double(0.04030),
    yerr_barrel_l1_=cms.untracked.vdouble(0.01375,0.00830,0.00850,0.00850,0.00830,0.00830,0.00810,0.00810,0.00840),
    yerr_barrel_l1_def_=cms.untracked.double(0.00810),
    xerr_barrel_ln_=cms.untracked.vdouble(0.00415,0.00420,0.00388),
    xerr_barrel_ln_def_=cms.untracked.double(0.04030),
    yerr_barrel_ln_=cms.untracked.vdouble(0.01375,0.00830,0.00850,0.00850,0.00830,0.00830,0.00810,0.00810,0.00840),
    yerr_barrel_ln_def_=cms.untracked.double(0.00810),
    xerr_endcap_=cms.untracked.vdouble(0.0080,0.0080),
    xerr_endcap_def_=cms.untracked.double(0.0080),
    yerr_endcap_=cms.untracked.vdouble(0.00810),
    yerr_endcap_def_=cms.untracked.double(0.00275)
    )

PixelCPE_dict = { 'pixel_CPE_100x150_default' : pixel_CPE_100x150_default,
                  'pixel_CPE_100x150_upgrade' : pixel_CPE_100x150_upgrade,
                  'pixel_CPE_50x75_upgrade'   : pixel_CPE_50x75_upgrade ,
                  'pixel_CPE_75x100_upgrade'  : pixel_CPE_75x100_upgrade ,
                  'pixel_CPE_dummy'           : pixel_CPE_dummy }
