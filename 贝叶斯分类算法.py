class NBClassify(object):
    def __init__(self, fillNa=1):
        self.fillNa = 1
        pass
    def train(self, trainSet):
    # 计算每种类别的概率
    # 保存所有tag 的所有种类，及它们出现的频次
        dictTag = {}
        for subTuple in trainSet:
            dictTag[str(subTuple[1])] = 1 if str(subTuple[1]) not in dictTag.keys() else dictTag[str(subTuple[1])] + 1
# 保存每个tag 本身的概率
        tagProbablity = {}
        totalFreq = sum([value for value in dictTag.values()])
        for key, value in dictTag.items():
            tagProbablity[key] = value / totalFreq
        # print(tagProbablity)
        self.tagProbablity = tagProbablity
##############################################################################
        # 计算特征的条件概率
        # 保存特征属性基本信息{特征1:{值1:出现5 次, 值2:出现1 次}, 特征2:{值1:出现1 次, 值2:出现5 次}}
        dictFeaturesBase = {}
        for subTuple in trainSet:
            for key, value in subTuple[0].items():
                if key not in dictFeaturesBase.keys():
                    dictFeaturesBase[key] = {value: 1}
                else:
                    if value not in dictFeaturesBase[key].keys():
                        dictFeaturesBase[key][value] = 1
                    else:
                        dictFeaturesBase[key][value] += 1
# dictFeaturesBase = {
# '职业': {'农夫': 1, '教师': 2, '建筑工人': 2, '护士': 1},
# '症状': {'打喷嚏': 3, '头痛': 3}
# }
        dictFeatures = {}.fromkeys([key for key in dictTag])
        for key in dictFeatures.keys():
            dictFeatures[key] = {}.fromkeys([key for key in dictFeaturesBase])
        for key, value in dictFeatures.items():
            for subkey in value.keys():
                value[subkey] = {}.fromkeys([x for x in dictFeaturesBase[subkey].keys()])

# initialise dictFeatures
        for subTuple in trainSet:
            for key, value in subTuple[0].items():
                dictFeatures[subTuple[1]][key][value] = 1 if dictFeatures[subTuple[1]][key][value] == None else \
                dictFeatures[subTuple[1]][key][value] + 1
# print(dictFeatures)
# 将驯良样本中没有的项目，由None 改为一个非常小的数值，表示其概率极小而并非是零
        for tag, featuresDict in dictFeatures.items():
            for featureName, fetureValueDict in featuresDict.items():
                for featureKey, featureValues in fetureValueDict.items():
                    if featureValues == None:
                        fetureValueDict[featureKey] = 1
# 由特征频率计算特征的条件概率P(feature|tag)
        for tag, featuresDict in dictFeatures.items():
            for featureName, fetureValueDict in featuresDict.items():
                totalCount = sum([x for x in fetureValueDict.values() if x != None])
            for featureKey, featureValues in fetureValueDict.items():
                fetureValueDict[featureKey] = featureValues / totalCount if featureValues != None else None
        self.featuresProbablity = dictFeatures
##############################################################################
    def classify(self, featureDict):
        resultDict = {}
    # 计算每个tag 的条件概率
        for key, value in self.tagProbablity.items():
            iNumList = []
            for f, v in featureDict.items():
                if self.featuresProbablity[key][f][v]:
                    iNumList.append(self.featuresProbablity[key][f][v])
            conditionPr = 1
            for iNum in iNumList:
                conditionPr *= iNum
            resultDict[key] = value * conditionPr
# 对比每个tag 的条件概率的大小
        resultList = sorted(resultDict.items(), key=lambda x: x[1], reverse=True)
        return resultList[0][0]
if __name__ == '__main__':
    trainSet = [
    ({"症状": "打喷嚏", "职业": "护士"}, "感冒 "),
    ({"症状": "打喷嚏", "职业": "农夫"}, "过敏 "),
    ({"症状": "头痛", "职业": "建筑工人"}, "脑震荡"),
    ({"症状": "打喷嚏", "职业": "建筑工人"}, "有人在背后指指点点"),
    ({"症状": "打喷嚏", "职业": "建筑工人"}, "有人在背后指指点点"),
    ({"症状": "打喷嚏", "职业": "建筑工人"}, "有人在背后指指点点"),
    ({"症状": "头痛", "职业": "建筑工人"}, "感冒 "),
    ({"症状": "打喷嚏", "职业": "教师"}, "感冒 "),
    ({"症状": "头痛", "职业": "教师"}, "脑震荡"),
    ]
    monitor = NBClassify()
    # trainSet is something like that [(featureDict, tag), ]
    monitor.train(trainSet)
    # 打喷嚏的建筑工人
    # 请问他患上感冒的概率有多大？
    result = monitor.classify({"症状": "打喷嚏", "职业": "建筑工人"})
    print(result)