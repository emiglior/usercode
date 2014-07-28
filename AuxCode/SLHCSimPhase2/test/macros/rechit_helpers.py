#!/usr/bin/env python

import math

# conversion factors
CmToUm = 10000.    # length -> from cm to um
ToKe = 0.001       # charge -> from e to ke
ELossSilicon = 78. # 78 e-h pairs/um in Silicon
##################################################


#######################################
def NotModuleEdge(x_local, y_local):
######################################
    """ x_local, y_local in um """

    accept = True
    if math.fabs(x_local)>7900. or math.fabs(y_local)>31150.:  # or alternativley if math.fabs(x_local)>7750. or math.fabs(y_local)>31150.:  #
        accept = False

    return accept
