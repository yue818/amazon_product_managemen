# -*- coding: utf-8 -*-

# import os
# import errno
# import base64
# import datetime
# import urllib
# import time
# import urllib
# import httplib
# import json

# try:
#     import xml.etree.cElementTree as ET
# except ImportError:
#     import xml.etree.ElementTree as ET

import sys
import urllib2
from bs4 import BeautifulSoup
from ebayTypes import Pagination, EBayOrder, EBayItemInfo, EBaySummary, Picture  # , Money, EBayUnissuedItem
from requests import Request, Session
from ebay_publish_logger import logger

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

CURRENCIES = {
    'USD': 'US Dollar',
    'CAD': 'Canadian Dollar',
    'GBP': 'British Pound',
    'AUD': 'Australian Dollar',
    'EUR': 'Euro',
    'CHF': 'Swiss Franc',
    'CNY': 'Chinese Renminbi',
    'HKD': 'Hong Kong Dollar',
    'PHP': 'Philippines Peso',
    'PLN': 'Polish Zloty',
    'SEK': 'Sweden Krona',
    'SGD': 'Singapore Dollar',
    'TWD': 'Taiwanese Dollar',
    'INR': 'Indian Rupee',
    'MYR': 'Malaysian Ringgit'
}

ORDERSTATUS = {
    "Active": "This value indicates that the cart is active. The 'Active' state is the only order state in which order line items can still be added, removed, or updated in the cart.",
    "All": "This value is passed into the OrderStatus of GetOrders to retrieve order in all states. This is the default value.",
    "Authenticated": "This value indicates that the cart was authenticated.",
    "Cancelled": "This value indicates that the cart was cancelled.",
    "CancelPending": "This value indicates that a buyer has initiated a cancellation request on the order. If a seller sees an order in this state, that seller must either approve or reject the cancellation request through My eBay Web flows or through the Post-Order API cancellation calls.This CancelPending value can be used as a filter in the GetOrders call request to discover recent buyer-initiated cancellations.",
    "Completed": "This value indicates that the order is completed.",
    "CustomCode": "Reserved for internal or future use.",
    "Default": "This value indicates that the order is in default status.",
    "Inactive": "This value indicates that the cart is inactive.",
    "InProcess": "This value indicates that processing of the buyer's cart has been initiated, but is not yet complete.",
    "Invalid": "This value indicates that the cart is invalid, or no longer exists."
}


PAYMENTSTATUS = {
    "BuyerCreditCardFailed": "This value indicates that the buyer's payment via a credit card failed. This value is only applicable if the seller accepts credit cards as a form of payment.",
    "BuyerECheckBounced": "This value indicates that the buyer's eCheck bounced. This value is only applicable if the seller accepts eChecks as a form of payment.",
    "BuyerFailedPaymentReportedBySeller": "This value indicates that the seller reported the buyer's payment as failed.",
    "CustomCode": "Reserved for internal or future use.",
    "NoPaymentFailure": "This value indicates that the buyer's payment for the order has cleared. A CheckoutStatus.eBayPaymentStatus value of 'NoPaymentFailure' and a CheckoutStatus.Status value of 'Complete' indicates that checkout is complete.",
    "PaymentInProcess": "This value indicates that the buyer's non-PayPal payment is in process. This value is only applicable if the buyer has selected a payment method other than PayPal.",
    "PayPalPaymentInProcess": "This value indicates that the buyer's PayPal payment is in process. This value is only applicable if the buyer has selected PayPal as the payment method."
}

CHECKOUTSTATUS = {
    "Complete": "This value indicates that the order or order line item is complete. Generally speaking, an order or order line item is complete when payment from the buyer has been initiated and has been processed.",
    "CustomCode": "Reserved for internal or future use",
    "Incomplete": "This value indicates that the order or order line item is in the incomplete state. Generally speaking, an order or order line item is considered incomplete when payment from the buyer has yet to be initiated.",
    "Pending": "This value indicates that the order or order line item is in the pending state. Generally speaking, an order is considered pending when payment from the buyer has been initiated but has yet to be fully processed."
}

ERRORCODE = {
    'InvalidToken': 'InvalidToken',
    'TokenExpired': 'InvalidToken',
    'NetError': 'NetError',
    'XmlParseError': 'XmlParseError'
}

SITEID = {
    'USA': '0',
    'UK': '3',
    'AU': '15',
    'CA': '2'
}


