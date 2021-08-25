import pandas as pds
import math

df = pds.read_excel("heart.xlsx", engine='openpyxl')
sample_to_test = df

full_tree = []


def entropy(data_list):
    total_sum = 0
    unique_list = list(set(data_list))
    for data in unique_list:
        total_sum = total_sum - (
                (data_list.count(data) / len(data_list)) * (math.log2(data_list.count(data) / len(data_list))))
    return total_sum


def gainRatio(des_entropy, data_set, values_check, col_c, find_v):
    gain = des_entropy
    splitInfo = 0
    for value in values_check:
        sub_data = data_set[data_set[col_c] == value]
        gain = gain - ((len(sub_data) / len(data_set)) * entropy(list(sub_data[find_v])))
        splitInfo = splitInfo - ((len(sub_data) / len(data_set)) * math.log2(len(sub_data) / len(data_set)))

    # return gain / splitInfo
    if splitInfo != 0:
        return gain / splitInfo
    else:
        return 0


def gainRatio_V(des_entropy, data_set, middleValue, col_c, find_v):
    gain = des_entropy
    splitInfo = 0
    sub_data = data_set[data_set[col_c] > middleValue]
    gain = gain - ((len(sub_data) / len(data_set)) * entropy(list(sub_data[find_v])))
    splitInfo = splitInfo - ((len(sub_data) / len(data_set)) * math.log2(len(sub_data) / len(data_set)))
    sub_data = data_set[data_set[col_c] <= middleValue]
    gain = gain - ((len(sub_data) / len(data_set)) * entropy(list(sub_data[find_v])))
    splitInfo = splitInfo - ((len(sub_data) / len(data_set)) * math.log2(len(sub_data) / len(data_set)))
    # return gain / splitInfo, gain
    if splitInfo != 0:
        return gain / splitInfo, gain
    else:
        return 0, gain


def findBest(des_entropy, data_set, values_check, col_c, find_v):
    values_check.sort()
    bestValue = 0
    bestGainRation = 0
    currenBestMedian = 0
    for i in range(0, len(values_check) - 1):
        eachGain, gain = gainRatio_V(des_entropy, data_set, values_check[i], col_c, find_v)
        # print(col_c,eachGain,gain,values_check[i], " gtt")
        if eachGain >= bestGainRation:
            bestValue = gain
            bestGainRation = eachGain
            currenBestMedian = values_check[i]
    return bestGainRation, currenBestMedian


def colToUse(data, tEntropy, tFind, colList):
    bestTotalGain = -10000000
    bestMedian = 0
    bestCol = ""
    for col in colList:
        to_check = list(set(data[col].values.tolist()))
        if len(to_check) > 5 and (type(to_check[0]) == int or type(to_check[0]) == float):
            total_gain, median = findBest(tEntropy, data, to_check, col, tFind)
        else:
            total_gain = gainRatio(tEntropy, data, to_check, col, tFind)
            median = ''
        if total_gain >= bestTotalGain:
            bestTotalGain = total_gain
            if median or median == 0:
                bestMedian = median
            else:
                bestMedian = ""
            bestCol = col
        # print(col, total_gain, median)

    # print(bestCol, bestMedian, "bhu")

    if bestMedian or bestMedian == 0:
        return bestCol, bestMedian
    else:
        return bestCol, None


