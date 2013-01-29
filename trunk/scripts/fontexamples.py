import re
import os
import shutil


def unfailingRemoveFile(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(filename + ' does not exist.')


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
    unfailingRemoveFile(filename + 'tex')
    unfailingRemoveFile(filename + 'log')

def insertSelectionInTemplate(fontSelectionList, fontTemplateFile, outputFile):
    for fontSelectionEntries in fontSelectionList:
        for line in fontSelectionEntries:
            # \renewcommand{\fontdesc}{Charter, Bera Sans, Luxi Mono}
            match = re.search(r"\\renewcommand{\\fontdesc}{(.+)}", line)
            if match:
                fontString = match.group(1)
                fontString = fontString.replace(', ','-')
                fontString = fontString.replace(',','-')
        outputFileChanged = outputFile + ' - ' + fontString + '.tex'
        with open(fontTemplateFile, 'r') as parseFileHandle:
            with open(outputFileChanged, 'w') as outputFileHandle:
                for lineParse in parseFileHandle:
                    # write line to output
                    if lineParse.startswith('%%?'):
                        index = lineParse.find('<*preamblefontcode*>')
                        if index >= 0:
                            for fontline in fontSelectionEntries:
                                outputFileHandle.write(fontline)
                        index = lineParse.find('<*fontcode*>')
                        if index >= 0:
                            for fontline in fontSelectionEntries:
                                index = fontline.find('fontdesc')
                                if index < 0:
                                    outputFileHandle.write(fontline)
                    else:
                        outputFileHandle.write(lineParse)
        newPath, filename = os.path.split(outputFileChanged)
        oldPath = os.getcwd()
        os.chdir(newPath)
        executeCode = 'pdflatex.exe -interaction=nonstopmode  -shell-escape "' \
                    + filename + '"'
        os.system(executeCode)
        filenamepdf = filename.replace('.tex', '.pdf')
        shutil.move(filenamepdf, 'fonts/' + filenamepdf)
        cleanupAuxFiles(filename.replace('.tex', '.'))
        os.chdir(oldPath)



def parseFontCodeFile(fontCodeFile):
    isReadCodeLines = False
    fontSelectionList = []
    fontSelectionEntries = []
    with open(fontCodeFile, 'r') as parseFileHandle:
        for lineParse in parseFileHandle:
            if isReadCodeLines:
                if lineParse.startswith('% <'):
                    isReadCodeLines = False
                    fontSelectionList.append(fontSelectionEntries)
                else:
                    fontSelectionEntries.append(lineParse)
            # test for string '% ->'
            if lineParse.startswith('% ->'):
                isReadCodeLines = True
                fontSelectionEntries = []
    return fontSelectionList


if __name__ == "__main__":
    baseFilePath = r"..\template\doc"
    fontCodeFile = baseFilePath + r"\font-combinations.tex"
    fontTemplateFile = baseFilePath + r"\fontsamples-template.tex"
    outputFile = r"..\template\fontsample"
    #
    fontSelectionList = parseFontCodeFile(fontCodeFile)
    insertSelectionInTemplate(fontSelectionList, fontTemplateFile, outputFile)
