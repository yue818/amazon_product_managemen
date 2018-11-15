# -*- coding: utf-8 -*-
from skuapp.table.t_store_marketplan_execution import t_store_marketplan_execution
from skuapp.table.t_store_status import t_store_status
from skuapp.table.t_store_weekly_statistics import t_store_weekly_statistics
from skuapp.table.t_store_summary_of_sales_profit_data import t_store_summary_of_sales_profit_data
from skuapp.table.t_store_configuration_file import t_store_configuration_file
from datetime import datetime
import logging
import csv
from django.contrib import messages


class t_importfile_Admin(object):

    list_display = ('Status','WeeklyStatistics','SalesData','MarketPlan','ConfigurationFile','Submitter','SubTime',)
    list_filter = ['Submitter','SubTime',]

    
    def save_models(self):
        obj = self.new_obj
        request = self.request

        obj.Submitter=request.user.first_name
        obj.SubTime=datetime.now()
        
        obj.save()
        
        logger = logging.getLogger('sourceDns.webdns.views')

        try :
            if obj.Status is not None and str(obj.Status).strip() !='' :
                i = 0
                INSERT_INTO_Status = []
                for row in csv.reader(obj.Status):#obj.Status本身就是16进制字节流，直接reader
                    if i < 1:
                        i = i + 1
                        continue
                    i = i + 1
                    
                    INSERT_INTO_Status.append(t_store_status(DepartmentID = row[1].decode("GBK"),ShopName = row[2].decode("GBK"),Seller = row[3].decode("GBK"),
                                                            StoreStatus = row[4].decode("GBK"),AccountName = row[5].decode("GBK"),AccountNote = row[6].decode("GBK"),
                                                            PaymentSituation = row[7].decode("GBK"),PaymentRemarks = row[8].decode("GBK"),AccountNumber = row[9].decode("GBK"),
                                                            AccountManager = row[10].decode("GBK"),CardNumber = row[11].decode("GBK"),ShopOperationsNote = row[12].decode("GBK"),
                                                            CreateStaffName = self.request.user.first_name,CreateTime = datetime.now()
                                                            ))

                t_store_status.objects.bulk_create(INSERT_INTO_Status)
                
            if obj.WeeklyStatistics is not None and str(obj.WeeklyStatistics).strip() !='' :
                i = 0
                INSERT_INTO_WeeklyStatistics = []
                for row in csv.reader(obj.WeeklyStatistics):
                    if i < 1:
                        i = i + 1
                        continue
                    i = i + 1
                    
                    INSERT_INTO_WeeklyStatistics.append(t_store_weekly_statistics(DepartmentID = row[1].decode("GBK"),ShopName = row[2].decode("GBK"),ShopAccount = row[3].decode("GBK"),
                                                                                 InvoiceTime = row[4].decode("GBK"),PromotionCosts = row[5].decode("GBK"),TrafficCosts = row[6].decode("GBK"),
                                                                                 SpendSubtotal = row[7].decode("GBK"),RefundAmount = row[8].decode("GBK"),OtherFee = row[9].decode("GBK"),
                                                                                 TotalSales = row[10].decode("GBK"),AmountMoney = row[11].decode("GBK"),Remarks = row[12].decode("GBK"),
                                                                                 CreateStaffName = self.request.user.first_name,CreateTime = datetime.now()
                                                                                 ))
                t_store_weekly_statistics.objects.bulk_create(INSERT_INTO_WeeklyStatistics)

            if obj.SalesData is not None and str(obj.SalesData).strip() !='' :
                i = 0
                INSERT_INTO_SalesData = []
                for row in csv.reader(obj.SalesData):
                    if i < 1:
                        i = i + 1
                        continue
                    i = i + 1
                    
                    INSERT_INTO_SalesData.append(t_store_summary_of_sales_profit_data(DepartmentID = row[1].decode("GBK"),ShopName = row[2].decode("GBK"),ShopAccount = row[3].decode("GBK"),
                                                                                     StartTime = row[4].decode("GBK"),EndTime = row[5].decode("GBK"),Seller = row[6].decode("GBK"),
                                                                                     Sales  = row[7].decode("GBK"),PaidProfits = row[8].decode("GBK"),ProfitMargins = row[9].decode("GBK"),
                                                                                     PreviouSales = row[10].decode("GBK"),Increase = row[11].decode("GBK"),GrowthRate = row[12].decode("GBK"),
                                                                                     Remarks = row[13].decode("GBK"),CreateStaffName = self.request.user.first_name,CreateTime = datetime.now()
                                                                                     ))
                    
                t_store_summary_of_sales_profit_data.objects.bulk_create(INSERT_INTO_SalesData)
                    
            if obj.MarketPlan is not None and str(obj.MarketPlan).strip() !='' :
                i = 0
                INSERT_INTO_MarketPlan = []
                for row in csv.reader(obj.MarketPlan):
                    if i < 1:
                        i = i + 1
                        continue
                    i = i + 1
                    
                    INSERT_INTO_MarketPlan.append(t_store_marketplan_execution(DepartmentID = row[1].decode("GBK"),ShopName = row[2].decode("GBK"),ShopAccount = row[3].decode("GBK"),
                                                                              ProductID = row[4].decode("GBK"),ParentSKU = row[5].decode("GBK"),Price = row[6].decode("GBK"),
                                                                              Demand = row[7].decode("GBK"),Quantity = row[8].decode("GBK"),Tracking = row[9].decode("GBK"),
                                                                              Remarks = row[10].decode("GBK"),BuyerAccountLocalmachineinfo = row[11].decode("GBK"),VpnInfo = row[12].decode("GBK"),
                                                                              BuyerAccount = row[13].decode("GBK"),ShopNumber = row[14].decode("GBK"),BrushPerson = row[15].decode("GBK"),
                                                                              BrushTime = row[16].decode("GBK"),CutPerson = row[17].decode("GBK"),CutTime = row[18].decode("GBK"),
                                                                              CreateStaffName = self.request.user.first_name,CreateTime = datetime.now()
                                                                              ))
                    
                t_store_marketplan_execution.objects.bulk_create(INSERT_INTO_MarketPlan)
                    
            if obj.ConfigurationFile is not None and str(obj.ConfigurationFile).strip() !='' :
                i = 0
                
                for row in csv.reader(obj.ConfigurationFile):
                    if i < 1:
                        i = i + 1
                        continue
                    i = i + 1

                    code = (row[2].decode("GBK")).strip().split('-')
                    if len(code) >= 2:
                        ShopName_temp = code[0] + '-' + code[1]
                    else:
                        ShopName_temp = (row[2].decode("GBK")).strip()
                    parems = {'Department':row[1].decode("GBK"),
                              'Seller':row[3].decode("GBK"),
                              'Published':row[4].decode("GBK"),
                              'Operators':row[5].decode("GBK"),
                              'ShopType':row[6].decode("GBK"),
                              'RealName':row[7].decode("GBK"),
                              'Submitter':self.request.user.first_name,
                              'ShopName_temp': ShopName_temp
                            }
                    t_store_configuration_file.objects.update_or_create(ShopName = (row[2].decode("GBK")).strip(),defaults = parems)
                    
        except Exception,ex :
            logger.error('%s============================%s'%(Exception,ex))
            messages.error(request,'%s============================%s'%(Exception,ex))
        #obj.ave()

        
