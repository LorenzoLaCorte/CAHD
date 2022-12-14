import pandas as pd
import numpy as np
import operator


class AnonymizationCAHD:

    bandwith_dataframe = None # dataframe after RCM
    sensitive_items = None # list all sensibile data
    nome_item = None # dict index --> nome_item
    privacy_level = None # requested privacy level
    alfa = None # checking the alfa * privacy_level transactions
    hists = None # histograms of sensitive items frequency
    sensitive_transactions = None # id of sensitive transactions
    all_sensitive_transactions = None
    sensitive_items_for_transaction = None # list sd for transaction

    dict_group = None 
    anonymized_dataframe = None
    group_list = None
    group_sd = None

    def __init__(self, dataframe=None, privacy_level=4, alfa=3):
        """
            Anonymization through CAHD algorithm
        """
        self.bandwith_dataframe = dataframe.bandwith_dataset.copy()
        self.sensitive_items = dataframe.list_sensitive # columns
        self.nome_item = dataframe.items_final
        self.privacy_level = privacy_level
        self.alfa = alfa

    def compute_hist(self):
        # initialize hist: list of histograms
        self.hists = []
        self.sensitive_items = list(self.sensitive_items)

        for s in self.sensitive_items:
            self.hists.append(int((self.bandwith_dataframe[s].sum()))) # one histogram
        
        

    # extract the same p-1 sensitive items with closest ID to t and unite it to t 
    def constructG(self, t, idx, CL):
        G = {}
        G[idx] = t

        diff = {}
        for i, x in enumerate(CL):
            diff[i] = abs(x-t)
        
        tmp = sorted(diff.items(), key=lambda x:x[1])
        for i in range(self.privacy_level-1):
            tup = tmp[i]
            G[tup[0]] = CL[tup[0]]
        return G
    
    def CAHD_algorithm(self):
        # number of remaining rows
        remaining = len(self.bandwith_dataframe.index)
        i = 0
        while i<len(self.hists) and sum(self.hists):
            if self.hists[i]: 
                starting_idx = max(0, i-self.alfa*self.privacy_level)
                ending_idx = min(len(self.sensitive_items), i+self.alfa*self.privacy_level)
                CL = self.sensitive_items[starting_idx:i] + self.sensitive_items[i+1:ending_idx] 
                G = self.constructG(self.sensitive_items[i], i, CL)
                self.dict_group = G
                self.group_list = list(G.keys())
                self.group_sd = list(G.values())

                hist_copy = self.hists.copy()
                for k, v in G.items():
                    self.hists[k] = v

                rollback = False
                for s in self.hists:
                    if(s * self.privacy_level <= remaining):
                        rollback = True
                
                if(rollback): 
                    self.hists = hist_copy
                else:
                    remaining -= len(G.keys())
            i+=1