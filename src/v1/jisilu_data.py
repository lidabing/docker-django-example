# jisilu的数据更新，
# 更新后的数据直接存放到redis数据库中，供后续使用

import requests
import os
import requests
from enum import Enum
from v1.common import *
from v1.redis_manager import redis_manager

def create_result(code, msg, data):
    return {
        "code": code,
        "msg": msg,
        "data": data
    }

#集思录的基础数据
def read_cookie_from_file(file_path):
    """
    从文件中读取cookie。

    参数:
        file_path: cookie文件的路径。

    返回:
        文件的内容。
    """
    with open(file_path, 'r') as f:
        return f.read()


def get_bond_data(url, referer):
    cookie_file = os.path.dirname(os.path.realpath(__file__)) +"/cookie.txt"
    cookie = read_cookie_from_file(cookie_file)  
    headers = {
        'Referer': referer,
        'cookie': cookie,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8,zh-HK;q=0.7,zh-TW;q=0.6,ko;q=0.5',
        'Dnt':'1',
        'If-Modified-Since':'Mon, 04 Sep 2023 11:10:38 GMT',
        'Init':'1',
        'Sec-Ch-Ua':'"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'Sec-Ch-Ua-Mobile':'?1',
        'Sec-Ch-Ua-Platform':"Android",
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response

# 功能性函数  
def get_bond_id_by_name(bond_name, all_bonds_info):
    """
    在所有转债信息中查找特定的转债代码。

    参数:
        bond_name: 要查找的转债的名称。
        all_bonds_info: 所有转债的信息。

    返回:
        如果找到了特定的转债代码,返回该代码,否则返回None。
    """
    for info in all_bonds_info:
        if bond_name in info['bond_nm']:
            return info['bond_id']
    return None

# 功能性函数，[todo]函数名称还需要修改
def get_bond_details_by_name(bond_name, all_bonds_info):
    """
    在所有转债信息中查找特定的转债详情。

    参数:
        bond_name: 要查找的转债的名称。
        all_bonds_info: 所有转债的信息。

    返回:
        如果找到了特定的转债详情,返回一个包含正股、溢价率、换手率、转股价和年华波动率的字典,否则返回None。
    """
    for info in all_bonds_info:
        if bond_name in info['bond_nm']:
            return {
                'stock': info['stock_nm'],
                'premium_rate': info['premium_rt'],
                'bond_id': info['bond_id'],
                'ref_yield_info': info['ref_yield_info'],
                #'annual_volatility': info['volatility_rt']
            }
    return None


# 转债的实时行情,
# key->realtime_bonds_market_data
def updata_realtime_bonds_market_data():
    """
    获取实时的转债市场行情。

    返回:
        实时的转债市场行情。
    """
    url = "https://www.jisilu.cn/webapi/cb/index_quote/"
    referer = 'https://www.jisilu.cn/web/data/cb/list'
    response = get_bond_data(url,referer)
    realtime_bond_market_data = []
    if response.status_code == 200:
        data = response.json()
        realtime_bond_market_data = data.get("data", [])
        new_data = create_result(response.status_code,'成功',realtime_bond_market_data)
        redis_manager.set_data('realtime_bonds_market_data',new_data)
    else:
        print(f"请求失败，状态码: {response.status_code}")
        
    
   
# 获取集思录的基础转债信息，该信息作为其他转债信息的基础，需要第一时间获取  
# key:basic_bonds
def update_basic_bonds():
    url = "https://www.jisilu.cn/webapi/cb/list/"
    referer = 'https://www.jisilu.cn/web/data/cb/list'
    
    #先获取基础转债信息
    print(f"开始获取basic bonds数据")
    response = get_bond_data(url,referer)
    bonds_data = []
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        bonds_data = data.get("data", [])
        #print(bonds_data)
        #new_data = create_result(response.status_code,'成功',bonds_data)
        redis_manager.set_data('basic_bonds',bonds_data)     
    else:
        print(f"请求失败，状态码: {response.status_code}")

# 功能函数，获取基础转债信息
def get_basic_bonds_data():
    basic_bonds_data = redis_manager.get_data("basic_bonds")
    if( basic_bonds_data == None):
           update_basic_bonds()    
    return redis_manager.get_data("basic_bonds")

# 获取集思录的基础转债信息，即将发行的转债  
# key:upcoming_bonds
def update_upcoming_bonds():
    print("update_upcoming_bonds")
    url = "https://www.jisilu.cn/webapi/cb/pre/?history=N"
    referer = 'https://www.jisilu.cn/web/data/cb/list'
    response = get_bond_data(url,referer)

    all_bonds_data = []
    if response.status_code == 200:
        data = response.json()
        all_bonds_data = data.get("data", [])
    else:
        print(f"请求失败，状态码: {response.status_code}")
        #return create_result(response.status_code,'请求失败')

    result = []
    for bond_data in all_bonds_data:
        record_dt = bond_data["record_dt"]
        apply_date = bond_data["apply_date"]
        
        if extract_date_info(record_dt) != None and compare_dates(apply_date,get_today_date()):
            bond_nm = bond_data["bond_nm"]
            bond_id = int(bond_data["bond_id"])
            stock_nm = bond_data["stock_nm"]
            stock_id = bond_data["stock_id"]
            apply_date = bond_data["apply_date"]
            record_dt = bond_data["record_dt"]
            cb_amount = bond_data["cb_amount"]
            apply10 =  bond_data["apply10"]
            amount = bond_data["amount"]
            item = {
            "bond_nm": bond_nm,
            "bond_id": bond_id,
            "stock_nm": stock_nm,
            "stock_id": stock_id,
            "apply_date": apply_date,
            "record_dt": record_dt,
            "cb_amount": cb_amount,
            "apply10": apply10,
            "amount": amount
            }        
            result.append(item)
            
    redis_manager.set_data('upcoming_bonds',result)  
    #return create_result(response.status_code,'成功',result)

#['转债名称','转债代码','收盘价','溢价率','下修日计数','到期税前收益率','剩余年限','备注']
# key->upcoming_adjust_bonds
def update_upcoming_adjust_bonds():
    basic_bonds_data = get_basic_bonds_data()
    print('update_upcoming_adjust_bonds')
     #再获取基础转债信息
    ajust_bonds_url = "https://www.jisilu.cn/webapi/cb/adjust/"
    ajust_bonds_referer = 'https://www.jisilu.cn/web/data/cb/list'
    adjust_bonds_response = get_bond_data(ajust_bonds_url,ajust_bonds_referer)
    adjust_bonds_data = []
    if adjust_bonds_response.status_code == 200:
        data = adjust_bonds_response.json()
        adjust_bonds_data = data.get("data", [])
    else:
        print(f"请求失败，状态码: {adjust_bonds_response.status_code}")
        return create_result(adjust_bonds_response.status_code,'请求失败')
    print('update_upcoming_adjust_bonds1')
    #print('data:',adjust_bonds_data)
    result = []
    print(len(basic_bonds_data))
    for adjust_bond in adjust_bonds_data:
        bond_code = adjust_bond["bond_id"]  
        #15天以内可能要下修的转债，才会记录
        adjust_count = find_property_value(adjust_bonds_data,bond_code, 'adjust_count')
        adjust = parse_adjust_string(adjust_count)
        #print(adjust)
        #print(adjust_bond)
        if adjust == None:
            continue
        if adjust[0] == 0:
            continue
        if adjust[0] > 15:
            continue
        
         #再判断收盘价，如果收盘价高于122，就不统计了
        price = find_property_value(adjust_bonds_data,bond_code, 'price')
        if price>122:
            continue
        
        bond_nm = find_property_value(adjust_bonds_data,bond_code, 'bond_nm')
        bond_id = find_property_value(adjust_bonds_data,bond_code, 'bond_id')
        #bond_id = int(bond_id)
        #price = find_property_value(all_bonds_data,bond_code, 'price')
        premium_rt = find_property_value(adjust_bonds_data,bond_code, 'premium_rt')
        #premium_rt = premium_rt/100.00

        #税前收益率,需要从other bonds里面获取
        ytm_rt = find_property_value(basic_bonds_data,bond_code, 'ytm_rt')

        #剩余到期年限
        year_left = find_property_value(basic_bonds_data,bond_code, 'year_left')

        #premium_rt_str =  str(premium_rt) + '%'
        readjust_dt = find_property_value(adjust_bonds_data,bond_code, 'readjust_dt')
        
        item = {
            "bond_nm": bond_nm,
            "bond_id": bond_id,
            "price": price,
            "premium_rt": f"{premium_rt}%",
            "adjust_count": adjust_count,
            "ytm_rt": f"{ytm_rt}%",
            "year_left": f"{year_left}"
        }        
    
        result.append(item)
    print('update_upcoming_adjust_bonds2')
    #print(result)
    redis_manager.set_data('upcoming_adjust_bonds',result)  


#['转债名称','转债代码','收盘价','溢价率','股东大会','备注']
# 已经提议下修的转债
# key->proposed_adjust_bonds
def update_proposed_adjust_bonds():
    url = 'https://www.jisilu.cn/webapi/cb/adjust/'
    referer = 'https://www.jisilu.cn/web/data/cb/adjust'
    
    response = get_bond_data(url,referer)
    bonds_data = []
    if response.status_code == 200:
        data = response.json()
        bonds_data = data.get("data", [])
    else:
        print(f"请求失败，状态码: {response.status_code}")
        #return create_result(response.status_code,'请求失败')
    
    result = []
    for bond in bonds_data:
        bond_code = bond["bond_id"]
        #print(bond_code)
        #adjust_count = find_property_value(bonds_data,bond_code, 'adjust_count')
        adjust_date = find_property_value(bonds_data,bond_code, 'adjust_date')
        #如果是过去的时间，就不统计了
        if is_past_time(adjust_date):
            continue
        
        #如果是未来三个月内的时间，设置h下修时间待定
        if is_over_three_months(adjust_date):
            adjust_date = '下修时间待定'
            
        #如果收盘价，如果收盘价高于122，就不统计了
        price = find_property_value(bonds_data,bond_code, 'price')
        if price>122:
            continue
        
        bond_nm = find_property_value(bonds_data,bond_code, 'bond_nm')
        bond_id = find_property_value(bonds_data,bond_code, 'bond_id')
    
        premium_rt = find_property_value(bonds_data,bond_code, 'premium_rt')
        #premium_rt = premium_rt/100.00
        
        item = { 
            "bond_nm": bond_nm,
            "bond_id": bond_id,
            "price": price,
            "premium_rt": f"{premium_rt}%",
            "adjust_date": adjust_date
        }        
        result.append(item)
    
    redis_manager.set_data('proposed_adjust_bonds',result)  

# 即将符合下修条件的转债
# key->upcoming_adjust_condition_bonds
def update_upcoming_adjust_condition_bonds():
    #先获取基础转债信息
    print('update_upcoming_adjust_condition_bonds')
    basic_bonds_data = get_basic_bonds_data()
    
     #再获取基础转债信息
    ajust_bonds_url = "https://www.jisilu.cn/webapi/cb/adjust/"
    ajust_bonds_referer = 'https://www.jisilu.cn/web/data/cb/list'
    adjust_bonds_response = get_bond_data(ajust_bonds_url,ajust_bonds_referer)
    adjust_bonds_data = []
    if adjust_bonds_response.status_code == 200:
        data = adjust_bonds_response.json()
        adjust_bonds_data = data.get("data", [])
    else:
        print(f"请求失败，状态码: {adjust_bonds_response.status_code}")
        #return create_result(adjust_bonds_response.status_code,'请求失败')
    print('update_upcoming_adjust_condition_bonds1')
    #['转债名称','转债代码','收盘价','溢价率','下修重算日','到期税前收益率','剩余年限','备注']
    result = []
    for bond_data in adjust_bonds_data:
        bond_code = bond_data["bond_id"]
        readjust_dt = find_property_value(adjust_bonds_data,bond_code, 'readjust_dt')
        #print(readjust_dt)
        if is_within_one_month(readjust_dt):
            bond_nm = find_property_value(adjust_bonds_data,bond_code, 'bond_nm')
            bond_id = find_property_value(adjust_bonds_data,bond_code, 'bond_id')
            premium_rt = find_property_value(adjust_bonds_data,bond_code, 'premium_rt')
            #premium_rt = premium_rt/100.00
            price = find_property_value(adjust_bonds_data,bond_code, 'price')
            
            #税前收益率,需要从other bonds里面获取
            ytm_rt = find_property_value(basic_bonds_data,bond_code, 'ytm_rt')
            #剩余到期年限
            year_left = find_property_value(basic_bonds_data,bond_code, 'year_left')

            #item = [bond_nm,int(bond_id),price,premium_rt,readjust_dt,f"{ytm_rt}%",f"{year_left}"]
            print(bond_nm)
            item = {
            "bond_nm": bond_nm,
            "bond_id": bond_id,
            "price": price,
            "premium_rt": f"{premium_rt}%",
            "readjust_dt": readjust_dt,
            "ytm_rt": f"{ytm_rt}%",
            "year_left": f"{year_left}"
            }        
            result.append(item)
        
    redis_manager.set_data('upcoming_adjust_condition_bonds',result)  


#这个函数要分析出来四种情况的转债
# 获取即将符合下修条件的转债列表
#'upcoming_adjust_condition_bonds': None,
#即将达到强制赎回条件的转债
#'upcoming_mandatory_redeem_bonds': None,
#已经满足强赎回条件的转债列表
#'mandatory_redeem_condition_bonds': None,
#已经发出强赎公告的转债列表
#'redeem_announced_bonds': None,
#转债即将自然到期,不是强赎的转债列表
#'upcoming_natural_expire_bonds': None,
class RedeemStatus(Enum):
    NOT_REDEEM_CONDITION = 0  # 未满足强赎条件
    REDEEM_CONDITION = 1  # 满足强赎条件
    REDEEM_NOTICE = 2  # 发出强赎回公告
    NOT_REDEEM_NOTICE = 3  # 发出不强赎公告
    EXPIRING_BOND = 4  # 即将到期转债


def get_redeem_status(string):
    if "已满足强赎条件" in string:
        return RedeemStatus.REDEEM_CONDITION
    if "不强赎" in string:
        return RedeemStatus.NOT_REDEEM_NOTICE
    elif "强赎" in string:
        return RedeemStatus.REDEEM_NOTICE
    elif "到期" in string:
        return RedeemStatus.EXPIRING_BOND
    else:
        return RedeemStatus.NOT_REDEEM_CONDITION #还没有达到强赎条件
  
# 获取过期相关转债，这个可以生成四张表单，分别是：
# key->upcoming_mandatory_redeem_bonds
# key->mandatory_redeem_condition_bonds
# key->redeem_announced_bonds
# key->upcoming_natural_expire_bonds    
def update_expired_bonds():
    url = "https://www.jisilu.cn/webapi/cb/redeem/"
    referer = 'https://www.jisilu.cn/data/cbnew/'
    response = get_bond_data(url,referer)

    #即将满足强赎条件的
    not_redeem_condition = []
    #宣布强赎
    redeem_notice = []
    #满足强赎条件了
    redeem_condition =  []
    # 过期转债
    expriry_bond = []
    
    redeem_bonds_data = []
    if response.status_code == 200:
        data = response.json()
        redeem_bonds_data = data.get("data", [])
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return create_result(response.status_code,'请求失败')
    
    basic_bonds_data = get_basic_bonds_data()
    
    for item in redeem_bonds_data:
        redeem_status = item["redeem_status"]
        status = get_redeem_status(redeem_status)
        premium_rt = find_property_value(basic_bonds_data,item["bond_id"],'premium_rt')
        if status == RedeemStatus.NOT_REDEEM_CONDITION:  
            number = separate_numbers(redeem_status)
            compliance_days = int(number[0])#numbers[1]-numbers[0]
            dif_days =  int(number[1])-  int(number[0])
            if compliance_days>5:
                print("即将达到强赎条件")
                cache = {
                "bond_nm": item["bond_nm"],
                "bond_id": int(item["bond_id"]),
                "price": item["price"],
                "premium_rt": f"{premium_rt}%",
                "curr_iss_amt": item["curr_iss_amt"],
                "redeem_status": redeem_status
                }        
                not_redeem_condition.append(cache)
               

        elif status == RedeemStatus.REDEEM_CONDITION:
            cache = [item["bond_nm"],int(item["bond_id"]),item["price"],premium_rt,item["curr_iss_amt"],redeem_status]
            cache = {
                "bond_nm": item["bond_nm"],
                "bond_id": int(item["bond_id"]),
                "price": item["price"],
                "premium_rt": f"{premium_rt}%",
                "curr_iss_amt": item["curr_iss_amt"],
                "redeem_status": redeem_status
                }        
            redeem_condition.append(cache)

        elif status == RedeemStatus.REDEEM_NOTICE:
            print("发出强赎公告")
            cache = {
                "bond_nm": item["bond_nm"],
                "bond_id": int(item["bond_id"]),
                "price": item["price"],
                "premium_rt": f"{premium_rt}%",
                "delist_dt": item["delist_dt"],
                "last_convert_dt": item["last_convert_dt"]
                }        
            redeem_notice.append(cache)
 

        elif status == RedeemStatus.EXPIRING_BOND:
            print("转债即将到期")
            cache = {
                "bond_nm": item["bond_nm"],
                "bond_id": int(item["bond_id"]),
                "price": item["price"],
                "premium_rt": f"{premium_rt}%",
                "delist_dt": item["delist_dt"],
                "last_convert_dt": item["last_convert_dt"]
                }        
            expriry_bond.append(cache)
    
    redis_manager.set_data('upcoming_mandatory_redeem_bonds',not_redeem_condition)
    redis_manager.set_data('mandatory_redeem_condition_bonds',redeem_condition)
    redis_manager.set_data('redeem_announced_bonds',redeem_notice)
    redis_manager.set_data('upcoming_natural_expire_bonds',expriry_bond)
    # return (
    #     create_result(200, '成功', not_redeem_condition),
    #     create_result(200, '成功', redeem_condition),
    #     create_result(200, '成功', redeem_notice),
    #     create_result(200, '成功', expriry_bond),
    # )