# Project 2 - Multi spectral BRDF

## Spectrum Sample
I'm sampling at this wavelengths `400, 445, 475, 510, 570, 590, 650` which
are the 7 colors of the rainbow (violet, indigo, blue, green, yellow, orange
and red).

## Illumination
I'm using sunlight.
It has this values `750, 1234, 1419, 1395, 1338, 1344, 1289`, that I got from
the NASA table https://ntrs.nasa.gov/citations/19810016493. The values given
were very high so I divided every single intensity by the sum of all
(making them relative and then multiplied everything by a scaling factor S
which seem to have good results at S=12 this is in constants.py)

## Metal
I used Chrome from https://refractiveindex.info/ and gave roughness values
of m=0.1, m=0.4 and m=0.8 (six_spheres.py).

## Other spheres
The other 3 spheres are two PVC with roughness of m=0.1 and m=0.3 and a silk
(silkworm) with m=0.05.

## Problems & Solutions
I'm not sure if the colors are right or not, I was expecting the Chrome to
be gray and PVC to be black. Also not sure if it is better to sample at the
7 colors of the rainbow or just sample uniformly dividing the wavelength range.

## Other
I'm using this matrix to go to sRGB:
```python
XYZ_TO_RGB = np.array([
    [3.2404542, -1.5371385, -0.4985314],
    [-0.9692660, 1.8760108, 0.0415560],
    [0.0556434, -0.2040259, 1.0572252]
])
```
- as extra credit I'm also using the extinction coefficient k for the calculations of Chrome
- I also did the extra credit of using only samples at Red, Green and Blue wavelengths

## Result
Rendering takes less than a minute for 600x400px. The top row three spheres are
Chrome with roughness values of m=0.1, m=0.4 and m=0.8 and the bottom row are
PVC with roughness of m=0.1 and m=0.3 and a silk (silkworm) with m=0.05. I used
Ks=0.2 for everything and Kd = 1 - Ks in the
`color = Kd * diffuse + Ks * specular` equation.

![output](output/ks2.jpg)

And this is using Ks = 0.5

![output](output/ks05.jpg)

For only RGB wavelength samples this is the result:

![output](output/rgb.jpg)

I think this is because XYZ has a big portion of the space with green color
