import re
import os
import shutil
import texBuildFunctions as tex

def main():
    baseFilePath = r"..\template\doc"
    fontCodeFile = baseFilePath + r"\font-combinations.tex"
    fontTemplateFile = baseFilePath + r"\fontsamples-template.tex"
    outputFile = r"..\template\fontsample"
    #
    fontSelectionList = parseFontCodeFile(fontCodeFile)
    insertSelectionInTemplate(fontSelectionList, fontTemplateFile, outputFile)


# loads Font combinations from a file
#
# The font combinations are saved in the format:
# % -> Palantino, Helvetica, Courier
# \usepackage{mathpazo}                 %% --- Palantino (incl math)
# \usepackage[scaled=.95]{helvet}       %% --- Helvetica (Arial)
# \usepackage{courier}                  %% --- Courier
# \renewcommand{\fontdesc}{Palantino, Arial, Courier}
# % <-------------------
#
# with "% ->" indicating the start of a new group
# and "% <" indicating the end.
def parseFontCodeFile(fontCodeFile):
    isReadCodeLines = False
    fontSelectionList = []
    fontSelectionEntries = []
    with open(fontCodeFile, 'r') as parseFileHandle:
        for lineParse in parseFileHandle:
            if isReadCodeLines:
                # test for string '% <'
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


# inserts font commands in tex file and compiles it
#
# the commands (lines in fontSelectionList) are inserted in these places
# %%? <*preamblefontcode*>
# %%? <*fontcode*>
def insertSelectionInTemplate(fontSelectionList, fontTemplateFile, outputFile):
    for fontSelectionEntries in fontSelectionList:
        # create fontString for output filename
        for line in fontSelectionEntries:
            # search for \fontdesc and change its string, if necessary
            # Example: \renewcommand{\fontdesc}{Charter, Bera Sans, Luxi Mono}
            match = re.search(r"\\renewcommand{\\fontdesc}{(.+)}", line)
            if match:
                fontString = match.group(1)
                fontString = fontString.replace(', ', '-')
                fontString = fontString.replace(',', '-')
        # Open output file with changed font string
        # Insert all lines of fontSelectionEntries to the template positions
        outputFileChanged = outputFile + ' - ' + fontString + '.tex'
        print ('Creating font sample: ' + outputFileChanged)
        with open(fontTemplateFile, 'r') as parseFileHandle:
            with open(outputFileChanged, 'w') as outputFileHandle:
                for lineParse in parseFileHandle:
                    # write line to output
                    if lineParse.startswith('%%?'):
                        # write all lines of fontSelectionEntries to outputFileHandle
                        index = lineParse.find('<*preamblefontcode*>')
                        if index >= 0:
                            for fontline in fontSelectionEntries:
                                outputFileHandle.write(fontline)
                        # write all lines of fontSelectionEntries to outputFileHandle
                        # except the line with 'fontdesc'
                        index = lineParse.find('<*fontcode*>')
                        if index >= 0:
                            for fontline in fontSelectionEntries:
                                index = fontline.find('fontdesc')
                                if index < 0:
                                    outputFileHandle.write(fontline)
                    else:
                        outputFileHandle.write(lineParse)
        # get path and file of full file name
        newPath, filename = os.path.split(outputFileChanged)
        # compile file in folder of file
        oldPath = os.getcwd()
        os.chdir(newPath)
        tex.callSystemCommand(['pdflatex', '-interaction=nonstopmode', '-shell-escape', filename])
        # executeCode = 'pdflatex.exe -interaction=nonstopmode  -shell-escape "' \
        #              + filename + '"'
        # os.system(executeCode)

        # move pdf to different folder "fonts/"
        filenamepdf = filename.replace('.tex', '.pdf')
        if os.path.isfile(filenamepdf):
            shutil.move(filenamepdf, 'fonts/' + filenamepdf)
        else:
            print('file ' + filenamepdf + ' not found, aborting!')
            sys.exit()

        # remove all aux files
        tex.cleanupAuxFiles(filename.replace('.tex', '.'))
        tex.unfailingRemoveFile(filename)
        tex.unfailingRemoveFile(filename.replace('.tex', '.log'))
        # change to previous folder
        os.chdir(oldPath)


if __name__ == "__main__":
    main()
