# -*- coding: utf-8 -*-

import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


class Pagination(object):
    totalpage = 1
    currpage = 1
    perpage = 100
    totalentries = 100

    def __init__(self):
        pass

    def clone(self, pagination):
        self.totalpage = pagination.totalpage
        self.currpage = pagination.currpage
        self.perpage = pagination.perpage
        self.totalentries = pagination.totalentries


class Picture(object):
    url = ''
    height = 0
    width = 0


class EBayOrder(object):

    class CheckoutStatus(object):
        paymentstatus = ''
        lastModifiedTime = ''
        paymentMethod = 'PayPal'
        status = ''
        iMCCEnabled = False
        paymentInstrument = 'CreditCard'

    class Transaction(object):
        buyer = ''
        shippingCarrier = ''
        shipmentTracking = ''
        createDate = ''
        itemid = ''
        itemSite = 'US'
        itemTitle = ''
        quantityPurchased = 0
        transactionID = ''
        price = 0.0
        tax = 0.0
        shipping = 0.0
        handling = 0.0

    orderid = ''
    status = ''
    currency = 'USD'
    adjustmentAmount = 0.0
    amountPaid = 0.0
    amountSaved = 0.0
    checkoutStatus = None
    # ShippingDetails = None
    createTime = ''
    paymentMethods = ''
    # sellerEmail = None
    shippingAddress = ''
    shippingService = ''
    shippingServiceCost = 0.0
    subtotal = 0.0
    total = 0.0  # subtotal + shipping +tax
    extendedOrderID = ''  # postOrder handling
    transactions = []
    buyerID = ''
    paidTime = ''
    shippedTime = ''
    paymentHoldStatus = ''
    sellerUserID = ''


class Money(object):
    currencyID = 'USD'
    value = 0.0


class EBaySummary(object):
    activeAuctionCount = 0
    auctionSellingCount = 0
    auctionBidCount = 0
    totalAuctionSellingValue = None  # Money
    totalSoldCount = 0
    totalSoldValue = None  # Money
    soldDurationInDays = 31  # or 30 1month
    classifiedAdCount = 0
    totalLeadCount = 0
    classifiedAdOfferCount = 0
    totalListingsWithLeads = 0
    quantityLimitRemaining = 0  # 5++
    amountLimitRemaining = None  # Money


class EBayItemInfo(object):

    class EBaySubSKU(object):
        itemid = ''
        subSKU = ''
        startPrice = 0.0
        total = 0
        sold = 0
        skutitle = ''

        def __init__(self):
            pass

    itemid = ''
    currency = 'USD'
    binPrice = 0.0
    startPrice = 0.0
    total = 0
    sold = 0
    startTime = ''
    endTime = ''
    url = ''
    currPrice = 0.0
    spPrice = 0.0
    itemtitle = ''
    available = 0
    SKU = ''
    img = ''
    subSKUs = []
    status = 'Active'
    shopName = ''

    errors = False
    ShortMessage = ''
    LongMessage = ''
    ErrorClassification = ''


class EBayUnissuedItem(object):

    class BuyerRequirementDetails(object):
        linkedPayPalAccount = 'false'
        minimumFeedbackScore = '-1'
        maximumItemCount = 5
        max_minimumFeedbackScore = 3
        shipToRegistrationCountry = 'true'

    class ReturnPolicy(object):
        returnsAcceptedOption = 'ReturnsAccepted'
        refundOption = 'MoneyBack'
        returnsWithinOption = 'Days_30'
        description = ''
        shippingCostPaidByOption = 'Buyer'

    class ShippingDetails(object):
        class SalesTax(object):
            salesTaxPercent = 0.0
            salesTaxState = 'CA'

        class ShippingServiceOptions(object):
            freeShipping = 'true'  # or true
            shippingServiceCost = 0.0
            shippingServiceAdditionalCost = 0.0
            shippingService = ''
            shippingServicePriority = 1  # 2,3 unique
            shippingSurcharge = 0.0
            shipToLocations = ''

        # CalculatedShippingRate
        originatingPostalCode = '200000'
        measurementUnit = 'English'
        packageDepth = 0
        packageLength = 0
        packageWidth = 0
        shippingPackage = ''
        weightMajor = 2
        weightMinor = 0

        paymentInstructions = 'Payment must be received within 7 business days of purchase.'
        salesTaxes = None
        shippingServiceOptions = None

        globalShipping = 'false'
        internationalShippingServiceOptions = None
        excludeShipToLocation = 'Alaska/Hawaii,APO/FPO,BO,BR,CO,EC,FK,GF,GY,PY,PE,SR,VE,BM,GL,MX,PM,DZ,AO,BJ,BW,BF,BI,CM,CV,CF,TD,KM,CD,CG,CI,DJ,EG,GQ,ER,ET,GA,GM,GH,GN,GW,KE,LS,LR,LY,MG,MW,ML,MR,'
        shippingType = 'Flat'

        def __init__(self):
            self.salesTaxes = []
            self.shippingServiceOptions = []
            self.internationalShippingServiceOptions = []

    class Variation(object):
        SKU = ''
        startPrice = 0.0
        quantity = 10
        variationSpecifics = None
        UPC = 'Does not Apply'  # '2233445566'
        EAN = 'Does not Apply'  # uk

        def __init__(self):
            self.variationSpecifics = {}

    SKU = ''
    startPrice = 0
    country = 'CN'
    location = 'Shanghai'
    currency = 'USD'
    description = '<html>aa</html>'
    dispatchTimeMax = 3
    listingDuration = 'GTC'
    listingType = 'FixedPriceItem'
    paymentMethods = 'PayPal'
    payPalEmailAddress = ''
    postalCode = ''
    primaryCategory = 'id'
    title = 'title'
    hitCounter = 'BasicStyle'
    photoDisplay = 'SuperSize'
    pictureDetail = None
    returnPolicy = None
    shippingDetails = None
    itemSpecifics = None
    variationSpecificsSet = None
    variations = None
    variationSpecificName = 'Color'
    variationSpecificPictureSets = None
    UPC = 'Does not Apply'  # '2233445566'
    EAN = 'Does not Apply'  # uk
    conditionID = 1000  # New ....1000-1499
    conditionDescription = 'New'
    quantity = 10

    # BuyerRequirementDetails
    buyerRequirementDetails = None

    autoPay = 'false'  # true or false, default false

    def __init__(self):
        self.pictureDetail = []
        self.returnPolicy = EBayUnissuedItem.ReturnPolicy()
        self.shippingDetails = EBayUnissuedItem.ShippingDetails()
        self.itemSpecifics = {}
        self.variationSpecificsSet = {}
        self.variations = []
        self.variationSpecificPictureSets = {}
        self.buyerRequirementDetails = EBayUnissuedItem.BuyerRequirementDetails()