DE_RETURN_DESCRIPTION = '''
                Sie haben das Recht, binnen vierzehn Tagen/eines Monats ohne Angabe von Gründen diesen Vertrag zu widerrufen.
                Die Widerrufsfrist beträgt vierzehn Tage/einen Monat ab dem Tag, an dem Sie oder ein von Ihnen benannter Dritter, der nicht der Beförderer ist, die Waren in Besitz genommen haben bzw. hat.
                Um Ihr Widerrufsrecht auszuüben, müssen Sie uns ([Name/Unternehmen], [Anschrift – kein Postfach], [Telefonnummer], [Telefaxnummer – falls vorhanden], [E-Mail-Adresse]) mittels einer eindeutigen Erklärung (z. B. ein mit der Post versandter Brief, Telefax oder E-Mail) über Ihren Entschluss, diesen Vertrag zu widerrufen, informieren.
                Sie können dafür das beigefügte Muster-Widerrufsformular verwenden, das jedoch nicht vorgeschrieben ist.
                Zur Wahrung der Widerrufsfrist reicht es aus, dass Sie die Mitteilung über die Ausübung des Widerrufsrechts vor Ablauf der Widerrufsfrist absenden.
                Folgen des Widerrufs
                Wenn Sie diesen Vertrag widerrufen, haben wir Ihnen alle Zahlungen, die wir von Ihnen erhalten haben, einschließlich der Lieferkosten (mit Ausnahme der zusätzlichen Kosten, die sich daraus ergeben, dass Sie eine andere Art der Lieferung als die von uns angebotene, günstigste Standardlieferung gewählt haben), unverzüglich und spätestens binnen vierzehn Tagen ab dem Tag zurückzuzahlen, an dem die Mitteilung über Ihren Widerruf dieses Vertrags bei uns eingegangen ist. Für diese Rückzahlung verwenden wir dasselbe Zahlungsmittel, das Sie bei der ursprünglichen Transaktion eingesetzt haben, es sei denn, mit Ihnen wurde ausdrücklich etwas anderes vereinbart; in keinem Fall werden Ihnen wegen dieser Rückzahlung Entgelte berechnet.
                Wir können die Rückzahlung verweigern, bis wir die Waren wieder zurückerhalten haben oder bis Sie den Nachweis erbracht haben, dass Sie die Waren zurückgesandt haben, je nachdem, welches der frühere Zeitpunkt ist.
                Sie haben die Waren unverzüglich und in jedem Fall spätestens binnen vierzehn Tagen ab dem Tag, an dem Sie uns über den Widerruf dieses Vertrags unterrichten, an uns oder an [hier sind gegebenenfalls der Name und die Anschrift der von Ihnen zur Entgegennahme der Waren ermächtigten Person einzufügen] zurückzusenden oder zu übergeben. Die Frist ist gewahrt, wenn Sie die Waren vor Ablauf der Frist von vierzehn Tagen absenden.
                l Option A:
                Wir tragen die Kosten der Rücksendung der Waren.
                l Option B:
                Sie tragen die unmittelbaren Kosten der Rücksendung der Waren.
                Sie müssen für einen etwaigen Wertverlust der Waren nur aufkommen, wenn dieser Wertverlust auf einen zur Prüfung der Beschaffenheit, Eigenschaften und Funktionsweise der Waren nicht notwendigen Umgang mit ihnen zurückzuführen ist.
                Muster-Widerrufsformular
                (Wenn Sie den Vertrag widerrufen wollen, dann füllen Sie bitte dieses Formular aus und senden Sie es zurück.)
                – An [Name/Unternehmen], [Adresse – kein Postfach], [Faxnummer – falls vorhanden], [E-Mail-Adresse – falls vorhanden]:
                – Hiermit widerrufe(n) ich/wir (*) den von mir/uns (*) abgeschlossenen Vertrag über den Kauf der folgenden Waren (*)/die Erbringung der folgenden Dienstleistung (*)
                – Bestellt am (*)/erhalten am (*)
                – Name des/der Verbraucher(s)
                – Anschrift des/der Verbraucher(s)
                – Unterschrift des/der Verbraucher(s) (nur bei Mitteilung auf Papier)
                – Datum
            '''


class EBayAPI(object):
    # sand_box
    # rurl = 'https://api.sandbox.ebay.com/ws/api.dll'
    # product
    rurl = 'https://api.ebay.com/ws/api.dll'
    runame = ''
    redirecturl = 'https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&runame=%s&SessID=%s'
    header = {'X-EBAY-API-SITEID': '0', 'X-EBAY-API-COMPATIBILITY-LEVEL': '989', 'Content-Type': 'application/xml'}

    def __init__(self, appinfo):
        self.header['X-EBAY-API-APP-NAME'] = appinfo['appid']
        self.header['X-EBAY-API-DEV-NAME'] = appinfo['devid']
        self.header['X-EBAY-API-CERT-NAME'] = appinfo['certid']
        self.runame = appinfo['runame']
        self.runip = appinfo['runip']
        if self.runip:
            self.rurl = "http://" + self.runip + ":9193/api.ebay.com/ws/api.dll"
        pass

    def getSessionID(self):
        self.header['X-EBAY-API-CALL-NAME'] = 'GetSessionID'
        xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<GetSessionIDRequest xmlns="urn:ebay:apis:eBLBaseComponents">' + \
            '<RuName>' + self.runame + '</RuName>' + \
            '</GetSessionIDRequest>'
        req = urllib2.Request(self.rurl, data=xmls, headers=self.header)
        resxml = urllib2.urlopen(req, timeout=10).read()
        soup = BeautifulSoup(resxml, 'xml')
        info = soup.find('SessionID')
        if info is None:
            return None
        else:
            return info.text

    def fetchToken(self, sessionid):
        self.header['X-EBAY-API-CALL-NAME'] = 'FetchToken'
        xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<FetchTokenRequest xmlns="urn:ebay:apis:eBLBaseComponents">' + \
            '<SessionID>' + sessionid + '</SessionID>' + \
            '</FetchTokenRequest>'
        req = urllib2.Request(self.rurl, data=xmls, headers=self.header)
        resxml = urllib2.urlopen(req, timeout=10).read()
        soup = BeautifulSoup(resxml, 'xml')
        etoken = soup.find('eBayAuthToken')
        etime = soup.find('HardExpirationTime')

        if etoken is None or etime is None:
            return None
        else:
            return (etoken.text, etime.text)

    def revokeToken(self, storetoken):
        self.header['X-EBAY-API-CALL-NAME'] = 'RevokeToken'
        xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<RevokeTokenRequest xmlns="urn:ebay:apis:eBLBaseComponents">' + \
            '<RequesterCredentials>' + \
            '<eBayAuthToken>' + storetoken + '</eBayAuthToken>' + \
            '</RequesterCredentials>' + \
            '</RevokeTokenRequest>'
        req = urllib2.Request(self.rurl, data=xmls, headers=self.header)
        resxml = urllib2.urlopen(req, timeout=10).read()
        soup = BeautifulSoup(resxml, 'xml')
        info = soup.find('Ack')
        if info is None:
            return False
        else:
            if info.text == 'Success':
                return True
            else:
                return False


