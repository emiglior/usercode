import FWCore.ParameterSet.Config as cms

#Pixel CPE for default pixel cell (100um x 150um)
pixel_CPE_standard= cms.VPSet()
pixel_CPE_standard.extend([
cms.PSet(xerr_barrel_l1_=cms.untracked.vdouble(0.00115,0.0012,0.00088),
         xerr_barrel_l1_def_=cms.untracked.double(0.01030),
         yerr_barrel_l1_=cms.untracked.vdouble(0.00375,0.00230,0.00250,0.00250,0.00230,0.00230,0.00210,0.00210,0.00240),
         yerr_barrel_l1_def_=cms.untracked.double(0.00210),
         xerr_barrel_ln_=cms.untracked.vdouble(0.00115,0.00120,0.00088),
         xerr_barrel_ln_def_=cms.untracked.double(0.01030),
         yerr_barrel_ln_=cms.untracked.vdouble(0.00375,0.00230,0.00250,0.00250,0.00230,0.00230,0.00210,0.00210,0.00240),
         yerr_barrel_ln_def_=cms.untracked.double(0.00210),
         xerr_endcap_=cms.untracked.vdouble(0.0020,0.0020),
         xerr_endcap_def_=cms.untracked.double(0.0020),
         yerr_endcap_=cms.untracked.vdouble(0.00210),
         yerr_endcap_def_=cms.untracked.double(0.00075))])


#Dummy Pixel CPE (for test purposes)  
pixel_CPE_dummy= cms.VPSet()
pixel_CPE_dummy.extend([
cms.PSet(xerr_barrel_l1_=cms.untracked.vdouble(0.00415,0.0042,0.00388),
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
         yerr_endcap_def_=cms.untracked.double(0.00275))])
