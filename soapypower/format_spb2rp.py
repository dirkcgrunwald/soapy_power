#!/usr/bin/env python3
# convert to rtl_power format file from soapy_power_bin format file
# $ python3 soapypower/format_spb2rp.py test_soapy_power_bin.csv converted_rtl_power.csv

import sys, logging, struct, collections, io

import numpy

from soapypower import threadpool
from soapypower import writer

if sys.platform == 'win32':
    import msvcrt

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    #soapypowerbin_file = open(sys.argv[1], mode='rb')
    #rtlpower_file = open(sys.argv[2], mode='w')
    read_check_soapypowerbin_file = open(sys.argv[2], mode='wb')
    #b = writer.BaseWriter()
    s = writer.SoapyPowerBinFormat()
    r = writer.RtlPowerWriter()
    with open(sys.argv[1], mode='rb') as soapypowerbin_file:
        while True:
            c = s.read(soapypowerbin_file)
            if c == None:
                break
            else:
                header = c[0]
                pwr_array = c[1]

            #r.write(psd_data_or_future, time_start, time_start, samples)
            s.write(read_check_soapypowerbin_file, header.time_start, header.time_stop, header.start, header.stop, header.step, header.samples, pwr_array)

    
    read_check_soapypowerbin_file.close()
    #soapypowerbin_file.close()
    #rtlpower_file.close()
