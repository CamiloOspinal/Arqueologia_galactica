# Arqueologia_galactica

## Introduction
This repository was created for the first project of Minería de Datos en Astronomía Course. It consists of building an HR diagram using Gaia DR3 data, selecting the first 50.000 stars with a parallax less than or equal to 5 mas or 200 pc. The goal is to select the Main-Sequence (MS) stars and the Red Giant (RG) stars.

## How were stars selected?
In our sample, we have MS stars, RG stars, Subgiants (SG), White Dwarfs (WD), or binaries, to name a few. A fine description and selection of each group implies a complete analysis beyond our needs, therefore we will use approximations for these regions in the Gaia magnitude and color based on what is available in the literature.

### Mamajek's table
Erik Mamajek, from JPL, has an empirical reference table where collect physical and photometric properties of MS stars. It's a conversion table where you can find spectral types and their magnitudes and colors in different photometric systems. I selected the columns of the Gaia absolute magnitude (Gmag) and BP-RP color to plot the points on the HR diagram to define the "main line" of the MS. Gaia is less sensitive in redder colors, which produces a data dispersion towards late-type stars. Furthermore, red dwarfs are more magnetically active; this chromospheric activity is responsible for increasing the magnitude. Unresolved binaries increase the magnitude, because of our query, which only selected Plx, colors, and magnitude; we are not able to discard possible binaries by considering only stars with RUWE < 1.4. For the above, the main sequence is steeper at bluer colors than redder colors.\
\
Using the distance modulus, I converted the apparent magnitude of the DR3 data to absolute magnitude, which allows us to see Mamajek's data with a basic interpolation with 200 points on the HR diagram. Next, without a physical meaning, I defined a box centered in each point ($(B_P - R_P)_i, G_{mag,i}$) to select stars into $G_{mag, i} - 1 < G_{mag, i} < G_{mag, i} - 1$
