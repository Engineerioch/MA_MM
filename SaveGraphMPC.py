import matplotlib.pyplot as plt
from plot_results_to_files import latex_base
from plot_results_to_files import  latex_twothird
import tikzplotlib

plt.rcParams.update(latex_base)

import matplotlib.lines as mlines

#time = ["t-2", "t-1", "t", "t+1","t+2","t+3","t+4","t+5","t+6","t+7"]
#futureStoerg = [18.5,18.5,18.5,18.5,19,19,18.5]
#reference_up = [21, 22, 22, 21, 21, 21, 21, 22, 22, 21]
#reference_down = [17, 18, 18, 17,17,17,17, 18, 18, 17]
#imp_stoerg = [18.5, 19]
#current_stoerg = [18.8]
##future_stoerg = [18, 19, 18, 18, 18, 18, 19]
#mes_reg = [17.3, 18.2, 18.1]
#fut_reg = [17.5, 17.2, 17.0, 17.6, 18.1, 18.0, 17.8]
#
#stoerg = imp_stoerg + current_stoerg + futureStoerg
#stoerg_colors = ['y' if i < 2 else 'purple' if i == 2 else 'green' for i in range(len(stoerg))]
#stoerg_labels = ['Implementierte Stellgröße' if i < 2 else 'Aktuelle Stellgröße' if i == 2 else 'Prognostizierte Stellgröße' for i in range(len(stoerg))]
#
#reg = mes_reg + fut_reg
#reg_colors = ['black' if i < 3 else 'orange' for i in range(len(reg))]
#reg_labels = ['Gemessene Regelgröße' if i < 3 else 'Prognostizierte Regelgröße' for i in range(len(reg))]
#
#plt.plot(time, reference_up, drawstyle='steps-post', color='red', label='Referenztrajektorie')
#plt.plot(time, reference_down, drawstyle='steps-post', color='red')
#plt.plot(time[:len(stoerg)], stoerg, color=stoerg_colors[0], label=stoerg_labels[0] ,drawstyle="steps-post")
#for i in range(1, len(stoerg)):
#    plt.plot(time[i:i+2], stoerg[i:i+2], color=stoerg_colors[i],drawstyle="steps-post")
#
#
#plt.plot(time[:len(reg)], reg, color=reg_colors[0], label=reg_labels[0])
#for i in range(1, len(reg)):
#    plt.plot(time[i:i+2], reg[i:i+2], color=reg_colors[i], marker=".")
##plt.ylim(15, 25)
#plt.xlabel('Zeitpunkt')
#plt.ylabel('')
#plt.legend()
#plt.show()

