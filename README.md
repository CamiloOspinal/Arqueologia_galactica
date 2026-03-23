# Arqueologia_galactica

## Introduction
This repository was created for the first project of Minería de Datos en Astronomía Course. It consists of building an HR diagram using Gaia DR3 data, selecting the first 50.000 stars with a parallax less than or equal to 5 mas or 200 pc. The goal is to select the Main-Sequence (MS) stars and the Red Giant (RG) stars.

## How were stars selected?
In our sample, we have MS stars, RG stars, Subgiants (SG), White Dwarfs (WD), or binaries, to name a few. A fine description and selection of each group implies a complete analysis beyond our needs, therefore we will use approximations for these regions in the Gaia magnitude and color based on what is available in the literature. The first step was to remove stars without Gmag, BP-RP or Plx information, which led to a 42968 data set.

### Mamajek's table
Erik Mamajek, from JPL, has an empirical reference table where collect physical and photometric properties of MS stars. It's a conversion table where you can find spectral types and their magnitudes and colors in different photometric systems. I selected the columns of the Gaia absolute magnitude (Gmag) and BP-RP color to plot the points on the HR diagram to define the "main line" of the MS. Gaia is less sensitive in redder colors, which produces a data dispersion towards late-type stars. Furthermore, red dwarfs are more magnetically active; this chromospheric activity is responsible for increasing the magnitude. Unresolved binaries increase the magnitude, because of our query, which only selected Plx, colors, and magnitude; we are not able to discard possible binaries by considering only stars with RUWE < 1.4. For the above, the main sequence is steeper at bluer colors than redder colors.\
\
Using the distance modulus, I converted the apparent magnitude of the DR3 data to absolute magnitude, which allows us to see Mamajek's data with a basic interpolation with 200 points on the HR diagram. Next, without a physical meaning, I defined a box centered in each point $((B_P - R_P)_i, G_{mag,i})$ to select stars into $[G_{mag, i} - 1, G_{mag, i} + 1]$ and $[(B_P - R_P)_i - 0.1, [(B_P - R_P)_i + 0.1] $. Because of Mamajek's data distribution, it results in a really good selection of the MS stars! For more visual information, I added a color map of the spectral types, using Mamajek's table again. You can find this table in https://www.pas.rochester.edu/~emamajek/EEM_dwarf_UBVIJHK_colors_Teff.txt

### Red Giants
It's less obvious to highlight the Red Giant branch. As most of the stars are living in the MS, we have a little cluster of possible RGs, which could be confused with SGs. So, the next selection is, of course, an approximation where I surely selected SGs stars. To do this, I take as a reference [Patton et al. 2024](https://academic.oup.com/mnras/article/528/2/3232/7560562), who defined the RGs as having a de-reddened Gaia BP − RP colour > 0.9 and de-reddened, absolute Gaia G-band magnitude < 0.3 + 3.4 * Gaia colour. Here, I don't take into account the reddening of the interstellar dust, because I assumed that these stars are close enough to ignore this effect. One problem with this definition is that it selects all the stars on a slanted line above the MS, including some possible red dwarfs. To solve this, I only took stars with Gaia color < 1.7, because only a few RGs are redder than this, as [Jao & Feiden (2020)](https://iopscience.iop.org/article/10.3847/1538-3881/aba192/pdf) claimed. Finally, to restrict the Gmag, I selected stars with Gmag < 6, as [Lindegreen et al. 2018](https://www.aanda.org/articles/aa/full_html/2018/08/aa32727-18/aa32727-18.html) mentioned; nevertheless, this condition doesn't make a difference in our set.

## Result
I decided not to remove all stars to show how the entire data is visualized, and to highlight our important stars.

<img width="2811" height="1695" alt="HRD_GaiaDR3" src="https://github.com/user-attachments/assets/f18bc859-9b78-438f-8019-670f69c1d879" />


