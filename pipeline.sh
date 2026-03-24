# Automatic bash script to plot the HR diagram using Gaia DR3 data

echo "Downloading data from Gaia DR3"

wget -q -O GaiaDR3.csv "https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?request=doQuery&lang=ADQL&format=csv&query=SELECT+TOP+50000+Source,Plx,Gmag,BPmag,RPmag+FROM+%22I/355/gaiadr3%22+WHERE+Plx%3E5"


echo "Data downloaded..."
echo "Starting to create the data base"

python3 constructor_db.py

echo "Data base created"
echo "Producing analysis and HR diagram plot"

python3 analisis_visual.py
