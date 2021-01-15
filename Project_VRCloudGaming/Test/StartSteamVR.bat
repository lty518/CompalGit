tasklist /FI "IMAGENAME eq steamvr.exe" /FO CSV > search.log
FOR /F %%A IN (search.log) do if %%A == 資訊: goto process_off
:process_on
goto end
:process_off
steam://rungameid/250820
:end

delete search.log