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

import os
import shutil
import texBuildFunctions as tex
import insertPrintCode as importInsertPrintCode
import fontexamples as importFontExamples
import createPackages as importCreatePackages

def main():
    print ("--- Creation of Packages ---")
    importCreatePackages.main()

    print ("--- Copy Packages ---")
    copyPackages()

    print ("--- Create Font Examaples ---")
    importFontExamples.main()

    print ("--- fill doc-code.tex ---")
    importInsertPrintCode.main()

    print ("--- compiling LaTeXTemplate.tex ---")
    texfile = '../template/LaTeXTemplate.tex'
    tex.compileLatexDocument(texfile)
    copyTeXFile(texfile)

    print ("--- compiling TemplateDocumentation.tex ---")
    texfile = '../template/TemplateDocumentation.tex'
    tex.compileLatexDocument(texfile)
    copyFile(texfile.replace('.tex', '.pdf'), '')
    tex.cleanupRecursiveAuxFiles('../template/', '*.aux')
    tex.unfailingRemoveFile('../template/content/demo/democode.tex')
    tex.unfailingRemoveFile('../template/content/longtable.tex')


    copyFile('bib/BibtexDatabase.bib', 'bib')
    copyFile('content/demo/demo.tex', 'content/demo/')
    copyFile('content/demo/latextutorial.tex', 'content/demo/')
    copyFile('content/*.tex', 'content')
    copyFile('fonts/*.tex', 'fonts')
    copyFile('images/*', 'images')
    copyFile('macros/*', 'macros')
    copyFile('preamble/commands.tex', 'preamble')
    copyFile('preamble/makeCommands.tex', 'preamble')
    copyFile('preamble/fix*.tex', 'preamble')
    copyFile('preamble/listings*.tex', 'preamble')
    copyFile('preamble/packages*.tex', 'preamble')
    copyFile('preamble/style*.tex', 'preamble')
    copyFile('version.txt', '')
    copyFile('*.sty', '')



def copyFile(filename, targetFolder):
    strBaseDir = '../template/publish/'
    tex.ensureDirectoryExists(strBaseDir)
    strTargetDir = strBaseDir + targetFolder
    tex.ensureDirectoryExists(strTargetDir)
    strFileOrigin = '../template/' + filename
    tex.copyfiles(strFileOrigin, strTargetDir)


def copyTeXFile(texfile):
    strTargetDir = '../template/publish'
    tex.ensureDirectoryExists(strTargetDir)
    shutil.copy(texfile, strTargetDir)
    shutil.copy(texfile.replace('.tex', '.pdf'), strTargetDir)




def copyPackage(package):
    packagesPath = r'..\packages\publish\CTAN'
    templatePath = r'..\template'
    packagefile = packagesPath + "\\" + package + "\\" + package + ".sty"
    if os.path.exists(packagefile):
        shutil.copy(packagefile, templatePath)
        print (package)
    else:
        print (package + ' not found')


def copyPackages():
    copyPackage('doctools')
    copyPackage('lastpackage')
    copyPackage('tablestyles')
    copyPackage('latexdemo')
    copyPackage('codesection')
    copyPackage('templatetools')

if __name__ == '__main__':
    main()
