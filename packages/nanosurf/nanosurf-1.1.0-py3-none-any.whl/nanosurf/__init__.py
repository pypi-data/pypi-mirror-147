"""Package for scripting the Nansurf control software.
Copyright (C) Nanosurf AG - All Rights Reserved (2021)
License - MIT"""

from nanosurf.lib.spm import *

class SPM(Spm):
    def __init__(self, *args, **kwargs):
        super().__init__("SPM.Application", *args, **kwargs)

class USPM(Spm):
    def __init__(self, *args, **kwargs):
        super().__init__("USPM.Application", *args, **kwargs)

class CX(Spm):
    def __init__(self, *args, **kwargs):
        super().__init__("CX.Application", *args, **kwargs)

class C3000(Spm):
    def __init__(self, *args, **kwargs):
        super().__init__("C3000.Application", *args, **kwargs)

class Naio(Spm):
    def __init__(self, *args, **kwargs):
        super().__init__("Naio.Application", *args, **kwargs)

class CoreAFM(Spm):
    def __init__(self, *args, **kwargs):
        super().__init__("CoreAFM.Application", *args, **kwargs)

class Easyscan2(Spm):
    def __init__(self, *args, **kwargs):
        super().__init__("Easyscan2.Application", *args, **kwargs)

class MobileS(Spm):
    def __init__(self, *args, **kwargs):
        super().__init__("MobileS.Application", *args, **kwargs)

class SPM_S(Spm):
    def __init__(self, *args, **kwargs):
        super().__init__("SPM_S.Application", *args, **kwargs)

