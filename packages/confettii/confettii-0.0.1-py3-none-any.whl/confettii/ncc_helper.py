import numpy as np

def norm_data(data):
    """
    normalize data to have mean=0 and standard_deviation=1
    """
    mean_data=np.mean(data)
    std_data=np.std(data, ddof=1)
    #return (data-mean_data)/(std_data*np.sqrt(data.size-1))
    return (data-mean_data)/(std_data)


def ncc(data0, data1):
    """
    normalized cross-correlation coefficient between two data sets

    Parameters
    ----------
    data0, data1 :  numpy arrays of same size
    """
    return (1.0/(data0.size-1)) * np.sum(norm_data(data0)*norm_data(data1))

def get_ncc_point_to_whole(pos,ori_feats):
    """
    calculate the ncc between feature at pos and the other features in feat_list
    return the ncc_map, notice: only accept "square"feature list

    Parameters
    ----------
    pos: the position of the sample point on ori_feats_map
    ori_feats: a feature_list 
    """
    size=int(np.sqrt(len(ori_feats)))
    feats_map=ori_feats.reshape(size,size,-1)
    template=feats_map[pos[0],pos[1]]
    
    ncc_list=[]
    for i in range(feats_map.shape[0]):
        for j in range(feats_map.shape[1]):
            # my_tools.plot([temp])
            temp=feats_map[i,j]
            ncc_list.append(ncc(template,temp))
    ncc_map=np.array(ncc_list)
    ncc_map=ncc_map.reshape(size,size)
    return ncc_map

print(norm_data(np.array([2,4,6])))