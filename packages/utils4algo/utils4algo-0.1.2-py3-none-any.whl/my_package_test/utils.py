import calendar
import datetime as dt
import json
import logging
import math
import smtplib
from email.message import EmailMessage
from json import JSONDecodeError

import pymongo
import pymongo.errors
import requests
from bson import ObjectId
from dateutil.relativedelta import relativedelta, TH
from log4mongo.handlers import MongoHandler
from pymongo import MongoClient
from termcolor import colored

logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger('utils_logger')
#logger.addHandler(MongoHandler(host='localhost', database_name='logs', collection='utils_atm_logs', reuse=True))
logger.addHandler(MongoHandler(host='mongodb://mongo-database:27018/', database_name='logs', collection='utils_atm_logs', reuse=True))
# TRAN_TYPE_BUY = "BUY"
# TRAN_TYPE_SELL = "SELL"
# QUANTITY = 50

# Base settings for local DB
PORT = 27018
HOST = "127.0.0.1"
# cluster = pymongo.MongoClient()
cluster = MongoClient()
db = cluster['ATM_ANALYSIS']
atm_ce = db['atm_CE_1']
atm_pe = db['atm_PE_1']
headers = {
    'Content-Type': 'application/json'
}
url = 'http://127.0.0.1:5010/options'
url_ltp = 'http://127.0.0.1:5010/get_price'
url_order_status = 'http://127.0.0.1:5010/get_order'


def send_email(subject, data):
    msg = EmailMessage()
    # import email.utils
    # os.environ["EMAIL_ADDRESS"] = "Algonotification@gmail.com"
    # os.environ["EMAIL_PASS"] = "ruiebaqymvswsdfr"
    EMAIL_ADDRESS = "Algonotification@gmail.com"
    EMAIL_PASS = "ruiebaqymvswsdfr"
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        try:
            msg['Subject'] = subject + str(dt.datetime.now())
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = "akhil.pakkath@gmail.com"
            # msg['Cc'] = "arunkk1010@gmail.com"
            msg.set_content(
                "Type\t: \t\t" + subject
                # + "\nStrike Price \t:\t" + str(data['data']['strike'])
                + "\nSymbol \t\t:\t" + str(data)
            )
            smtp.send_message(msg)
        except Exception as EX:
            logger.exception(EX)
            print("send email exception : ", EX.args)
            pass


def update_ltp(ts, option_type, id_1):
    global response, ltp
    try:
        ltp = 0
        response = requests.request("POST", url_ltp, data=ts, headers=headers)  # .json()
        ltp = json.loads(response.text.encode('utf8'))
    except JSONDecodeError:
        ltp = 0000000
        pass
    except requests.exceptions.ConnectionError as CE:
        response = ""
        logger.exception(CE)
        pass
    except NameError as NE:
        logger.exception(NE)
        ltp = 0000000
        pass
    except Exception as EX:
        print("EX : ", str(EX.args))
        logger.exception(EX)
        pass
    try:
        if response.status_code == 200 and option_type == "CE":
            try:
                atm_ce.update_one({"_id": ObjectId(id_1)},
                                  {
                                      "$set": {"last_price": ltp,
                                               "last_updated": dt.datetime.now(),
                                               },
                                      # "$push": {"order_id_test": "TESTING123",
                                      #           "test_list_1": [exit_condition]
                                      #           }

                                  }
                                  )
                return ltp
            except Exception as EX:
                print("EX : ", str(EX.args))
                logger.exception(EX)
                return 0
                pass
    except Exception as EX:
        print("EX : ", str(EX.args))
        logger.exception(EX)
        return 0
        pass
    try:
        if response.status_code == 200 and option_type == "PE":
            try:
                atm_pe.update_one({"_id": ObjectId(id_1)},
                                  {
                                      "$set": {"last_price": ltp,
                                               "last_updated": dt.datetime.now(),
                                               },
                                      # "$push": {"order_id_test": "TESTING123",
                                      #           "test_list_1": [exit_condition]
                                      #           }

                                  }
                                  )
                return ltp
            except Exception as EX:
                print("EX : ", str(EX.args))
                logger.exception(EX)
                pass
    except Exception as EX1:
        logger.exception(EX1)
        return 0
        pass
    return 0



