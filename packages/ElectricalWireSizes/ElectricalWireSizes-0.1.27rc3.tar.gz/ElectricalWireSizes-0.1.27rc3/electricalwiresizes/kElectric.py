from tabulate import tabulate
from .bd import dbConductorCu, dbConductorAl, dbConductorCuStd
from .basicelecfunc import Rn, RnCd, Z, Rcd, dbc, FCT, zpucu, zpual
from .mbtcu import mbtcu
from .mbtal import mbtal
from .mbtcustd import mbtcustd
from .dbcircuit import dbcircuit
from .dbcircuitcd import dbcircuitcd
from .graph import autolabel, graph
from .shortcircuit import icc

import numpy as np
import matplotlib.pyplot as plt
import math
import time


'''
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
| PYEWS, ElectricalWireSizes, 20/04/2022                                 |
| Version : 0.1.27rc3                                                    |
| Autor : Marco Polo Jacome Toss                                         |
| License: GNU Affero General Public License v3 (GPL-3.0)                |
| Requires: Python >=3.5                                                 |
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Changelog:

0.1.27rc3: En esta versión los módulos se han clasificado e independizado
           en distintos archivos además se mejora la salida de datos
           del módulo dbcircuit para funciones futuras.

'''


def version():
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("                                                                          ")
    print("                         ─▄▀─▄▀")
    print("                         ──▀──▀")
    print("                         █▀▀▀▀▀█▄")
    print("                         █░░░░░█─█")
    print("                         ▀▄▄▄▄▄▀▀")
    print("                                                                          ")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("| Python ElectricalWireSizes, 13/04/2022                                 |")
    print("| Version : 0.1.27rc3                                                    |")
    print("| Autor : Marco Polo Jacome Toss                                         |")
    print("| License: GNU Affero General Public License v3 (GPL-3.0)                |")
    print("| Requires: Python >=3.5                                                 |")
    print("| PyPi : https://pypi.org/project/ElectricalWireSizes/                   |")
    print("| Donativos : https://ko-fi.com/jacometoss                               |")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")  

    


