# Copyright (C) 2008 University of Maryland
# All rights reserved.
# See LICENSE.txt for details.
# Author: Christopher Metting

#Starting Date:9/21/2009

from numpy import shape, searchsorted
from .wxrebin import *
from osrefl.model.sample_prep import *
from osrefl.viewers.view import *
from .ginput_rect import ginput_rect


class Data(object):
    '''
    **Overview:**

        This is a data loader for .cg1 files which is converted into a format
        that can be understood by the rest of software infrastructure.

    '''
    def __init__(self,preSpace = None,centerPixel=309.0):

        a = rebinned_data(plot_data = False)

        xindex = [None]*2
        zindex = [None]*2
        
        if preSpace == None:
            a.runConversion(plot_result = False)
            
            qz_for_search = a.qz[0,:]
            qx_for_search = a.qx[:,0]
    
            plot_for_select = view.intensity_plot(
                                          a.qxqz_2d_data.bin_data[:,:,3],
                                          [a.qx[0,0],a.qz[0,0]],
                                          [a.qx[-1,-1],a.qz[-1,-1]],
                                          'Please Select Data:', bar = False)
            
            data = a.qxqz_2d_data.bin_data[:,:,3]
            
            x1,x2,z1,z2 = ginput_rect()
            
            xindex[0] = searchsorted(qx_for_search,x1)
            xindex[1] = searchsorted(qx_for_search,x2)
    
            zindex[0] = searchsorted(qz_for_search,z1)
            zindex[1] = searchsorted(qz_for_search,z2)
    
            self.data = data[xindex[0]:xindex[1],zindex[0]:zindex[1]]
    
            mins = ([qx_for_search[xindex[0]],qx_for_search[xindex[0]],
                     qz_for_search[zindex[0]]])
    
            maxs = ([qx_for_search[xindex[1]],qx_for_search[xindex[1]],
                     qz_for_search[zindex[1]]])
    
            self.space = Q_space(mins,maxs,[shape(self.data)[0],
                                shape(self.data)[0]/3.0,shape(self.data)[1]])
        else:
            
            params = {
              'description': '',
              'x_max': preSpace.maximums[0],
              'x_min': preSpace.minimums[0],
              'x_steps': preSpace.points[0],
              'y_max': preSpace.maximums[2],
              'y_min': preSpace.minimums[2],
              'y_steps': preSpace.points[2],
              'x_units': 'Qx (inv Angstroms)',
              'y_units': 'Qz (inv Angstroms)',
              'qZeroAngle': 0.0,
              'qZeroPixel': centerPixel
              }
            
            a.runConversion(plot_result = False,params_in=params)
            data = a.qxqz_2d_data.bin_data[:,:,3]
            qz_for_search = a.qz[0,:]
            qx_for_search = a.qx[:,0]
            
            xindex[0] = searchsorted(qx_for_search,preSpace.minimums[0])
            xindex[1] = searchsorted(qx_for_search,preSpace.maximums[0],side ='right')

            zindex[0] = searchsorted(qz_for_search,preSpace.minimums[2])
            zindex[1] = searchsorted(qz_for_search,preSpace.maximums[2],side ='right')

            self.data = data[xindex[0]:xindex[1],zindex[0]:zindex[1]]
        return

    def view(self):
        '''
        **Overview:**

            This module plots out the data for viewing.

        '''

        view.intensity_plot(self.data,self.Q.minimums,self.Q.maximums ,
                            header = 'Data')
        return




def _test():
    a = Data()
    print 'You have made it'

if __name__=="__main__":_test()