def holiday_check(exp):
    format_exp = exp.strftime("%d-%m-%Y")
    nse_holidays = [dt.datetime(2022, 1, 26).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 3, 1).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 3, 18).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 4, 1).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 4, 14).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 4, 15).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 5, 3).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 5, 16).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 8, 9).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 8, 15).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 8, 16).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 8, 31).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 10, 5).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 10, 24).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 10, 26).strftime("%d-%m-%Y"),
                    dt.datetime(2022, 11, 8).strftime("%d-%m-%Y")
                    ]
    if format_exp in nse_holidays:
        return holiday_check(exp - dt.timedelta(days=1))
    else:
        return exp


def init_function():
    global fut_expiry, expiry_format, expiry, option_expiry, p3_fut, current_time, current_date, expiry_date, chain_data_exp
    try:
        # Calculating future expiry
        end_of_month = dt.datetime.today() + relativedelta(day=31)
        last_thursday = end_of_month + relativedelta(weekday=TH(-1))
        fut_expiry = last_thursday.strftime("%d-%m-%Y")
        if fut_expiry < dt.datetime.today().strftime("%d-%m-%Y"):
            # print("past date")
            fut_expiry = last_thursday + dt.timedelta(days=7)
            # print(fut_expiry.strftime("%d-%m-%Y"))
            end_of_month = fut_expiry + relativedelta(day=31)
            last_thursday = end_of_month + relativedelta(weekday=TH(-1))
            fut_expiry = last_thursday.strftime("%d-%m-%Y")
        # Calculating weekly expiry
        today = dt.datetime.today()
        expiry_date = today + dt.timedelta((calendar.THURSDAY - today.weekday()) % 7)
        expiry_date_1 = holiday_check(expiry_date)
        if (dt.datetime.now().strftime("%d-%m-%Y")) == expiry_date_1.strftime("%d-%m-%Y"):
            order_expiry = holiday_check(expiry_date + dt.timedelta(days=7))
        else:
            order_expiry = expiry_date_1
        expiry_format = expiry_date_1.strftime("%d-%m-%Y")
        nex_exp_format = order_expiry.strftime("%d-%m-%Y")
        current_expiry = expiry_date_1
        next_expiry = order_expiry
        # Arranging date parameter for kite connect order for monthly expiry, Need to pass symbolYYMONDDstrikeCE
        # format to kite connect
        if str(fut_expiry) == str(expiry_format):
            option_month = expiry_date_1.strftime("%b").upper()
            option_year = expiry_date_1.strftime("%y")
            option_date = expiry_date_1.strftime("%d")
            option_expiry = option_year + option_month
            chain_data_exp = option_expiry
        else:
            option_month = expiry_date_1.strftime("%-m")
            option_month = option_month[:1]
            option_date = expiry_date_1.strftime("%d")
            option_year = expiry_date_1.strftime("%y")
            option_expiry = option_year + option_month + option_date
            chain_data_exp = option_expiry
            # print("chain", chain_data_exp)
        # if current day = expiry day, order to be placed for next expiry
        if str(fut_expiry) == str(nex_exp_format):
            option_month = next_expiry.strftime("%b").upper()
            option_year = next_expiry.strftime("%y")
            option_date = next_expiry.strftime("%d")
            option_expiry = option_year + option_month
        else:
            option_month = next_expiry.strftime("%-m")
            option_month = option_month[:1]
            option_date = next_expiry.strftime("%d")
            option_year = next_expiry.strftime("%y")
            option_expiry = option_year + option_month + option_date

        expiry_kite = option_expiry
        # formatting futures expiry for kite connect
        fut_month = last_thursday.strftime("%b").upper()
        fut_year = last_thursday.strftime("%y")
        fut_expiry_kite = fut_year + fut_month
        # print("option expiry : ", option_expiry)
        fut_tradingsymbol1 = "NIFTY" + fut_expiry_kite + "FUT"
        p3_fut = '{"tradingsymbol": "' + str(fut_tradingsymbol1) + '"}'
        # print(expiry_date_1, p3_fut, expiry_kite, order_expiry, chain_data_exp)

        return current_expiry, p3_fut, option_expiry, next_expiry, chain_data_exp, fut_tradingsymbol1
    except Exception as EX1:
        logger.exception(EX1)
        print("init function excepton : ", EX1.args)
        pass


