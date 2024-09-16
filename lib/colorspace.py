import numpy as np

# Color standards and constants

# CIE 1931 RGB -> XYZ


class CIE_1931(object):

    RGB2XYZ = np.array([[0.49000, 0.31000, 0.20000],
                        [0.17697, 0.81240, 0.01063],
                        [0.00000, 0.01000, 0.99000]])

    WHITE = np.array([0.33333333, 0.33333333])
    RED = np.array([0.73466573, 0.26533427])
    GREEN = np.array([0.27375486, 0.71741434])
    BLUE = np.array([0.16657921, 0.00885369])

    CYAN = (BLUE + GREEN) / 2
    MAGENTA = (RED + BLUE) / 2
    YELLOW = (RED + GREEN) / 2

    def __init__(self) -> None:
        pass

    @classmethod
    def rgb2xyz(cls, R: int, G: int, B: int) -> np.ndarray:
        rgbMatrix = np.array([[R],
                              [G],
                              [B]])
        xxyyzzMatrix = cls.RGB2XYZ @ rgbMatrix
        xxyyzzSum = np.sum(xxyyzzMatrix)
        xyz = np.array(xxyyzzMatrix/xxyyzzSum).T.flatten()
        return xyz

    @classmethod
    def dxyzdrgb(cls, R: int, G: int, B: int):
        dxyzdr = (CIE_1931.rgb2xyz(R+1, G, B) - CIE_1931.rgb2xyz(R-1, G, B)) / 2
        dxyzdg = (CIE_1931.rgb2xyz(R, G+1, B) - CIE_1931.rgb2xyz(R, G-1, B)) / 2
        dxyzdb = (CIE_1931.rgb2xyz(R, G, B+1) - CIE_1931.rgb2xyz(R, G, B-1)) / 2
        return np.array([dxyzdr, dxyzdg, dxyzdb])

    @classmethod
    def xy2udvd(cls, x: float, y: float):
        ud = (4 * x) / (-2 * x + 12 * y + 3)
        vd = (6 * y) / (-2 * x + 12 * y + 3)
        return np.array([ud, vd])

    pass


# Display-P3 standard
class DISPLAY_P3(object):

    WHITE = np.array([0.3127, 0.3290])  # DCI-P3 WHITE
    RED = np.array([0.680, 0.320])
    GREEN = np.array([0.265, 0.690])
    BLUE = np.array([0.150, 0.060])

    CYAN = (BLUE + GREEN) / 2
    MAGENTA = (RED + BLUE) / 2
    YELLOW = (RED + GREEN) / 2

    def __init__(self) -> None:
        pass

    pass


# Theater-P3 standard
class THEATER_P3(object):

    WHITE = np.array([0.314, 0.351])  # DCI-P3 WHITE
    RED = np.array([0.680, 0.320])
    GREEN = np.array([0.265, 0.690])
    BLUE = np.array([0.150, 0.060])

    CYAN = (BLUE + GREEN) / 2
    MAGENTA = (RED + BLUE) / 2
    YELLOW = (RED + GREEN) / 2

    def __init__(self) -> None:
        pass

    pass


# Rec.2020 standard
class REC_2020(object):

    WHITE = np.array([0.3127, 0.3290])  # DCI-P3 WHITE
    RED = np.array([0.708, 0.292])
    GREEN = np.array([0.170, 0.797])
    BLUE = np.array([0.131, 0.046])

    CYAN = (BLUE + GREEN) / 2
    MAGENTA = (RED + BLUE) / 2
    YELLOW = (RED + GREEN) / 2

    def __init__(self) -> None:
        pass

    pass


pass