class EBayStoreAPI(EBayAPI):
    storetoken = ''

    def __init__(self, appinfo, storetoken, siteID=0):
        EBayAPI.__init__(self, appinfo)
        self.storetoken = storetoken
        self.header['X-EBAY-API-SITEID'] = str(siteID)

    def rmNoASCII(self, inputStr):
        resultStr = ''
        for i in inputStr:
            if ord(i) < 128:
                resultStr += i
            else:
                resultStr += ' '
        return resultStr
        # return ''.join([i if ord(i) < 128 else ' ' for i in inputStr])
        # return inputStr.replace('[\x00-\x7F]', ':').replace('[\x00-\x7F]', ':').replace('[\x00-\x7F]', ':')

    def xmlToOrders(self, xmls, srcpagination):
        soup = BeautifulSoup(xmls, 'xml')
        errorcode = '0'
        info = soup.find('Ack')
        if info is None:
            errorcode = '95106'     # without ack info
        elif info.text == 'Failure':
            errorinfo = soup.find('Errors')
            if errorinfo is None:
                errorcode = '95107'        # without error info
            else:
                el_errorcode = errorinfo.find('ErrorCode')
                if el_errorcode is None:
                    errorcode = '95108'
                else:
                    errorcode = el_errorcode.text
        orders = soup.find('OrderArray')

        if orders is None:
            errorcode = '95109'
        if errorcode != '0':
            return {'errorcode': errorcode, 'pagination': None, 'orderlist': None}

        result = []
        listOrder = orders.find_all('Order')
        for order in listOrder:
            obj = EBayOrder()
            orderid = order.find('OrderID')
            if orderid is not None:
                obj.orderid = orderid.text
            else:
                continue

            status = order.find('OrderStatus')
            if status is not None:
                obj.status = status.text

            adjustmentAmount = order.find('AdjustmentAmount')
            if adjustmentAmount is not None:
                obj.adjustmentAmount = adjustmentAmount.text
                obj.currency = adjustmentAmount.attrs['currencyID']

            amountPaid = order.find('AmountPaid')
            if amountPaid is not None:
                obj.amountPaid = amountPaid.text

            amountSaved = order.find('AmountSaved')
            if amountSaved is not None:
                obj.amountSaved = amountSaved.text

            checkoutStatus = EBayOrder.CheckoutStatus()
            el_checkoutStatus = order.find('CheckoutStatus')
            if el_checkoutStatus is not None:
                cs_paymentstatus = el_checkoutStatus.find('eBayPaymentStatus')
                if cs_paymentstatus is not None:
                    checkoutStatus.paymentstatus = cs_paymentstatus.text
                cs_lastModifiedTime = el_checkoutStatus.find('LastModifiedTime')
                if cs_lastModifiedTime is not None:
                    checkoutStatus.lastModifiedTime = cs_lastModifiedTime.text
                cs_paymentMethod = el_checkoutStatus.find('PaymentMethod')
                if cs_paymentMethod is not None:
                    checkoutStatus.paymentMethod = cs_paymentMethod.text
                cs_status = el_checkoutStatus.find('Status')
                if cs_status is not None:
                    checkoutStatus.status = cs_status.text
                cs_iMCCEnabled = el_checkoutStatus.find('IntegratedMerchantCreditCardEnabled')
                if cs_iMCCEnabled is not None:
                    checkoutStatus.iMCCEnabled = cs_iMCCEnabled.text
                cs_paymentInstrument = el_checkoutStatus.find('PaymentInstrument')
                if cs_paymentInstrument is not None:
                    checkoutStatus.paymentInstrument = cs_paymentInstrument.text
            obj.checkoutStatus = checkoutStatus

            createTime = order.find('CreatedTime')
            if createTime is not None:
                obj.createTime = createTime.text

            paymentMethods = order.find('PaymentMethods')
            if paymentMethods is not None:
                obj.paymentMethods = paymentMethods.text

            shippingAddress = order.find('ShippingAddress')
            if shippingAddress is not None:
                obj.shippingAddress = str(shippingAddress)

            el_shippingService = order.find('ShippingServiceSelected')
            if el_shippingService is not None:
                ss_shippingService = el_shippingService.find('ShippingService')
                if ss_shippingService is not None:
                    obj.shippingService = ss_shippingService.text
                ss_shippingServiceCost = el_shippingService.find('ShippingServiceCost')
                if ss_shippingServiceCost is not None:
                    obj.shippingServiceCost = ss_shippingServiceCost.text

            subtotal = order.find('Subtotal')
            if subtotal is not None:
                obj.subtotal = subtotal.text

            total = order.find('Total')
            if total is not None:
                obj.total = total.text

            extendedOrderID = order.find('ExtendedOrderID')
            if extendedOrderID is not None:
                obj.extendedOrderID = extendedOrderID.text

            transactions = []
            el_transactions = order.find('TransactionArray')
            if el_transactions is not None:
                el_transaction_list = el_transactions.find_all('Transaction')
                for el_transaction in el_transaction_list:
                    transaction = EBayOrder.Transaction()
                    el_buyer = el_transaction.find('Buyer')
                    t_buyer = ''
                    if el_buyer is not None:
                        el_lastname = el_buyer.find('UserLastName')
                        if el_lastname is not None:
                            t_buyer = el_lastname.text + ' '
                        el_firstname = el_buyer.find('UserFirstName')
                        if el_firstname is not None:
                            t_buyer = t_buyer + el_firstname.text
                    transaction.buyer = t_buyer
                    info = el_transaction.find('ShippingDetails')
                    if info is not None:
                        info = info.find('ShipmentTrackingDetails')
                        if info is not None:
                            t_shippingCarrier = info.find('ShippingCarrierUsed')
                            if t_shippingCarrier is not None:
                                transaction.shippingCarrier = t_shippingCarrier.text
                            t_shipmentTracking = info.find('ShipmentTrackingNumber')
                            if t_shipmentTracking is not None:
                                transaction.shipmentTracking = t_shipmentTracking.text
                    t_createDate = el_transaction.find('CreatedDate')
                    if t_createDate is not None:
                        transaction.createDate = t_createDate.text
                    t_item = el_transaction.find('Item')
                    if t_item is not None:
                        t_itemid = t_item.find('ItemID')
                        if t_itemid is not None:
                            transaction.itemid = t_itemid.text
                        t_itemSite = t_item.find('Site')
                        if t_itemSite is not None:
                            transaction.itemSite = t_itemSite.text
                        t_itemTitle = t_item.find('Title')
                        if t_itemTitle is not None:
                            transaction.itemTitle = t_itemTitle.text
                    t_quantityPurchased = el_transaction.find('QuantityPurchased')
                    if t_quantityPurchased is not None:
                        transaction.quantityPurchased = t_quantityPurchased.text
                    t_transactionID = el_transaction.find('TransactionID')
                    if t_transactionID is not None:
                        transaction.transactionID = t_transactionID.text
                    t_price = el_transaction.find('TransactionPrice')
                    if t_price is not None:
                        transaction.price = t_price.text
                    el_tax = el_transaction.find('Taxes')
                    if el_tax is not None:
                        t_tax = el_tax.find('TotalTaxAmount')
                        if t_tax is not None:
                            transaction.tax = t_tax.text
                    t_shipping = el_transaction.find('ActualShippingCost')
                    if t_shipping is not None:
                        transaction.shipping = t_shipping.text
                    t_handling = el_transaction.find('ActualHandlingCost')
                    if t_handling is not None:
                        transaction.handling = t_handling.text
                    transactions.append(transaction)
            obj.transactions = transactions

            buyerID = order.find('BuyerUserID')
            if buyerID is not None:
                obj.buyerID = buyerID.text

            paidTime = order.find('PaidTime')
            if paidTime is not None:
                obj.paidTime = paidTime.text

            shippedTime = order.find('ShippedTime')
            if shippedTime is not None:
                obj.shippedTime = shippedTime.text

            paymentHoldStatus = order.find('PaymentHoldStatus')
            if paymentHoldStatus is not None:
                obj.paymentHoldStatus = paymentHoldStatus.text

            sellerUserID = order.find('SellerUserID')
            if sellerUserID is not None:
                obj.sellerUserID = sellerUserID.text

            result.append(obj)

        pagination = Pagination()
        pagination.clone(srcpagination)
        el_pagination = soup.find('PaginationResult')
        if el_pagination is not None:
            el_totalpage = el_pagination.find('TotalNumberOfPages')
            if el_totalpage is not None:
                pagination.totalpage = int(el_totalpage.text)
            el_totalentries = el_pagination.find('TotalNumberOfEntries')
            if el_totalentries is not None:
                pagination.totalentries = int(el_totalentries.text)
        el_pageNumber = soup.find('PageNumber')
        # currpage = 1
        if el_pageNumber is not None:
            pagination.currpage = int(el_pageNumber.text)

        return {'errorcode': errorcode, 'pagination': pagination, 'orderlist': result}

    # createTime
    def getOrderListByCreateTime(self, beginTime, endTime, pagination):
        self.header['X-EBAY-API-CALL-NAME'] = 'GetOrders'
        # construct request
        xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<GetOrdersRequest xmlns="urn:ebay:apis:eBLBaseComponents">' + \
            '<RequesterCredentials><eBayAuthToken>' + self.storetoken + '</eBayAuthToken></RequesterCredentials>' + \
            '<CreateTimeFrom>' + beginTime.strftime('%Y-%m-%dT%H:%M:%SZ') + '</CreateTimeFrom>' + \
            '<CreateTimeTo>' + endTime.strftime('%Y-%m-%dT%H:%M:%SZ') + '</CreateTimeTo>' + \
            '<Pagination><EntriesPerPage>' + str(pagination.perpage) + '</EntriesPerPage><PageNumber>' + str(pagination.currpage) + '</PageNumber></Pagination>' +\
            '<OrderRole>Seller</OrderRole></GetOrdersRequest>'
        try:
            for i in range(0, 3):
                req = urllib2.Request(self.rurl, data=xmls, headers=self.header)
                resxml = urllib2.urlopen(req, timeout=60).read()
                return self.xmlToOrders(resxml, pagination)
        except:
            pass

    def getOrderListByTime(self, beginTime, endTime, pagination):
        self.header['X-EBAY-API-CALL-NAME'] = 'GetOrders'
        # construct request
        xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<GetOrdersRequest xmlns="urn:ebay:apis:eBLBaseComponents">' + \
            '<RequesterCredentials><eBayAuthToken>' + self.storetoken + '</eBayAuthToken></RequesterCredentials>' +\
            '<ModTimeFrom>' + beginTime.strftime('%Y-%m-%dT%H:%M:%SZ') + '</ModTimeFrom>' +\
            '<ModTimeTo>' + endTime.strftime('%Y-%m-%dT%H:%M:%SZ') + '</ModTimeTo>' +\
            '<Pagination><EntriesPerPage>' + str(pagination.perpage) + '</EntriesPerPage><PageNumber>' + str(pagination.currpage) + '</PageNumber></Pagination>' +\
            '<OrderRole>Seller</OrderRole></GetOrdersRequest>'

        req = urllib2.Request(self.rurl, data=xmls, headers=self.header)
        resxml = urllib2.urlopen(req, timeout=60).read()
        return self.xmlToOrders(resxml, pagination)

        # return {'errorcode':'95112', 'pagination': None, 'orderlist':None}

    def xmlToItems(self, xmls, srcpagination):
        soup = BeautifulSoup(xmls, 'xml')
        errorcode = '0'
        info = soup.find('Ack')
        if info is None:
            errorcode = '95106'     # without ack info
        elif info.text == 'Failure':
            errorinfo = soup.find('Errors')
            if errorinfo is None:
                errorcode = '95107'        # without error info
            else:
                el_errorcode = errorinfo.find('ErrorCode')
                if el_errorcode is None:
                    errorcode = '95108'
                else:
                    errorcode = el_errorcode.text

        itemarray = soup.find('ItemArray')
        if itemarray is None and errorcode == '0':
            errorcode = '95110'

        if errorcode != '0':
            return {'errorcode': errorcode, 'pagination': None, 'orderlist': None}

        result = []
        listItem = itemarray.find_all('Item')
        for el_item in listItem:
            obj = EBayItemInfo()

            itemid = el_item.find('ItemID')
            if itemid is not None:
                obj.itemid = itemid.text
            else:
                continue

            binPrice = el_item.find('BuyItNowPrice')
            if binPrice is not None:
                obj.binPrice = binPrice.text

            startPrice = el_item.find('StartPrice')
            if startPrice is not None:
                obj.startPrice = startPrice.text

            total = el_item.find('Quantity')
            if total is not None:
                obj.total = total.text

            listingDetail = el_item.find('ListingDetails')
            if listingDetail is not None:
                startTime = listingDetail.find('StartTime')
                if startTime is not None:
                    obj.startTime = startTime.text
                endTime = listingDetail.find('EndTime')
                if endTime is not None:
                    obj.endTime = endTime.text
                url = listingDetail.find('ViewItemURL')
                if url is not None:
                    obj.url = url.text

            sellingStatus = el_item.find('SellingStatus')
            if sellingStatus is not None:
                currPrice = sellingStatus.find('CurrentPrice')
                if currPrice is not None:
                    obj.currPrice = currPrice.text
                    obj.currency = currPrice.attrs['currencyID']
                sold = sellingStatus.find('QuantitySold')
                if sold is not None:
                    obj.sold = sold.text
                status = sellingStatus.find('ListingStatus')
                if status is not None:
                    obj.status = status.text

            available = el_item.find('QuantityAvailable')
            if available is not None:
                obj.available = available.text
                obj.sold = int(obj.total) - int(obj.available)

            el_spPrice = el_item.find('ShippingDetails')
            if el_spPrice is not None:
                ss_spPrice = el_spPrice.find('ShippingServiceOptions')
                if ss_spPrice is not None:
                    spPrice = ss_spPrice.find('ShippingServiceCost')
                    if spPrice is not None:
                        obj.spPrice = spPrice.text

            el_title = el_item.find('Title')
            if el_title is not None:
                obj.itemtitle = el_title.text

            SKU = el_item.find('SKU')
            if SKU is not None:
                obj.SKU = SKU.text

            el_img = el_item.find('PictureDetails')
            if el_img is not None:
                img = el_img.find('GalleryURL')
                if img is not None:
                    obj.img = img.text

            subSKUs = []
            el_variations = el_item.find('Variations')
            if el_variations is not None:
                variations = el_variations.find_all('Variation')
                for variation in variations:
                    subsku = EBayItemInfo.EBaySubSKU()
                    subsku.itemid = obj.itemid
                    subSKUInfo = variation.find('SKU')
                    if subSKUInfo is not None:
                        subsku.subSKU = subSKUInfo.text
                    ss_startPrice = variation.find('StartPrice')
                    if ss_startPrice is not None:
                        subsku.startPrice = ss_startPrice.text
                    ss_total = variation.find('Quantity')
                    if ss_total is not None:
                        subsku.total = ss_total.text

                    ss_sellingstatus = variation.find('SellingStatus')
                    if ss_sellingstatus is not None:
                        ss_sold = ss_sellingstatus.find('QuantitySold')
                        if ss_sold is not None:
                            subsku.sold = ss_sold.text

                    ss_skutitle = variation.find('VariationTitle')
                    if ss_skutitle is not None:
                        subsku.skutitle = ss_skutitle.text
                    subSKUs.append(subsku)
            obj.subSKUs = subSKUs
            result.append(obj)
        pagination = Pagination()
        pagination.clone(srcpagination)
        el_pagination = soup.find('PaginationResult')
        if el_pagination is not None:
            el_totalpage = el_pagination.find('TotalNumberOfPages')
            if el_totalpage is not None:
                pagination.totalpage = int(el_totalpage.text)
            el_totaletries = el_pagination.find('TotalNumberOfEntries')
            if el_totaletries is not None:
                pagination.totaletries = int(el_totaletries.text)
        el_pageNumber = soup.find('PageNumber')
        # currpage = 1
        if el_pageNumber is not None:
            pagination.currpage = int(el_pageNumber.text)

        return {'errorcode': errorcode, 'pagination': pagination, 'itemlist': result}

    def getEbaySelling(self, pagination):
        self.header['X-EBAY-API-CALL-NAME'] = 'GetMyeBaySelling'
        # construct request
        xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<GetMyeBaySellingRequest xmlns="urn:ebay:apis:eBLBaseComponents">' + \
            '<RequesterCredentials><eBayAuthToken>' + self.storetoken + '</eBayAuthToken></RequesterCredentials>' + \
            '<ActiveList><Include>true</Include><Pagination><EntriesPerPage>' + str(pagination.perpage) + '</EntriesPerPage><PageNumber>' + str(pagination.currpage) + '</PageNumber></Pagination></ActiveList>' +\
            '</GetMyeBaySellingRequest>'
        req = urllib2.Request(self.rurl, data=xmls, headers=self.header)
        resxml = urllib2.urlopen(req, timeout=60).read()
        return self.xmlToItems(resxml, pagination)

    def getEbayEndList(self, beginTime, endTime, pagination):
        self.header['X-EBAY-API-CALL-NAME'] = 'GetSellerList'
        # construct request
        xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<GetSellerListRequest xmlns="urn:ebay:apis:eBLBaseComponents">' + \
            '<RequesterCredentials><eBayAuthToken>' + self.storetoken + '</eBayAuthToken></RequesterCredentials>' + \
            '<EndTimeFrom>' + beginTime.strftime('%Y-%m-%dT%H:%M:%SZ') + '</EndTimeFrom>' + \
            '<EndTimeTo>' + endTime.strftime('%Y-%m-%dT%H:%M:%SZ') + '</EndTimeTo>' + \
            '<Pagination><EntriesPerPage>' + str(pagination.perpage) + '</EntriesPerPage><PageNumber>' + str(pagination.currpage) + '</PageNumber></Pagination>' + \
            '<GranularityLevel>Coarse</GranularityLevel><IncludeWatchCount>true</IncludeWatchCount>' + \
            '</GetSellerListRequest>'

        req = urllib2.Request(self.rurl, data=xmls, headers=self.header)
        resxml = urllib2.urlopen(req, timeout=60).read()
        return self.xmlToItems(resxml, pagination)

    def xmlToSummary(self, xmls):
        soup = BeautifulSoup(xmls, 'xml')
        summary = soup.find('Summary')
        result = EBaySummary()
        result.activeAuctionCount = summary.find('ActiveAuctionCount')
        result.auctionSellingCount = summary.find('AuctionSellingCount')
        result.auctionBidCount = summary.find('AuctionBidCount')
        result.totalAuctionSellingValue = summary.find('TotalAuctionSellingValue')
        result.totalSoldCount = summary.find('TotalSoldCount')
        result.totalSoldValue = summary.find('TotalSoldValue')
        result.soldDurationInDays = summary.find('SoldDurationInDays')
        result.classifiedAdCount = summary.find('ClassifiedAdCount')
        result.totalLeadCount = summary.find('TotalLeadCount')
        result.classifiedAdOfferCount = summary.find('ClassifiedAdOfferCount')
        result.totalListingsWithLeads = summary.find('TotalListingsWithLeads')
        result.quantityLimitRemaining = summary.find('QuantityLimitRemaining')
        result.amountLimitRemaining = summary.find('AmountLimitRemaining')

        return result

    def getEbaySummary(self):
        self.header['X-EBAY-API-CALL-NAME'] = 'GetMyeBaySelling'
        # construct request
        xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<GetMyeBaySellingRequest xmlns="urn:ebay:apis:eBLBaseComponents">' + \
            '<RequesterCredentials><eBayAuthToken>' + self.storetoken + '</eBayAuthToken></RequesterCredentials>' + \
            '<SellingSummary><Include>true</Include></SellingSummary>' + \
            '</GetMyeBaySellingRequest>'
        req = urllib2.Request(self.rurl, data=xmls, headers=self.header)
        resxml = urllib2.urlopen(req, timeout=60).read()
        return self.xmlToSummary(resxml)

    # Name, Value element
    def buildDictXml(self, info, tagRoot):
        resXml = ''
        if info is not None and len(info) > 0:
            resXml = '<%s>' % (tagRoot) + self.buildListXml(info) + '</%s>' % (tagRoot)
            resXml = resXml
        return resXml

    # Name, Value element -- List
    def buildListXml(self, info, tagList='NameValueList', tagName='Name', tagValue='Value'):
        resXml = ''
        if info is not None and len(info) > 0:
            for (k, v) in info.items():
                if isinstance(v, str):
                    resXml = resXml + '<%s><%s>%s</%s><%s>%s</%s></%s>' % (tagList, tagName, k, tagName, tagValue, v, tagValue, tagList)
                elif isinstance(v, list):
                    resXml = resXml + '<%s><%s>%s</%s>' % (tagList, tagName, k, tagName)
                    for value in v:
                        resXml = resXml + '<%s>%s</%s>' % (tagValue, value, tagValue)
                    resXml = resXml + '</%s>' % (tagList)
                elif isinstance(v.encode('utf-8'), str):
                    resXml = resXml + '<%s><%s>%s</%s><%s>%s</%s></%s>' % (tagList, tagName, k, tagName, tagValue, v, tagValue, tagList)
        return resXml

    # Convert str to Xml contains multiple elements, split by ','
    def convertStrToXml(self, inputStr, tagList='ExcludeShipToLocation'):
        resXml = ''
        if inputStr is not None and len(inputStr) > 0:
            info = inputStr.split(',')
            for valueStr in info:
                act_v = valueStr.strip()
                if valueStr.strip() != '':
                    resXml = resXml + '<%s>%s</%s>' % (tagList, act_v, tagList)
        return resXml

    # shippingOptions
    def buildShippingDetailXml(self, shippingDetail):
        shippingServiceOptionsXml = ''
        internationalShippingServiceOptionXml = ''
        salesTaxesXml = ''
        if shippingDetail is not None and shippingDetail.shippingServiceOptions is not None:
            for option in shippingDetail.shippingServiceOptions:
                if option.freeShipping == 'true':
                    shippingServiceOptionsXml = shippingServiceOptionsXml + '<ShippingServiceOptions><FreeShipping>%s</FreeShipping>' % (option.freeShipping) +\
                        '<ShippingService>%s</ShippingService>' % (option.shippingService) +\
                        '<ShippingServicePriority>%s</ShippingServicePriority></ShippingServiceOptions>' % (option.shippingServicePriority)
                else:
                    shippingServiceOptionsXml = shippingServiceOptionsXml + '<ShippingServiceOptions><FreeShipping>false</FreeShipping>' +\
                        '<ShippingService>%s</ShippingService>' % (option.shippingService) +\
                        '<ShippingServiceCost>%s</ShippingServiceCost>' % (str(option.shippingServiceCost)) +\
                        '<ShippingServiceAdditionalCost>%s</ShippingServiceAdditionalCost>' % (str(option.shippingServiceAdditionalCost)) +\
                        '<ShippingServicePriority>%s</ShippingServicePriority></ShippingServiceOptions>' % (option.shippingServicePriority)

            if shippingDetail.globalShipping == 'false':
                for option in shippingDetail.internationalShippingServiceOptions:
                    locationsXml = self.convertStrToXml(option.shipToLocations, 'ShipToLocation')

                    internationalShippingServiceOptionXml = internationalShippingServiceOptionXml + \
                        '<InternationalShippingServiceOption><ShippingService>%s</ShippingService>' % (option.shippingService) +\
                        '<ShippingServiceCost>%s</ShippingServiceCost>' % (str(option.shippingServiceCost)) +\
                        '<ShippingServiceAdditionalCost>%s</ShippingServiceAdditionalCost>' % (str(option.shippingServiceAdditionalCost)) +\
                        locationsXml +\
                        '<ShippingServicePriority>%s</ShippingServicePriority></InternationalShippingServiceOption>' % (option.shippingServicePriority)

            if shippingDetail.salesTaxes is not None and len(shippingDetail.salesTaxes) > 0:
                salesTaxesXml = '<SalesTax>'
                for salesTax in shippingDetail.salesTaxes:
                    salesTaxesXml = salesTaxesXml + '<SalesTaxPercent>%s</SalesTaxPercent><SalesTaxState>%s</SalesTaxState></SalesTax>' % (salesTax.salesTaxPercent, salesTax.salesTaxState)

        resXml = '<ShippingDetails><PaymentInstructions>%s</PaymentInstructions>' % (shippingDetail.paymentInstructions) + salesTaxesXml + shippingServiceOptionsXml +\
            '<GlobalShipping>%s</GlobalShipping>' % (shippingDetail.globalShipping) + internationalShippingServiceOptionXml + \
            self.convertStrToXml(shippingDetail.excludeShipToLocation) + \
            '<ShippingType>%s</ShippingType></ShippingDetails>' % (shippingDetail.shippingType)

        return resXml

    def buildVariationsXml(self, item):
        setsXml = self.buildDictXml(item.variationSpecificsSet, 'VariationSpecificsSet')

        variationsXml = ''
        if item.variations is not None and len(item.variations) > 0:
            for variation in item.variations:
                ewmXml = '<VariationProductListingDetails><UPC>%s</UPC></VariationProductListingDetails>' % (item.UPC)
                # Site UK
                if self.header['X-EBAY-API-SITEID'] in ['3', '71', '77']:
                    ewmXml = '<VariationProductListingDetails><EAN>%s</EAN></VariationProductListingDetails>' % (item.EAN)

                variationsXml = variationsXml + '<Variation><SKU>%s</SKU><StartPrice>%s</StartPrice><Quantity>%s</Quantity>' % (variation.SKU, variation.startPrice, variation.quantity) + \
                    self.buildDictXml(variation.variationSpecifics, 'VariationSpecifics') + ewmXml + '</Variation>'

            picturesXml = ''
            if item.variationSpecificPictureSets is not None and len(item.variationSpecificPictureSets) > 0:
                picturesXml = '<Pictures><VariationSpecificName>%s</VariationSpecificName>' % (item.variationSpecificName)
                picturesXml = picturesXml + self.buildListXml(item.variationSpecificPictureSets, 'VariationSpecificPictureSet', 'VariationSpecificValue', 'PictureURL') + '</Pictures>'

            return '<Variations>' + setsXml + variationsXml + picturesXml + '</Variations>'
        else:
            return '<SKU>%s</SKU>' % (item.SKU)

    def buildBuyerReqXml(self, buyerReq):
        resXml = '<BuyerRequirementDetails><MaximumItemRequirements><MaximumItemCount>%s</MaximumItemCount>' % (buyerReq.maximumItemCount) +\
            '<MinimumFeedbackScore>%s</MinimumFeedbackScore></MaximumItemRequirements>' % (buyerReq.max_minimumFeedbackScore) +\
            '<MinimumFeedbackScore>%s</MinimumFeedbackScore>' % (buyerReq.minimumFeedbackScore) +\
            '<ShipToRegistrationCountry>%s</ShipToRegistrationCountry></BuyerRequirementDetails>' % (buyerReq.shipToRegistrationCountry)
        return resXml

    def publishItem(self, item):
        self.header['X-EBAY-API-CALL-NAME'] = 'AddFixedPriceItem'

        # pictrueDetail
        picDetailXml = ''
        if item.pictureDetail is not None:
            picDetailXml = '<PictureDetails><GalleryType>Gallery</GalleryType><PhotoDisplay>SuperSize</PhotoDisplay>'
            for url in item.pictureDetail:
                picDetailXml = picDetailXml + '<PictureURL>%s</PictureURL>' % (url)
            picDetailXml = picDetailXml + '</PictureDetails>'

        ewmXml = '<ProductListingDetails><UPC>%s</UPC></ProductListingDetails>' % (item.UPC)
        if self.header['X-EBAY-API-SITEID'] in ['71', '77', '3']:
            ewmXml = '<ProductListingDetails><EAN>%s</EAN></ProductListingDetails>' % (item.EAN)
        # elif self.header['X-EBAY-API-SITEID'] == '3':
        #     ewmXml = ''
        elif self.header['X-EBAY-API-SITEID'] == '2':
            item.currency = 'CAD'
        quantityXml = '<Quantity>%s</Quantity>' % (item.quantity)
        priceXml = '<StartPrice currencyID="%s">%s</StartPrice>' % (item.currency, item.startPrice)
        # Site UK

        if item.variations is not None and len(item.variations) > 0:
            ewmXml = ''
            quantityXml = ''
            priceXml = ''

        logger.debug('=============item.title %s' % item.title)
        logger.debug('=============item.itemSpecifics %s' % item.itemSpecifics)
        if self.header['X-EBAY-API-SITEID'] in ['3', '71']:
            # flag = 1
            xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
                '<AddFixedPriceItemRequest xmlns="urn:ebay:apis:eBLBaseComponents"><Item>' + \
                '<Country>%s</Country>' % (item.country) + \
                '<Location>%s</Location>' % (item.location) + \
                '<Currency>%s</Currency>' % (item.currency) + \
                '<Description><![CDATA[%s]]></Description>' % (str(item.description)) + \
                '<DispatchTimeMax>%d</DispatchTimeMax>' % (item.dispatchTimeMax) + \
                '<ListingDuration>%s</ListingDuration>' % (item.listingDuration) + \
                '<ListingType>%s</ListingType>' % (item.listingType) + \
                '<PaymentMethods>%s</PaymentMethods>' % (item.paymentMethods) + \
                '<PayPalEmailAddress>%s</PayPalEmailAddress>' % (item.payPalEmailAddress) + \
                '<PostalCode>%s</PostalCode>' % (str(item.postalCode)) + \
                '<PrimaryCategory><CategoryID>%s</CategoryID></PrimaryCategory>' % (item.primaryCategory) + \
                '<Title>%s</Title>' % str(item.title) + \
                str(picDetailXml) + \
                '<HitCounter>%s</HitCounter>' % (item.hitCounter) + \
                '<ReturnPolicy><ReturnsAcceptedOption>%s</ReturnsAcceptedOption>' % (item.returnPolicy.returnsAcceptedOption) + \
                '<ReturnsWithinOption>%s</ReturnsWithinOption>' % (item.returnPolicy.returnsWithinOption) + \
                '<ShippingCostPaidByOption>%s</ShippingCostPaidByOption></ReturnPolicy>' % (item.returnPolicy.shippingCostPaidByOption) + \
                self.buildShippingDetailXml(item.shippingDetails) + \
                self.buildDictXml(item.itemSpecifics, 'ItemSpecifics') + \
                str(self.buildVariationsXml(item)) + \
                self.buildBuyerReqXml(item.buyerRequirementDetails) + \
                ewmXml + quantityXml + priceXml + \
                '<ConditionID>%s</ConditionID></Item>' % (str(item.conditionID)) + \
                '<RequesterCredentials><eBayAuthToken>%s</eBayAuthToken></RequesterCredentials></AddFixedPriceItemRequest>' % (self.storetoken)
        elif self.header['X-EBAY-API-SITEID'] == '77':
            # flag = 3
            xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
                '<AddFixedPriceItemRequest xmlns="urn:ebay:apis:eBLBaseComponents"><Item>' + \
                '<Country>%s</Country>' % (item.country) + \
                '<Location>%s</Location>' % (item.location) + \
                '<Currency>%s</Currency>' % (item.currency) + \
                '<Description><![CDATA[%s]]></Description>' % (str(item.description)) + \
                '<DispatchTimeMax>%d</DispatchTimeMax>' % (item.dispatchTimeMax) + \
                '<ListingDuration>%s</ListingDuration>' % (item.listingDuration) + \
                '<ListingType>%s</ListingType>' % (item.listingType) + \
                '<PaymentMethods>%s</PaymentMethods>' % (item.paymentMethods) + \
                '<PayPalEmailAddress>%s</PayPalEmailAddress>' % (item.payPalEmailAddress) + \
                '<PostalCode>%s</PostalCode>' % (str(item.postalCode)) + \
                '<PrimaryCategory><CategoryID>%s</CategoryID></PrimaryCategory>' % (item.primaryCategory) + \
                '<Title>%s</Title>' % str(item.title) + \
                str(picDetailXml) + \
                '<HitCounter>%s</HitCounter>' % (item.hitCounter) + \
                '<ReturnPolicy><ReturnsAcceptedOption>%s</ReturnsAcceptedOption>' % (item.returnPolicy.returnsAcceptedOption) + \
                '<Description>%s</Description>' % DE_RETURN_DESCRIPTION +\
                '<ShippingCostPaidByOption>%s</ShippingCostPaidByOption></ReturnPolicy>' % (item.returnPolicy.shippingCostPaidByOption) + \
                self.buildShippingDetailXml(item.shippingDetails) + \
                self.buildDictXml(item.itemSpecifics, 'ItemSpecifics') + \
                str(self.buildVariationsXml(item)) + \
                self.buildBuyerReqXml(item.buyerRequirementDetails) + \
                ewmXml + quantityXml + priceXml + \
                '<ConditionID>%s</ConditionID></Item>' % (str(item.conditionID)) + \
                '<RequesterCredentials><eBayAuthToken>%s</eBayAuthToken></RequesterCredentials></AddFixedPriceItemRequest>' % (self.storetoken)
        else:
            # flag = 2
            xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
                '<AddFixedPriceItemRequest xmlns="urn:ebay:apis:eBLBaseComponents"><Item>' + \
                '<Country>%s</Country>' % (item.country) + \
                '<Location>%s</Location>' % (item.location) + \
                '<Currency>%s</Currency>' % (item.currency) + \
                '<Description><![CDATA[%s]]></Description>' % (str(item.description)) + \
                '<DispatchTimeMax>%d</DispatchTimeMax>' % (item.dispatchTimeMax) + \
                '<ListingDuration>%s</ListingDuration>' % (item.listingDuration) + \
                '<ListingType>%s</ListingType>' % (item.listingType) + \
                '<PaymentMethods>%s</PaymentMethods>' % (item.paymentMethods) + \
                '<PayPalEmailAddress>%s</PayPalEmailAddress>' % (item.payPalEmailAddress) + \
                '<PostalCode>%s</PostalCode>' % (str(item.postalCode)) + \
                '<PrimaryCategory><CategoryID>%s</CategoryID></PrimaryCategory>' % (item.primaryCategory) + \
                '<Title>%s</Title>' % str(item.title) + \
                str(picDetailXml) + \
                '<HitCounter>%s</HitCounter>' % (item.hitCounter) + \
                '<ReturnPolicy><ReturnsAcceptedOption>%s</ReturnsAcceptedOption>' % (item.returnPolicy.returnsAcceptedOption) + \
                '<RefundOption>%s</RefundOption>' % (item.returnPolicy.refundOption) + \
                '<ReturnsWithinOption>%s</ReturnsWithinOption>' % (item.returnPolicy.returnsWithinOption) + \
                '<ShippingCostPaidByOption>%s</ShippingCostPaidByOption></ReturnPolicy>' % (item.returnPolicy.shippingCostPaidByOption) + \
                self.buildShippingDetailXml(item.shippingDetails) + \
                self.buildDictXml(item.itemSpecifics, 'ItemSpecifics') + \
                str(self.buildVariationsXml(item)) + \
                self.buildBuyerReqXml(item.buyerRequirementDetails) + \
                ewmXml + quantityXml + priceXml + \
                '<ConditionID>%s</ConditionID></Item>' % (str(item.conditionID)) + \
                '<RequesterCredentials><eBayAuthToken>%s</eBayAuthToken></RequesterCredentials></AddFixedPriceItemRequest>' % (self.storetoken)
        # return xmls
        xmls = self.rmNoASCII(xmls)
        logger.debug('BBBBBBBBBAAA====%s' % xmls)
        logger.debug('====AAABBBBBBBBB')

        req = urllib2.Request(self.rurl, data=xmls, headers=self.header)
        resxml = urllib2.urlopen(req, timeout=60).read()
        logger.debug(resxml)
        soup = BeautifulSoup(resxml, 'xml')
        basicInfo = EBayItemInfo()
        if soup.find('ItemID'):
            basicInfo.itemid = soup.find('ItemID').text
            basicInfo.startTime = soup.find('StartTime').text
            basicInfo.endTime = soup.find('EndTime').text
        elif soup.find('Errors'):
            basicInfo.errors = True
            basicInfo.ShortMessage = soup.find('ShortMessage').text
            basicInfo.LongMessage = soup.find('LongMessage').text
            basicInfo.ErrorClassification = soup.find('ErrorClassification').text
        return basicInfo

    def xmlToPictures(self, xmls):
        soup = BeautifulSoup(xmls, 'xml')
        info = soup.find('Ack')
        if info.text == 'Failure':
            logger.debug('@@@@@@@@@@@@@@@@@@@%s' % str([self.header, self.storetoken]))
            return
        result = []
        details = soup.find('SiteHostedPictureDetails')
        members = details.find_all('PictureSetMember')

        for member in members:
            picture = Picture()
            picture.url = member.find('MemberURL').text
            picture.height = member.find('PictureHeight').text
            picture.width = member.find('PictureWidth').text
            result.append(picture)

        return result

    # don't suggested
    def uploadImgBin(self, filePathName, picSet='Supersize'):
        self.header['X-EBAY-API-CALL-NAME'] = 'UploadSiteHostedPictures'
        xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<UploadSiteHostedPicturesRequest xmlns="urn:ebay:apis:eBLBaseComponents">' + \
            '<PictureSet>%s</PictureSet>' % (picSet) + \
            '<RequesterCredentials><eBayAuthToken>%s</eBayAuthToken></RequesterCredentials></UploadSiteHostedPicturesRequest>' % (self.storetoken)

        request = Request(
            'POST',
            self.rurl,
            data={'XMLPayload': xmls},
            headers=self.header,
            files={'file': ('EbayImage', open(filePathName, 'rb'))}
        )
        try:
            del(self.header['Content-Type'])
            request = request.prepare()
            session = Session()
            response = session.send(
                request,
                verify=True,
                timeout=60
            )

            self.header['Content-Type'] = 'application/xml'
            return self.xmlToPictures(response.content)
        except:
            self.header['Content-Type'] = 'application/xml'
            return None

    def uploadImgURL(self, url, picSet='Supersize'):
        self.header['X-EBAY-API-CALL-NAME'] = 'UploadSiteHostedPictures'
        xmls = '<?xml version="1.0" encoding="utf-8"?>' + \
            '<UploadSiteHostedPicturesRequest xmlns="urn:ebay:apis:eBLBaseComponents">' + \
            '<ExtensionInDays>3</ExtensionInDays>' + \
            '<PictureSet>%s</PictureSet>' % (picSet) + \
            '<ExternalPictureURL>%s</ExternalPictureURL>' % (url) + \
            '<RequesterCredentials><eBayAuthToken>%s</eBayAuthToken></RequesterCredentials></UploadSiteHostedPicturesRequest>' % (self.storetoken)

        req = urllib2.Request(self.rurl, data=xmls, headers=self.header)
        resxml = urllib2.urlopen(req, timeout=60).read()
        return self.xmlToPictures(resxml)