def get_ltp(ts):
    global response, ltp, india_vix
    try:
        response = requests.request("POST", url_ltp, data=ts, headers=headers)  # .json()
        ltp = json.loads(response.text.encode('utf8'))
        return ltp
    except JSONDecodeError:
        ltp = 0000000
        pass
    except requests.exceptions.ConnectionError as CE:
        response = ""
        pass
    except NameError as NE:
        logger.exception(NE)
        ltp = 0000000
        pass
    except Exception as EX:
        logger.exception(EX)
        print("EX : ", str(EX.args))
        pass

    return 0


straddles = []


def straddle_price(t1, t2):
    global t1_response, t2_response, t1_ltp, t2_ltp
    try:
        t1_response = requests.request("POST", url_ltp, data=t1, headers=headers)  # .json()
        t1_ltp = json.loads(t1_response.text.encode('utf8'))
        t2_response = requests.request("POST", url_ltp, data=t2, headers=headers)  # .json()
        t2_ltp = json.loads(t2_response.text.encode('utf8'))
        straddle_price = {t1: t1_ltp, t2: t2_ltp}
        data = {"straddle_price": straddle_price}
        straddles.append(t1_ltp)
        straddles.append(t2_ltp)
        return t1_ltp, t2_ltp
    except JSONDecodeError:
        t1_ltp = 0000000
        pass
    except requests.exceptions.ConnectionError as CE:
        response = ""
        t1_ltp = 0
        t2_ltp = 0
        pass
    except NameError as NE:
        logger.exception(NE)
        t1_ltp = 0
        t2_ltp = 0
        pass
    except Exception as EX:
        print("EX : ", str(EX.args))
        logger.exception(EX)
        t1_ltp = 0
        t2_ltp = 0
        pass


def update_futures():
    fut_data = init_function()
    future_symbol = fut_data[5]


def get_order_status(order_id):
    global response, ltp, india_vix
    try:
        response = requests.request("POST", url_order_status, data=order_id, headers=headers)  # .json()
        order_status = json.loads(response.text.encode('utf8'))
        print("oder details : ", order_status)
        return order_status
    except JSONDecodeError as JE:
        order_status = {"status": "error"}
        logger.exception(JE)
        return order_status
    except requests.exceptions.ConnectionError as CE:
        order_status = {"status": "error"}
        logger.exception(CE)
        return order_status
    except NameError as NE:
        logger.exception(NE)
        order_status = {"status": "error"}
        return order_status
    except Exception as EX:
        print("EX : ", str(EX.args))
        logger.exception(EX)
        order_status = {"status": "error"}
        return order_status


