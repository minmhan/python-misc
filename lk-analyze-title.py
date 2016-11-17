# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 20:44:07 2016

@author: minmhan
"""

import sys
import nltk
import csv
from prettytable import PrettyTable

CSV_FILE = sys.argv[1]

transforms = [
    ('Sr.', 'Senior'),
    ('Sr', 'Senior'),
    ('Jr.', 'Junior'),
    ('Jr', 'Junior'),
    ('CEO', 'Chief Executive Officer'),
    ('COO', 'Chief Operating Officer'),
    ('CTO', 'Chief Technology Officer'),
    ('CFO', 'Chief Finance Officer'),
    ('VP', 'Voice President')
]