"""
ERTplot.py

Landon Halloran 29-Nov-2016

Script to read in 2D electrical resistivity tomography (ERT) data 
(i.e., inversion output from RES2DINV) and topography data and plot 
it with much more user control than RES2DINV allows. Data must first be 
exported to .xls/.xlsx format (see example file). 
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

###### User must define these: ######
filein = "example/Resistivity_and_Topography_Data.xlsx"  # where the data is located
ncolours=12 # number of colours for plots
colourscheme='viridis' # for others see https://matplotlib.org/examples/color/colormaps_reference.html
linekeys=['LINE_A','LINE_B'] # labels of tabs of ERT data
topokeys=['LINE_A_TOPO','LINE_B_TOPO'] # labels of tabs of topography data (e.g. from GNSS survey)
#####################################

nsubfigs=np.size(linekeys)

xl_file = pd.ExcelFile(filein)
ERT={}
for j in xl_file.sheet_names:
    ERT[j]=xl_file.parse(j)

allrhos=[]
for i in linekeys:
    rho=ERT[i]['Res'].values
    allrhos.append(rho)
allrhos = np.concatenate(allrhos)
clevels = np.logspace(np.log10(np.min(allrhos)),np.log10(np.max(allrhos)),num=ncolours,base=10)

fig, axes = plt.subplots(nrows=nsubfigs, ncols=1,sharex=False) # turn on sharex to share x!
i=0
for ax in axes.flat:
    keyhere=linekeys[i]
    x=ERT[keyhere]['X']
    z=ERT[keyhere]['Z']
    rho=ERT[keyhere]['Res']
    triang = mpl.tri.Triangulation(x, z)
    mask = mpl.tri.TriAnalyzer(triang).get_flat_tri_mask(.1)
    triang.set_mask(mask)
    topokeyhere=topokeys[i]
    xt=ERT[topokeyhere]['X']
    zt=ERT[topokeyhere]['Z']
    #plt.tricontourf(triang,rho,levels=clevels, cmap=colourscheme)
    #cc=ax.tricontourf(triang,rho,levels=clevels, cmap=colourscheme)
    cc=ax.tricontourf(triang,rho,levels=clevels, norm=mpl.colors.LogNorm(vmin=allrhos.min(), vmax=allrhos.max()), cmap=colourscheme)
    ax.axis('equal') # make axes equal (i.e. 1m x = 1m y)
    topokeyhere=topokeys[i]
    ax.plot(xt,zt,'k')
    i=i+1

fig.text(0.5, 0.04, 'X (m)', ha='center')
fig.text(0.04, 0.5, 'Z (m)', va='center', rotation='vertical')
fig.suptitle('Resistivity ($\Omega\cdot$m)')
clabels=[]
for c in clevels: 
    clabels.append('%d' % c) # label all levels with no-decimal formatting
thecbar=fig.colorbar(cc, ax=axes,ticks=clevels)
thecbar.ax.set_yticklabels(clabels)