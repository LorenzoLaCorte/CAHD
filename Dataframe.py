import pandas as pd
import numpy as np
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csr_matrix
import matplotlib.pylab as plt
import scipy.sparse as sps

class Dataframe:

    dataframe = None # original dataset
    bandwith_dataset = None # dataframe after RCM and square
    items_final = None # list of all products
    list_sensitive = None # sensitive products list
    original_band = None
    band_after_rcm = None

    def __init__(self,nome_file=None):
        """
            Constructor of the DataFrame class. It builds the dataframe from a csv file
        """
        self.dataframe = pd.read_csv(nome_file,header=None,index_col=None)

    def compute_band_matrix(self, final_dim = 1000, file_item_name = None, sensitive_num = 1, plot = True):
        """
            Compute band_matrix, random permutation of rows and columns.
            It randomly extracts :sensitive_num sensitive data
        """
        original_dataset = self.dataframe
        if original_dataset is not None and file_item_name is not None and len(original_dataset) >= final_dim and len(original_dataset.columns) >= final_dim:

            file_read = open(file_item_name, "r")
            items = file_read.read().splitlines()
            file_read.close()

            random_column = np.random.permutation(original_dataset.shape[1])[:final_dim]
            random_row = np.random.permutation(original_dataset.shape[0])[:final_dim]
            items_reordered = [items[i] for i in random_column]
            
            df_square = original_dataset.iloc[random_row][random_column];
            #f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
            sensitive_list = df_square.columns[-sensitive_num:]
            #ax1.spy(df_square, marker='.', markersize='1')
            #ax1.show()
            sparse = csr_matrix(df_square)
            order = reverse_cuthill_mckee(sparse)
            items_final = [items_reordered[i] for i in order]
            column_reordered = [df_square.columns[i] for i in order]
            items_final = dict(zip(column_reordered,items_final))
            df_square_band = df_square.iloc[order][column_reordered]
            #ax2.spy(df_square_band, marker='.', markersize='1')
            #ax2.show()
            #if plot:
            #    plt.show()

            # initial bande dataframe
            [i, j] = np.where(df_square == 1)
            bw = max(i-j) + 1
            self.original_band = bw
            print("Bandwidth first RCM", bw)

            [i, j] = np.where(df_square_band == 1)
            bw = max(i-j) + 1
            self.band_after_rcm = bw
            print("Bandwidth after RCM", bw)

            self.bandwith_dataset = df_square_band
            self.items_final = items_final
            self.list_sensitive = sensitive_list

        elif original_dataset is not None and file_item_name is not None and len(original_dataset) >= final_dim:
            #in this case, the dataset is not a square matrix
            #np.random.seed(seed=30)
            random_row = np.random.permutation(original_dataset.shape[0])
            original_dataset = original_dataset.iloc[random_row][:final_dim]
            file_read = open(file_item_name, "r")
            items = file_read.read().splitlines()
            file_read.close()
            original_dataset = original_dataset.reset_index()
            original_dataset.drop('index',axis=1,inplace=True)
            columns = original_dataset.columns
            zero_data_to_add = np.zeros(shape=(len(original_dataset),len(original_dataset)-len(columns)))
            
            columns_to_add = ["temp"+str(x) for x in range(0,len(original_dataset)-len(columns))]
            df_to_add = pd.DataFrame(zero_data_to_add, columns=columns_to_add, index=original_dataset.index,dtype='uint8')
            
            original_dataset = pd.concat([original_dataset, df_to_add], axis=1)
            #np.random.seed(seed=13)
            items = original_dataset.columns

            random_column = np.random.permutation(original_dataset.shape[1])
            random_row = np.random.permutation(original_dataset.shape[0])

            original_dataset.columns = [i for i in range(0,len(original_dataset.columns))]
            items_reordered = [items[i] for i in random_column]

            df_square = original_dataset.iloc[random_row][random_column];
            #f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
            sensitive_list = df_square.columns[-sensitive_num:]
            #ax1.spy(df_square, marker='.', markersize='1')
            #ax1.show()
            sparse = csr_matrix(df_square)
            order = reverse_cuthill_mckee(sparse)
            items_final = [items_reordered[i] for i in order]
            column_reordered = [df_square.columns[i] for i in order]
            
            items_final = dict(zip(column_reordered,items_final))
            df_square_band = df_square.iloc[order][column_reordered]
            
            #ax2.spy(df_square_band, marker='.', markersize='1')
            #ax2.show()
            #if plot:
            #    plt.show()
            [i, j] = np.where(df_square == 1)
            bw = max(i-j) + 1
            self.original_band = bw
            print("Bandwidth first RCM", bw)

            [i, j] = np.where(df_square_band == 1)
            bw = max(i-j) + 1
            self.band_after_rcm = bw
            print("Bandwidth after RCM", bw)

            self.bandwith_dataset = df_square_band
            self.items_final = items_final
            self.list_sensitive = sensitive_list
