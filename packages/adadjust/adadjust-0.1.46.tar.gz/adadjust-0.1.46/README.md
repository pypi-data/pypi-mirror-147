[![doc](https://img.shields.io/badge/-Documentation-blue)](https://advestis.github.io/adadjust)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

#### Status
[![pytests](https://github.com/Advestis/adadjust/actions/workflows/pull-request.yml/badge.svg)](https://github.com/Advestis/adadjust/actions/workflows/pull-request.yml)
[![push-pypi](https://github.com/Advestis/adadjust/actions/workflows/push-pypi.yml/badge.svg)](https://github.com/Advestis/adadjust/actions/workflows/push-pypi.yml)
[![push-doc](https://github.com/Advestis/adadjust/actions/workflows/push-doc.yml/badge.svg)](https://github.com/Advestis/adadjust/actions/workflows/push-doc.yml)

![maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![issues](https://img.shields.io/github/issues/Advestis/adadjust.svg)
![pr](https://img.shields.io/github/issues-pr/Advestis/adadjust.svg)


#### Compatibilities
![ubuntu](https://img.shields.io/badge/Ubuntu-supported--tested-success)
![unix](https://img.shields.io/badge/Other%20Unix-supported--untested-yellow)

![python](https://img.shields.io/pypi/pyversions/adadjust)


##### Contact
[![linkedin](https://img.shields.io/badge/LinkedIn-Advestis-blue)](https://www.linkedin.com/company/advestis/)
[![website](https://img.shields.io/badge/website-Advestis.com-blue)](https://www.advestis.com/)
[![mail](https://img.shields.io/badge/mail-maintainers-blue)](mailto:pythondev@advestis.com)

# AdAdjust

Package allowing to fit any mathematical function to (for now 1-D only) data.


## Installation

```bash
pip install adadjust
```

## Usage

```python
from adadjust import Function
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({"text.usetex": True})  # Needs texlive installed

nsamples = 1000
a = 0.3
b = -10
xstart = 0
xend = 1
noise = 0.01
x = np.linspace(xstart, xend, nsamples)
y = a * x ** 2 + b + np.random.normal(0, noise, nsamples)


def linfunc(xx, p):
    return xx * p[0] + p[1]


def square(xx, p):
    return xx ** 2 * p[0] + p[1]


func = Function(linfunc, "$a \\times p[0] + p[1]$")
func2 = Function(square, "$a^2 \\times p[0] + p[1]$")

params = func.fit(x, y, np.array([0, 0]))[0]
rr = func.compute_rsquared(x, y, params)

params2 = func2.fit(x, y, np.array([0, 0]))[0]
rr2 = func2.compute_rsquared(x, y, params2)

table = Function.make_table(
    [func, func2], [params, params2], [rr, rr2], caption="Linear and Square fit", path_output="table.pdf"
)
table.compile()
Function.plot(x, [func, func2], [params, params2], y=y, rsquared=[rr, rr2])
plt.gcf().savefig("plot.pdf")
```

**NOTE** : to have pretty gaphs, put the line `plt.rcParams.update({"text.usetex": True})` just after you imported adadjust.
This requiers that you have TexLive full installed on your computer.

The result will be :

![Alt text](tests/data/plot.png)