def atm_place_order(option_type, option_price, id_):
    global ltp_fut, trading_symbol, trading_symbol_straddle, json_data, response1, order_detail, order_detail, p3_order
    try:
        order_detail = {"order_id": 000000000000000, "status": "order_not_placed"}
        order_exp = init_function()
        p3_fut = order_exp[1]
        exp_option_expiry = order_exp[2]
        current_exp = order_exp[0].strftime("%d-%b-%Y")
        try:
            response_fut_price = requests.request("POST", url_ltp, data=p3_fut,
                                                  headers=headers)  # .json()
            ltp_fut = json.loads(response_fut_price.text.encode('utf8'))
        except Exception as OE2:
            logger.exception(OE2)
            print("Excetpion future price 2 ", OE2.args)
            pass
        enter_strike = (math.floor(ltp_fut / 50) * 50)
        if option_type == "PE":
            trading_symbol = "NIFTY" + exp_option_expiry + str(enter_strike) + "PE"
            trading_symbol_straddle = "NIFTY" + exp_option_expiry + str(enter_strike) + "CE"
        elif option_type == "CE":
            trading_symbol = "NIFTY" + exp_option_expiry + str(enter_strike) + "CE"
            trading_symbol_straddle = "NIFTY" + exp_option_expiry + str(enter_strike) + "PE"

        if (dt.datetime.now().strftime("%d-%m-%Y")) == order_exp[0].strftime("%d-%m-%Y"):
            trading_symbol_CE = "NIFTY" + order_exp[4] + str(enter_strike) + "PE"
            trading_symbol_straddle_PE = "NIFTY" + order_exp[4] + str(enter_strike) + "CE"
            straddle_data = [trading_symbol_CE, trading_symbol_straddle_PE]
        else:
            straddle_data = [trading_symbol, trading_symbol_straddle]

        print(trading_symbol)
        ts = '{"tradingsymbol": "' + str(trading_symbol) + '"}'
        price = get_ltp(ts)
        if price == 0 and option_type == "PE":
            price = option_price
        if price == 0 and option_type == "CE":
            price = option_price
        transaction_type = "BUY"
        quantity = 150
        p3_1 = '{"tradingsymbol": "' + str(trading_symbol) + '","expiry": "' + str(
            current_exp) + '","price": "' + str(
            price) + '", "transaction_type": "' + str(transaction_type) + '",' \
                                                                          '"quantity": "' + str(
            quantity) + '"}'
        print(p3_1)
        try:
            response1 = requests.request("POST", url, data=p3_1,
                                         headers=headers)
            print(colored("Kite connect response LBP: ", 'red'),
                  response1.status_code,
                  end="")
            print("  ", response1.text.encode('utf8'))
            # json_data = response1.text.encode('utf8')
            try:
                json_data = json.loads(response1.text.encode('utf8'))
            except Exception as JSE:
                print(JSE.args)
                logger.exception(JSE)
                json_data = response1.text.encode('utf8')
                pass
        except Exception as EX2:
            print("EX2", EX2.args)
            logger.exception(EX2)
            json_data = response1.text.encode('utf8')
            pass
        if response1.status_code == 200:
            try:
                if isinstance(json_data, int):
                    p3_order = '{"order_id": "' + str(json_data) + '"}'
                    print(p3_order)
                    kite_order_id = json_data
                    order_status = get_order_status(p3_order)
                    try:
                        order_detail = {"order_id": kite_order_id, "status": order_status['status']}
                    except Exception as EX_oder:
                        order_detail = {"order_id": kite_order_id,
                                        "status": "COMPLETE",
                                        "details": order_status,
                                        }
                        logger.exception(EX_oder, p3_order, order_detail)
                        pass
                else:
                    order_detail = {"order_id": 000000000000000, "status": "order_not_placed"}
            except Exception as E:
                logger.exception(E, p3_order, order_detail)
                pass
        if response1.status_code == 200 and option_type == "PE":
            try:
                atm_pe.update_one \
                    ({"_id": id_},
                     {"$set": {
                         "order_detail": order_detail,
                         "entry_price": price,
                         "entry_time": dt.datetime.now(),
                         "exit_flag": "N",
                         "trading_symbol": trading_symbol,
                         "trading_symbol_straddle": trading_symbol_straddle,
                     }
                     }
                     )
                print(colored("Entry Automate PE", 'green'))
            except Exception as OE2:
                print("other excetpion 2 ", OE2.args)
                logger.exception(OE2)
                pass
        if response1.status_code == 200 and option_type == "CE":
            try:
                atm_ce.update_one \
                    ({"_id": id_},
                     {"$set": {
                         "order_detail": order_detail,
                         "entry_price": price,
                         "entry_time": dt.datetime.now(),
                         "exit_flag": "N",
                         "trading_symbol": trading_symbol,
                         "trading_symbol_straddle": trading_symbol_straddle,
                     }
                     }
                     )
                print(colored("Entry Automate CE", 'green'))
            except Exception as OE2:
                print("other excetpion 2 ", OE2.args)
                logger.exception(OE2)
                pass
    except Exception as E:
        logger.exception(E)
        pass


