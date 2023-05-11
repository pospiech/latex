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


def main():        

    # print ("--- clean up main folder before compilation ---")
    #tex.unfailingRemoveFile('../template/TemplateDocumentation-figure*.log')
    #tex.cleanupRecursiveAuxFiles('../template/', '*.aux')
    #texfile = '../template/LaTeXTemplate.'
    #tex.cleanupAuxFiles(texfile)
    #texfile = '../template/TemplateDocumentation.'
    #tex.cleanupAuxFiles(texfile)
    # sys.exit()

    print ("--- Creation of Packages ---")
    importCreatePackages.main()
    sys.exit()

    print ("--- Copy Packages ---")
    # copyPackages()

    print ("--- Create Font Examaples ---")
    # importFontExamples.main()

    print ("--- fill doc-code.tex ---")
    importInsertPrintCode.main()
    sys.exit()

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
    tex.unfailingRemoveFile('../template/demo-glossaries-*')

    copyFile('bib/BibtexDatabase.bib', 'bib')
    copyFile('bib/publications.bib', 'bib')
    copyFile('content/template/latextutorial.tex', 'content/template/')
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
    copyFile('licence.txt', '')
    # copyFile('*.sty', '')


    # zip publish folder
    oldPath = os.getcwd()
    os.chdir('../template/')

    currentDateStr = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = 'latexthesistemplate-' + currentDateStr + '.zip'
    executeCode = 'zip -r ' + filename + ' latexthesistemplate/*'
    print (executeCode)
    result = os.system(executeCode)

    os.chdir(oldPath)


def copyFile(filename, targetFolder):
    strBaseDir = '../template/latexthesistemplate/'
    tex.ensureDirectoryExists(strBaseDir)
    strTargetDir = strBaseDir + targetFolder
    tex.ensureDirectoryExists(strTargetDir)
    strFileOrigin = '../template/' + filename
    tex.copyfiles(strFileOrigin, strTargetDir)


def copyTeXFile(texfile):
    strTargetDir = '../template/latexthesistemplate'
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
