@ECHO OFF
cls
SET PERLEXE=C:\texlive\2012\tlpkg\tlperl\bin\perl.exe
SET TEXENGINE=pdflatex
SET TARGETDIR=CTAN
call:funcCreateDir %TARGETDIR%

:: Package: doctools
SET PACKAGE=doctools
SET FOLDER=%TARGETDIR%
call:createPackage %FOLDER% %PACKAGE%

:: Package: templatedemo
SET PACKAGE=templatedemo
SET FOLDER=%TARGETDIR%
call:createPackage %FOLDER% %PACKAGE%
IF EXIST "%FOLDER%\%PACKAGE%\doctools.sty" del "%FOLDER%\%PACKAGE%\doctools.sty"

:: Package: tablestyles
SET PACKAGE=tablestyles
SET FOLDER=%TARGETDIR%
call:createPackage %FOLDER% %PACKAGE%
IF EXIST "%FOLDER%\%PACKAGE%\doctools.sty" del "%FOLDER%\%PACKAGE%\doctools.sty"


:: Package: templatesection
SET PACKAGE=templatesection
SET FOLDER=%TARGETDIR%
call:createPackage %FOLDER% %PACKAGE%
IF EXIST "%FOLDER%\%PACKAGE%\doctools.sty" del "%FOLDER%\%PACKAGE%\doctools.sty"

:: Package: templatetools
SET PACKAGE=templatetools
SET FOLDER=%TARGETDIR%
call:createPackage %FOLDER% %PACKAGE%
IF EXIST "%FOLDER%\%PACKAGE%\doctools.sty" del "%FOLDER%\%PACKAGE%\doctools.sty"

call:CleanUP
echo.&pause&goto:eof



::--------------------------------------------------------
::-- Function section starts below here
::--------------------------------------------------------

:createPackage
	set FOLDER=%~1
	set PACKAGE=%~2
	call:funcCreateDir "%FOLDER%\%PACKAGE%\"
	copy %PACKAGE%.ins "%FOLDER%\%PACKAGE%\"
	%PERLEXE% ExchangeInputByFile.pl %PACKAGE%.dtx "%FOLDER%\%PACKAGE%\%PACKAGE%.dtx"	
	IF EXIST "%FOLDER%\doctools\doctools.sty" copy "%FOLDER%\doctools\doctools.sty" "%FOLDER%\%PACKAGE%"
	REM Compile
	set OLDDIR=%CD%
	cd "%FOLDER%\%PACKAGE%\"
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
	call %TEXENGINE% -shell-escape  %TEXFILE%.ins
	call %TEXENGINE% -shell-escape  %TEXFILE%.dtx
	call makeindex.exe -s gind.ist %TEXFILE%.idx
	call %TEXENGINE% -shell-escape  %TEXFILE%.dtx
	call %TEXENGINE% -shell-escape  %TEXFILE%.dtx
	:: -interaction=nonstopmode
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
@del *.hd
@del *.out
goto:eof


