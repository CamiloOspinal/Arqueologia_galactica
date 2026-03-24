import pandas as pd
import sqlite3

# Read GaiaDR3.csv
Gaia_df = pd.read_csv('GaiaDR3.csv')

# Clearing NaN files, it reduces the file to 42968 rows
Gaia_df = Gaia_df.dropna(subset=['BPmag', 'RPmag', 'Gmag', 'Plx'])

# Creating the data base datos_mision.db
conn = sqlite3.connect('datos_mision.db')

# Creating the table
Gaia_df.to_sql('GaiaDR3_stars', conn, if_exists='replace', index=False)

conn.close()

print("GaiaDR3.csv is now a sql table!")
