import re
import os
import shutil
import datetime
import texBuildFunctions as tex


def main():
    strTargetDir = "CTAN"
    createPackage('doctools', strTargetDir)
    createPackage('latexdemo', strTargetDir)
    return
    createPackage('lastpackage', strTargetDir)
    createPackage('tablestyles', strTargetDir)
    createPackage('codesection', strTargetDir)
    createPackage('templatetools', strTargetDir)


def compileDTXPackage(package):
    # move to path of package
    newPath, filename = os.path.split(package)
    oldPath = os.getcwd()
    if os.path.exists(newPath):
        os.chdir(newPath)
    # base filename
    packageName = filename.replace('.dtx', '')
    print ('----> creating package ' + packageName + ' ---' )
    # call pdflatex on package.ins
    executeCode = 'pdflatex -shell-escape "' + packageName + '.ins"'
    print (executeCode)
    result = os.system(executeCode)

    # call pdflatex on package.dtx
    executeCode = 'pdflatex -shell-escape "' + packageName + '.dtx"'
    print (executeCode)
    result = os.system(executeCode)

    # call makeindex
    executeCode = 'makeindex -s gind.ist "' + packageName + '.idx"'
    print (executeCode)
    result = os.system(executeCode)

    # call pdflatex on package.dtx
    executeCode = 'pdflatex -shell-escape "' + packageName + '.dtx"'
    print (executeCode)
    result = os.system(executeCode)

    # call pdflatex on package.dtx
    executeCode = 'pdflatex -shell-escape "' + packageName + '.dtx"'
    print (executeCode)
    result = os.system(executeCode)

    # clean up temp files
    print ('----> cleaning up temp files')
    tex.cleanupAuxFiles(filename.replace('.dtx', '.'))
    # move back to original path
    os.chdir(oldPath)


def compileLaTeXPackage(package):
    # move to path of package
    newPath, filename = os.path.split(package)
    oldPath = os.getcwd()
    if os.path.exists(newPath):
        os.chdir(newPath)
    # call pdflatex on package
    executeCode = 'pdflatex' \
                + ' -interaction=nonstopmode  ' \
                + '-shell-escape "' \
                + filename + '"'
    result = os.system(executeCode)
    print ('Execution returns: ' + result)
    # clean up temp files
    tex.cleanupAuxFiles(filename.replace('.tex', '.'))
    # move back to original path
    os.chdir(oldPath)


def exchangeInputByFile(package, targetFolder):
    parseFile = package + ".dtx"
    outputFile = targetFolder + "\\" + package + "\\" + package + ".dtx"

    currentDateStr = datetime.datetime.now().strftime("%Y/%m/%d")
    currentYearStr = datetime.datetime.now().strftime("%Y")
    with open(parseFile, 'r') as parseFileHandle:
        with open(outputFile, 'w') as outputFileHandle:
            for lineParse in parseFileHandle:
                # replace <*date*> by date
                lineParse = lineParse.replace("<*year*>", currentYearStr)
                # replace <*date*> by date
                lineParse = lineParse.replace("<*date*>", currentDateStr)
                # replace <*author*> by Author
                lineParse = lineParse.replace("<*author*>", 'Matthias Pospiech')
                # replace <*email*> by mail
                lineParse = lineParse.replace("<*email*>", 'matthias@pospiech.eu')
                # if string \input{preamble/*} is found
                # write whole input to output file
                match = re.search(r"\\input\{preamble\/(.*?)\}", lineParse)
                if match:
                    inputfile = 'preamble/' + match.group(1)
                    with open(inputfile, 'r') as inputFileHandle:
                        for lineInput in inputFileHandle:
                            # write line to output
                            outputFileHandle.write(lineInput)

                    outputFileHandle.write('\n')
                # if no input file is found,
                # print parse file line ot output file
                else:
                    outputFileHandle.write(lineParse)
            outputFileHandle.write('\n')



# the os must be in the path of the package. All command act only
# on the current path.
def createPackage(package, targetFolder):
    # change to base path of packages
    oldPath = os.getcwd()
    packagesPath = r'..\packages\publish'
    os.chdir(packagesPath)
    # string with target directory
    strTargetDir = targetFolder + "\\" + package
    # create folder
    tex.ensureDirectoryExists(strTargetDir)
    # copy .ins file to folder
    shutil.copy(package + '.ins', strTargetDir)
    # rewrite .dtx file in target folder
    exchangeInputByFile(package, targetFolder)
    # copy doctools.sty to target folder if it exists
    if package != 'doctools':
        doctoolsTargetFile = targetFolder + "\\doctools\\doctools.sty"
        if os.path.exists(doctoolsTargetFile):
            shutil.copy(doctoolsTargetFile, strTargetDir)
    # compile package
    packageFile = strTargetDir + "\\" + package + ".dtx"
    compileDTXPackage(packageFile)
    # remove doctools.sty
    if package != 'doctools':
        tex.unfailingRemoveFile(strTargetDir + "\\doctools.sty")
    # remove package.log
    tex.unfailingRemoveFile(strTargetDir + "\\" + package + '.log')
    # remove package.sty
    # tex.unfailingRemoveFile(strTargetDir + "\\" + package + '.sty')
    # remove any .tex file
    tex.unfailingRemoveFile(strTargetDir + "\\" + '*.tex')


    # copy README
    readmeOriginFile = package + ".README.txt"
    readmeTargetFile = strTargetDir + "\\README"
    if os.path.exists(readmeOriginFile):
        shutil.copy(readmeOriginFile, readmeTargetFile)
        print ('copying README file')

    # zip package folder
    os.chdir(targetFolder)
    filename = package + '.zip'
    executeCode = 'zip -x *.sty -r ' +  filename + ' ' + package + '/*'
    print (executeCode)
    result = os.system(executeCode)

    # change folder back to origin
    os.chdir(oldPath)


if __name__ == "__main__":
    main()

