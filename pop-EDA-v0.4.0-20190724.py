"""
Created on Jul. 19, 2019

@author: whyang
"""
# -*- coding: utf-8 -*-
import os
import csv # deal with csv file
import pandas as pd
from cippackage.popEDA import cipFacetGrid # the Analytic package for the data of CIP's population

#######################################################################################
# declare functions                                                                   #
#######################################################################################
###
# remove leading and trailing characters of each value across all cells in dataframe
#
def trim_all_cells(df):
    # trim whitespace from ends of each value across all series in dataframe
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)

###
# set output figure and input data directories
#
pathdir = '.\\figure'  # directory of output folder 
if not os.path.isdir(pathdir): 
    os.mkdir(pathdir)
datadir = '.\\data'  # directory of input data folder 
if not os.path.isdir(datadir): 
    os.mkdir(datadir)

###
# read into the amount of aboriginal peoples' population
#
with open(datadir+'\\'+'population-sum-ETL.csv', 'r', encoding='utf-8', newline='') as csvfile:
    df = pd.read_csv(
            csvfile,
            header = 0,
            usecols = ['日期', '身分', '區域別', '總計',
                       '阿美族', '泰雅族', '排灣族', '布農族', '魯凱族', '卑南族', '鄒族', '賽夏族',
                       '雅美族', '邵族', '噶瑪蘭族', '太魯閣族', '撒奇萊雅族', '賽德克族',
                       '拉阿魯哇族', '卡那卡那富族',
                       '尚未申報'],
            verbose = True,
            skip_blank_lines = True,
            )
    df = trim_all_cells(df) # trim whitespace from each cell in dataframe

    ###
    # transform to array format applied for presenting the figures with profile
    #    
    df1 = pd.DataFrame(columns=['身分', '日期', '區域別', '原住民族', '人口數'])
    dict = {'身分':'', '日期':'', '區域別':'', '原住民族':'', '人口數':0}
    col = {0:'阿美族', 1:'泰雅族', 2:'排灣族', 3:'布農族', 4:'魯凱族', 5:'卑南族', 6:'鄒族', 7:'賽夏族',
           8:'雅美族', 9:'邵族', 10:'噶瑪蘭族', 11:'太魯閣族', 12:'撒奇萊雅族', 13:'賽德克族',
           14:'拉阿魯哇族', 15:'卡那卡那富族',
           16:'尚未申報'}
    base = 0 # the base point for the dataframe of df1 used as the transformed data
    for i in range(0, len(df.index)):
        for j in range(0, 17, 1): # currently, there are 16 tribes and one as 尚未申報
            dict['身分'] = df.at[ i, '身分']
            df1.at[base + j, '身分'] = dict['身分'] # retrieve the field of 身分(不分山地平地)
        
            dict['日期'] = df.at[i, '日期']
            df1.at[base + j, '日期'] = dict['日期'] # retrieve the field of 日期

            dict['區域別'] = df.at[i, '區域別']
            if dict['區域別'] == '桃園縣':
                dict['區域別'] = '桃園市' # to align 桃園縣 with 桃園市 for the convenience of analyzing 
            df1.at[base + j, '區域別'] = dict['區域別'] # retrieve the field of 區域別(縣市)
            
            dict['原住民族'] = col[j]
            df1.at[base + j, '原住民族'] = str(dict['原住民族']) # retrieve the field of 原住民族(tribe's name)
        
            dict['人口數'] = df.at[i, col[j]]
            df1.at[base + j, '人口數'] = dict['人口數'] # retrieve the field of 人口數 (amount of people)
        # adjust base location by the placement
        base += 17 # the placement is 17 (each tribe is flatten to one row, totaly 16 tribes plus 1 undecisive)
 
    print('**** total number of transformed data: ', base)
    
###
# restore the transformed population info. to a specific file
#
df1.to_csv(datadir+'\\'+'population-sum-EDA.csv', index=False, encoding='cp950') # for windows environment (encoding as ANSI format)

###
# prepare the figures in which population distribution is illustrated
# corresponding to the period of date, location area, and tribe
#

# figure1: illustrate the spatial distribution that the people of the specified tribe
grid1 = cipFacetGrid(df1, row='日期', col='原住民族', margin_titles=True,
                 plotkind='line', x='區域別', y='人口數',
                 tribe=['泰雅族', '卑南族', '排灣族', '布農族', '阿美族', '魯凱族'],
                 area=['新北市', '新竹縣', '花蓮縣', '南投縣', '高雄市', '屏東縣', '桃園市'],
                 title='原住民(身分:不分山地平地)在各縣市之分佈狀況',
                 figfile=pathdir+'\\'+'EDA-tribe-area.png')
grid1.plot(rotation=30)

# figure2: illustrate the amount of each tribe in the specified area
grid2 = cipFacetGrid(df1, row='日期', col='區域別', margin_titles=True,
                 plotkind='bar', x='原住民族', y='人口數',
                 tribe=['泰雅族', '卑南族', '排灣族', '布農族', '阿美族', '魯凱族'],
                 area=['新北市', '新竹縣', '花蓮縣', '南投縣', '高雄市', '屏東縣', '桃園市'],
                 title='各縣市之原住民族人口(身分:不分山地平地)分佈狀況',
                 figfile=pathdir+'\\'+'EDA-area-tribe.png')
grid2.plot(rotation=300)
     
#######################################################################################
# end of file                                                                         #
#######################################################################################