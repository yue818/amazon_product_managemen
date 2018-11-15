#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os, urllib2, hashlib, time, json, base64
import os.path
from pyPdf import PdfFileReader,PdfFileWriter

"""  
 @desc:  
 @author: yewangping  
 @site: 
 @software: PyCharm
 @file: download_trackinfo_pdf.py
 @time: 2018/1/4 9:48
"""
class download_trackinfo_pdf():
    def __init__(self):
        pass

    def calcsign(self, request_data, appKey):
        keyset = sorted(request_data.keys())
        signdata = ''
        for i in range(0, len(keyset)):
            signdata = signdata + keyset[i] + '=' + str(request_data[keyset[i]])
        signdata += 'Key=' + appKey
        m = hashlib.md5()
        m.update(signdata)
        psw = m.hexdigest()
        signature = psw.upper()
        return signature

    def get_each_trackinfo_pdf(self, params):
        url = 'http://120.78.88.110:9090/service/parser'
        timeStamp = int(time.time() * 1000)
        appKey = '6dd8a3d04db5430c9ab1eebe6373b82d'
        appId = '07AADCF1662M1ZH'

        params = {"AppId": appId, "TimeStamp": timeStamp, "RequestName": "getLables",
                  "Content": "{'TrackNumber':['"+params['trackNumber']+"'],'ImageType':'PDF'}"}

        tosignature = {"AppId": appId, "TimeStamp": timeStamp}
        signature = self.calcsign(tosignature, appKey)
        params['Sign'] = signature

        req = urllib2.Request(url=url)
        req.add_header("Content-Type", "application/json")
        print json.dumps(params)
        respons = urllib2.urlopen(req, data=json.dumps(params))
        responsData = respons.read()
        pdfData = eval(responsData)['Data']['Labels'][0]['LableData']
        pdfData = base64.b64decode(pdfData)
        return pdfData


    ######## 使用os模块walk函数，搜索出某目录下的全部pdf文件
    ######################获取同一个文件夹下的所有PDF文件名#######################
    def getFileName(self, filepath):
        file_list = []
        for root,dirs,files in os.walk(filepath):
            for filespath in files:
                # print(os.path.join(root,filespath))
                file_list.append(os.path.join(root,filespath))

        return file_list

    ##########################合并同一个文件夹下所有PDF文件########################
    def MergePDF(self, params):
        output=PdfFileWriter()
        outputPages=0
        pdf_fileName= self.getFileName(params['filepath'])
        if len(pdf_fileName)<1:
            print 'there is not any files'
            return
        for i in range(0, params['fileCount']):
            filename = params['filepath'] + str(i) + '.pdf'
            print '*********************%s************************' % i
            # print 'filename: %s and pdf_fileName: %s' % (filename, pdf_fileName[i])
            # 读取源pdf文件
            input = PdfFileReader(file(filename, "rb"))

            # 如果pdf文件已经加密，必须首先解密才能使用pyPdf
            if input.isEncrypted == True:
                input.decrypt("map")

            # 获得源pdf文件中页面总数
            pageCount = input.getNumPages()
            outputPages += pageCount
            print pageCount

            # 分别将page添加到输出output中
            for iPage in range(0, pageCount):
                output.addPage(input.getPage(iPage))

        print "All Pages Number:"+str(outputPages)
        # 最后写pdf文件
        filePath = params['filepath']+params['outfile']
        outputStream = file(filePath,"wb")
        output.write(outputStream)
        outputStream.close()
        print "finished"