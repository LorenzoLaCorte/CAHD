import Dataframe
import AnonymizationCAHD
import time
import numpy as np
import KLDivergence
import random

if __name__ == "__main__":

    final_dim = 2000
    num_sensitive = 10
    privacy_list = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    KLs = list()
    for privacy_level in privacy_list:
        alpha = 3
        nameFile = "Dataset Paper/dataBMS1_transaction.csv"
        listaItem = "Dataset Paper/list_items_BMS1.txt"
        print("")
        print("Read Dataset")
        df = Dataframe.Dataframe(nameFile)
        start_time = time.time()
        print("")
        print("Computing the band matrix")
        df.compute_band_matrix(
            final_dim=final_dim,
            file_item_name=listaItem,
            sensitive_num=num_sensitive)

        print("")
        cahd = AnonymizationCAHD.AnonymizationCAHD(
            df,
            privacy_level=privacy_level,
            alfa=alpha)

        cahd.compute_hist()
        hist_item = cahd.hists
        print("Executing the anonymization...")
        cahd.CAHD_algorithm()
        end_time = time.time() - start_time
        print("Execution time for privacy %s is %s" %(privacy_level, end_time))
        print("")
    
        r = 4 # number of QID inside the query
        all_item = list(df.items_final.keys())
        columns_item_sensibili = df.list_sensitive.values.tolist()
        bandwith_dataframe = df.bandwith_dataset
        QID = cahd.group_list[0].columns.tolist()


        QID_select = list()
        while len(QID_select) < r:
            temp = random.choice(QID)
            if temp not in QID_select:
                QID_select.append(temp)
        all_value = KLDivergence.get_all_combination_of_n(r)

        # get max value of sensibile data
        item_sensibile = int(max(hist_item.keys(), key=(lambda k: hist_item[k])))
        print(hist_item)
        print(item_sensibile)
        KL_Divergence = 0
        for valori in all_value:
            actsc = KLDivergence.compute_act_s_in_c(bandwith_dataframe, QID_select, valori, item_sensibile)
            estsc = KLDivergence.compute_est_s_in_c(bandwith_dataframe,cahd.group_sd,
                                                    cahd.group_list, QID_select, valori, item_sensibile)
            if actsc > 0 and estsc > 0:
                temp = actsc * np.log(actsc/estsc)
            else:
                temp = 0
            KL_Divergence = KL_Divergence + temp
        KLs.append(KL_Divergence)
        print("p: "+str(privacy_level)+" m: "+str(num_sensitive)+" KL: "+str(KL_Divergence))
    if nameFile == "Dataset Paper/dataBMS2_transaction.csv":
        open_file = "valuesKLD_BMS2_"+str(num_sensitive)+".txt"
    else:
        open_file = "valuesKLD_BMS1_"+str(num_sensitive)+".txt"

    file = open(open_file,"w")
    file.write("num_sensitive " + str(num_sensitive) + "\n")
    file.write("dimension " + str(final_dim) + "\n")

    for index in range(0, len(privacy_list)):
        file.write(str(privacy_list[index]) + " " + str(KLs[index]) + "\n")
    file.close()

