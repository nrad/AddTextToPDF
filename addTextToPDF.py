"""
Based on replacepdftext.sh by  Claudio 09-mar-2017
https://twiki.cern.ch/twiki/pub/CMS/SUSY-PublicAnalysisWebPageInstructions/replacepdftext.sh

Can add a new text to the given pdffile(s) at the certain x,y position
the actual values for x,y might need a bit of try and error

the main catch is that *uncompressed* pdf should contain the "lookfor" string
since this is where the new text will be added. There is almost certainty 
better ways of doing this.
If you need to change the "lookfor" it might be useful to do
  pdftk <pdffile> output test.tmp uncompress
and you might be able to find a suitable "lookfor" candidate in test.tmp


2018 NR
"""

from argparse import ArgumentParser

default_newtext =   "Preliminary"
default_posX    =   100
default_posY    =   100
default_size    =   14
default_lookfor =   "(CMS) Tj ET"
default_font    =   "F5"

parser = ArgumentParser()
parser.add_argument("pdffiles",  nargs="+", default="", help="pdf files to process" )
parser.add_argument("--outputdir", default="./fixed/", help="output directory")

parser.add_argument("--y"       , default= default_posY, help="Y position for new text")
parser.add_argument("--x"       , default= default_posX, help="X position for new text")
parser.add_argument("--size"    , default= default_size, help="size of new text")
parser.add_argument("--newtext", default= default_newtext, help="new text")
parser.add_argument("--lookfor", default= default_lookfor, help="String to look for in the uncompressed pdf" )
parser.add_argument("--font"   , default= default_font, help="pdf font F1 F2 .... FX" )
options = parser.parse_args()

import os, sys, subprocess, glob


print options.pdffiles

pdffiles = options.pdffiles
lookfor  = options.lookfor



#
# Don't change below, unless for a good reaason
#

lineToAdd_template="Q q 0 164.951 566.929 384.885 re W n 1 0 0 1 {posX} {posY} cm BT \/{font} {size} Tf ({newtext}) Tj ET"
lineToAdd=lineToAdd_template.format( posX = options.x, posY=options.y, size=options.size, font=options.font, newtext=options.newtext,)


def runCommand( command ):
    popen = subprocess.Popen( command , stdout=subprocess.PIPE, stderr=subprocess.PIPE , shell=True)
    return popen.stdout, popen.stderr


test_pdftk = runCommand( "pdftk --version" )
stdout, stderr = map( lambda x: x.readlines(), test_pdftk )
if stderr:
    raise Exception( "pdftk package doesn't seem to be available. Please install it before using this script" )

else:
    for l in stdout:
        print l.rstrip("\n")
    print "\n"

if not os.path.isdir( options.outputdir ):
    os.makedirs( options.outputdir )


for pdffile in pdffiles:
    print "Processing %s ..."%pdffile
    os.system( "pdftk {pdffile} output {pdffile}.tmp uncompress".format(pdffile=pdffile) )
    os.system( 'sed -i -e "s/{lookfor}/{lookfor} {lineToAdd}/g" {pdffile}.tmp'.format(lookfor=lookfor, lineToAdd=lineToAdd, pdffile=pdffile) )
    outputpdf = options.outputdir +"/" +os.path.basename(pdffile)
    os.system( "pdftk {pdffile}.tmp output {outputpdf} compress".format(pdffile=pdffile, outputpdf=outputpdf))
    os.system( "rm {pdffile}.tmp".format(pdffile=pdffile) )
    print "output created in %s \n"%outputpdf
