#!/bin/bash
time_now=$(date +%Y_%m_%d_%H_%M_%S)
LOG_DIR="~/toronto_climate_data/logs/"
LOGS=${LOG_DIR}/${time_now}.log

# Redirect stdout/stderr to tee to write the log file
exec 1> >( tee "${LOGS}" ) 2>&1

cd ~/toronto_climate_data/inputfiles

for year in {2020..2022}; 
do wget  --content-disposition "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=48549&Year=${year}&Month=2&Day=14&timeframe=1&submit= Download+Data";
done;

return_code=$?
if [ $return_code != 0 ]
then
echo "ERROR in DOWLOADING..."
exit 1
fi

python3 ~/toronto_climate_data/scripts/concat.py
return_code=$?
if [ $return_code != 0 ]
then
echo "ERROR in concatenating downloaded files..."
exit 1
fi	