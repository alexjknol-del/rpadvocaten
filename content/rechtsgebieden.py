# -*- coding: utf-8 -*-
from content.rg_1 import DEEL1
from content.rg_2 import DEEL2
from content.rg_3 import DEEL3

RECHTSGEBIEDEN = sorted(DEEL1 + DEEL2 + DEEL3, key=lambda g: g["titel"].lower())
