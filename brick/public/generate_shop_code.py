# coding=utf-8
import random
from random import choice
from random import randint

Letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
Numbers = ['0','1','2','3','4','5','6','7','8','9']
Characters = ['#','$','!','@',':','_','(',')','{','}']

class generate_shop_code(object):
    """生成全平台全店铺的特征码"""

    def random_code(self, type, length):
        """随机生成特征码"""
        # 字母
        if type == 1:
            tempList = Letters
        # 特殊字符
        elif type == 2:
            tempList = Characters
        # 字母+特殊字符
        elif type == 3:
            tempList = Letters + Characters
        # 字母+数字
        elif type == 4:
            tempList = Letters + Numbers
        # 数字+特殊字符
        elif type == 5:
            tempList = Numbers + Characters
        # 字母+数字+特殊字符
        elif type == 6:
            tempList = Letters + Numbers + Characters

        thelist = []
        for a in range(0,3):
            if length == 0:
                break
            resultList = []
            for i in range(length):
                resultList.append(choice(tempList))
            if len(resultList) >= 1 and resultList[0] != '0':
                thelist = resultList
                break
        result = ''.join(thelist)
        return result

    def get_exists_code(self, client, shopname):
        """判断该店铺是否已经有特征码"""
        cur = client.cursor()
        sql = 'select Code,CurrentNum from t_all_plateform_code_shopname where ShopName=\"%s\"; ' % shopname
        cur.execute(sql)
        infos = cur.fetchall()
        cur.close()
        if infos:
            info = infos[0]
        else:
            info = None
        return info
        
    def update_shop_currentnum(self, client, shopname, num, befornum):
        myresult = {}
        cur = client.cursor()
        newnum = befornum
        for i in range(0,3):
            sql = 'update t_all_plateform_code_shopname set CurrentNum = CurrentNum + %d where ShopName= \"%s\" ; '%(num, shopname)
            cur.execute(sql)
            cur.execute("commit;")
            currnum = self.get_exists_code(client, shopname)
            # print currnum,num,newnum
            if currnum[1] == num + newnum:
                myresult['Code'] = 0
                myresult['result'] = currnum
                break
            else:
                myresult['Code'] = 1
                myresult['result'] = []
                newnum = currnum[1]
        cur.close()
        return myresult
        

    def get_max_type(self, client):
        """获取当前表格里最大的类型序号"""
        cur = client.cursor()
        sql = 'select TypeNum from t_all_plateform_code_shopname order by id desc limit 1'
        cur.execute(sql)
        infos = cur.fetchall()
        cur.close()
        if infos:
            return infos[0][0]
        else:
            return 0

    def insert_into_mysql(self, client, TypeNum, Length, ShopName, Code, InitialNum, CurrentNum):
        """插入到店铺SKU特征编码表"""
        cur = client.cursor()
        sql = 'insert into t_all_plateform_code_shopname(TypeNum, `Length`, ShopName, Code, InitialNum, CurrentNum) ' \
              'VALUES (%s,%s,%s,%s,%s,%s)'
        print sql
        params = (TypeNum, Length, ShopName, Code, InitialNum, CurrentNum)
        cur.execute(sql, params)
        cur.execute("commit;")
        #client.commit()
        cur.close()

    def  generate_code(self, client, shopname, num):
        """生成新的特征码"""
        max_type_index = self.get_max_type(client)
        
        if (max_type_index + 1) % 6 == 0:
            TypeNum = 6
        else:
            TypeNum = (max_type_index + 1) % 6
        # 下面4个平台的店铺SKU是字母和数字的拼接，不能有特殊字符
        if shopname.split('-')[0] in ['Ali','Top','CDIS','LZD','UMKA']: #
            TypeNum = random.sample([1,4], 1)[0]
        print '---',TypeNum
        Length = randint(5, 10)
        InitialNum = randint(100, 10000)
        newcode = ''
        while newcode == '' or newcode[0] == '0':
            Code = self.random_code(TypeNum, Length)
            newcode = self.judexist(Code,client)
        self.insert_into_mysql(client, TypeNum, Length, shopname, newcode, InitialNum, InitialNum)
        myresult = self.update_shop_currentnum(client, shopname, num, InitialNum)
        self.insert_used(newcode,client)
        return myresult

        
    def judexist(self,code,client):
        judcur = client.cursor()
        judcur.execute("select count(id) from t_old_used_shopcode where shopcode_used = %s ;",(code,))
        judecou = judcur.fetchone()
        judcur.close()
        if judecou[0] <= 0:
            return code
        else:
            return ''
    
    def insert_used(self,code,client):
        inscur = client.cursor()
        inscur.execute('insert into t_old_used_shopcode(shopcode_used) VALUES (%s) ;', (code,))
        inscur.execute("commit;")
        inscur.close()
    
    def sku(self, client, shopname, num):

        exists_info = self.get_exists_code(client, shopname)
        if exists_info:
            info = self.update_shop_currentnum(client, shopname, num, exists_info[1])
        else:
            info = self.generate_code(client, shopname, num)
        return info


def generate_code_func(client, shopname, num):
    code = generate_shop_code()
    return code.sku(client, shopname, num)
    
    
    
    
    
    