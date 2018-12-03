def split_list(array,no_items=4):
    i=-1
    k=0
    res_list=[]
    for a in array:
        if k%no_items==0:
            res_list.append([])
            i+=1
        res_list[i].append(a)
        k+=1
    return res_list
