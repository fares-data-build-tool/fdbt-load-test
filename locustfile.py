import time
from locust import HttpUser, task, between
import json
import re
import os


email = os.getenv("FDBT_LOAD_TEST_USERNAME")
password = os.getenv("FDBT_LOAD_TEST_PASSWORD")


def form_post(l, form_page, payload):
    page_response = l.client.get(form_page)
    csrf_token_search = re.search(
        '\?_csrf=(.*?)"', page_response.text)

    if csrf_token_search:
        csrf_token = csrf_token_search.group(1)

        l.client.post("/api"+form_page+"?_csrf="+csrf_token,
                      data=payload, cookies=l.client.cookies.get_dict(), name="/api"+form_page, allow_redirects=False)


def auth(l):
    login_api_payload = {"email": email,
                         "password": password}

    form_post(l, "/login", login_api_payload)


class FDBTTest(HttpUser):
    wait_time = between(5, 10)
    cookie = ""

    @task(1)
    def single_journey(self):
        form_post(self, "/fareType", {"fareType": "single"})
        form_post(self, "/passengerType", {"passengerType": "anyone"})
        form_post(self, "/timeRestrictions", {"timeRestrictions": "no"})
        form_post(self, "/service", {"service": "47#01/07/2019"})
        form_post(self, "/singleDirection",
                  {"directionJourneyPattern": "069000022450#0600MA6021"})
        form_post(self, "/inputMethod", {"inputMethod": "manual"})
        form_post(self, "/howManyStages", {"howManyStages": "lessThan20"})
        form_post(self, "/chooseStages", {"fareStageInput": "3"})
        form_post(self, "/stageNames",
                  {"stageNameInput": ["stage1", "stage2", "stage3"]})
        form_post(self, "/priceEntry",
                  {"stage2-stage1": "100", "stage3-stage1": "120", "stage3-stage2": "140"})
        form_post(self, "/matching", {"option-0": "{\"stop\": {\"stopName\": \"Lymm Cross\", \"naptanCode\": \"wrgjtga\", \"atcoCode\": \"069000022450\", \"localityCode\": \"E0053807\", \"localityName\": \"Lymm\", \"parentLocalityName\": \"Warrington\", \"indicator\": \"opp\", \"street\": \"Rectory Lane\"}, \"stage\": \"stage1\"}",
                                      "option-1": "{\"stop\": {\"stopName\": \"Lymm Church\", \"naptanCode\": \"wrgamjd\", \"atcoCode\": \"069000013400\", \"localityCode\": \"E0042991\", \"localityName\": \"Church Green\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"opp\", \"street\": \"Church Road\"}, \"stage\": \"stage1\"}",
                                      "option-2": "{\"stop\": {\"stopName\": \"Grammar School Road\", \"naptanCode\": \"wrgamgw\", \"atcoCode\": \"069000013410\", \"localityCode\": \"E0042991\", \"localityName\": \"Church Green\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"cnr\", \"street\": \"Higher Lane\"}, \"stage\": \"stage2\"}",
                                      "option-3": "{\"stop\": {\"stopName\": \"Woodlands Avenue\", \"naptanCode\": \"wrgamjw\", \"atcoCode\": \"069000013420\", \"localityCode\": \"E0042991\", \"localityName\": \"Church Green\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"cnr\", \"street\": \"Higher Lane\"}, \"stage\": \"stage2\"}",
                                      "option-4": "{\"stop\": {\"stopName\": \"Oughtrington Lane\", \"naptanCode\": \"wrgajmg\", \"atcoCode\": \"069000013430\", \"localityCode\": \"E0042988\", \"localityName\": \"Broomedge\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"nr\", \"street\": \"Higher Lane\"}, \"stage\": \"stage3\"}",
                                      "option-5": "{\"stop\": {\"stopName\": \"Field House\", \"naptanCode\": \"wrgajgp\", \"atcoCode\": \"069000013440\", \"localityCode\": \"E0042988\", \"localityName\": \"Broomedge\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"opp\", \"street\": \"Higher Lane\"}, \"stage\": \"stage3\"}",
                                      "option-6": "{\"stop\": {\"stopName\": \"Jolly Thresher\", \"naptanCode\": \"wrgajgt\", \"atcoCode\": \"0690WNA02878\", \"localityCode\": \"E0042988\", \"localityName\": \"Broomedge\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"adj\", \"street\": \"High Legh Road\"}, \"stage\": \"stage3\"}",
                                      "service": "{\"lineName\": \"47\", \"nocCode\": \"IWBusCo\", \"operatorShortName\": \"Warrington's Own Buses\", \"serviceDescription\": \"Warrington - Lymm - High Legh - Knutsford\"}",
                                      "userfarestages": "{\"fareStages\": [{\"stageName\": \"stage1\", \"prices\": [{\"price\": \"1.00\", \"fareZones\": [\"stage2\"]}, {\"price\": \"1.20\", \"fareZones\": [\"stage3\"]}]}, {\"stageName\": \"stage2\", \"prices\": [{\"price\": \"1.40\", \"fareZones\": [\"stage3\"]}]}, {\"stageName\": \"stage3\", \"prices\": []}]}"})
        form_post(self, "/selectSalesOfferPackage", {"Awesome Product": ["{\"name\": \"Onboard (cash)\", \"description\": \"Purchasable on board the bus, with cash, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"cash\"], \"ticketFormats\": [\"paperTicket\"]}",
                                                                         "{\"name\": \"Onboard (contactless)\", \"description\": \"Purchasable on board the bus, with a contactless card or device, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"contactlessPaymentCard\"], \"ticketFormats\": [\"paperTicket\"]}"]})

    @task(2)
    def return_journey(self):
        form_post(self, "/fareType", {"fareType": "return"})
        form_post(self, "/passengerType", {"passengerType": "adult"})
        form_post(self, "/definePassengerType",
                  {"ageRange": "Yes", "ageRangeMin": "17", "ageRangeMax": "65", "passengerType": "adult"})
        form_post(self, "/timeRestrictions", {"timeRestrictions": "yes"})
        form_post(self, "/defineTimeRestrictions",
                  {"timeRestriction": "Yes", "startTime": "0600", "endTime": "1000", "validDaysSelected": "Yes", "validDays": ["monday", "tuesday", "wednesday", "thursday", "friday"]})
        form_post(self, "/service", {"service": "47#01/07/2019"})
        form_post(self, "/returnDirection",
                  {"outboundJourney": "069000022450#0600MA6021", "inboundJourney": "0600MA6021#069000022450"})
        form_post(self, "/inputMethod", {"inputMethod": "manual"})
        form_post(self, "/howManyStages", {"howManyStages": "lessThan20"})
        form_post(self, "/chooseStages", {"fareStageInput": "3"})
        form_post(self, "/stageNames",
                  {"stageNameInput": ["stage1", "stage2", "stage3"]})
        form_post(self, "/priceEntry",
                  {"stage2-stage1": "100", "stage3-stage1": "120", "stage3-stage2": "140"})
        form_post(self, "/outboundMatching", {"option-0": "{\"stop\": {\"stopName\": \"Lymm Cross\", \"naptanCode\": \"wrgjtga\", \"atcoCode\": \"069000022450\", \"localityCode\": \"E0053807\", \"localityName\": \"Lymm\", \"parentLocalityName\": \"Warrington\", \"indicator\": \"opp\", \"street\": \"Rectory Lane\"}, \"stage\": \"stage1\"}",
                                              "option-1": "{\"stop\": {\"stopName\": \"Lymm Church\", \"naptanCode\": \"wrgamjd\", \"atcoCode\": \"069000013400\", \"localityCode\": \"E0042991\", \"localityName\": \"Church Green\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"opp\", \"street\": \"Church Road\"}, \"stage\": \"stage1\"}",
                                              "option-2": "{\"stop\": {\"stopName\": \"Grammar School Road\", \"naptanCode\": \"wrgamgw\", \"atcoCode\": \"069000013410\", \"localityCode\": \"E0042991\", \"localityName\": \"Church Green\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"cnr\", \"street\": \"Higher Lane\"}, \"stage\": \"stage2\"}",
                                              "option-3": "{\"stop\": {\"stopName\": \"Woodlands Avenue\", \"naptanCode\": \"wrgamjw\", \"atcoCode\": \"069000013420\", \"localityCode\": \"E0042991\", \"localityName\": \"Church Green\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"cnr\", \"street\": \"Higher Lane\"}, \"stage\": \"stage2\"}",
                                              "option-4": "{\"stop\": {\"stopName\": \"Oughtrington Lane\", \"naptanCode\": \"wrgajmg\", \"atcoCode\": \"069000013430\", \"localityCode\": \"E0042988\", \"localityName\": \"Broomedge\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"nr\", \"street\": \"Higher Lane\"}, \"stage\": \"stage3\"}",
                                              "option-5": "{\"stop\": {\"stopName\": \"Field House\", \"naptanCode\": \"wrgajgp\", \"atcoCode\": \"069000013440\", \"localityCode\": \"E0042988\", \"localityName\": \"Broomedge\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"opp\", \"street\": \"Higher Lane\"}, \"stage\": \"stage3\"}",
                                              "option-6": "{\"stop\": {\"stopName\": \"Jolly Thresher\", \"naptanCode\": \"wrgajgt\", \"atcoCode\": \"0690WNA02878\", \"localityCode\": \"E0042988\", \"localityName\": \"Broomedge\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"adj\", \"street\": \"High Legh Road\"}, \"stage\": \"stage3\"}",
                                              "service": "{\"lineName\": \"47\", \"nocCode\": \"IWBusCo\", \"operatorShortName\": \"Warrington's Own Buses\", \"serviceDescription\": \"Warrington - Lymm - High Legh - Knutsford\"}",
                                              "userfarestages": "{\"fareStages\": [{\"stageName\": \"stage1\", \"prices\": [{\"price\": \"1.00\", \"fareZones\": [\"stage2\"]}, {\"price\": \"1.20\", \"fareZones\": [\"stage3\"]}]}, {\"stageName\": \"stage2\", \"prices\": [{\"price\": \"1.40\", \"fareZones\": [\"stage3\"]}]}, {\"stageName\": \"stage3\", \"prices\": []}]}"})
        form_post(self, "/inboundMatching", {"option-0": "{\"stop\": {\"stopName\": \"Lymm Cross\", \"naptanCode\": \"wrgjtga\", \"atcoCode\": \"069000022450\", \"localityCode\": \"E0053807\", \"localityName\": \"Lymm\", \"parentLocalityName\": \"Warrington\", \"indicator\": \"opp\", \"street\": \"Rectory Lane\"}, \"stage\": \"stage1\"}",
                                             "option-1": "{\"stop\": {\"stopName\": \"Lymm Church\", \"naptanCode\": \"wrgamjd\", \"atcoCode\": \"069000013400\", \"localityCode\": \"E0042991\", \"localityName\": \"Church Green\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"opp\", \"street\": \"Church Road\"}, \"stage\": \"stage1\"}",
                                             "option-2": "{\"stop\": {\"stopName\": \"Grammar School Road\", \"naptanCode\": \"wrgamgw\", \"atcoCode\": \"069000013410\", \"localityCode\": \"E0042991\", \"localityName\": \"Church Green\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"cnr\", \"street\": \"Higher Lane\"}, \"stage\": \"stage2\"}",
                                             "option-3": "{\"stop\": {\"stopName\": \"Woodlands Avenue\", \"naptanCode\": \"wrgamjw\", \"atcoCode\": \"069000013420\", \"localityCode\": \"E0042991\", \"localityName\": \"Church Green\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"cnr\", \"street\": \"Higher Lane\"}, \"stage\": \"stage2\"}",
                                             "option-4": "{\"stop\": {\"stopName\": \"Oughtrington Lane\", \"naptanCode\": \"wrgajmg\", \"atcoCode\": \"069000013430\", \"localityCode\": \"E0042988\", \"localityName\": \"Broomedge\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"nr\", \"street\": \"Higher Lane\"}, \"stage\": \"stage3\"}",
                                             "option-5": "{\"stop\": {\"stopName\": \"Field House\", \"naptanCode\": \"wrgajgp\", \"atcoCode\": \"069000013440\", \"localityCode\": \"E0042988\", \"localityName\": \"Broomedge\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"opp\", \"street\": \"Higher Lane\"}, \"stage\": \"stage3\"}",
                                             "option-6": "{\"stop\": {\"stopName\": \"Jolly Thresher\", \"naptanCode\": \"wrgajgt\", \"atcoCode\": \"0690WNA02878\", \"localityCode\": \"E0042988\", \"localityName\": \"Broomedge\", \"parentLocalityName\": \"Lymm\", \"indicator\": \"adj\", \"street\": \"High Legh Road\"}, \"stage\": \"stage3\"}",
                                             "service": "{\"lineName\": \"47\", \"nocCode\": \"IWBusCo\", \"operatorShortName\": \"Warrington's Own Buses\", \"serviceDescription\": \"Warrington - Lymm - High Legh - Knutsford\"}",
                                             "userfarestages": "{\"fareStages\": [{\"stageName\": \"stage1\", \"prices\": [{\"price\": \"1.00\", \"fareZones\": [\"stage2\"]}, {\"price\": \"1.20\", \"fareZones\": [\"stage3\"]}]}, {\"stageName\": \"stage2\", \"prices\": [{\"price\": \"1.40\", \"fareZones\": [\"stage3\"]}]}, {\"stageName\": \"stage3\", \"prices\": []}]}"})
        form_post(self, "/salesOfferPackages",
                  {"purchaseLocations": ["onBoard"], "paymentMethods": ["debitCard"], "ticketFormats": ["paperTicket"]})
        form_post(self, "/describeSalesOfferPackage",
                  {"salesOfferPackageName": "Load Test SoP", "salesOfferPackageDescription": "Best SoP"})
        form_post(self, "/selectSalesOfferPackage", {"Awesome Product": ["{\"name\": \"Onboard (cash)\", \"description\": \"Purchasable on board the bus, with cash, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"cash\"], \"ticketFormats\": [\"paperTicket\"]}",
                                                                         "{\"name\": \"Onboard (contactless)\", \"description\": \"Purchasable on board the bus, with a contactless card or device, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"contactlessPaymentCard\"], \"ticketFormats\": [\"paperTicket\"]}"]})

    @task(2)
    def multiservice_multiproduct_journey(self):
        form_post(self, "/fareType", {"fareType": "period"})
        form_post(self, "/passengerType", {"passengerType": "group"})
        form_post(self, "/groupSize", {"maxGroupSize": "3"})
        form_post(self, "/groupPassengerTypes",
                  {"passengerTypes": ["adult", "child"]})
        form_post(self, "/definePassengerType",
                  {"ageRange": "No", "ageRangeMin": "", "ageRangeMax": "", "passengerType": "adult", "minNumber": "0", "maxNumber": "2"})
        form_post(self, "/definePassengerType",
                  {"ageRange": "Yes", "ageRangeMin": "0", "ageRangeMax": "16", "passengerType": "child", "minNumber": "0", "maxNumber": "2", "proof": "Yes", "proofDocuments": ["studentCard", "identityDocument"]})
        form_post(self, "/timeRestrictions", {"timeRestrictions": "yes"})
        form_post(self, "/defineTimeRestrictions",
                  {"timeRestriction": "Yes", "startTime": "0600", "endTime": "1000", "validDaysSelected": "Yes", "validDays": ["friday"]})
        form_post(self, "/periodType",
                  {"periodType": "periodMultipleServices"})
        form_post(self, "/serviceList", {"47#NW_01_WBTR_47_1#01/07/2019": "Warrington - Lymm - High Legh - Knutsford",
                                         "641#NW_04_WBTR_641_1#30/08/2020": "WIGAN - SHEVINGTON MOOR via Standish",
                                         "640#NW_04_WBTR_640_1#30/08/2020": "Wigan - Shevington Circular via Standish",
                                         "613#NW_04_WBTR_613_1#30/08/2020": "NEW SPRINGS - WIGAN",
                                         "630#NW_04_WBTR_630_1#30/08/2020": "LOWER INCE - WIGAN"})
        form_post(self, "/howManyProducts", {"numberOfProductsInput": "3"})
        form_post(self, "/multipleProducts", {"multipleProductNameInput0": "product1",
                                              "multipleProductPriceInput0": "11",
                                              "multipleProductDurationInput0": "11",
                                              "multipleProductNameInput1": "product2",
                                              "multipleProductPriceInput1": "22",
                                              "multipleProductDurationInput1": "22",
                                              "multipleProductNameInput2": "product3",
                                              "multipleProductPriceInput2": "33",
                                              "multipleProductDurationInput2": "33"})
        form_post(self, "/multipleProductValidity", {"validity-row0": "24hr",
                                                     "validity-row1": "endOfCalendarDay",
                                                     "validity-row2": "24hr"})
        form_post(self, "/selectSalesOfferPackage", {"product1": ["{\"name\": \"Onboard (cash)\", \"description\": \"Purchasable on board the bus, with cash, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"cash\"], \"ticketFormats\": [\"paperTicket\"]}",
                                                                  "{\"name\": \"Onboard (contactless)\", \"description\": \"Purchasable on board the bus, with a contactless card or device, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"contactlessPaymentCard\"], \"ticketFormats\": [\"paperTicket\"]}"], "product2": ["{\"name\": \"Onboard (cash)\", \"description\": \"Purchasable on board the bus, with cash, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"cash\"], \"ticketFormats\": [\"paperTicket\"]}",
                                                                                                                                                                                                                                                                                                                                                                 "{\"name\": \"Onboard (contactless)\", \"description\": \"Purchasable on board the bus, with a contactless card or device, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"contactlessPaymentCard\"], \"ticketFormats\": [\"paperTicket\"]}"], "product3": ["{\"name\": \"Onboard (cash)\", \"description\": \"Purchasable on board the bus, with cash, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"cash\"], \"ticketFormats\": [\"paperTicket\"]}",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                "{\"name\": \"Onboard (contactless)\", \"description\": \"Purchasable on board the bus, with a contactless card or device, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"contactlessPaymentCard\"], \"ticketFormats\": [\"paperTicket\"]}"]})

    @task(1)
    def multiservice_singleproduct_journey(self):
        form_post(self, "/fareType", {"fareType": "period"})
        form_post(self, "/passengerType", {"passengerType": "group"})
        form_post(self, "/groupSize", {"maxGroupSize": "3"})
        form_post(self, "/groupPassengerTypes",
                  {"passengerTypes": ["adult", "child"]})
        form_post(self, "/definePassengerType",
                  {"ageRange": "No", "ageRangeMin": "", "ageRangeMax": "", "passengerType": "adult", "minNumber": "0", "maxNumber": "2"})
        form_post(self, "/definePassengerType",
                  {"ageRange": "Yes", "ageRangeMin": "0", "ageRangeMax": "16", "passengerType": "child", "minNumber": "0", "maxNumber": "2", "proof": "Yes", "proofDocuments": ["studentCard", "identityDocument"]})
        form_post(self, "/timeRestrictions", {"timeRestrictions": "yes"})
        form_post(self, "/defineTimeRestrictions",
                  {"timeRestriction": "Yes", "startTime": "0600", "endTime": "1000", "validDaysSelected": "Yes", "validDays": ["friday"]})
        form_post(self, "/periodType",
                  {"periodType": "periodMultipleServices"})
        form_post(self, "/serviceList", {"47#NW_01_WBTR_47_1#01/07/2019": "Warrington - Lymm - High Legh - Knutsford",
                                         "641#NW_04_WBTR_641_1#30/08/2020": "WIGAN - SHEVINGTON MOOR via Standish",
                                         "640#NW_04_WBTR_640_1#30/08/2020": "Wigan - Shevington Circular via Standish",
                                         "613#NW_04_WBTR_613_1#30/08/2020": "NEW SPRINGS - WIGAN",
                                         "630#NW_04_WBTR_630_1#30/08/2020": "LOWER INCE - WIGAN"})
        form_post(self, "/howManyProducts", {"numberOfProductsInput": "1"})
        form_post(self, "/productDetails",
                  {"productDetailsNameInput": "Awesome Product", "productDetailsPriceInput": "123"})
        form_post(self, "/chooseValidity", {"validityInput": "6"})
        form_post(self, "/periodValidity", {"periodValid": "endOfCalendarDay"})
        form_post(self, "/salesOfferPackages",
                  {"purchaseLocations": ["onBoard"], "paymentMethods": ["debitCard"], "ticketFormats": ["paperTicket"]})
        form_post(self, "/describeSalesOfferPackage",
                  {"salesOfferPackageName": "Load Test SoP", "salesOfferPackageDescription": "Best SoP"})
        form_post(self, "/selectSalesOfferPackage", {"Awesome Product": ["{\"name\": \"Onboard (cash)\", \"description\": \"Purchasable on board the bus, with cash, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"cash\"], \"ticketFormats\": [\"paperTicket\"]}",
                                                                         "{\"name\": \"Onboard (contactless)\", \"description\": \"Purchasable on board the bus, with a contactless card or device, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"contactlessPaymentCard\"], \"ticketFormats\": [\"paperTicket\"]}"]})

    @task(3)
    def flatfare_journey(self):
        form_post(self, "/fareType", {"fareType": "flatFare"})
        form_post(self, "/passengerType", {"passengerType": "anyone"})
        form_post(self, "/timeRestrictions", {"timeRestrictions": "yes"})
        form_post(self, "/defineTimeRestrictions",
                  {"timeRestriction": "Yes", "startTime": "0600", "endTime": "1000", "validDaysSelected": "Yes", "validDays": ["friday"]})
        form_post(self, "/serviceList", {"47#NW_01_WBTR_47_1#01/07/2019": "Warrington - Lymm - High Legh - Knutsford",
                                         "641#NW_04_WBTR_641_1#30/08/2020": "WIGAN - SHEVINGTON MOOR via Standish",
                                         "640#NW_04_WBTR_640_1#30/08/2020": "Wigan - Shevington Circular via Standish",
                                         "613#NW_04_WBTR_613_1#30/08/2020": "NEW SPRINGS - WIGAN",
                                         "630#NW_04_WBTR_630_1#30/08/2020": "LOWER INCE - WIGAN"})
        form_post(self, "/productDetails",
                  {"productDetailsNameInput": "Awesome Product", "productDetailsPriceInput": "123"})
        form_post(self, "/selectSalesOfferPackage", {"Awesome Product": ["{\"name\": \"Onboard (cash)\", \"description\": \"Purchasable on board the bus, with cash, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"cash\"], \"ticketFormats\": [\"paperTicket\"]}",
                                                                         "{\"name\": \"Onboard (contactless)\", \"description\": \"Purchasable on board the bus, with a contactless card or device, as a paper ticket.\", \"purchaseLocations\": [\"onBoard\"], \"paymentMethods\": [\"contactlessPaymentCard\"], \"ticketFormats\": [\"paperTicket\"]}"]})

    def on_start(self):
        self.client.get("/")
        self.cookie = auth(self)
