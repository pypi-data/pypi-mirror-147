from abc import ABC, abstractmethod


class FirstockAPI(ABC):
    @abstractmethod
    def firstockLogin(self, domain, apkVersion, uid, pwd, factor2, imei, source, vc, appkey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockClientDetails(self, domain, uid, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockLogout(self, domain, uid, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockPlaceOrder(self, domain, uid, actid, exch, tsym, qty, prc,
                           prd, trantype, prctyp, ret, jKey, trgprc):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockGetOrderMargin(self, domain, uid, actid, exch, tsym, qty, prc,
                               prd, trantype, prctyp, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockGetBasketManagement(self, domain):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockOrderBook(self, domain, uid, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockCancelOrder(self, domain, uid, norenordno, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockModifyOrder(self, domain, uid, exch, norenordno, tsym, prc, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockSingleOrderHistory(self, domain, uid, norenordno, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockTradeBook(self, domain, uid, actid, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockPositionBook(self, domain, uid, actid, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockConvertProduct(self, domain, exch, tsym, qty, uid, actid, prd, prevprd, trantype, postype,
                               jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockHoldings(self, domain, uid, actid, prd, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockLimits(self, domain, uid, actid, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockGetQuotes(self, domain, uid, exch, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockSearchScrips(self, domain, uid, stext, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockGetSecurityInfo(self, domain, uid, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockGetIndexList(self, domain, uid, exch, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockGetOptionChain(self, domain, uid, tsym, exch, strprc, cnt, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockSpanCalculator(self, domain, actid, pos, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockTimePriceSeries(self, domain, uid, exch, token, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockConnection(self):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockDepth(self):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockOrder(self):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockTouchline(self):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockPlaceGttOrder(self, domain, uid, tsym, exch, ai_t, validity, remarks, trantype, prctyp,
                 prd, ret, actid, qty, prc, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockModifyGttOrder(self, domain, uid, tsym, exch, ai_t, validity, remarks, trantype, prctyp,
                 prd, ret, actid, qty, prc, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockCancelGttOrder(self, domain, uid, al_id, jKey):
        """
        :return:
        """
        pass

    @abstractmethod
    def firstockGetPendingGttOrder(self, domain, uid, jKey):
        """
        :return:
        """
        pass
