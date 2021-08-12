# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 20:41:15 2021

@author: Barbf
"""

from ftplib import FTP
import os

G_year = ''
G_month = ''

ftp = FTP('ftp.nodc.noaa.gov')
ftp.login()


def main():
    years = ['1970']
    for year in years:
        getYear(year)

def getYear(year):    
    global G_year
    G_year = year
    yearfolder = 'C:/Users/Barbf/Downloads/cmanwx' + '/' + G_year
    
    if not os.path.isdir( yearfolder ):
        print()
        os.mkdir(yearfolder)

    ftp.cwd('/pub/data.nodc/ndbc/cmanwx' + '/' + G_year)
    ftp.retrlines('NLST' , callback=getMonth )



def getMonth(month):
    print('month:', month)
    global G_month
    G_month = month
    monthfolder = 'C:/Users/Barbf/Downloads/cmanwx' + '/' + G_year + '/' + G_month
    if not os.path.isdir( monthfolder ):
        print('G_year: ', G_year)
        os.mkdir(monthfolder)
    
    ftp.set_pasv(False)

    ftp.cwd('/pub/data.nodc/ndbc/cmanwx' + '/' + G_year + '/' + G_month)
    ftp.retrlines('NLST', callback=grabFile)


def grabFile(filename):
    print('filename:', filename)
    global G_year
    global G_month
    if not filename.endswith('.nc'):
        return
    savefile = filename
    savefolder = 'C:/Users/Barbf/Downloads/cmanwx' + '/' + G_year + '/' + G_month
    
    localfile = open(savefolder + '/' + savefile, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write)
    
    localfile.close()


if __name__ == '__main__':
    main()