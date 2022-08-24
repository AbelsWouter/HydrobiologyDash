import numpy as np
import pandas as pd
import plotly.express as px

class Statistics:

    def location():
        return

    def Year():
        return

#Bray Curtis dissimilarity based on ecopy function
    def bray_curtis(bray_data):
        bray = np.zeros((bray_data.shape[0], bray_data.shape[0]))
        for i in range(0, bray.shape[0]):
            bray[i,i] = 0
            for j in range(i+1, bray.shape[0]):
                x1 = bray_data.loc[i,~np.isnan(bray_data.loc[i,:])]
                x2 = bray_data.loc[j,~np.isnan(bray_data.loc[i,:])]
                x1 = x1[~np.isnan(x2)]
                x2 = x2[~np.isnan(x2)]
                bray[i,j] = 1 - ((2 * np.sum(np.minimum(x1, x2)))/(np.sum(x1) + np.sum(x2)))
                bray[j,i] = bray[i,j]
        return bray
    
# Choa similarity
    # Schao1 = Sobs + F1*(F1-1)/2*(F2+1)
    # Where F1 and F2 are the count of singeltons and doubletons,
    # and Sobs is the number of observed species.x
    # d[jk] = (1/S) * sum(log(n[i]/2) - (x[ij]*log(x[ik]) + x[ik]*log(x[ij]))/n[i])

    def chao(chao_data):
        chao = np.zeros((chao_data.shape[0], chao_data.shape[0]))
        for i in range(0, chao.shape[0]):
            chao[i,i] = 0
            for j in range(i+1, chao.shape[0]):
                x1 = chao_data.loc[i,~np.isnan(chao_data.loc[i,:])]
                x2 = chao_data.loc[j,~np.isnan(chao_data.loc[i,:])]
                x1 = x1[~np.isnan(x2)]
                x2 = x2[~np.isnan(x2)]
                chao[i,j] = 1 - ((2 * np.sum(np.minimum(x1, x2)))/(np.sum(x1) + np.sum(x2)))
                chao[j,i] = chao[i,j]
        return chao
    
    def jaccard(jaccard_data):
        return

    def Sorensen(sorensen_data):
        return
    

# Diversity Hill's numbers
