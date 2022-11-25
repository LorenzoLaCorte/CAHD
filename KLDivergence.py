import itertools


def compute_act_s_in_c(bandwith_dataframe, listQID, valuesQID, sensitiveItem):
    """
    function that computes the pdf of a sensitive data s within a cell C;
    where the cell C is identified from a subset of QID of the dataset

    :param bandwith_dataframe:
    :param listQID:
    :param valuesQID:
    :param sensitiveItem:
    :return: number occurrences of s in C / number occurrences of s in T
    """
    sensitive_item = list()

    if type(sensitiveItem) is int:
        sensitive_item = bandwith_dataframe[bandwith_dataframe[sensitiveItem] == 1].index.tolist()
        number_s_t = len(sensitive_item)
        set_row = set(sensitive_item)
        
        for i in range(0,len(listQID)):
            set_temp = bandwith_dataframe[bandwith_dataframe[listQID[i]] == valuesQID[i]].index.tolist()
            set_temp = set(set_temp)
            set_row = set_row.intersection(set_temp)
        number_s_c = len(set_row)
        if number_s_t > 0:
            return number_s_c/number_s_t
        else:
            return 0
    elif type(sensitiveItem) is list:
        listOccurrences = list()
        for s in sensitiveItem:
            value = compute_act_s_in_c(bandwith_dataframe, listQID, valuesQID, s)
            listOccurrences.append(value)
        return listOccurrences
    else:
        return 0


def compute_est_s_in_c(bandwith_dataframe, sd_groups, list_groups, listQID, valuesQID, sensitiveItem):
    """
    a *b/|G|
    where a is the number of sensitive items inside the group G,
    b is the number of transactions that match QIDs inside the group
    |G| is the size of the group and it is computed with all groups
    that intersect the cell C
    :param bandwith_dataframe:
    :param sd_groups:
    :param list_groups:
    :return:
    """
    value_tot = 0
    for index in range(0, len(list_groups)):
        cardinality_G = len(list_groups[index])
        set_row = set(list_groups[index].index.tolist())
        for i in range(0, len(listQID)):

            set_temp = list_groups[index][list_groups[index][listQID[i]] == valuesQID[i]].index.tolist()
            set_temp = set(set_temp)
            set_row = set_row.intersection(set_temp)

        value_b = len(set_row)
        value_a = sd_groups[index][sensitiveItem]
        value_tot = value_tot + ((value_a * value_b) / cardinality_G)

    sensitive_row = bandwith_dataframe[bandwith_dataframe[sensitiveItem] == 1].index.tolist()
    number_s_t = len(sensitive_row)
    if number_s_t > 0:
        value_tot = value_tot / number_s_t
    else:
        value_tot = 0
    return value_tot


def get_all_combination_of_n(n):
    """
    compute all possible combination of n bit
    :param n: number of QID items
    :return lst: all possibile combination of n value
    """
    lst = [list(i) for i in itertools.product([0, 1], repeat=n)]
    return lst
