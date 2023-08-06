from src.thefirstock.base import *


class FirstockLogin:
    def __init__(self, loginDetails: FirstockAPI, domain, apkVersion, uid, pwd, factor2, imei, source, vc, appkey):
        self.loginDetails = loginDetails
        self.domain = domain
        self.apkVersion = apkVersion
        self.uid = uid
        self.pwd = pwd
        self.factor2 = factor2
        self.imei = imei
        self.source = source
        self.vc = vc
        self.appkey = appkey

    def firstockLogin(self):
        result = self.loginDetails.firstockLogin(self.domain, self.apkVersion, self.uid, self.pwd,
                                                 self.factor2, self.imei, self.source, self.vc, self.appkey)
        return result


class FirstockClientDetails:
    def __init__(self, clientDetails: FirstockAPI, domain, uid, jKey):
        self.clientDetails = clientDetails
        self.domain = domain
        self.uid = uid
        self.jKey = jKey

    def firstockClientDetails(self):
        result = self.clientDetails.firstockClientDetails(self.domain, self.uid, self.jKey)
        return result


class FirstockLogout:
    def __init__(self, logoutDetails: FirstockAPI, domain, uid, jKey):
        self.logoutDetails = logoutDetails
        self.domain = domain
        self.uid = uid
        self.jKey = jKey

    def firstockLogout(self):
        result = self.logoutDetails.firstockLogout(self.domain, self.uid, self.jKey)
        return result


class FirstockPlaceOrder:
    def __init__(self, placeOrder: FirstockAPI, domain, uid, actid, exch, tsym, qty, prc,
                 prd, trantype, prctyp, ret, jKey, trgprc):
        self.placeOrder = placeOrder
        self.domain = domain
        self.uid = uid
        self.actid = actid
        self.exch = exch
        self.tsym = tsym
        self.qty = qty
        self.prc = prc
        self.prd = prd
        self.trantype = trantype
        self.prctyp = prctyp
        self.ret = ret
        self.jKey = jKey
        self.trgprc = trgprc

    def firstockPlaceOrder(self):
        result = self.placeOrder.firstockPlaceOrder(self.domain, self.uid, self.actid, self.exch, self.tsym, self.qty,
                                                    self.prc, self.prd, self.trantype, self.prctyp, self.ret,
                                                    self.jKey, self.trgprc)
        return result


class FirstockGetOrderMargin:
    def __init__(self, getOrderMargin: FirstockAPI, domain, uid, actid, exch, tsym, qty, prc, prd, trantype, prctyp,
                 jKey):
        self.getOrderMargin = getOrderMargin
        self.domain = domain
        self.uid = uid
        self.actid = actid
        self.exch = exch
        self.tsym = tsym
        self.qty = qty
        self.prc = prc
        self.prd = prd
        self.trantype = trantype
        self.prctyp = prctyp
        self.jKey = jKey

    def firstockGetOrderMargin(self):
        result = self.getOrderMargin.firstockGetOrderMargin(self.domain, self.uid, self.actid, self.exch, self.tsym,
                                                            self.qty, self.prc, self.prd, self.trantype, self.prctyp,
                                                            self.jKey)
        return result


class FirstockGetBasketManagement:
    def __init__(self, getBasketManagement: FirstockAPI):
        self.getBasketManagement = getBasketManagement

    def firstockGetBasketManagement(self):
        result = self.getBasketManagement.firstockGetBasketManagement()
        return result


class FirstockOrderBook:
    def __init__(self, orderBook: FirstockAPI, domain, uid, jKey):
        self.orderBook = orderBook
        self.domain = domain
        self.uid = uid
        self.jKey = jKey

    def firstockOrderBook(self):
        result = self.orderBook.firstockOrderBook(self.domain, self.uid, self.jKey)
        return result


class FirstockCancelOrder:
    def __init__(self, cancelOrder: FirstockAPI, domain, uid, norenordno, jKey):
        self.cancelOrder = cancelOrder
        self.domain = domain
        self.uid = uid
        self.norenordno = norenordno
        self.jKey = jKey

    def firstockCancelOrder(self):
        result = self.cancelOrder.firstockCancelOrder(self.domain, self.uid, self.norenordno, self.jKey)
        return result


class FirstockModifyOrder:
    def __init__(self, modifyOrder: FirstockAPI, domain, uid, exch, norenordno, tsym, prc, jKey):
        self.modifyOrder = modifyOrder
        self.domain = domain
        self.uid = uid
        self.exch = exch
        self.norenordno = norenordno
        self.tsym = tsym
        self.prc = prc
        self.jKey = jKey

    def firstockModifyOrder(self):
        result = self.modifyOrder.firstockModifyOrder(self.domain, self.uid, self.exch, self.norenordno, self.tsym,
                                                      self.prc, self.jKey)
        return result


