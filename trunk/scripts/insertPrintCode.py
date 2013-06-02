import sys
import re




class FileSearch:
    startline = 0
    endline = 0
    filename = None
    minline = 0


def main():
    baseFilePath = r"..\template\doc"
    parseFile = baseFilePath + r"\doc-code.tex"
    outputFile = baseFilePath + r"\doc-code-filled.tex"
    baseInputPath = r"..\template"
    #
    parseDefinitionFile(parseFile, outputFile, baseInputPath)


def prepareSearchString(strfind):
    strfind = strfind.replace('(', '\(')
    strfind = strfind.replace(')', '\)')
    return strfind


def findLinesInInputFile(inputFileName,
        fileSearch,
        strStart,
        strEnd):
    #
    lineNumber = 0
    lineStart = 0
    lineEnd = 0
    debugOutput = False
    #
    # strStart = prepareSearchString(strStart)
    # strEnd = prepareSearchString(strEnd)
    #
    fileSearch.startline = 0
    fileSearch.endline = 0
    #
    minimumLineNumber = fileSearch.minline
    #
    with open(inputFileName, 'r', encoding="utf8") as inputFileHandle:
        for lineInput in inputFileHandle:
            lineNumber = lineNumber + 1
            if lineNumber > minimumLineNumber:
                if lineStart < 1:
                    # mStart = re.search(strStart, lineInput)
                    # if mStart:
                    index = lineInput.find(strStart)
                    if index >= 0:
                        lineStart = lineNumber
                        fileSearch.startline = lineNumber
                        # test for single line
                        if (strStart == strEnd):
                            lineEnd = lineNumber
                            fileSearch.endline = lineNumber
                else:
                    if lineEnd < 1:
                        # mEnd = re.search(strEnd, lineInput)
                        # if mEnd:
                        index = lineInput.find(strEnd)
                        if index >= 0:
                            lineEnd = lineNumber
                            fileSearch.endline = lineNumber
                    else:
                        break
        if (fileSearch.startline > 0) and \
           (fileSearch.endline > 0):
            filename = fileSearch.filename
            filename = filename.replace('\\', '/')
            outputStr = "\\printCodeFromFile[{}]".format(fileSearch.startline) + \
                        "{{{endline}}}".format(endline=fileSearch.endline) + \
                        "{{{name}}}".format(name=filename)

        else:
            print ('ERROR')
            print (inputFileName)
            print (fileSearch.startline)
            print (fileSearch.endline)
            print (strStart)
            print (strEnd)
            sys.exit(0)
        # new minimum is last line
        fileSearch.minline = fileSearch.endline
        return outputStr


def parseDefinitionFile(parseFile, outputFile, baseInputPath):
    debugOutput = False
    isSearchValid = False
    mapFiles = dict()
    with open(parseFile, 'r') as parseFileHandle:
        with open(outputFile, 'w') as outputFileHandle:
            newSearch = FileSearch()
            for lineParse in parseFileHandle:
                # write line to output
                outputFileHandle.write(lineParse)
                # test for string '%%?'
                if lineParse.startswith('%%?'):
                    searchLine = lineParse.replace('%%?', '')
                    searchLine = searchLine.strip()
                    # file
                    match = re.search(r"file: (.+)", lineParse)
                    if match:
                        inputfile = match.group(1)
                        inputfile = inputfile.replace('/', '\\')
                        newSearch.filename = inputfile
                    # start
                    match = re.search(r"start: (.+)", lineParse)
                    if match:
                        strStart = match.group(1)
                    # end
                    match = re.search(r"end: (.+)", lineParse)
                    if match:
                        strEnd = match.group(1)
                        isSearchValid = True
                    # open file and read contents
                    if isSearchValid:
                        isSearchValid = False
                        if inputfile not in mapFiles:
                            mapFiles[inputfile] = newSearch
                            newSearch = FileSearch()
                        inputFileName = baseInputPath + "\\" + inputfile
                        outputStr = findLinesInInputFile(
                            inputFileName,
                            mapFiles[inputfile],
                            strStart,
                            strEnd)
                        outputStr = outputStr + '\n'
                        # print resulting string to output
                        outputFileHandle.write(outputStr)
                        if debugOutput:
                            print (strStart)
                            print (strEnd)
                            print (outputStr)


if __name__ == "__main__":
    main()