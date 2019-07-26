"""
Created on Jul. 23, 2019

@author: whyang
"""
# -*- coding: utf-8 -*-
import os
import csv # deal with csv file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#######################################################################################
# declare ETL classes for CIP's population data                                       #                              #
#######################################################################################

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
# create the csv file of population summary for the sake of analysis
#
class etlCreateCSV:
    def __init__(self, csvFilePath, date):
        self.csvFilePath = datadir + '\\' + csvFilePath #csvFilePath
        self.date = date
        
    ###
    # parse process for collecting population data
    # 
    def parsePopTab(self):
        with open(self.csvFilePath, 'r', encoding='utf-8', newline='') as csvfile:
            df = pd.read_csv(
                    csvfile,
                    header = 0,
                    usecols = ['身分', '區域別', '性別', '總計',
                               '阿美族', '泰雅族', '排灣族', '布農族', '魯凱族', '卑南族', '鄒族', '賽夏族',
                               '雅美族', '邵族', '噶瑪蘭族', '太魯閣族', '撒奇萊雅族', '賽德克族',
                               '拉阿魯哇族', '卡那卡那富族',
                               '尚未申報'],
                    #verbose = True,
                    skip_blank_lines = True,
            )
            df = trim_all_cells(df) # trim whitespace from each cell in dataframe
            ###
            # 各縣市不分平地山地身分的人口總數(依照原住民族)
            # selecting the accumulated records(rows) in order to the needs of analysis
            # add the 'selected' column as the mark: True and null
            # drop the rows that are marked as 'null' (nan)
            #
            df.loc[(df.身分 == '不分平地山地'), 'selected'] = np.nan # mark all of the rows as null
            df.loc[(df.身分 != '不分平地山地'), 'selected'] = np.nan # mark all of the rows as null
            df.loc[(df.身分 == '不分平地山地') & (df.性別 == '計') & (
                    (df.區域別 == '新北市') | (df.區域別 == '臺北市') | (df.區域別 == '臺中市') |
                    (df.區域別 == '臺南市') | (df.區域別 == '高雄市') | (df.區域別 == '桃園市') | # 桃園縣 promote as 桃園市
                    (df.區域別 == '宜蘭縣') | (df.區域別 == '桃園縣') | (df.區域別 == '新竹縣') |
                    (df.區域別 == '苗栗縣') | (df.區域別 == '彰化縣') | (df.區域別 == '南投縣') |
                    (df.區域別 == '雲林縣') | (df.區域別 == '嘉義縣') | (df.區域別 == '屏東縣') |
                    (df.區域別 == '臺東縣') | (df.區域別 == '花蓮縣') | (df.區域別 == '澎湖縣') |
                    (df.區域別 == '基隆市') | (df.區域別 == '新竹市') | (df.區域別 == '嘉義市') |
                    (df.區域別 == '金門縣') | (df.區域別 == '連江縣') ), 
                    'selected'] = True # 只取各區域的合計資料(row)
            df.loc[(df.區域別 == '總計') | (df.區域別 == '臺灣省') | (df.區域別 == '福建省'), 'selected'] = np.nan # 拿掉總數合計的資料(全國、省)
            df.dropna(subset=['selected'], inplace=True) # conduct dropping of the row that are marked as null
            
            ###
            # show the profile of the gotten data
            #
            # note:
            # 1. You should assign index (for the bar-figure), hence the names of x-axis will be shown.
            # 2. Showing line-graph firstly, then the bar-graph, otherwise the style of x-axis won't be workable.
            #
            df.set_index('區域別', inplace=True, drop=False) # index column is 區域別
            ax = plt.gca() # gca stands for 'get current axis'
            # line-graph
            df.plot.line(y='魯凱族', ax=ax)
            df.plot.line(y='卑南族', ax=ax)
            df.plot.line(y='鄒族', ax=ax)
            df.plot.line(y='賽夏族', ax=ax)
            df.plot.line(y='雅美族', ax=ax)
            df.plot.line(y='邵族', ax=ax)
            df.plot.line(y='噶瑪蘭族', ax=ax)
            df.plot.line(y='太魯閣族', ax=ax)
            df.plot.line(y='撒奇萊雅族', ax=ax)
            df.plot.line(y='賽德克族', ax=ax)
            df.plot.line(y='拉阿魯哇族', ax=ax)
            df.plot.line(y='卡那卡那富族', ax=ax)
            df.plot.line(y='尚未申報', ax=ax)
            # bar-graph
            df.plot.bar(
                    rot=30,
                    y=['阿美族', '泰雅族', '排灣族', '布農族'],
                    ax=ax,
                    figsize=(15, 10),
                    title='原住民族人口統計 (' + self.date + ') '
                    )
            # print out figure to a file 
            figName = pathdir + '\\' + 'ETL-pop sum-' + self.date + '.png'
            plt.savefig(figName) # print out the selected firgure format (PNG)
            # display figure
            plt.show()
            
            ###
            # coming out a csv file which is reformed the population data related to Taiwan's aboriginal peoples
            #
            df.drop(columns=['性別', 'selected'], inplace=True) # skip fields that are not used
            df['日期']=self.date # amend one column named as '日期' and place it to the first column
            cols = df.columns.tolist()
            cols = cols[-1:] + cols[:-1] # re-order the sequence of the whole columns
            df = df[cols] # or df = df.ix[:, cols]
            return df
#
# end of etlCreateCSV
###
        
###
# append the collected population data to the csv file of population summary for the sake of analysis
#
class etlAppendCSV(etlCreateCSV):
    def __init__(self, csvFilePath, date='0000-12-31', encoding='cp950', append=True, populationSum='population-sum-ETL.csv'):
        super().__init__(csvFilePath, date)
        self.append = append # use as switch indicating to create a new populationSum file or append to the existing populationSum file
        self.pupulationSum = datadir + '\\' + populationSum # assign the population summary for collecting cip's population data
        self.encoding = encoding # assign the encoding type for writing csv file (populationSum file)
   
    def etlPopTab(self):
        df = super().parsePopTab()
        if self.append:
            # append rows
            df.to_csv(self.pupulationSum, index=False, encoding=self.encoding, mode='a', header=False, sep=',') # for windows environment (encoding as ANSI format)
        else:
            # create new file and write rows
            df.to_csv(self.pupulationSum, index=False, encoding=self.encoding) # for windows environment (encoding as ANSI format)
#
# end of etlAppendCSV
###

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
           
#######################################################################################
# end of file                                                                         #
#######################################################################################