# coding=utf-8

class url_Stitching():
    def __init__(self,request):
        self.requst = request

    def reStitching_url(self,delParams,replaceParams,addParams):
        postParamsDict = self.requst.GET.copy()
        postStr = '?'
        if postParamsDict:
            if delParams:
                for delParam in delParams:
                    del postParamsDict[delParam]
            if replaceParams:
                for replaceParamKey,replaceParamValue in replaceParams.items():
                    if postParamsDict.has_key(replaceParamKey):
                        del postParamsDict[replaceParamKey]
                        reParam = replaceParamValue.split(',')
                        postParamsDict[reParam[0]] = replaceParams[reParam[1]]
            if addParams:
                for addParamKey,addParamValue in addParams.items():
                    postParamsDict[addParamKey] = addParamValue
            for postParamKey,postParamValue in postParamsDict.items():
                postStr += postParamKey + '=' + postParamValue + '&'
        return postStr[:-1]