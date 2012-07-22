@ECHO OFF
cls

SET TEXENGINE=pdflatex
SET TARGETDIR=CTAN
call:funcCreateDir %TARGETDIR%

:: Package: tablestyles
SET PACKAGE=tablestyles
SET FOLDER=%TARGETDIR%\%PACKAGE%
call:createPackage %FOLDER% %PACKAGE%

:: Package: templatedemo
SET PACKAGE=templatedemo
SET FOLDER=%TARGETDIR%\%PACKAGE%
call:createPackage %FOLDER% %PACKAGE%

:: Package: templatesection
SET PACKAGE=templatesection
SET FOLDER=%TARGETDIR%\%PACKAGE%
call:createPackage %FOLDER% %PACKAGE%

:: Package: templatetools
SET PACKAGE=templatetools
SET FOLDER=%TARGETDIR%\%PACKAGE%
call:createPackage %FOLDER% %PACKAGE%

call:CleanUP

echo.&pause&goto:eof



::--------------------------------------------------------
::-- Function section starts below here
::--------------------------------------------------------

:createPackage
	set FOLDER=%~1
	set PACKAGE=%~2
	call:funcCreateDir %FOLDER%
	copy %PACKAGE%.ins %FOLDER%
	ExchangeInputByFile.pl %PACKAGE%.dtx "%FOLDER%\%PACKAGE%.dtx"
	REM Compile
	set OLDDIR=%CD%
	cd "%FOLDER%"
	call:Compile %PACKAGE%
	REM cleanup
	call:CleanUP
	chdir /d %OLDDIR%
	goto:eof

:funcCreateDir
	echo "creating folder %~1"
	IF NOT EXIST "%~1" md "%~1"
	goto:eof

:Compile	
	SET TEXFILE=%~1
	echo "creating .sty and .pdf file of package %TEXFILE%"
	call %TEXENGINE% -shell-escape -interaction=nonstopmode %TEXFILE%.ins
	call %TEXENGINE% -shell-escape -interaction=nonstopmode %TEXFILE%.dtx
	call %TEXENGINE% -shell-escape -interaction=nonstopmode %TEXFILE%.dtx
	goto:eof

:: clean up
:CleanUP
@del *.aux
@del *.dvi
@del *.acn
@del *acr
@del *alg
@del *blg
@del *glg
@del *gls
@del *slg
@del *syi
@del *blx.bib
@del *.glo
@del *.idx
@del *.ilg
@del *.ind
@del *.ist
@del *.lof
@del *.lol
@del *.lot
@del *.ps
@del *.gnuplot
@del *.table
@del *.xml
@del *.syg
@del *.toc
@del *.bcf
@del democode.tex
@del *.log
@del *.gz
goto:eof


