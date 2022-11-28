# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 20:26:38 2022

@author: luizg
"""

import os                                                                       
from multiprocessing import Pool                                                
                                                                                
                                                                                
processos = ('processo1.py')                                    
outros = ('processo2.py',)
                                                  
                                                                                
def roda_processo(processo):                                                             
    os.system('python {}'.format(processo))                                       
                                                                                
                                                                                
pool = Pool(processes=2)                                                        
pool.map(roda_processo, processos) 
pool.map(roda_processo, outros) 