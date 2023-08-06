Project pyfromroot
==================

*initial setup*

The goal is to have a framework to run Python from root\'s CLINT. Why?

-   TH1F and TGraph on TCanvas is superior over python stuff
-   and it is interactive
-   staying in root allows to have a access to histograms and all other
    stuff

Usage
=====

From python
-----------

Full example:

``` {.python results="replace output" session="test" exports="both"}

#!/usr/bin/env python3

from  pyfromroot import  prun
import ROOT
import time
import sys
from fire import Fire

def calib():
    # loading
    prun.loadpy("load","calib.txt x,y,dy")

    # fitting
    res = prun.loadpy("fit","calib pol2")  #print(res.keys() )



def gaus():

    # loading histogram
    prun.loadpy("load","cugamma_cu4.txt _,h")


    # zooming
    prun.loadpy("zoom","cugamma_cu4 7432,50")


    # fitting
    res = prun.loadpy("fit","cugamma_cu4 gpol1")  #print(res.keys() )




    if ( type(res) is dict) and ( res['noerror']):
        print(f"@ {res['channel']:.2f} A = {res['area']:.2f} {res['darea']:.2f}")
        print(res['diff_fit_int_proc'],"%" )
    else:
        print("X... problem in fit OR data not returned in dict")



if __name__ == "__main__":
    Fire()
    # wait closing
    while ROOT.addressof(ROOT.gPad)!=0: time.sleep(0.2)
    sys.exit(0)



```

From root
---------

*to be done*

Versions
========

-   0.1.
