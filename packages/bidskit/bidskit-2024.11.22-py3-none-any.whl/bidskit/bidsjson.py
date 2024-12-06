"""
Utility functions for JSON sidecars

MIT License

Copyright (c) 2017-2022 Mike Tyszka

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np
import datetime as dt

from . import io as bio


def acqtime_mins(json_file):
    """
    Extract acquisition time from JSON sidecar of Nifti file
    :param json_file: str, JSON sidecar filename
    :return: acq_time: int, integer datetime
    """

    info = bio.read_json(json_file)

    if 'AcquisitionTime' in info:
        t1 = dt.datetime.strptime(info['AcquisitionTime'], '%H:%M:%S.%f0')
        t0 = dt.datetime(1900, 1, 1)
        t_mins = float((t1 - t0).total_seconds() / 60.0)
    else:
        print(f'* WARNING: AcquisitionTime not found in {json_file} (deidentified?)')
        print(f'* WARNING: Automatic fieldmap binding will not work correctly')
        t_mins = -1

    return t_mins