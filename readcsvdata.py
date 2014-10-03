import csv

import numpy as np


class ReadCsvData:
    """
    read in data from a csv file
    
    if column_fields is False, each row is a associated with a field
    eg the first row contains all the headers
    
    each field will create an attribute named after the first value in it
    the rest of the data in the row/column will be stored in a numpy array of 
    floats if possible, else characters
    """
    def __init__(self, csv_file_path, column_fields=True, 
                 name_attributes_with_headers=True, 
                 replace_blanks_with_nans=True):
        ## read in data from csv
        with open(csv_file_path, 'r', newline='') as file:
            rdr = csv.reader(file)
            lines = np.asarray([line for line in rdr])
        if column_fields:
            ## transpose so each row in the array will become an attribute
            row_data = lines.T
        else:
            row_data = lines
        if replace_blanks_with_nans:
            row_data[row_data == ''] = 'nan'
        for ii, r in enumerate(row_data):
            data = r[1:]
            try:
                data = data.astype(float)
            except ValueError:
                pass
            if name_attributes_with_headers:
                ## try to name the attributes after headers
                header = r[0].lower().replace(' ','_')
                try:
                    setattr(self, header, 1)
                    ## check if this is a valid attribute name
                    if eval('self.{} == 1'.format(header)):
                        setattr(self, header, data)
                    else:
                        raise Exception
                except:
                    ## remove invalid attribute and rename generically
                    delattr(self, header)
                    setattr(self, 'field{}'.format(ii+1), data)
            else:
                setattr(self, 'field{}'.format(ii+1), data)
