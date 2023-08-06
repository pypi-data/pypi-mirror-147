import numpy as np
import tensorflow as tf
import torch

def mat2latex(table_data, index_row=None, index_column=None, borders=True, round=50):
    if round < 0: 
      raise ValueError("The decimals to round off to cannot be negative")

    just_converted = False
    
    if tf.is_tensor(table_data):
        table_data = table_data.numpy()
        just_converted = True
    elif torch.is_tensor(table_data):
        table_data = table_data.detach().cpu().numpy()
        just_converted = True
    elif isinstance(table_data,list):
        table_data = np.asarray(table_data)

    if isinstance(table_data, np.ndarray):
      matrix_shape = table_data.shape
      if len(matrix_shape) > 2:
        raise ValueError('bmatrix can at most display two dimensions')

      table_data = np.round(table_data,decimals=round)

      if index_row is not None:
        if len(index_row) != (matrix_shape[1] + (1 if index_column is not None else 0)):
          raise ValueError('Number of elements in the index row must match the number of columns in the matrix.')

      if index_column is not None:
          if len(index_column) != matrix_shape[0]:
            raise ValueError('Number of elements in the index column must match the number of rows in the matrix.')

      lines = str(table_data).replace('[', '').replace(']', '').splitlines()
      rv = "\\"+"begin{tabular}{"
      for l in lines:
        rv += "|c"
      rv += "|}\n"
      
      if index_row is not None:
        rv += ' \hline ' + ' & '.join(index_row) + '\\\\ \n'
      for lineno,l in enumerate(lines):
        if index_row is not None:
          rv += ' \hline ' + index_column[lineno] + ' & ' + ' & '.join(l.split()) + '\\\\ \n' 
        else:
          rv += ' \hline ' + ' & '.join(l.split()) + '\\\\ \n' 
      rv +=  '\hline \end{tabular}'
      print(rv)

    else:
      raise ValueError('the input matrix must be a matrix, numpy array, PyTorch tensor or a TensorFlow tensor')