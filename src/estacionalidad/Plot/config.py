import os
import matplotlib.pyplot as plt
from matplotlib import font_manager

module_dir = os.path.dirname(os.path.abspath(__file__))

FONT_PATH = os.path.join(
    module_dir, "../fonts/Helvetica-Neue-LT-Std-77-Bold-Condensed_22542.ttf")

font_manager.fontManager.addfont(FONT_PATH)
prop = font_manager.FontProperties(fname=FONT_PATH)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()