def atm_place_exit_order(data, option_type, exit_condition, symbol, id_1, first_exit, second_exit, status):
    print("in atm exit : ", status, type, id_1, symbol)
    global exit_pe_response1, exit_flag
    if first_exit == "Y":
        exit_flag = "N"
    if second_exit == "Y":
        exit_flag = "N"
    if first_exit == "N" and second_exit == "N":
        first_exit = "Y"
        second_exit = "Y"
        exit_flag = "Y"
    try:
        # if status == "COMPLETE" or status == "OPEN" or status == "OPEN PENDING":
        if status != "REJECTED":
            exit_pe_response1 = requests.request("POST", url, data=data,
                                                 headers=headers)
            print(colored("Kite connect response LBP: ", 'red'),
                  exit_pe_response1.status_code,
                  end="")
            print("  ", exit_pe_response1.text.encode('utf8'))
    except ConnectionError as E:
        print("Connecting to Algo Trade API failed", E)
        pass
    except requests.exceptions.ConnectionError as E1:
        print("Connecting to Algo Trade API failed", E1)
        pass
    except Exception as EX:
        print("EX : ", str(EX.args))
        logger.exception(EX)
        pass
    try:
        json_data = json.loads(exit_pe_response1.text.encode('utf8'))
        exit_condition.update({"exit_order_id": json_data})
    except JSONDecodeError:
        # print("Json decode error")
        json_data = 0000000
        pass
    except NameError as NE:
        logger.exception(NE)
        json_data = 0000000
        pass
    except Exception as EX:
        print("EX : ", str(EX.args))
        logger.exception(EX)
        pass
    if option_type == "PE":
        try:
            atm_pe.update_one({"_id": ObjectId(id_1)},
                              {"$set": {"exit_flag": exit_flag,
                                        "data.exit_flag": exit_flag,
                                        "data.first_exit": first_exit,
                                        "data.second_exit": second_exit,
                                        "data.re_enter": exit_condition['re_enter'],
                                        "exit_time": dt.datetime.now(),
                                        "exit_price": exit_condition
                                        },
                               "$push": {"exit_condition": [exit_condition],
                                         }
                               }
                              )
        except pymongo.errors as Py_E:
            logger.exception(Py_E)
            print(Py_E)
            pass
        except Exception as EX:
            logger.exception(EX)
            print("EX : ", str(EX.args))
            pass
        try:
            send_email("Exit Position PE atm ", exit_condition)
        except Exception as EX:
            logger.exception(EX)
            print("EX : ", str(EX.args))
            pass
    if option_type == "CE":
        try:
            atm_ce.update_one({"_id": ObjectId(id_1)},
                              {"$set": {"exit_flag": exit_flag,
                                        "data.exit_flag": exit_flag,
                                        "data.first_exit": first_exit,
                                        "data.second_exit": second_exit,
                                        "data.re_enter": exit_condition['re_enter'],
                                        "exit_time": dt.datetime.now(),
                                        "exit_price": exit_condition
                                        },
                               "$push": {"exit_condition": [exit_condition],
                                         }
                               }
                              )
        except pymongo.errors as Py_E:
            logger.exception(Py_E)
            print(Py_E)
            pass
        except Exception as EX:
            print("EX : ", str(EX.args))
            logger.exception(EX)
            pass
        try:
            send_email("Exit Position CE atm ", exit_condition)
        except Exception as EX:
            print("EX : ", str(EX.args))
            logger.exception(EX)
            pass

