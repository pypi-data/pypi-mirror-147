import ast
import json
import hashlib
import requests

from src.thefirstock.base import *


class ApiRequests(FirstockAPI):
    def firstockLogin(self, domain: str, apkVersion: str, uid: str, pwd: str, factor2: str, imei: str, source: str,
                      vc: str, appkey: str):
        """
        :return: The json response
        """
        encryptedPassword = hashlib.sha256((pwd.encode()))
        keyGenerator = f"{uid}|{appkey}"
        apiKey = hashlib.sha256((keyGenerator.encode()))
        url = domain
        payload = {
            "apkversion": apkVersion,
            "uid": uid,
            "pwd": encryptedPassword.hexdigest(),
            "factor2": factor2,
            "imei": imei,
            "source": source,
            "vc": vc,
            "appkey": apiKey.hexdigest()
        }
        jsonPayload = json.dumps(payload)

        result = requests.post(url, f'jData={jsonPayload}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockClientDetails(self, domain, uid, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockLogout(self, domain, uid, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockPlaceOrder(self, domain, uid, actid, exch, tsym, qty, prc, prd, trantype, prctyp, ret, jKey,
                           trgprc):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "actid": actid,
            "exch": exch,
            "tsym": tsym,
            "qty": qty,
            "prc": prc,
            "prd": prd,
            "trantype": trantype,
            "prctyp": prctyp,
            "ret": ret,
            "trgprc": trgprc
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockGetOrderMargin(self, domain, uid, actid, exch, tsym, qty, prc,
                               prd, trantype, prctyp, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "actid": actid,
            "exch": exch,
            "tsym": tsym,
            "qty": qty,
            "prc": prc,
            "prd": prd,
            "trantype": trantype,
            "prctyp": prctyp,
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockGetBasketManagement(self, domain):
        """
        :return:
        """
        pass

    def firstockOrderBook(self, domain, uid, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockCancelOrder(self, domain, uid, norenordno, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "norenordno": norenordno
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockModifyOrder(self, domain, uid, exch, norenordno, tsym, prc, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "norenordno": norenordno,
            "exch": exch,
            "prc": prc,
            "tsym": tsym
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockSingleOrderHistory(self, domain, uid, norenordno, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "norenordno": norenordno,
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockTradeBook(self, domain, uid, actid, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "actid": actid,
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockPositionBook(self, domain, uid, actid, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "actid": actid,
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockConvertProduct(self, domain, exch, tsym, qty, uid, actid, prd, prevprd, trantype, postype,
                               jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "exch": exch,
            "tsym": tsym,
            "qty": qty,
            "actid": actid,
            "prd": prd,
            "prevprd": prevprd,
            "trantype": trantype,
            "postype": postype
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockHoldings(self, domain, uid, actid, prd, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "actid": actid,
            "prd": prd,
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockLimits(self, domain, uid, actid, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "actid": actid,
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockGetQuotes(self, domain, uid, exch, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "exch": exch
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockSearchScrips(self, domain, uid, stext, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "stext": stext
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockGetSecurityInfo(self, domain, uid, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockGetIndexList(self, domain, uid, exch, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "exch": exch
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockGetOptionChain(self, domain, uid, tsym, exch, strprc, cnt, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "exch": exch,
            "tsym": tsym,
            "strprc": strprc,
            "cnt": cnt
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockSpanCalculator(self, domain, actid, pos, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "actid": actid,
            "pos": pos
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockTimePriceSeries(self, domain, uid, exch, token, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "exch": exch,
            "token": token,
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockConnection(self):
        """
        :return:
        """
        pass

    def firstockDepth(self):
        """
        :return:
        """
        pass

    def firstockOrder(self):
        """
        :return:
        """
        pass

    def firstockTouchline(self):
        """
        :return:
        """
        pass

    def firstockPlaceGttOrder(self, domain, uid, tsym, exch, ai_t, validity, remarks, trantype, prctyp,
                 prd, ret, actid, qty, prc, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "tsym": tsym,
            "exch": exch,
            "ai_t": ai_t,
            "validity": validity,
            "remarks": remarks,
            "trantype": trantype,
            "prctyp": prctyp,
            "prd": prd,
            "ret": ret,
            "actid": actid,
            "qty": qty,
            "prc": prc
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockModifyGttOrder(self, domain, uid, tsym, exch, ai_t, validity, remarks, trantype, prctyp,
                 prd, ret, actid, qty, prc, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "tsym": tsym,
            "exch": exch,
            "ai_t": ai_t,
            "validity": validity,
            "remarks": remarks,
            "trantype": trantype,
            "prctyp": prctyp,
            "prd": prd,
            "ret": ret,
            "actid": actid,
            "qty": qty,
            "prc": prc
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockCancelGttOrder(self, domain, uid, al_id, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
            "al_id": al_id
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

    def firstockGetPendingGttOrder(self, domain, uid, jKey):
        """
        :return:
        """
        url = domain
        payload = {
            "uid": uid,
        }
        jsonPayload = json.dumps(payload)
        result = requests.post(url, f'jData={jsonPayload}&jKey={jKey}')
        jsonString = result.content.decode("utf-8")

        finalResult = ast.literal_eval(jsonString)

        return finalResult

