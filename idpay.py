# author : MohamadReza Hassani
# UTF-8
# Python 3.10
######################## Import Modules ########################
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import time
import sqlite3

# Central class for basic software settings
class api:
    #Global Var
    global url
    global url_verify
    global url_inquiry
    global content_type
    global id_payment
    global json_verify
    global url_transactions
    # Dynamic Var
    id_payment = ""
    json_verify = ""
    content_type = "application/json"
    order_id_ = ''
    url = "https://api.idpay.ir/v1.1/payment"
    url_verify = 'https://api.idpay.ir/v1.1/payment/verify'
    url_inquiry = 'https://api.idpay.ir/v1.1/payment/inquiry'
    url_transactions = "https://api.idpay.ir/v1.1/payment/transactions?page=0&page_size=25"

    # init Function
    def __init__(self, X_API_KEY, domain, sandbox = True):
        self.API_KEY = X_API_KEY
        self.domain = domain
        self.sandbox = sandbox

    def status_(code):
        status = {
            1: 'پرداخت انجام نشده است',
            2: 'پرداخت ناموفق بوده است',
            3: 'خطا رخ داده است',
            4: 'بلوکه شده',
            5: 'برگشت به پرداخت کننده',
            6: 'برگشت خورده سیستمی',
            7: 'انصراف از پرداخت',
            8: 'به درگاه پرداخت منتقل شد',
            10: 'در انتظار تایید پرداخت',
            100: 'پرداخت تایید شده است',
            101: 'پرداخت قبلا تایید شده است',
            200: 'به دریافت کننده واریز شد',
        }

        if code in status.keys():
            print(status[int(code)])

        else:
            print('Status Key Error. Your Resoponse not in Status Code Please Check Your Status Code Number.')


    def expections(status_code_):
        if status_code_.status_code == 200:
            print("Response 200 ! transactions Successful")

        elif status_code_.status_code == 201:
            print("Payment Successful")

        elif status_code_.status_code == 204:
            print('Error 204 ! The sent request is correct, but no transaction was found. Get to => https://idpay.ir/web-service/v1.1/#d7b83cfb9c')

        elif status_code_.status_code == 400:
            print('Error 400. The inquiry had no result. Get to => https://idpay.ir/web-service/v1.1/#d7b83cfb9c')

        elif status_code_.status_code == 403:
            print('Error 403. API Key not found. Get to => https://idpay.ir/web-service/v1.1/#d7b83cfb9c')

        elif status_code_.status_code == 405:
            print('Error 405. The transaction could not be created.. Get to => https://idpay.ir/web-service/v1.1/#d7b83cfb9c')

        elif status_code_.status_code == 406:
            print("Error 406. get to => https://idpay.ir/web-service/v1.1/#d7b83cfb9c")

        else:
            print('Unknown error...Call Admin IDPay')

    # ---> 1
    # Sending basic information to EDP servers and receiving output information to store in the database
    def payment(self, order_id, amount, callback_page, info = {}):
        global url
        global content_type
        global id_payment
        global order_id_
        headers = {
        'Content-Type': content_type,
        'X-API-KEY': self.API_KEY,
        'X-SANDBOX': '1' if self.sandbox else '0',
        }

        payload = json.dumps({
        "order_id": order_id, #required
        "amount": amount, #required
        "name" : str(info.get('name')),   #Not required
        "phone" : str(info.get('phone')),   #Not required
        "mail" : str(info.get('mail')),   #Not required
        "desc" : str(info.get('desc')),   #Not required
        "callback": self.domain + callback_page #required
        })

        response = requests.request("POST", url, headers=headers, data=payload)
        api.expections(response)
        print(response.json())
        id_payment = response.json()['id']
        order_id_ = order_id
        params = (order_id_, id_payment)
        print(id_payment, order_id_)
        #Connect To Database
        sqliteConnection = sqlite3.connect('repo.db') #Find Database & Connected
        cursor = sqliteConnection.cursor() # set Cursor
        cursor.execute("INSERT INTO orders (order_id, idpay_id) VALUES (?, ?)", params)
        sqliteConnection.commit() #Commit
        cursor.close() #Closed Database
        # return id_payment , order_id_


    def callback(satuts_code, order_id_db, transaction_id_db, order_id_server, id_server):
        if satuts_code == 10:
            # Double Spand.
            if order_id_db == order_id_server:
                if transaction_id_db == id_server:
                    print('Shoma 10 Daghighe vaght darid Ta Trakonesh Khodra Baraye IDPay Verify Konid !')
                    ques = input('Aya Mikhad Be Sorat Automatic In Kar Anjam Shavad ?[yes | no]').lower()
                    if ques == 'yes' or 'y':
                        id_input = input('Loftan IDi Khod Ra Vared Konid :')
                        order_id_input = input('Loftan Shomare Sefaresh KhodRa Vared Konid :')
                        def verify(id, order_id):
                            global url_verify
                            global content_type
                            global json_verify
                            
                            payload = json.dumps({
                                'id': str(id),
                                'order_id': str(order_id),
                            })

                            headers = {
                                'Content-Type': content_type,
                                'X-API-KEY': "Token Here",
                                'X-SANDBOX': '1',
                            }

                            response = requests.post(url_verify, data=payload, headers=headers)
                            api.expections(response)
                            print(response.json())
                            json_verify = response.json()['status']
                            api.status_(int(json_verify))
                            
                            return json_verify
                        verify(id_input, order_id_input)

                    else:
                        print('Agar Tarakonsh khodra Tayid ta 10 daghighe digar Tayid nakonid, Poli be hesab shoma variz nmishad.')
                else:
                    print('Trasaction Shoma Ba Trasaction Dakheye Database Yeki nist')
            else:
                print('Order_id shoma Ba order id Dakhele Paygah dade yeki nist.')       
        else:
            api.status_(satuts_code)






    def inquiry(self, id, order_id):
        global url_inquiry
        global content_type

        payload = json.dumps({
            'id': str(id),
            'order_id': str(order_id),
        })
        headers = {
            'Content-Type': content_type,
            'X-API-KEY': self.API_KEY,
            'X-SANDBOX': '1' if self.sandbox else '0'
        }

        response = requests.post(url_inquiry, data=payload, headers=headers)
        api.expections(response)
        print(response.json())


    def transactions(self, info={}):
        global url_transactions

        headers = {
            'Content-Type': content_type,
            'X-API-KEY': self.API_KEY,
            'X-SANDBOX': '1' if self.sandbox else '0',
            }

        payload = json.dumps({
            "id": "",
            "order_id": "",
            "amount" : "",
            "status" : "",
            "track_id" : "",
            "payment_card_no" : "",
            "payment_hashed_card_no": "",
            "track_id" : "",
            "payment_date" : "",
            "settlement_date": "",
            })


        response = requests.request("POST", url_transactions, headers=headers)


        api.expections(response)
        response.text

id = api("Token Here.", "http://localhost:8000/")
id.payment(1200 ,1000, 'dashboard')
questions = input('Aya Link Ra Moshahede Kardid ?[Yes | No ]').lower()
if questions == 'no':
    print('Pass Dobare Link Morede Nazar Ra baraye Shoma Ersam mikonam Ta Pardakht Ra anjam dahid !')
elif questions == 'yes':
    print('Montazere Tayid Pardakht Bashid !')

status_code_khod = input('Status Code : ')
order_id_dakhele_database = input('Order ID Dakhele Data Base Ra vared konid : ')
trans_action_dakhele_db = input('Transaction Dakhele Data Base Ra vared konid : ')
order_id_server_online = input('order id server Ra vared konid : ')
trans_action_server = input('Trasnaction server Ra vared konid : ')


api.callback(int(status_code_khod), order_id_dakhele_database, trans_action_dakhele_db, order_id_server_online, trans_action_server)