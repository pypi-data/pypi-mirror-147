import math
from random import choice
import pandas as pd
from sty import fg, bg
import os
import numpy as np
from numba import njit


class CMatcher:
    def __init__(self):
        self.searched_color = None
        self.relativeluminence_searched_color = None
        self.sumcolor = None
        self.hsv_searched_color = None
        self.here = os.path.abspath(os.path.dirname(__file__))
        self.df_filename = "colordataframe_CMatcher.pkl"
        self.df_filepath = os.path.join(self.here, self.df_filename)
        if not os.path.exists(self.df_filepath):
            self.create_dataframe()
        self.df = pd.read_pickle(self.df_filepath)
        self.results = []
    @staticmethod
    def get_all_rgb_colors():
        liste = [
            (x, y, z)
            for x in list(range(0, 256, 8))
            for y in list(range(0, 256, 8))
            for z in list(range(0, 256, 8))
        ]
        liste.append((255, 255, 255))
        return liste

    @staticmethod
    @njit
    def rgb_to_hsv(r, g, b):
        r = float(r)
        g = float(g)
        b = float(b)
        high = max(r, g, b)
        low = min(r, g, b)
        h, s, v = high, high, high
        d = high - low
        s = 0 if high == 0 else d / high
        if high == low:
            h = 0.0
        else:
            h = {
                r: (g - b) / d + (6 if g < b else 0),
                g: (b - r) / d + 2,
                b: (r - g) / d + 4,
            }[high]
            h /= 6
        return h, s, v

    def create_dataframe(self):
        x = CMatcher.get_all_rgb_colors()
        df = pd.DataFrame(x)
        df.columns = ["R", "G", "B"]
        df["sum"] = df.R + df.G + df.B
        df["Ri"] = df.R / 255
        df["Gi"] = df.G / 255
        df["Bi"] = df.G / 255
        mask = df.Ri < 0.03928
        df.loc[mask, "Ri"] = df.Ri / 12.92
        mask = df.Gi < 0.03928
        df.loc[mask, "Gi"] = df.Gi / 12.92
        mask = df.Bi < 0.03928
        df.loc[mask, "Bi"] = df.Bi / 12.92
        df.Ri = ((df.Ri + 0.055) / 1.055) ** 2.4
        df.Gi = ((df.Ri + 0.055) / 1.055) ** 2.4
        df.Bi = ((df.Ri + 0.055) / 1.055) ** 2.4
        df["relative_luminance"] = 0.2126 * df.Ri + 0.7152 * df.Gi + 0.0722 * df.Bi
        df["relative_luminance"] = df["relative_luminance"] + 0.05
        applied_df = df.apply(
            lambda x: CMatcher.rgb_to_hsv(x.R, x.G, x.B),
            axis="columns",
            result_type="expand",
        )
        df = pd.concat([df, applied_df], axis="columns")
        df.drop(columns=["Ri", "Gi", "Bi"], inplace=True)
        df.columns = df.columns.to_list()[:-3] + ["H", "S", "V"]
        df["R"] = df["R"].astype(np.uint8)
        df["G"] = df["G"].astype(np.uint8)
        df["B"] = df["B"].astype(np.uint8)
        df.to_pickle(self.df_filepath)

    @staticmethod
    @njit
    def _cor_distance(color1, color2):
        dh = min(abs(color2[0] - color1[0]), 360 - abs(color2[0] - color1[0])) / 180.0
        ds = abs(color2[1] - color1[1])
        dv = abs(color2[2] - color1[2]) / 255.0
        return math.sqrt(dh * dh + ds * ds + dv * dv)

    def get_best_contrast_colors(self, color, lum_dif=80, hsv_dif=80):
        if lum_dif > 99:
            lum_dif = 99
        if hsv_dif > 99:
            hsv_dif = 99
        self.results = []
        searched_color = color
        hsv_searched_color = CMatcher.rgb_to_hsv(
            searched_color[0], searched_color[1], searched_color[2]
        )
        sumcolor = searched_color[0] + searched_color[1] + searched_color[2]
        searched_color0i = searched_color[0] / 255
        if searched_color0i < 0.03928:
            searched_color0i = searched_color0i / 12.92
        searched_color1i = searched_color[1] / 255
        if searched_color1i < 0.03928:
            searched_color1i = searched_color1i / 12.92
        searched_color2i = searched_color[2] / 255
        if searched_color2i < 0.03928:
            searched_color2i = searched_color2i / 12.92
        searched_color0i = ((searched_color0i + 0.055) / 1.055) ** 2.4
        searched_color1i = ((searched_color1i + 0.055) / 1.055) ** 2.4
        searched_color2i = ((searched_color2i + 0.055) / 1.055) ** 2.4
        relativeluminence_searched_color = (
            0.2126 * searched_color0i
            + 0.7152 * searched_color1i
            + 0.0722 * searched_color2i
        )
        relativeluminence_searched_color = relativeluminence_searched_color + 0.05
        self.relativeluminence_searched_color = relativeluminence_searched_color
        self.sumcolor = sumcolor
        self.hsv_searched_color = hsv_searched_color
        self.searched_color = searched_color
        self.df["relativeluminence_searched_color"] = relativeluminence_searched_color
        self.df["final_value"] = 0
        mask2 = self.df["sum"] > sumcolor
        self.df.loc[mask2, "final_value"] = (
            self.df["relative_luminance"] / self.df["relativeluminence_searched_color"]
        )
        self.df.loc[~mask2, "final_value"] = (
            self.df["relativeluminence_searched_color"] / self.df["relative_luminance"]
        )
        df2 = self.df.loc[
            self.df["final_value"] > self.df.final_value.max() * lum_dif / 100
        ].copy()
        df2["color_distance"] = df2.apply(
            lambda x: CMatcher._cor_distance((x.H, x.S, x.V), hsv_searched_color),
            axis=1,
        )
        df3 = df2.loc[
            df2["color_distance"] > df2["color_distance"].max() * hsv_dif / 100
        ]
        r1= df3.R.to_numpy()
        r2=df3.G.to_numpy()
        r3=df3.B.to_numpy()
        self.results = np.dstack(
            (r1, r2, r3)
        ).tolist()[0]
        return self

    def print_results(self):
        foreground = self.searched_color
        if any(self.results):
            for background in self.results:
                bar = (
                    bg(background[0], background[1], background[2])
                    + fg(foreground[0], foreground[1], foreground[2])
                    + "     "
                    + str(foreground)
                    + " - "
                    + str(background)
                    + "     "
                    + fg.rs
                    + bg.rs
                )
                bar2 = (
                    bg(foreground[0], foreground[1], foreground[2])
                    + fg(background[0], background[1], background[2])
                    + "     "
                    + str(background)
                    + " - "
                    + str(foreground)
                    + "     "
                    + fg.rs
                    + bg.rs
                )
                print(bar + bar2)
if __name__ == "__main__":
    cormatcher = CMatcher() #create an instance, first time takes longer because a color dataframe will be created and saved to HDD
    for x in range(100):
        luminancedifference_from_best_result = choice(range(80,99)) #the higher the number, the less results (more contrast), max is 99
        hsv_difference_from_best_result = choice(range(80,99)) #the higher the number, the less results (more contrast), max is 99
        print(f'{x}. Test - Lum: {luminancedifference_from_best_result} - hsv: {hsv_difference_from_best_result}')
        cormatcher.get_best_contrast_colors(
            color=(choice(range(256)), choice(range(256)), choice(range(256))),
            lum_dif=luminancedifference_from_best_result,
            hsv_dif=hsv_difference_from_best_result,
        )
        cormatcher.print_results() #a function to see all results in color
        print(cormatcher.results) #the results are saved in this list
        print('----------------------------------------------------------------------------')