class FirstockSingleOrderHistory:
    def __init__(self, singleOrderHistory: FirstockAPI, domain, uid, norenordno, jKey):
        self.singleOrderHistory = singleOrderHistory
        self.domain = domain
        self.uid = uid
        self.norenordno = norenordno
        self.jKey = jKey

    def firstockSingleOrderHistory(self):
        result = self.singleOrderHistory.firstockSingleOrderHistory(self.domain, self.uid, self.norenordno, self.jKey)
        return result


class FirstockTradeBook:
    def __init__(self, tradeBook: FirstockAPI, domain, uid, actid, jKey):
        self.tradeBook = tradeBook
        self.domain = domain
        self.uid = uid
        self.actid = actid
        self.jKey = jKey

    def firstockTradeBook(self):
        result = self.tradeBook.firstockTradeBook(self.domain, self.uid, self.actid, self.jKey)
        return result


class FirstockPositionBook:
    def __init__(self, positionBook: FirstockAPI, domain, uid, actid, jKey):
        self.positionBook = positionBook
        self.domain = domain
        self.uid = uid
        self.actid = actid
        self.jKey = jKey

    def firstockPositionBook(self):
        result = self.positionBook.firstockPositionBook(self.domain, self.uid, self.actid, self.jKey)
        return result


class FirstockConvertProduct:
    def __init__(self, convertProduct: FirstockAPI, domain, exch, tsym, qty, uid, actid, prd, prevprd, trantype,
                 postype,
                 jKey):
        self.convertProduct = convertProduct
        self.domain = domain
        self.exch = exch
        self.tsym = tsym
        self.qty = qty
        self.uid = uid
        self.actid = actid
        self.prd = prd
        self.prevprd = prevprd
        self.trantype = trantype
        self.postype = postype
        self.jKey = jKey

    def firstockConvertProduct(self):
        result = self.convertProduct.firstockConvertProduct(self.domain, self.exch, self.tsym, self.qty, self.uid,
                                                            self.actid,
                                                            self.prd, self.prevprd, self.trantype, self.postype,
                                                            self.jKey)
        return result


class FirstockHoldings:
    def __init__(self, holdings: FirstockAPI, domain, uid, actid, prd, jKey):
        self.holdings = holdings
        self.domain = domain
        self.uid = uid
        self.actid = actid
        self.prd = prd
        self.jKey = jKey

    def firstockHoldings(self):
        result = self.holdings.firstockHoldings(self.domain, self.uid, self.actid, self.prd, self.jKey)
        return result


class FirstockLimits:
    def __init__(self, limits: FirstockAPI, domain, uid, actid, jKey):
        self.limits = limits
        self.domain = domain
        self.uid = uid
        self.actid = actid
        self.jKey = jKey

    def firstockLimits(self):
        result = self.limits.firstockLimits(self.domain, self.uid, self.actid, self.jKey)
        return result


class FirstockGetQuotes:
    def __init__(self, getQuotes: FirstockAPI, domain, exch, uid, jKey):
        self.getQuotes = getQuotes
        self.domain = domain
        self.uid = uid
        self.exch = exch
        self.jKey = jKey

    def firstockGetQuotes(self):
        result = self.getQuotes.firstockGetQuotes(self.domain, self.uid, self.exch, self.jKey)
        return result


class FirstockSearchScrips:
    def __init__(self, searchScrips: FirstockAPI, domain, uid, stext, jKey):
        self.searchScrips = searchScrips
        self.domain = domain
        self.uid = uid
        self.stext = stext
        self.jKey = jKey

    def firstockSearchScrips(self):
        result = self.searchScrips.firstockSearchScrips(self.domain, self.uid, self.stext, self.jKey)
        return result


class FirstockGetSecurityInfo:
    def __init__(self, getSecurityInfo: FirstockAPI, domain, uid, jKey):
        self.getSecurityInfo = getSecurityInfo
        self.domain = domain
        self.uid = uid
        self.jKey = jKey

    def firstockGetSecurityInfo(self):
        result = self.getSecurityInfo.firstockGetSecurityInfo(self.domain, self.uid, self.jKey)
        return result


class FirstockGetIndexList:
    def __init__(self, getIndexList: FirstockAPI, domain, uid, exch, jKey):
        self.getIndexList = getIndexList
        self.domain = domain
        self.uid = uid
        self.exch = exch
        self.jKey = jKey

    def firstockGetIndexList(self):
        result = self.getIndexList.firstockGetIndexList(self.domain, self.uid, self.exch, self.jKey)
        return result


class FirstockGetOptionChain:
    def __init__(self, getOptionChain: FirstockAPI, domain, uid, tsym, exch, strprc, cnt, jKey):
        self.getOptionChain = getOptionChain
        self.domain = domain
        self.uid = uid
        self.tsym = tsym
        self.exch = exch
        self.strprc = strprc
        self.cnt = cnt
        self.jKey = jKey

    def firstockGetOptionChain(self):
        result = self.getOptionChain.firstockGetOptionChain(self.domain, self.uid, self.tsym, self.exch, self.strprc,
                                                            self.cnt, self.jKey)
        return result


