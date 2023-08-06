# AquaCrop-OSPy
> Crop-water model based on AquaCrop-OS


AquaCrop-OSPy is a python implementation of the popular crop-water model AquaCrop, built from the AquaCrop-OS source code.

AquaCrop-OS, an open source version of FAO’s multi-crop model, was released in August 2016 and is the result of collaboration between researchers at the University of Manchester, Water for Food Global Institute, U.N. Food and Agriculture Organization, and Imperial College London.

AquaCrop-OSPy has been designed in way that users can conduct cutting edge research with only basic python experience. In particular for the design and testing of irrigation stratgeies.

Open access journal article <a href=https://doi.org/10.1016/j.agwat.2021.106976> here </a>

It is built upon the AquaCropOS crop-growth model written in Matlab (<a href=https://doi.org/10.1016/j.agwat.2016.11.015> paper </a>,  <a href=https://www.aquacropos.com/> webpage </a>) which itself itself is based on the FAO AquaCrop model <a href=http://www.fao.org/aquacrop/en/>Webpage </a>. Comparisons to both base models are shown <a href=https://aquacropos.github.io/aquacrop/comparison.html> here. </a>


A <a href=https://forum.aquacroposforum.com/>forum </a> has also been created so that users of AquaCrop-OSPy and AquaCrop-OS can discuss research, bugs and future development. 

There is also an extensive <a href=https://aquacropos.github.io/aquacrop/>documentation </a> for the model

## Install

`pip install aquacrop`

If you encounter this error:

`“ModuleNotFoundError: No module named ‘aquacrop.solution_aot’”`

then you must also run 

`python -m aquacrop.solution` 

after installation to compile the internal aquacrop functions.

## Quickstart

A number of tutorials has been created (more to be added in future) to help users jump straight in and run their first simulation. Run these tutorials instantly on Google Colab:


1.   <a href=https://colab.research.google.com/github/aquacropos/aquacrop/blob/master/docs/notebooks/AquaCrop_OSPy_Notebook_1.ipynb>Running an AquaCrop-OSPy model</a>
2.   <a href=https://colab.research.google.com/github/aquacropos/aquacrop/blob/master/docs/notebooks/AquaCrop_OSPy_Notebook_2.ipynb>Estimation of irrigation water demands</a>
3.   <a href=https://colab.research.google.com/github/aquacropos/aquacrop/blob/master/docs/notebooks/AquaCrop_OSPy_Notebook_3.ipynb>Optimisation of irrigation management strategies</a>
4.  <a href=https://colab.research.google.com/github/aquacropos/aquacrop/blob/master/docs/notebooks/AquaCrop_OSPy_Notebook_4.ipynb>Projection of climate change impacts</a>