def formStructure(filteredData, t_find, c_list, current_tree):
    # print(filteredData,c_list,current_tree, "top")
    total_entropy = entropy(list(filteredData[to_find]))
    bestCol, isMedian = colToUse(filteredData, total_entropy, t_find, c_list)
    # print(lastBest, bestCol, isMedian, c_list)
    if isMedian or isMedian == 0:
        # print(bestCol,c_list, 'ui')
        c_list.remove(bestCol)
        newFilterData = filteredData[filteredData[bestCol] <= isMedian]
        # print(newFilterData, bestCol, isMedian)
        if len(c_list) == 0:
            current_tree[bestCol] = [2, isMedian, "<="]
            t_find_list = newFilterData[t_find].values.tolist()
            # current_tree[t_find] = [max(set(t_find_list), key=t_find_list.count)]
            current_tree[t_find] = [max(set(t_find_list), key=t_find_list.count), t_find_list.count(0),
                                    t_find_list.count(1)]
            # current_tree[t_find] = (set(t_find_list))
            # print(t_find_list.count(0))
            # print(t_find_list.count(1))
            # print(current_tree, c_list, "<p")
            full_tree.append(current_tree.copy())
            current_tree.pop(bestCol)
            current_tree.pop(t_find)
        elif len(set(newFilterData[t_find].values.tolist())) == 1:
            current_tree[bestCol] = [2, isMedian, "<="]
            current_tree[t_find] = list(set(newFilterData[t_find].values.tolist()))
            # print(bestCol, isMedian, set(newFilterData[t_find].values.tolist()))
            # print(current_tree, "<")
            full_tree.append(current_tree.copy())
            current_tree.pop(bestCol)
            current_tree.pop(t_find)
        else:
            current_tree[bestCol] = [2, isMedian, "<="]
            formStructure(newFilterData.copy(), t_find, c_list.copy(), current_tree.copy())
            current_tree.pop(bestCol)

        newFilterData = filteredData[filteredData[bestCol] > isMedian]
        # print(newFilterData, bestCol, isMedian, ">")
        if len(c_list) == 0:
            current_tree[bestCol] = [2, isMedian, ">"]
            t_find_list = newFilterData[t_find].values.tolist()
            # current_tree[t_find] = [max(set(t_find_list), key=t_find_list.count)]
            current_tree[t_find] = [max(set(t_find_list), key=t_find_list.count), t_find_list.count(0),
                                    t_find_list.count(1)]
            # current_tree[t_find] = (set(t_find_list))
            # print(t_find_list.count(0))
            # print(t_find_list.count(1))
            # print(current_tree, c_list, ">p")
            full_tree.append(current_tree.copy())
            current_tree.pop(bestCol)
            current_tree.pop(t_find)
        elif len(set(newFilterData[t_find].values.tolist())) == 1:
            current_tree[bestCol] = [2, isMedian, ">"]
            current_tree[t_find] = list(set(newFilterData[t_find].values.tolist()))
            # print(bestCol, isMedian, ">", set(newFilterData[t_find].values.tolist()))
            # print(current_tree, ">")
            full_tree.append(current_tree.copy())
            current_tree.pop(bestCol)
            current_tree.pop(t_find)
        else:
            current_tree[bestCol] = [2, isMedian, ">"]
            formStructure(newFilterData.copy(), t_find, c_list.copy(), current_tree.copy())
            current_tree.pop(bestCol)

    else:
        # print(bestCol,c_list, 'kl')
        c_list.remove(bestCol)
        colInList = list(set(filteredData[bestCol].values.tolist()))
        for coll in colInList:
            newFilterData = filteredData[filteredData[bestCol] == coll]
            # print(newFilterData, bestCol, coll)
            if len(c_list) == 0:
                current_tree[bestCol] = [1, coll]
                t_find_list = newFilterData[t_find].values.tolist()
                # current_tree[t_find] = [max(set(t_find_list), key=t_find_list.count)]
                current_tree[t_find] = [max(set(t_find_list), key=t_find_list.count), t_find_list.count(0),
                                        t_find_list.count(1)]
                # current_tree[t_find] = (set(t_find_list))
                # print(t_find_list.count(0))
                # print(t_find_list.count(1))
                # print(current_tree, c_list, "=p")
                full_tree.append(current_tree.copy())
                current_tree.pop(bestCol)
                current_tree.pop(t_find)
            elif len(set(newFilterData[t_find].values.tolist())) == 1:
                current_tree[bestCol] = [1, coll]
                current_tree[t_find] = list(set(newFilterData[t_find].values.tolist()))
                # print(bestCol, coll, set(newFilterData[t_find].values.tolist()))
                # print(current_tree, "=")
                full_tree.append(current_tree.copy())
                current_tree.pop(bestCol)
                current_tree.pop(t_find)
            else:
                current_tree[bestCol] = [1, coll]
                formStructure(newFilterData.copy(), t_find, c_list.copy(), current_tree.copy())
                current_tree.pop(bestCol)


col_list = list(df.columns)
# print(col_list)
to_find = col_list[-1]
col_list = col_list[:-1]
sample_data_list = sample_to_test.values.tolist()
formStructure(df, to_find, col_list.copy(), {})
pass_count = 0
fail_count = 0


def predecto(userdata):
    result = 0
    for tree in full_tree:
        done = True
        for att in tree:
            if att == to_find:
                print(tree[att][0])
                result = tree[att][0]
            else:
                if tree[att][0] == 2:
                    if tree[att][2] == '<=':
                        if int(userdata[col_list.index(att)]) > tree[att][1]:
                            done = False
                    elif tree[att][2] == '>':
                        if int(userdata[col_list.index(att)]) <= tree[att][1]:
                            done = False
                elif tree[att][0] == 1:
                    if tree[att][1] != int(userdata[col_list.index(att)]):
                        done = False
            if not done:
                break
        if done:
            break
    return result
