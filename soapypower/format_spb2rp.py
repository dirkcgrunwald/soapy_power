#!/usr/bin/env python3
# convert to rtl_power format file from soapy_power_bin format file
# $ python3 soapypower/format_spb2rp.py test_soapy_power_bin.csv converted_rtl_power.csv

import sys, logging, struct, collections, io

import numpy
import datetime

from soapypower import threadpool
from soapypower import writer

if sys.platform == 'win32':
    import msvcrt

logger = logging.getLogger(__name__)

def write_rtl_power(f, time_start, time_stop, start, stop, step, samples, pwr_array):
    """Write soapy_power_bin file of one frequency hop"""
    try:
        row = [
            time_stop.strftime('%Y-%m-%d'), time_stop.strftime('%H:%M:%S'),
            start, stop, step, samples
        ]
        row += list(pwr_array)
        f.write('{}\n'.format(', '.join(str(x) for x in row)))
        f.flush()
    except Exception as e:
        logging.exception('Error writing to output file:')

if __name__ == '__main__':
    s = writer.SoapyPowerBinFormat()
    with open(sys.argv[1], mode='rb') as soapypowerbin_file:
        with open(sys.argv[2], mode='w') as rtlpower_file:
            while True:
                c = s.read(soapypowerbin_file)
                if c == None:    # -> Not magic byte, head of 5 byte. -> If format of sopay_power_bin is correct, it is EOF.
                    break
                else:
                    header = c[0]
                    pwr_array = c[1]
                
                time_start = datetime.datetime.fromtimestamp(header.time_start)
                time_stop = datetime.datetime.fromtimestamp(header.time_stop)
                write_rtl_power(rtlpower_file, time_start, time_stop, header.start, header.stop, header.step, header.samples, pwr_array)
            
        
    
