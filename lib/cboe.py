# -*- coding: utf-8 -*-
"""
toolset working with cboe data

@author: Jev Kuznetsov
Licence: BSD
"""
import datetime
from datetime import datetime, date
import urllib2
from pandas import DataFrame, Index, DateRange
from pandas.core import datetools 
import numpy as np


def monthCode(month):
    """ 
    perform month->code and back conversion
    
    Input: either month nr (int) or month code (str)
    Returns: code or month nr
    
    """
    codes = ('F','G','H','J','K','M','N','Q','U','V','X','Z')
    
    if isinstance(month,int):
        return codes[month-1]
    elif isinstance(month,str):
        return codes.index(month)+1
    else:
        raise ValueError('Function accepts int or str')
    
    
def vixExpiration(year,month):
    """
    expriration date of a VX future
    """
    t = datetime(year,month,1)+datetools.relativedelta(months=1)
    
    
    offset = datetools.Week(weekday=4)
    if t.weekday()<>4:
        t_new = t+3*offset
    else:
        t_new = t+2*offset    
    
    t_exp = t_new-datetools.relativedelta(days=30)
    return t_exp

def getPutCallRatio():
    """ download current Put/Call ratio"""
    urlStr = 'http://www.cboe.com/publish/ScheduledTask/MktData/datahouse/totalpc.csv'

    try:
        lines = urllib2.urlopen(urlStr).readlines()
    except Exception, e:
        s = "Failed to download:\n{0}".format(e);
        print s
       
    headerLine = 2
    
    header = lines[headerLine].strip().split(',')
    
    data =   [[] for i in range(len(header))]
    
    for line in lines[(headerLine+1):]:
        fields = line.rstrip().split(',')
        data[0].append(datetime.strptime(fields[0],'%m/%d/%Y'))
        for i,field  in enumerate(fields[1:]):
            data[i+1].append(float(field))
    
   
    return DataFrame(dict(zip(header[1:],data[1:])), index = Index(data[0]))


def getHistoricData(symbol):
    ''' get historic data from CBOE
        symbol: VIX or VXV
        return dataframe
    '''
    print 'Downloading %s' % symbol
    urls = {'VIX':'http://www.cboe.com/publish/ScheduledTask/MktData/datahouse/vixcurrent.csv', 
            'VXV':'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vxvdailyprices.csv'}
    
    startLine = {'VIX':2,'VXV':3}    
    
    urlStr = urls[symbol]
    
    try:
        lines = urllib2.urlopen(urlStr).readlines()
    except Exception, e:
        s = "Failed to download:\n{0}".format(e);
        print s
        
    header = ['open','high','low','close']   
    dates = []
    data = [[] for i in range(len(header))]
     
     
    for line in lines[startLine[symbol]:]:
        fields = line.rstrip().split(',')
        try:
            dates.append(datetime.strptime( fields[0],'%m/%d/%Y'))
            for i,field in enumerate(fields[1:]):
                data[i].append(float(field))
        except ValueError as e:
            print 'Catched error:' , e
            print 'Line:', line
            
        
    
    
    return DataFrame(dict(zip(header,data)),index=Index(dates)).sort()


#---------------------classes--------------------------------------------
class VixFuture(object):
    """
    Class for easy handling of futures data.
    """    
    
    def __init__(self,year,month):
        self.year = year
        self.month = month
        
    def expirationDate(self):
        return vixExpiration(self.year,self.month)
    
    def daysLeft(self,date):
        """ business days to expiration date """
        r = DateRange(date,self.expirationDate())
        return len(r)
    
    def __repr__(self):
        return 'VX future [%i-%i %s] Exprires: %s' % (self.year,self.month,monthCode(self.month),
                                                        self.expirationDate())
#-------------------test functions---------------------------------------
def testDownload():
    vix = getHistoricData('VIX')
    vxv = getHistoricData('VXV')
    vix.plot()
    vxv.plot()       

def testExpiration():
    for month in xrange(1,13):
        d = vixExpiration(2011,month)
        print d.strftime("%B, %d %Y (%A)")    



if __name__ == '__main__':
    
    #testExpiration()
    v = VixFuture(2011,11)
    print v
    
    print v.daysLeft(datetime(2011,11,10))
        
    