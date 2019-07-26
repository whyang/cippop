"""
Created on Jul. 15, 2019

@author: whyang
"""
# -*- coding: utf-8 -*-
from cippackage.popETL import etlAppendCSV # the ETL package for the data of CIP's population

###
# read a csv file- the population of Taiwan's aboriginal peoples of Dec. 2011 (100-12)
#
appendcsv = etlAppendCSV(csvFilePath='population-100-12.csv', # constuct the object in which data collection of pupulation are fulfilled 
                         date='2011-12-31', # date corresponding to the csvFilePath
                         encoding='cp950', # assign encoding format for writing csv file in windows environment (encoding as ANSI format)
                         populationSum='population-sum-ETL.csv', # assign the summary file of pupulation for sake of analysis 
                         append=False)
appendcsv.etlPopTab() # conduct ETL process

###
# read a csv file- the population of Taiwan's aboriginal peoples of Dec. 2013 (102-12)
#
appendcsv = etlAppendCSV(csvFilePath='population-102-12.csv', # constuct the object in which data collection of pupulation are fulfilled 
                         date='2013-12-31', # date corresponding to the csvFilePath
                         encoding='cp950', # assign encoding format for writing csv file in windows environment (encoding as ANSI format)
                         populationSum='population-sum-ETL.csv') # assign the summary file of pupulation for sake of analysis 
appendcsv.etlPopTab() # conduct ETL process

###
# read a csv file- the population of Taiwan's aboriginal peoples of Dec. 2014 (103-12)
#
#etlAppendCSV.do(csvFilePath='population-103-12.csv', date='2014/12/31', encoding='cp950')
appendcsv = etlAppendCSV(csvFilePath='population-103-12.csv', # constuct the object in which data collection of pupulation are fulfilled 
                         date='2014-12-31', # date corresponding to the csvFilePath
                         encoding='cp950', # assign encoding format for writing csv file in windows environment (encoding as ANSI format)
                         populationSum='population-sum-ETL.csv') # assign the summary file of pupulation for sake of analysis 
appendcsv.etlPopTab() # conduct ETL process

###
# read a csv file- the population of Taiwan's aboriginal peoples of Dec. 2018 (107-4)
#
#etlAppendCSV.do(csvFilePath='population-107-4.csv', date='2018/04/30', encoding='cp950')
appendcsv = etlAppendCSV(csvFilePath='population-107-4.csv', # constuct the object in which data collection of pupulation are fulfilled 
                         date='2018-12-31', # date corresponding to the csvFilePath
                         encoding='cp950', # assign encoding format for writing csv file in windows environment (encoding as ANSI format)
                         populationSum='population-sum-ETL.csv')# assign the summary file of pupulation for sake of analysis 
appendcsv.etlPopTab()  # conduct ETL process

#######################################################################################
# end of file                                                                         #
#######################################################################################