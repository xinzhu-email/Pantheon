import scanpy as sc
import os

from scpantheon.front_end.data_qt import dir, read_path

data_path = read_path(dir)[1]
filetype = os.path.splitext(data_path)[-1]
if filetype == '.csv':
    adata = sc.read_csv(data_path) 
    print('csv data')
elif filetype == '.h5ad':
    adata = sc.read_h5ad(data_path)
    print('h5ad data')
elif filetype == '': # not tested
    print("read_10x")
    adata = sc.read_10x_mtx(
        data_path,# the directory with the `.mtx` file
        var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
        cache=True)                              # write a cache file for faster subsequent reading
else:
    print("error input")