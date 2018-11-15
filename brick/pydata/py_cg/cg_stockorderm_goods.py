# -*- coding: utf-8 -*-
import traceback
import pymssql
import os,sys
import json

class cg_stockorderm_goods(object):
    def __init__(self):
        #self.py_conn = pymssql.connect(host='122.226.216.10', port=18794, user='sa', password='$%^AcB2@9!@#',database='ShopElf', charset='utf8')
        self.py_conn = pymssql.connect(host='122.226.216.10', user='fancyqube', password='K120Esc1',
                                 database='ShopElf',
                                 port='18793')
    def get_goods(self, nid, firstName):
        sql = '''SELECT
                s.Goodscode AS '商品编码',
                s.Goodsname AS '商品名称',
                gs.SKU AS '商品SKU码',
                s.Class AS '规格',
                d.amount AS '采购数量',
                s.Model AS '型号',
                gs.property1 AS '款式1',
                gs.property2 AS '款式2',
                gs.property3 AS '款式3',
                s.Unit AS '单位',
                (
                    SELECT
                        SUM (isnull(id.amount, 0))
                    FROM
                        CG_StockInD (nolock) id
                    INNER JOIN CG_StockInM (nolock) im ON im.NID = id.StockInNID
                    WHERE
                        im.checkflag = 1
                    AND id.GoodsSKUID = d.GoodsSKUID
                    AND im.StockOrder = m.Billnumber
                    AND im.storeid = m.storeid
                ) AS '已入库数量',
                CASE
            WHEN d.amount - isnull(
                (
                    SELECT
                        SUM (isnull(id.amount, 0))
                    FROM
                        CG_StockInD (nolock) id
                    INNER JOIN CG_StockInM (nolock) im ON im.NID = id.StockInNID
                    WHERE
                        im.checkflag = 1
                    AND id.GoodsSKUID = d.GoodsSKUID
                    AND im.StockOrder = m.Billnumber
                    AND im.storeid = m.storeid
                ),
                0
            ) > 0 THEN
                d.amount - isnull(
                    (
                        SELECT
                            SUM (isnull(id.amount, 0))
                        FROM
                            CG_StockInD (nolock) id
                        INNER JOIN CG_StockInM (nolock) im ON im.NID = id.StockInNID
                        WHERE
                            im.checkflag = 1
                        AND id.GoodsSKUID = d.GoodsSKUID
                        AND im.StockOrder = m.Billnumber
                        AND im.storeid = m.storeid
                    ),
                    0
                )
            ELSE
                0
            END AS '未入库数量',
             d.price AS '含税单价',
             d.TaxPrice AS '未含税进价',
             d.money AS '含税金额',
             --税率
            D.TaxRate AS '税额',
             --金额
            D.Remark AS '备注',
             gs.GoodsSKUStatus AS '销售状态',
             isnull(s.PackageCount, 0) '最小包装数',
             (
                SELECT
                    SUM (isnull(id.amount, 0))
                FROM
                    CG_StockInD (nolock) id
                INNER JOIN CG_StockInM (nolock) im ON im.NID = id.StockInNID
                WHERE
                    im.checkflag = 0
                AND id.GoodsSKUID = d.GoodsSKUID
                AND im.StockOrder = m.Billnumber
            ) AS '入库未审',
             isnull(
                (
                    SELECT
                        number - ReservationNum
                    FROM
                        KC_CurrentStock (nolock) k
                    WHERE
                        k.GoodsSKUID = d.GoodsSKUID
                    AND k.storeid = m.storeid
                ),
                0
            ) AS '当前可用数',
             (
                CASE
                WHEN kc.sellcount1 = 0 THEN
                    CAST (gs.SellCount1 AS VARCHAR)
                ELSE
                    CAST (kc.SellCount1 AS VARCHAR)
                END
            ) AS '7天销量',
             (
                CASE
                WHEN kc.sellcount1 = 0 THEN
                    CAST (gs.SellCount2 AS VARCHAR)
                ELSE
                    CAST (kc.SellCount2 AS VARCHAR)
                END
            ) AS '15天销量',
             (
                CASE
                WHEN kc.sellcount1 = 0 THEN
                    CAST (gs.SellCount3 AS VARCHAR)
                ELSE
                    CAST (kc.SellCount3 AS VARCHAR)
                END
            ) AS '30天销量',
             d.SupplierName AS '供应商',
             d.Telphone AS '联系电话',
             d.StockAddress AS '取货地址',
             s.linkurl AS '网址1',
             s.linkurl2 AS '网址2',
             s.linkurl3 AS '网址3',
             s.linkurl4 AS '网址4',
             s.linkurl5 AS '网址5',
             s.linkurl6 AS '网址6',
             isnull(d.MInPrice, 0) AS '最低采购单价',
             (
                SELECT
                    SUM (isnull(id.CheckQty, 0))
                FROM
                    CG_StockInD (nolock) id
                INNER JOIN CG_StockInM (nolock) im ON im.NID = id.StockInNID
                WHERE
                    im.checkflag IN (0, 1)
                AND id.GoodsSKUID = d.GoodsSKUID
                AND im.StockOrder = m.Billnumber
            ) AS '质检数量',
             Bsl.LocationName AS '货位',
             s.BMPFileName AS '图片路径',
             CASE
            WHEN (
                d.amount - isnull(
                    (
                        SELECT
                            SUM (isnull(id.amount, 0))
                        FROM
                            CG_StockInD (nolock) id
                        INNER JOIN CG_StockInM (nolock) im ON im.NID = id.StockInNID
                        WHERE
                            im.checkflag = 1
                        AND id.GoodsSKUID = d.GoodsSKUID
                        AND im.StockOrder = m.Billnumber
                        AND im.storeid = m.storeid
                    ),
                    0
                )
            ) * TaxPrice > 0 THEN
                (
                    d.amount - isnull(
                        (
                            SELECT
                                SUM (isnull(id.amount, 0))
                            FROM
                                CG_StockInD (nolock) id
                            INNER JOIN CG_StockInM (nolock) im ON im.NID = id.StockInNID
                            WHERE
                                im.checkflag = 1
                            AND id.GoodsSKUID = d.GoodsSKUID
                            AND im.StockOrder = m.Billnumber
                            AND im.storeid = m.storeid
                        ),
                        0
                    )
                ) * TaxPrice
            ELSE
                0
            END AS '未入库金额',
             (
                cast(isnull(
                    (
                        SELECT
                            SUM (
                                isnull(id.amount * id.TaxPrice, 0)
                            )
                        FROM
                            CG_StockInD (nolock) id
                        INNER JOIN CG_StockInM (nolock) im ON im.NID = id.StockInNID
                        WHERE
                            im.checkflag = 1
                        AND id.GoodsSKUID = d.GoodsSKUID
                        AND im.StockOrder = m.Billnumber
                    ),
                    0
                ) as numeric(18,4))
            ) AS '已入库金额',
             gs.SkuName AS 'SKU名称',
             s.Style AS '主商品款式',
             '历史已采购数量' = (
                SELECT
                    SUM (IsNull(Amount, 0))
                FROM
                    CG_StockOrderD (nolock) A
                INNER JOIN CG_StockOrderM (nolock) B ON A.StockOrderNid = B.Nid
                WHERE
                    B.CheckFlag = 1
                AND A.GoodsSkuID = d.GoodsSkuID
                GROUP BY
                    GoodsSKUID
            ),
             s.Material AS '材质',
             s.salername AS '业绩归属人1',
             s.salername2 AS '业绩归属人2',
             '物流费分摊前单价' = CONVERT (
                NUMERIC (18, 2),
                BeforeAvgPrice
            ),
             S.barCode AS '采购渠道',
             s.MaxNum AS '库存上限',
             s.MinNum AS '库存下限'
            FROM
                CG_StockOrderD (nolock) d
            INNER JOIN CG_StockOrderM (nolock) M ON m.NID = d.StockOrderNID
            INNER JOIN B_GoodsSKU (nolock) gs ON gs.NID = d.GoodsSKUID
            INNER JOIN B_Goods (nolock) s ON s.NID = gs.GoodsID
            LEFT JOIN B_GoodsSKULocation (nolock) tmpb ON d.GoodsSKUID = tmpb.GoodsSKUID
            AND tmpb.StoreID = M.StoreID
            LEFT JOIN kc_currentstock (nolock) kc ON d.GoodsSKUID = kc.GoodsSKUID
            AND kc.StoreID = M.StoreID
            LEFT JOIN B_Storelocation Bsl ON tmpb.LocationID = Bsl.NID
            WHERE
                m.NID IN (%s)
            AND (
                s.ViewUser = ''
                OR s.ViewUser LIKE '%s,''%s'',%s'
            )
            ORDER BY
                M.nid,
                gs.SKU''' % (nid,'%',firstName,'%')
        result_goods = {}
        try:
            py_cur = self.py_conn.cursor(as_dict=True)
            py_cur.execute(sql)
            
            result_goods = py_cur.fetchall()
            for result_good in result_goods:
                for i,v in result_good.items():
                    print (i + ':' + str(v))
        except Exception, e:
            traceback.print_exc()
        py_cur.close()
        self.py_conn.close()
        
        return result_goods
if __name__ == '__main__':
    req = cg_stockorderm_goods()
    req.get_goods(1124474,"袁永亮")