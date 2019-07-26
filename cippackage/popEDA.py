"""
Created on Jul. 23, 2019

@author: whyang
"""
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

#######################################################################################
# declare Analytic classes for CIP's population data                                       #                              #
#######################################################################################

###
# create the FacetGrid figure in Seaborn for the sake of analyzing the population profile
#
class cipFacetGrid:
    def __init__(self, df, row='日期', col='原住民族', margin_titles=True, 
                 plotkind='plot', x='區域別', y='人口數', 
                 tribe=['阿美族', '泰雅族', '排灣族', '布農族', '魯凱族', '卑南族', '鄒族', '賽夏族', 
                        '雅美族', '邵族', '噶瑪蘭族', '太魯閣族', '撒奇萊雅族', '賽德克族', 
                        '拉阿魯哇族', '卡那卡那富族', '尚未申報'],
                 area=['新北市', '臺北市', '臺中市', '臺南市', '高雄市',
                       '宜蘭縣', '桃園市', '新竹縣', '苗栗縣', '彰化縣', '南投縣',
                       '雲林縣', '嘉義縣', '屏東縣', '臺東縣', '花蓮縣', '澎湖縣',
                       '基隆市', '新竹市', '嘉義市', '金門縣', '連江縣'],
                 title='原住民(身分:不分山地平地)在各縣市之分佈狀況',
                 figfile='fig-population.png'):
        self.df = df # dataframe 
        self.row = row # the row in the FacetGrid figure
        self.col = col # the column in the FacetGrid figure
        self.margin_titles = margin_titles # indicate to show the row's and column's titles in the FacetGrid figure 
        self.plotkind = plotkind # indicate the grid's figure genre in the FacetGrid 
        self.x = x # the x-axis of the grid figure
        self.y = y # the y-axis of the grid figure
        self.tribe = tribe # indicate the tribes that are observed
        self.area = area # indicate the areas that will be evaluated
        self.title = title # indicate the figure's title
        self.figfile = figfile # indicate the file name stored as the FacetGrid figure
        
    ###
    # conduct the plot process for the collecting population data
    # 
    def plot(self, rotation=270):
        ###
        # prepare the figures in which population distribution is illustrated
        # corresponding to the period of date, location area, and tribe
        #
        
        # shrink down the dataframe in according to the requested tribes and areas
        alltribes = self.tribe[:]
        allareas = self.area[:]
        self.df['selected'] = np.nan # ammend the 'selected' column 
        for tribe in alltribes:
            for area in allareas:
                self.df.loc[(self.df.原住民族 == tribe) & (self.df.區域別 == area), 'selected'] = True
                #self.df.loc[(self.df.區域別 == area), 'selected'] = True # 只取要看的區域的合計資料(row)
                #self.df.loc[(self.df.原住民族 == tribe), 'selected'] = True # 只取要看的原住民族的合計資料(row)
        
        # remove unnecessary data in terms of the rows of data in the dataframe
        self.df.dropna(subset=['selected'], inplace=True) # conduct dropping of the row that are marked as null      
        self.df.drop(columns=['selected'], inplace=True) # remove the "selected' column          
        
        # figure: illustrate the distribution of people among the specified tribe, area and the period of time
        sb.set() # for the sake of compaired explanation, Seaborn is adopted
        
        # indicate to illustrate Chinese characters in each figure
        #sb.set(font=['sans-serif'])
        sb.set_style("darkgrid",{"font.sans-serif":['Microsoft JhengHei']})

        # for the sake of compaired explanation, Seaborn FacetGrid is adopted
        grid = sb.FacetGrid(self.df, row=self.row, col=self.col, margin_titles=self.margin_titles)        
        
        # set the scale of 人口數 shown in figure
        # selected by the default that system trade off the whole data aspects 
        #bins = np.linspace(0, 60000, 20)
        if self.plotkind == 'bar':
            grid.map(plt.bar, self.x, self.y)
        else:
            grid.map(plt.plot, self.x, self.y, color='steelblue', marker='.')
        # roate the notation in x label, which can be read friendly 
        for ax in grid.axes.flat:
            labels = ax.get_xticklabels() # get x labels
            ax.set_xticklabels(labels, rotation=rotation) # set new labels with different angle rotation
        
        grid.fig.subplots_adjust(top=0.92, bottom=0.08)
        grid.fig.suptitle(self.title,  fontsize=18)
        grid.savefig(self.figfile) # print out the selected firgure format
        plt.show() # show this figure
#
# end of cipFacetGrid
###

#######################################################################################
# end of file                                                                         #
#######################################################################################
