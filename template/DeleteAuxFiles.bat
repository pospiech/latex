@ECHO OFF
cls

call:CleanUP

::echo.&pause&goto:eof

::--------------------------------------------------------
::-- Function section starts below here
::--------------------------------------------------------

:: clean up
:CleanUP
del *.mw
del *.bbl
del *.log
del *.ptc
del *.aux
del *.dvi
del *.acn
del *acr
del *alg
del *blg
del *glg
del *gls
del *slg
del *syi
del *blx.bib
del *.glo
del *.idx
del *.ilg
del *.ind
del *.ist
del *.lof
del *.lol
del *.lot
del *.ps
del *.gnuplot
del *.table
del *.xml
del *.syg
del *.toc
del *.bcf
del *.tdo
del *.bak
del *.filelist
del *.gz
del fit.log
del plotdata.txt



