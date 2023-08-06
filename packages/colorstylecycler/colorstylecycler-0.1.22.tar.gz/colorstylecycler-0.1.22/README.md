[![doc](https://img.shields.io/badge/-Documentation-blue)](https://advestis.github.io/colorstylecycler)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

#### Status
[![push-pypi](https://github.com/Advestis/colorstylecycler/actions/workflows/push-pypi.yml/badge.svg)](https://github.com/Advestis/colorstylecycler/actions/workflows/push-pypi.yml)
[![push-doc](https://github.com/Advestis/colorstylecycler/actions/workflows/push-doc.yml/badge.svg)](https://github.com/Advestis/colorstylecycler/actions/workflows/push-doc.yml)

![maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![issues](https://img.shields.io/github/issues/Advestis/colorstylecycler.svg)
![pr](https://img.shields.io/github/issues-pr/Advestis/colorstylecycler.svg)


#### Compatibilities
![ubuntu](https://img.shields.io/badge/Ubuntu-supported--tested-success)
![unix](https://img.shields.io/badge/Other%20Unix-supported--untested-yellow)

![python](https://img.shields.io/pypi/pyversions/colorstylecycler)


##### Contact
[![linkedin](https://img.shields.io/badge/LinkedIn-Advestis-blue)](https://www.linkedin.com/company/advestis/)
[![website](https://img.shields.io/badge/website-Advestis.com-blue)](https://www.advestis.com/)
[![mail](https://img.shields.io/badge/mail-maintainers-blue)](mailto:pythondev@advestis.com)

# Color and Style Cycler

Colors and style cycler

Can cycle through combination of colors and line or marker styles. Colors will be computed from a color gradient,
depending on the number of lines to plot, which is given as an argument at object creation, and the number of
styles. By default, styles are supposed to be linestyles. This can be changed to marker with the 'style' argument.


## Installation

`pip install colorstylecycler`

## Usage

```python

    
# noinspection PyUnresolvedReferences
from matplotlib import pyplot as plt
from colorstylecycler import Cycler
number_of_curves = 15
cy = Cycler(ncurves=number_of_curves)
plt.rc('axes', prop_cycle=cy.cycler)
```
