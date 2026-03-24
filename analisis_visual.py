import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy import interpolate as inpol

# Connection with the local data base
conn = sqlite3.connect('datos_mision.db')

# Definint the SQL request
request = "SELECT Gmag, BPmag, RPmag, Plx FROM GaiaDR3_stars;"

Gaia_df = pd.read_sql_query(request, conn)

conn.close()

# Import Mamajek's table
url = "https://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt"

mmjk_df = pd.read_csv(url, skiprows=22, sep=r'\s+', nrows=87, na_values=['...'])

# Discard NaN values
mmjk_df = mmjk_df.dropna(subset=['Bp-Rp'])

# Creating a absoulte magnitude column for Gaia
Gaia_df['d_pc'] = 1000/Gaia_df['Plx'] # mas to pc
Gaia_df['Gmag_abs'] = Gaia_df['Gmag'] - 5*np.log10(Gaia_df['d_pc']) + 5
Gaia_df['Bp-Rp'] = Gaia_df['BPmag'] - Gaia_df['RPmag']

# Interpolation
def interpol(x, y, s = 0, k = 3, n = 100):
	
	spline = inpol.UnivariateSpline(x, y, s = s, k = k)
	# print(len(spline.get_knots())) # If you want to verify the s value
	
	x_grid = np.linspace(x.min()*0.99, y.max()*1.01, n)
	y_grid = spline(x_grid)

	return x_grid, y_grid

# Mamajek's table has a "duplicate" value, we have to "correct" it to use interpol

idx = np.where(mmjk_df['M_G'] == 15.2)[0][1] # duplicate value index
MG_value = mmjk_df['M_G'].iloc[idx]
Mamajek_GM = np.array(mmjk_df['M_G'].copy())
Mamajek_GM[idx] = 1.01*MG_value              # Correction

# Select Gaia color
Mamajek_BpRp = np.array(mmjk_df['Bp-Rp'])
# Select Spectral type
Mamajek_SpT = np.array(mmjk_df['#SpT'])
# Interpolation 
mmjk_BpRp_grid, mmjk_GM_grid = interpol(Mamajek_BpRp[:-2], Mamajek_GM[:-2], n=300) # The last 2 points are decreasing

# Selection or red giants

# Patton conditions
patton_color_mask = Gaia_df['Bp-Rp'] > 0.9
patton_mag_mask = Gaia_df['Gmag_abs'] < 0.3 + 3.4*Gaia_df['Bp-Rp']

# Jao condition
jao_color_mask = Gaia_df['Bp-Rp'] < 1.7 

# Lindegreen condition
lindegreen_mag_mask = Gaia_df['Gmag_abs'] < 6

# Complete mask
giants_mask = patton_color_mask & patton_mag_mask & jao_color_mask & lindegreen_mag_mask

# Final selection
red_giants = Gaia_df[giants_mask]

# Spectral types selection and their Gaia colors
SpT_ticks_mask = np.isin(Mamajek_SpT, ['A0V', 'F0V', 'G0V', 'K0V', 'M0V', 'M5V'])
tick_values = Mamajek_BpRp[SpT_ticks_mask]
tick_labels = Mamajek_SpT[SpT_ticks_mask]

######################################
# FIGURE
#####################################

plt.style.use('dark_background')

fig, axs = plt.subplots(1, 1, figsize=(12, 6), facecolor='#1a1a1a')

axs.invert_yaxis()

axs.scatter(Gaia_df['Bp-Rp'], Gaia_df['Gmag_abs'], s=2, alpha=0.3, c='w')
axs.scatter(mmjk_df['Bp-Rp'], mmjk_df['M_G'],  s=3, zorder=0)
axs.plot(mmjk_BpRp_grid, mmjk_GM_grid, zorder = 3, label = "Mamajek's data fit")

# Red giants
axs.scatter(red_giants['Bp-Rp'], red_giants['Gmag_abs'], s = 2, c = 'r')

# map color
norm = plt.Normalize(Mamajek_BpRp.min(), Mamajek_BpRp.max())
cmap = plt.cm.RdYlBu_r

for i in range(len(mmjk_GM_grid) - 1):
	MS_Gmask = (Gaia_df['Gmag_abs'] > mmjk_GM_grid[i]-1) & (Gaia_df['Gmag_abs'] < mmjk_GM_grid[i+1] + 1)
	MS_BpRpmask = (Gaia_df['Bp-Rp'] > mmjk_BpRp_grid[i] - 0.1) & (Gaia_df['Bp-Rp'] < mmjk_BpRp_grid[i+1] + 0.1)

	MainS_mask = MS_Gmask & MS_BpRpmask

	axs.scatter(Gaia_df['Bp-Rp'][MainS_mask], Gaia_df['Gmag_abs'][MainS_mask], s=2, alpha=1, zorder=2, c=Gaia_df['Bp-Rp'][MainS_mask], cmap=cmap, norm=norm)

axs.text(2.3, 9.5, 'Main Sequence', fontsize=14, rotation = -45)
axs.annotate('Red Giants', (1.7, 2.5), (1.7, 2), c = 'r')

cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=axs)
cb.set_ticks(tick_values)
cb.set_ticklabels(tick_labels)

axs.set_title('Gaia DR3 stars - Plx < 5 mas', fontsize = 20)
axs.set_xlabel('G$_{BP}$ - G$_{RP}$', fontsize = 18)
axs.set_ylabel('G$_{mag}$', fontsize = 18)

axs.set_ylim(15, -2)
axs.set_xlim(-3, 6.5)

plt.legend()

plt.savefig('HRD_GaiaDR3.png', dpi = 300, bbox_inches = 'tight')

plt.show() 
