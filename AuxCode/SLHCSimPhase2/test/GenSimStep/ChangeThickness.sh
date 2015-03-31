#!/bin/bash

export PKG_DIR=${CMSSW_BASE}/src/AuxCode/SLHCSimPhase2/test

# A Tricomi's recipe to change the sensors thickness
# (in this example all layers are set 150 um)
sed -e "s%BPIXLAYER01THICKNESS%0.150%g" ${PKG_DIR}/pixbarladderfull0_template.xml > ${CMSSW_BASE}/src/Geometry/TrackerCommonData/data/PhaseI/pixbarladderfull0.xml 
sed -e "s%BPIXLAYER01THICKNESS%0.150%g" ${PKG_DIR}/pixbarladderfull1_template.xml > ${CMSSW_BASE}/src/Geometry/TrackerCommonData/data/PhaseI/pixbarladderfull1.xml 
sed -e "s%BPIXLAYER23THICKNESS%0.150%g" ${PKG_DIR}/pixbarladderfull2_template.xml > ${CMSSW_BASE}/src/Geometry/TrackerCommonData/data/PhaseI/pixbarladderfull2.xml 
sed -e "s%BPIXLAYER23THICKNESS%0.150%g" ${PKG_DIR}/pixbarladderfull3_template.xml > ${CMSSW_BASE}/src/Geometry/TrackerCommonData/data/PhaseI/pixbarladderfull3.xml 

