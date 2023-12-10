#-------------------------------------------------------------------------------
# Name:        createDocumentation
# Purpose:
#
# Author:      Matthias Pospiech
#
# Created:     01.04.2013
# Copyright:   (c) Matthias Pospiech 2013
# Licence:     GPL
#-------------------------------------------------------------------------------
import sys
import os
import shutil
import datetime
import texBuildFunctions as tex
import insertPrintCode as importInsertPrintCode
import fontexamples as importFontExamples
import createPackages as importCreatePackages
import time
from statistics import mean

def main():
    print ("--- clean up main folder before compilation ---")
    tex.unfailingRemoveFile('../template/TemplateDocumentation-figure*.log')
    tex.cleanupRecursiveAuxFiles('../template/', '*.aux')
    texfile = '../template/LuaLaTeXTemplate.tex'
    tex.cleanupAuxFiles(texfile)

    oldPath = os.getcwd()
    os.chdir('../template/')

    tlist = list()
    
    for index in range(5):
        # get the start time
        tstart = time.time()
        print ("--- compiling LuaLaTeXTemplate.tex ---")
        texfile = 'LuaLaTeXTemplate.tex'
        tex.latexCommand(texfile)

        # get the end time
        tend = time.time()

        # get the execution time
        elapsed_time = tend - tstart    
        print('Execution time:', elapsed_time, 'seconds')
        tlist.append(elapsed_time)
    
    print(tlist)
    print(min(tlist))

    meanStr = "{:.2f}".format(mean(tlist))
    with open("RunStatistics.txt", "a") as file_object:
        # Append string' at the end of file
        file_object.write("\n" + meanStr + "\n")

    file_object.close()

if __name__ == '__main__':
    main()
