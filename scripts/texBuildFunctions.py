import os
import glob
import fnmatch
import subprocess
import sys
import glob
import shutil
import re

def main():
    logfile = '../template/TemplateDocumentation.log'
    outputFile = '../template/TemplateDocumentation-FileList.txt'
    extractFileList(logfile, outputFile)

def extractFileList(logfile, outputFile):
    strStart = ' *File List*'
    strEnd = ' ***********'
    logFileListValid = False
    array = []

    with open(logfile, 'r') as parseFileHandle:
        with open(outputFile, 'w') as outputFileHandle:
            for lineParse in parseFileHandle:
                # test for string '%%?'
                if lineParse.startswith(strEnd):
                    logFileListValid = False
                    break

                if lineParse.startswith(strStart):
                    logFileListValid = True
                    continue

                if (logFileListValid):
                    array.append( lineParse )
                    logFileEntryNumbers = 0
                    for lineInput in array:
                        if lineInput == lineParse:
                            logFileEntryNumbers = logFileEntryNumbers + 1
                            # print (lineInput)
                        if logFileEntryNumbers > 2:
                            # print(lineParse)
                            break
                    # output only if entry is unique
                    if logFileEntryNumbers < 2:
                        # write line to output
                        outputFileHandle.write(lineParse)

def ensureDirectoryExists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def unfailingRemoveFile(filename):
    for filePath in glob.glob(filename):
        print(filePath)
        if os.path.isfile(filePath):
            os.remove(filePath)
            print("removed: " + filePath)
        else:
            print(filePath + " not found")

def cleanupRecursiveAuxFiles(rootPath, filetype):
    for root, dirs, files in os.walk(rootPath):
        for filename in fnmatch.filter(files, filetype):
            unfailingRemoveFile(os.path.join(root, filename))

# from http://stackoverflow.com/questions/2584414/python-windows-file-copy-with-wildcard-support
def copyfiles(src_glob, dst_folder):
    for fname in glob.iglob(src_glob):
        filename = fname.replace('\\', '/')
        print(filename )
        shutil.copy(filename, dst_folder)

def cleanupAuxFiles(filename):
    unfailingRemoveFile(filename + 'aux')
    unfailingRemoveFile(filename + 'aux')
    unfailingRemoveFile(filename + 'dvi')
    unfailingRemoveFile(filename + 'acn')
    unfailingRemoveFile(filename + 'acr')
    unfailingRemoveFile(filename + 'alg')
    unfailingRemoveFile(filename + 'blg')
    unfailingRemoveFile(filename + 'glg')
    unfailingRemoveFile(filename + 'gls')
    unfailingRemoveFile(filename + 'slg')
    unfailingRemoveFile(filename + 'syi')
    unfailingRemoveFile(filename + 'blx.bib')
    unfailingRemoveFile(filename + 'glo')
    unfailingRemoveFile(filename + 'idx')
    unfailingRemoveFile(filename + 'ilg')
    unfailingRemoveFile(filename + 'ind')
    unfailingRemoveFile(filename + 'ist')
    unfailingRemoveFile(filename + 'lof')
    unfailingRemoveFile(filename + 'lol')
    unfailingRemoveFile(filename + 'lot')
    unfailingRemoveFile(filename + 'ps')
    unfailingRemoveFile(filename + 'gnuplot')
    unfailingRemoveFile(filename + 'table')
    unfailingRemoveFile(filename + 'xml')
    unfailingRemoveFile(filename + 'syg')
    unfailingRemoveFile(filename + 'toc')
    unfailingRemoveFile(filename + 'bcf')
    unfailingRemoveFile(filename + 'tdo')
    unfailingRemoveFile(filename + 'bak')
    unfailingRemoveFile(filename + 'filelist')
    unfailingRemoveFile(filename + 'gz')
    unfailingRemoveFile(filename + 'run.xml')
    unfailingRemoveFile(filename + 'log')
    unfailingRemoveFile(filename + 'out')
    unfailingRemoveFile(filename + 'hd')
    unfailingRemoveFile(filename + 'ptc')
    unfailingRemoveFile(filename + 'mw')
    unfailingRemoveFile(filename + 'bbl')
    unfailingRemoveFile(filename + 'pgf-plot.gnuplot')
    unfailingRemoveFile(filename + 'pgf-plot.table')
    unfailingRemoveFile(filename + 'plotdata.gnuplot')
    unfailingRemoveFile(filename + 'plotdata.table')
    unfailingRemoveFile(filename + 'tex.blg')
    unfailingRemoveFile(filename + 'wrt')
    unfailingRemoveFile(filename + 'auxlock')
    unfailingRemoveFile(filename + 'glsdefs')
    unfailingRemoveFile(filename + 'synctex.gz')
    unfailingRemoveFile('plotdata.txt')
    unfailingRemoveFile('fit.log')



# executes python script
def execfile(filename):
    exec(compile(open(filename).read(), filename, 'exec'))


def callSystemCommand(command):
    try:
        print ( command )
        retcode = subprocess.call(command, shell=True)
        if retcode != 0:
            print("System command was terminated by signal", -retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)

def compileLatexDocument(texfile):
    # move to path of tex file
    newPath, filename = os.path.split(texfile)
    oldPath = os.getcwd()
    if os.path.exists(newPath):
        os.chdir(newPath)
    # base filename
    texName = filename.replace('.tex', '')

    # delete previous aux files
    print ('--- delete previous aux files ---' )
    cleanupRecursiveAuxFiles(newPath, '*.aux')

    print ('--- creating document ' + texName + ' ---' )
    # call pdflatex
    callSystemCommand(['pdflatex', '--interaction', 'nonstopmode', '-shell-escape', texName + '.tex'])

    # call makeglossaries
    callSystemCommand(['makeglossaries', texName])

    # call biber
    callSystemCommand(['biber', texName])

    # call makeindex
    callSystemCommand(['makeindex', texName + '.ist'])
    # executeCode = 'makeindex "' + texName + '.ist"'
    # result = os.system(executeCode)

    # call pdflatex
    callSystemCommand(['pdflatex', '--interaction', 'nonstopmode', '-shell-escape', texName + '.tex'])

    logfile = texName + '.log'
    outputFile = texName + '-FileList' + '.txt'
    extractFileList(logfile, outputFile)

    # call pdflatex
    callSystemCommand(['pdflatex', '--interaction', 'nonstopmode', '-shell-escape', texName + '.tex'])

    # call pdflatex
    callSystemCommand(['pdflatex', '--interaction', 'nonstopmode', '-shell-escape', texName + '.tex'])

    # clean up temp files
    print ('cleaning up temp files')
    cleanupAuxFiles(texName + '.')
    cleanupRecursiveAuxFiles(newPath, '*.aux')
    # move back to original path
    os.chdir(oldPath)


main()