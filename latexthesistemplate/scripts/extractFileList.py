import os
import shutil

def main():
    baseFilePath = r"../template/"
    logFile = "LuaLaTeXTemplate.log"
    
    parseFile = baseFilePath + logFile
    outputFile = baseFilePath + logFile.replace('.log', '-FileList.txt')        
    
    print(parseFile)
    print(outputFile)
    
    copyLine = False
    
    with open(parseFile, 'r') as parseFileHandle:
        with open(outputFile, 'w') as outputFileHandle:            
            for lineParse in parseFileHandle:
                # test for string '%%?'
                if '*File List*' in lineParse:
                    copyLine = True
                if ' ***********' in lineParse:
                    copyLine = False
                if copyLine:
                    # write line to output
                    # print(lineParse)                    
                    outputFileHandle.write(lineParse)    


if __name__ == "__main__":
    main()
