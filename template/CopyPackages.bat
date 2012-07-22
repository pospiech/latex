@ECHO OFF
cls

SET package=tablestyles
copy ..\packages\publish\CTAN\%package%\%package%.sty .

SET package=templatedemo
copy ..\packages\publish\CTAN\%package%\%package%.sty .

SET package=templatesection
copy ..\packages\publish\CTAN\%package%\%package%.sty .

SET package=templatetools
copy ..\packages\publish\CTAN\%package%\%package%.sty .
