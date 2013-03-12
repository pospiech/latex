@ECHO OFF
cls

set WORKING_DIRECTORY=%cd%

echo.##########################################
echo.# Creation of Packages
echo.##########################################

cd ..\packages\publish\
call CreatePackages.bat
cd %WORKING_DIRECTORY%

call CopyPackages.bat

echo.##########################################
echo.# doc-code.tex - doc-code-filled.tex
echo.##########################################

..\scripts\insertPrintCode.py

SET TEXFILE=TemplateDocumentation
echo.##########################################
echo.# compiling document:
echo.%TEXFILE%
echo.##########################################

:: -interaction=nonstopmode
pdflatex -shell-escape  %TEXFILE%
makeglossaries %TEXFILE%
biber %TEXFILE%
makeindex %TEXFILE%.ist
pdflatex -shell-escape  %TEXFILE%
pdflatex -shell-escape  %TEXFILE%

echo.##########################################
echo.# deleting Aux Files
echo.##########################################

call DeleteAuxFiles.bat

copy /Y TemplateDocumentation publish

echo.&pause&goto:eof

::--------------------------------------------------------
::-- Function section starts below here
::--------------------------------------------------------
