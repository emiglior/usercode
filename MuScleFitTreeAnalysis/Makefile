# Makefile for shared libraries
# on MacOS requires
# export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:./

### definitions
MAIN_SRC=main.cpp 
MAIN_OBJ=$(MAIN_SRC:.cpp=.o)

MODULE_SRC=dict.cpp
MODULE_SRC+=Helpers.cpp
MODULE_SRC+=CollinsSoperAnalysis.cpp
MODULE_SRC+=GeneralizedEndPointAnalysis.cpp
MODULE_SRC+=GeneralizedEndPointAnalysisOld.cpp

MODULE_LIB=./libModules.so
MODULE_OBJ=$(MODULE_SRC:.cpp=.o)

# if MuScleFit corrections are used....
# MFCORRECTOR= ../MuScleFitCorrector_v4_2

EXECUTABLE=./main

### rules
CC     = g++
CCFLAG = -g -c -fPIC -Wall $(shell root-config --cflags)
LDFLAG = $(shell root-config --libs) -L/opt/local/root/lib -lRooFitCore -lGenVector


dict.cpp: Muon.h MuonPair.h GenMuonPair.h Event.h LinkDef.h
	rootcint -f $@ -c $^

%.o: %.cpp 
	$(CC) -I. $(CCFLAG) -o $@ $<

%.o: %.cpp %.h
	$(CC) -I. $(CCFLAG) -o $@ $<

$(MODULE_LIB): $(MODULE_OBJ)
	$(CC) -shared $(LDFLAG) -o $@ $^ 

$(EXECUTABLE): $(MAIN_OBJ) $(MODULE_LIB)
	$(CC) $(LDFLAG) -L. -lModules -o $@ $< 

### general
all: $(EXECUTABLE) 

.PHONY: clean cleanest

clean:
	rm -f $(EXECUTABLE) $(MAIN_OBJ) $(MODULE_OBJ) dict.*









