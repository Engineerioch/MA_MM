

#matplotlib notebook
from cycler import cycler
import numpy as np
import pandas as pd
import pylab as plt
import pickle
import locale
import matplotlib
import latex
import tikzplotlib

#Use desired decimal point. Set via locale package and tell matplotlib later to use the locale settings via axes.formatter.use_locale = True.

lang_identifier = 'german'
try:
    locale.setlocale(locale.LC_NUMERIC, lang_identifier) # or 'english'. Important for axes.formatter
except:
    locale.setlocale(locale.LC_NUMERIC, '')  # Use default system locale setting if selected one is not available
print(locale.getlocale(locale.LC_NUMERIC))



latex_base = {'figure.figsize'   : [6.220, 2.5]    # figure size in inches
                ,'figure.dpi'       : 80      # figure dots per inch
                # Eigenschaften der Achsen
                ,'axes.linewidth'      : 0.5     # edge linewidth
                ,'axes.grid'           : False   # display grid or not
                ,'axes.titlesize'      : 11.0   # fontsize of the axes title
                ,'axes.labelsize'      : 11.0  # fontsize of the x any y labels
  #              ,'axes.prop_cycle'    : (cycler('color',['#EC635C', '#4B81C4','#F49961','grey',  '#8768B4','#B45955','#CB74F4','#6EBB96']))# cycler(linestyle=['solid','dashed','dashdot','dotted',(5,(10,3)),(1,(3,1,2,1,2,1)),(0,(3,5,1,5,1,5)),(0,(5,5))]))  # color cycle for plot lines
                ,'axes.formatter.use_locale': True  # use decimal point or comma depending on locale.setlocale()

                # Eigenschaften der Tick-Marker
                ,'xtick.labelsize'      : 11.0 # fontsize of the tick labels
                ,'ytick.labelsize'      : 11.0 # fontsize of the tick labels
                # Eigenschaften der Linienplots
                ,'lines.linewidth'   : 1.5     # line width in points
     #           ,'lines.linestyle'   : (cycler('linestyle',['solid','dotted']))      # solid line
                ,'lines.marker'      : None    # the default marker
                ,'lines.markeredgewidth'  : 1.5     # the line width around the marker symbol
                # Eigenschaften der Flächen
                ,'patch.linewidth'        : 1.5     # edge width in points
                ,'patch.facecolor'        : '#EC635C'
                ,'patch.edgecolor'        : '#EC635C'
                # Eigenschaften der Legende
                ,'legend.fontsize'      : 11.0
                ,'legend.borderpad'     : 0.5    # border whitespace in fontsize units
                ,'legend.markerscale'   : 1.0    # the relative size of legend markers vs. original
                ,'legend.frameon'       : True   # whether or not to draw a frame around legend
                # Eigenschaften der Schriften
                ,'font.family'         : 'sans-serif'
                ,'font.stretch'        : 'normal'
                ,'font.size'           : 11.0
                ,'font.sans-serif'     : ['Arial', 'Helvetica','sans-serif']
                # Eigenschaften fürs Speichern
                ,'savefig.dpi'         : 600      # figure dots per inch
                ,'savefig.format'      : 'png'      # png, ps, pdf, svg
                , 'figure.autolayout' : True,


                "pgf.texsystem": "pdflatex",
#'text.usetex': True,
#   'pgf.rcfonts': False,

                }

# Create another dictionary from the old one for larger figures.
latex_twothird = latex_base.copy() # You need to use the copy method, otherwise you will alter both dictionaries
latex_twothird['figure.figsize'] = [6.1015, 5.5]


# And one for fullsize figures
latex_fullpage = latex_base.copy()
latex_fullpage['figure.figsize'] = [6.220, 7.87]

# And here is one for Powerpoint presentations with fancy colors. Note that the save-format is also changed from pdf (which is
# vecorized and thus great for use in latex) to png because older version of PowerPoint can not handle pdfs
pp_figure = latex_base.copy()
pp_figure['axes.prop_cycle'] = (cycler('color',['#ff33cc', '#79f169', '#F49961', '#8768B4', '#B45955','#CB74F4','#6EBB96']))  # color cycle for plot lines
pp_figure['figure.figsize'] = [10,5.9]    # figure size in inches
pp_figure['axes.linewidth'] = 1     # edge linewidth
pp_figure['axes.titlesize'] =  18.0   # fontsize of the axes title
pp_figure['axes.labelsize'] = 18.0  # fontsize of the x any y labels
pp_figure['xtick.major.size'] = 6      # major tick size in points
pp_figure['xtick.minor.size'] = 3      # minor tick size in points
pp_figure['xtick.major.width'] = 1    # major tick width in points
pp_figure['xtick.minor.width'] = 1    # minor tick width in points
pp_figure['xtick.labelsize'] = 18.0 # fontsize of the tick labels
pp_figure['ytick.major.size'] = 6      # major tick size in points
pp_figure['ytick.minor.size'] = 3      # minor tick size in points
pp_figure['ytick.major.width'] = 1    # major tick width in points
pp_figure['ytick.minor.width'] = 1    # minor tick width in points
pp_figure['ytick.labelsize'] = 18.0 # fontsize of the tick labels
pp_figure['lines.linewidth'] = 2     # line width in points
pp_figure['lines.markeredgewidth'] = 2     # the line width around the marker symbol
pp_figure['lines.markersize'] = 8            # markersize, in points
pp_figure['patch.linewidth'] = 2.0     # edge width in points
pp_figure['legend.fontsize'] = 18.0
pp_figure['font.size'] = 18.0
pp_figure['font.family'] = 'sans-serif'
pp_figure['savefig.dpi'] = 1500     # figure dots per inch
pp_figure['savefig.format'] = 'pdf'      # png, ps, pdf, svg