# Daten für den Plot
#time = ["t-2", "t-1", "t", "t+1","t+2","t+3","t+4","t+5","t+6","t+7"]
#
#reference_up = [20, 21, 21, 20, 20, 20, 20, 21, 21, 20]
#reference_down = [17, 18, 18, 17,17,17,17, 18, 18, 17]
#
#imp_stoerg = [18.5, 18.5]
#current_stoerg = [18]
#futureStoerg = [18,18.5,18.5,18.5,18.5,19,18]
#stoerg = imp_stoerg + current_stoerg + futureStoerg
#
#mes_reg = [18.2, 18.4, 18.3]
#fut_reg = [17.7, 17.5, 18, 18.2, 18.15, 18]
#reg = mes_reg + fut_reg
#
## Erstelle einen neuen Plot
#fig, ax = plt.subplots(figsize=(6.22, 4))
#
## Zeichne die Daten für List1 und List2 auf den Plot
#ax.plot(time, reference_up, color='#EC635C', label="Regelungstrajektorie", drawstyle="steps")
#ax.plot(time, reference_down, color='#EC635C', drawstyle="steps")
##'#EC635C', '#4B81C4', '#F49961', '#8768B4', '#B45955
## Zeichne die Daten für List3 auf den Plot, wobei der Graph ab dem dritten Wert gestrichelt ist
#ax.plot(time[:3], stoerg[:3] ,linestyle=":", color='#4B81C4', drawstyle="steps-post")
#ax.plot(time[3:8], stoerg[3:8], color='#4B81C4', drawstyle="steps-post", label="Stellgröße")
#ax.plot(time[2:4], stoerg[2:4], linestyle="--", color="#4B81C4", drawstyle="steps")
#
#ax.plot(time[:3], reg[:3], linestyle=":", color='#F49961', marker=".")
#ax.plot(time[2:8], reg[2:8], color='#F49961', marker=".", label="Regelgröße")
##ax.plot(time[7:], reg[7:], linestyle="--", color='#F49961')
#
## Stelle die Achsenbeschriftungen ein
#ax.set_xlabel("Zeit")
#ax.set_ylabel("Wert")
#ax.axvline(x="t", color='black', linestyle='--')
##ax.text("t+3", 22, "current time", ha='center')
#
#
## Add two horizontal arrows with labels
#ax.annotate("", xy=("t", 19.5), xytext=("t+5", 19.5), arrowprops=dict(arrowstyle="<->", color="black"))
#ax.annotate("", xy=("t", 18.7), xytext=("t+1", 18.7), arrowprops=dict(arrowstyle="<->", color="black"))
#ax.text(4.5, 19.6, "P", ha='center')
#ax.text(2.5, 18.8, "K", ha='center')
#
##ax.annotate("arrow 2", xy=(3.5, 17.7), xytext=(2.5, 17.7),
##            arrowprops=dict(facecolor='black', arrowstyle='<->'), ha='center')
#
#
#
#
#plt.ylim(15, 21.5)
## Füge eine Legende hinzu
#legend1 = ax.legend(loc='lower right')
#legend2 = plt.legend(handles=[plt.Line2D([],[], linestyle='dotted', color='black', label='Gemessen/Implementiert'),
#                              plt.Line2D([],[], linestyle='--', color='black', label='Aktuell'),
#                              plt.Line2D([],[], linestyle='-', color='black', label='Prognostiziert')],
#                    loc='lower left')
#ax.add_artist(legend1)
## Entferne y-Achsenticklabels und -ticks
#ax.set_yticklabels([])
#ax.tick_params(axis='y', length=0, labelleft=False)
#
#plt.xlabel('Zeitpunkt')
#plt.ylabel('')
#
##plt.show()
##plt.legend(loc='lower right')
##plt.show()#
#plt.rcParams.update(latex_base)
##plt.figsize= 6.220, 4
##tikzplotlib.save('D://lma-mma/Repos/MA_MM/Test_base15')
#plt.savefig('D://lma-mma/Arbeit/Plots/Kontrollhorizont')
##plt.show()


###############################Ende#####################################
#################Clustering Beispiel####################################
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.decomposition import PCA, IncrementalPCA

iris = load_iris()
X = iris.data
y = iris.target

n_components = 2
ipca = IncrementalPCA(n_components=n_components, batch_size=10)
X_ipca = ipca.fit_transform(X)

pca = PCA(n_components=n_components)
X_pca = pca.fit_transform(X)

colors = ["navy", "turquoise", "darkorange"]
names= ["Cluster 1", "Cluster 2", "Cluster 3"]


for X_transformed, title in [(X_ipca, "Incremental PCA"), (X_pca, "PCA")]:
    plt.figure(figsize=(6.22, 3))
    for colors, i, name in zip(colors, [0, 1, 2], names):
        plt.scatter(
            X_transformed[y == i, 0],
            X_transformed[y == i, 1],
        #    color=color,
            lw=1,
            label=name,
        )

    if "Incremental" in title:
        err = np.abs(np.abs(X_pca) - np.abs(X_ipca)).mean()
        plt.title(title + " of iris dataset\nMean absolute unsigned error %.6f" % err)
    else:
        pass#plt.title(title + " of iris dataset")
    plt.legend(loc="best", shadow=False, scatterpoints=1)
    plt.axis([-4, 4, -1.5, 1.5])
 #   plt.yticks(np.arange(-1.5,1.5, step=1))

#plt.show()

#tikzplotlib.save('DT_Beispiel.tex')

plt.savefig('DT_Beispiel.svg')
#plt.savefig('DT_Beispiel.pdf')

####################################################Ende################################################################