class FirstockSpanCalculator:
    def __init__(self, spanCalculator: FirstockAPI, domain, actid, pos, jKey):
        self.spanCalculator = spanCalculator
        self.domain = domain
        self.actid = actid
        self.pos = pos
        self.jKey = jKey

    def firstockSpanCalculator(self):
        result = self.spanCalculator.firstockSpanCalculator(self.domain, self.actid, self.pos, self.jKey)
        return result


class FirstockTimePriceSeries:
    def __init__(self, timePriceSeries: FirstockAPI, domain, uid, exch, token, jKey):
        self.timePriceSeries = timePriceSeries
        self.domain = domain
        self.uid = uid
        self.exch = exch
        self.token = token
        self.jKey = jKey

    def firstockTimePriceSeries(self):
        result = self.timePriceSeries.firstockTimePriceSeries(self.domain, self.uid, self.exch, self.token, self.jKey)
        return result


class FirstockConnection:
    def __init__(self, connection: FirstockAPI):
        self.connection = connection

    def firstockConnection(self):
        result = self.connection.firstockConnection()
        return result


class FirstockDepth:
    def __init__(self, depth: FirstockAPI):
        self.depth = depth

    def firstockDepth(self):
        result = self.depth.firstockDepth()
        return result


class FirstockOrder:
    def __init__(self, order: FirstockAPI):
        self.order = order

    def firstockOrder(self):
        result = self.order.firstockOrder()
        return result


class FirstockTouchline:
    def __init__(self, touchline: FirstockAPI):
        self.touchline = touchline

    def firstockTouchline(self):
        result = self.touchline.firstockTouchline()
        return result


class FirstockPlaceGttOrder:
    def __init__(self, placeGttOrder: FirstockAPI, domain, uid, tsym, exch, ai_t, validity, remarks, trantype, prctyp,
                 prd, ret, actid, qty, prc, jKey):
        self.placeGttOrder = placeGttOrder
        self.domain = domain
        self.uid = uid
        self.tsym = tsym
        self.exch = exch
        self.ai_t = ai_t
        self.validity = validity
        self.remarks = remarks
        self.trantype = trantype
        self.prctyp = prctyp
        self.prd = prd
        self.ret = ret
        self.actid = actid
        self.qty = qty
        self.prc = prc
        self.jKey = jKey

    def firstockPlaceGttOrder(self):
        result = self.placeGttOrder.firstockPlaceGttOrder(self.domain,
                                                          self.uid,
                                                          self.tsym,
                                                          self.exch,
                                                          self.ai_t,
                                                          self.validity,
                                                          self.remarks,
                                                          self.trantype,
                                                          self.prctyp,
                                                          self.prd,
                                                          self.ret,
                                                          self.actid,
                                                          self.qty,
                                                          self.prc,
                                                          self.jKey)
        return result


class FirstockModifyGttOrder:
    def __init__(self, modifyGttOrder: FirstockAPI, domain, uid, tsym, exch, ai_t, validity, remarks, trantype, prctyp,
                 prd, ret, actid, qty, prc, jKey):
        self.modifyGttOrder = modifyGttOrder
        self.domain = domain
        self.uid = uid
        self.tsym = tsym
        self.exch = exch
        self.ai_t = ai_t
        self.validity = validity
        self.remarks = remarks
        self.trantype = trantype
        self.prctyp = prctyp
        self.prd = prd
        self.ret = ret
        self.actid = actid
        self.qty = qty
        self.prc = prc
        self.jKey = jKey

    def firstockModifyGttOrder(self):
        result = self.modifyGttOrder.firstockModifyGttOrder(self.domain,
                                                            self.uid,
                                                            self.tsym,
                                                            self.exch,
                                                            self.ai_t,
                                                            self.validity,
                                                            self.remarks,
                                                            self.trantype,
                                                            self.prctyp,
                                                            self.prd,
                                                            self.ret,
                                                            self.actid,
                                                            self.qty,
                                                            self.prc,
                                                            self.jKey)
        return result


class FirstockCancelGttOrder:
    def __init__(self, cancelGttOrder: FirstockAPI, domain, uid, al_id, jKey):
        self.cancelGttOrder = cancelGttOrder
        self.domain = domain
        self.uid = uid
        self.al_id = al_id
        self.jKey = jKey

    def firstockCancelGttOrder(self):
        result = self.cancelGttOrder.firstockCancelGttOrder(self.domain, self.uid, self.al_id, self.jKey)
        return result


class FirstockGetPendingGttOrder:
    def __init__(self, getPendingGttOrder: FirstockAPI, domain, uid, jKey):
        self.getPendingGttOrder = getPendingGttOrder
        self.domain = domain
        self.uid = uid
        self.jKey = jKey

    def firstockGetPendingGttOrder(self):
        result = self.getPendingGttOrder.firstockGetPendingGttOrder(self.domain, self.uid, self.jKey)
        return result
