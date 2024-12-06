import datetime
import requests
import json
from jsonpath import jsonpath
import time
import random
import hmac
from hashlib import sha1
import random


def create_activity(data):
    env = data["env"]
    headers = data["headers"]
    body = data["body"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/activity/%s"%(env,sales_id)
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data["platform"].upper()
    response = requests.post(url,headers=headers,json=body)
    print(response.json())
    if response.status_code==200:
        activity_id = response.json()["data"]
        return activity_id
    else:
        return response

def delate_activity(data):
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    url = "%s/api/activity/%s" % (env, activity_id)
    response = requests.delete(url,headers=headers).json()
    return response

def start_activity(data):
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    url = "%s/api/activity/%s/start" % (env, activity_id)
    response = requests.post(url,headers=headers).json()
    return response

def end_activity(data):
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    url = "%s/api/activity/%s/end" % (env, activity_id)
    response = requests.post(url, headers=headers).json()
    return response

def send__live_comment(data):
    env = data["env"]
    key = data["key"]
    platform = "FACEBOOK"
    page_id = ""
    post_id = ""
    group_id = ""

    if "page_id" in data:
        page_id = data['page_id']
    if "platform" in data:
        platform = data['platform']
    if "post_id" in data:
        post_id = data['post_id']
    if "group_id" in data:
        post_id = data['group_id']
    if page_id == "" or post_id == "":
        info = get_live_info(data)
        platform_list = jsonpath(info, "$..relatedPostList..platform")
        i = platform_list.index(platform.upper())
        page_id = info["data"]["relatedPostList"][i]["page_id"]
        platform = info["data"]["relatedPostList"][i]["platform"]
        post_id = info["data"]["relatedPostList"][i]["post_id"]
        group_id = info["data"]["relatedPostList"][i]["group_id"]
    # info = get_live_info(data)
    # related_post_list = info["data"]["relatedPostList"][0]
    # page_id = related_post_list["page_id"]
    # post_id = related_post_list["post_id"]
    # platform = related_post_list["platform"]
    stamp = int(time.time())
    num = random.randint(100000, 999999)
    user_id = "488864%d" % int(time.time())
    if "user_id" in data:
        user_id = data['user_id']
    name = "test live%d" % int(time.time())
    if "name" in data:
        name = data['name']
    comment_id = "%s_%d%d" % (page_id, stamp, num)
    if "comment_id" in data:
        comment_id = data['comment_id']
    keyword = "接口测试普通留言"
    if "keyword" in data:
        keyword = data['keyword']
    body = {"object": "page", "entry": [{"id": page_id, "time": stamp, "changes": [{"field": "feed", "value": {
            "from": {"id": user_id, "name": name},
            "post": {"status_type": "added_video", "is_published": True, "updated_time": "2022-11-18T09:57:26+0000",
                     "permalink_url": "https://www.facebook.com/permalink.php?story_fbid=pfbid02jLK3e6YdFSXp2DmD7j7vtStLXoBzTi8rxKrp6jFhVMUTTEgz6qvZA8soR9Uwydd8l&id=107977035056574",
                     "promotion_status": "inactive", "id": post_id}, "message": keyword, "item": "comment",
            "verb": "add", "post_id": post_id, "comment_id": comment_id,
            "created_time": stamp, "parent_id": post_id}}]}]}

    if platform.upper() == "INSTAGRAM":
        body = {"entry": [{"id": page_id, "time": stamp, "changes": [{"value": {"from": {"id": user_id,
                 "username": name},
                  "media": {"id": post_id,
                   "media_product_type": "FEED"},
                "id": comment_id, "text": keyword},
                   "field": "comments"}]}], "object": "instagram"}
    elif platform.upper() == "FB_GROUP":
        t_time = stamp*1000
        post_id = post_id.split("_")[-1]
        comment_id = "%d%d" % ( stamp, num)
        body = {"object":"page","entry":[{"id":page_id,"time":t_time,"messaging":[{"recipient":{"id":page_id},"message":keyword,
        "from":{"id":user_id,"name":name},"group_id":group_id,"post_id":post_id,"comment_id":comment_id,"created_time":stamp,"item":"comment",
         "verb":"add","parent_id":post_id,"field":"group_feed"}]}]}

    print(body)
    url = "%s/facebook/webhook" % env
    sign_text = hmac.new(key.encode("utf-8"), json.dumps(body).encode("utf-8"), sha1)
    signData = sign_text.hexdigest()
    # print("body", json.dumps(body))
    header = {"Content-Type": "application/json", "x-hub-signature": "sha1=%s" % signData}
    response = requests.post(url, headers=header, data=json.dumps(body))
    print(response.text)
    return user_id, name, comment_id

def send_mc_message(data):
    env = data["env"]
    key = data["key"]
    stamp = int(time.time()*1000)
    user_id = "488864%d" % int(time.time())
    type = "commment"
    payload = "{}"
    if "payload" in data:
        payload = data["payload"]
    if "type" in data:
        type = data["type"]
    if "user_id" in data:
        user_id = data['user_id']
    name = "test live%d" % int(time.time())
    if "name" in data:
        name = data['name']
    message = "接口测试普通留言"
    if "message" in data:
        message = data['message']
    page_id = ""
    if "page_id" in data:
        page_id = data['page_id']
    platform = "FACEBOOK"
    if "platform" in data:
        platform = data['platform']
    if page_id=="":
        info = get_live_info(data)
        platform_list = jsonpath(info, "$..relatedPostList..platform")
        i = platform_list.index(platform)
        page_id = info["data"]["relatedPostList"][i]["page_id"]
        platform = info["data"]["relatedPostList"][i]["platform"]
    mid = "m_hhAqPhSlMTY4En2oWjSB59T3BFjeU97DdDV4WHr3DLWnPrO0iCsjQlG3hBN%d-sBlT26-6oNg" % stamp
    body = {"entry": [{"id": "%s" % page_id, "messaging": [{"message":
      {
       "mid": mid,
        "text": "%s" % message},
         "recipient": {"id": "%s" % page_id},
         "sender": {"id": "%s" % user_id}, "timestamp": stamp}],
         "time": stamp}], "object": "page"}
    # if platform.upper()=="FACEBOOK":
    #     body = {"entry":[{"id":"%s"%page_id,"messaging":[{"message":
    #     {"mid":"m_hhAqPhSlMTY4En2oWjSB59T3BFjeU97DdDV4WHr3DLWnPrO0iCsjQlG3hBN%d-sBlT26-6oNg"%stamp,"text":"%s"%message},
    #     "recipient":{"id":"%s"%page_id},"sender":{"id":"%s"%user_id},"timestamp":stamp}],"time":stamp}],"object":"page"}
    if platform.upper()=="INSTAGRAM":
        body={"object":"instagram","entry":[{"time":stamp,"id":"%s"%page_id,"messaging":[{"sender":{"id":"%s"%user_id},"recipient":{"id":"%s"%page_id},
       "timestamp":stamp,"message":{"mid":"aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDUwMzgwODgwNTMzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI3NjAyNDExMzcwMDc2NTA5MDozMTgzODU0Mzg3NTY4MDYwMTE3ODUxOTE2MD%d"%stamp,"text":"%s"%message}}]}]}
    elif type=="postback" and platform.upper() in ("FB_GROUP","FACEBOOK"):
        # t_time = stamp * 1000
        body = {"object":"page","entry":[{"time":stamp,"id":"%s"%page_id,"messaging":[{"sender":{"id":"%s"%user_id},"recipient":{"id":"%s"%page_id},"timestamp":stamp,"postback":{"title":"继续 ➡️","payload":payload,"mid":"m_w6KNGd0PMndK0LvCw7Hzy1zsVSWT0fpN3ievQ9LtB0NxnnTQGDMyKI5DFeVbaJIRni1cqqJYXIJ-wq98aw%d"%stamp}}]}]}
    elif type=="postback" and platform.lower()=="instagram":
        body = {"object": "instagram", "entry": [{"time": stamp, "id": "%s" % page_id, "messaging": [
            {"sender": {"id": "%s" % user_id}, "recipient": {"id": "%s" % page_id}, "timestamp": stamp,
             "postback": {"title": "继续 ➡️", "payload": payload,
                          "mid": "m_w6KNGd0PMndK0LvCw7Hzy1zsVSWT0fpN3ievQ9LtB0NxnnTQGDMyKI5DFeVbaJIRni1cqqJYXIJ-wq98aw%d" % stamp}}]}]}

    url = "%s/facebook/webhook" % env
    sign_text = hmac.new(key.encode("utf-8"), json.dumps(body).encode("utf-8"), sha1)
    signData = sign_text.hexdigest()
    header = {"Content-Type": "application/json", "x-hub-signature": "sha1=%s" % signData}
    response = requests.post(url, headers=header, data=json.dumps(body))
    # print(response.text)
    print(body)
    return user_id, name



def get_live_info(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s" % (env, sales_id)
    response = requests.get(url,headers=headers).json()
    return response



def get_activity_detail(data):
    """
    type:
    luckyDraw,抽奖活动
    voucher--留言抢优惠
    answerFirst--抢答
    bidding--竞标
    vote:投票
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    activity_id = data["activity_id"]
    type = data["type"]
    url = ""
    if type in "luckyDraw":
        url = "%s/api/activity/luckyDraw/%s"% (env, activity_id)
    elif type in "voucher":
        url = "%s/api/activity/voucher/%s" % (env, activity_id)
    elif type in "answerFirst":
        url = "%s/api/activity/answerFirst/%s" % (env, activity_id)
    elif type in "bidding":
        url = "%s/api/activity/bidding/%s" % (env, activity_id)
    elif type in "vote":
        url = "%s/api/activity/vote/%s" % (env, activity_id)
    response = requests.get(url,headers=headers).json()
    return response

def live_search_oa_gift(data):
    """
    查询oa赠品，命名转为驼峰和返回第一个赠品的信息
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/gifts"%env
    params = {"page":1}
    response = requests.get(url,headers=headers,params=params).json()
    items = response["data"]["items"]

    if items == []:
        # 新增赠品
        body = {"unlimited_quantity": True, "title_translations": {"zh-cn": "接口自动化新增的赠品%s" % int(time.time())},
                "media_ids": "610d2865ca92cf00264c563c"}
        requests.post(url, headers=headers, json=body).json()
        time.sleep(5)
        #新增后去查询
        response = requests.get(url, headers=headers, params=params).json()
        items = response["data"]["items"]

    # 返回数量不是0的赠品和spu_id
    # print(json.dumps(items))
    quantityList = jsonpath(items,"$..quantity")
    gift_info = items[0]
    for a,b in enumerate(quantityList):
        if b!=0:
            gift_info = items[a]
    spu_id = gift_info["id"]
    return spu_id,gift_info,response

def live_search_oa_product(data):
    """
    查询OA的商品，并返回响应,返回第一个有库存的商品
    spu:返回无规格
    sku:返回多规格
    quantity:0 返回无库存商品
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/products?page=1&per_page=50" %env
    type = "spu"
    quantity = 100
    if "type" in data:
        type = data["type"]
    if "quantity" in data:
        quantity = data["quantity"]
    if "query" in data:
        query = data["query"]
        url = "%s/openApi/proxy/v1/products?page=1&per_page=4&query=%s" % (env,query)
    response = requests.get(url, headers=headers).json()
    items = response["data"]["items"]
    variant_options_list = jsonpath(items,"$..variations")
    product_info = ""
    spu_id = ""
    sku_id = ""
    sku_id_quantity =[]
    for a, b in enumerate(variant_options_list):
        if type=="spu" and b==[] and quantity!=0:
            quantitys=items[a]["total_orderable_quantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys!=0 or unlimited_quantity==True:
                product_info=items[a]
                spu_id = items[a]["id"]
                break
        elif type=="sku" and b!=[] and quantity!=0:
            quantitys = items[a]["total_orderable_quantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys!=0 or unlimited_quantity==True:
                product_info = items[a]
                spu_id = items[a]["id"]
                sku_id = jsonpath(items[a]["variations"],"$..id")
                sku_id_quantity = jsonpath(items[a]["variations"],"$..total_orderable_quantity")
                break
        elif type == "spu" and b == [] and quantity == 0:
            quantitys = items[a]["total_orderable_quantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys != 0 or unlimited_quantity == True:
                product_info = items[a]
                spu_id = items[a]["id"]
                break
        elif type == "sku" and b != [] and quantity == 0:
            quantitys = items[a]["total_orderable_quantity"]
            unlimited_quantity = items[a]["unlimited_quantity"]
            if quantitys != 0 or unlimited_quantity == True:
                product_info = items[a]
                spu_id = items[a]["id"]
                sku_id = jsonpath(items[a]["variations"], "$..id")
                sku_id_quantity = jsonpath(items[a]["variations"], "$..total_orderable_quantity")
                break
    return spu_id,sku_id,sku_id_quantity,product_info



def get_merchant_info(data):
    env = data["env"]
    headers = data["headers"]
    merchant_id = data["merchant_id"]
    url = "%s/openApi/proxy/v1/merchants/%s" % (env,merchant_id)
    response = requests.get(url, headers=headers).json()
    base_country_code = response["data"]["base_country_code"]
    default_language_code = response["data"]["default_language_code"]
    currency = ""
    if base_country_code=="TW":
        currency="NT$"
    elif base_country_code=="TH":
        currency = "฿"
    elif base_country_code == "VN":
        #放金额后面
        currency = "₫"
    return base_country_code,currency,response

def delete_broadcast(data):
    env = data["env"]
    headers = data["headers"]
    broadcast_id = data["broadcast_id"]
    url = "%s/admin/api/bff-web/live/broadcast/%s"%(env,broadcast_id)
    response = requests.delete(url,headers=headers).json()
    return response

def get_broadcast_list(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    name = ""
    platform= data["platform"]
    broadcast_id = ""
    pageNum = 1
    pageSize = 12
    if "pageNum" in data:
        pageNum = data["pageNum"]
    if "pageSize" in data:
        pageSize = data["pageSize"]
    if "name" in data:
        name= data["name"]
    url = "%s/admin/api/bff-web/live/broadcast/query"%env
    body = {
    "businessId": "%s"%sales_id,
    "businessType": "LIVE",
    "businessSubType": "LIVE_STREAM",
    "platform": "%s"%platform,
    "pageNum": pageNum,
    "pageSize": pageSize
    }
    reponse = requests.post(url,headers=headers,json=body).json()
    if name !="":
        name_list = jsonpath(reponse,"$..name")
        broadcast_id_list = jsonpath(reponse,"$..id")
        for i,value in enumerate(name_list):
            if value==name:
                broadcast_id =broadcast_id_list[i]
    return broadcast_id,reponse

def get_broadcast_detail(data):
    env = data["env"]
    headers = data["headers"]
    broadcast_id = data["broadcast_id"]
    platform = data["platform"]
    url = "%s/admin/api/bff-web/live/broadcast/detail"%env
    body = {
    "id": "%s"%broadcast_id,
    "platform": "%s"%platform
        }
    response = requests.post(url,headers=headers,json=body).json()
    return response

def end_live(data):
    """结束帖文"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s/end" % (env, sales_id)
    response = requests.put(url, headers=headers).json()
    return response

def get_channel(data):
    "查询粉丝页信息，用于创建帖文"
    env = data["env"]
    headers = data["headers"]
    platform = data["platform"]
    url = "%s/api/posts/post/sales/multiPlatformChannelList?platformList=%s"%(env,platform.upper())
    response = requests.get(url,headers=headers).json()
    return response



def create_live(data):
    """创建直播，不套用通用配置"""
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/live/sales" % (env)
    stamp = int(time.time())
    title = "接口创建的直播活动名称%d"%stamp
    salesDescription = "接口创建的直播活动介绍%d"%stamp
    salesOwner =  "接口创建的直播主%d"%stamp
    platform = "FB_GROUP"
    patternModel = "INCLUDE_MATCH"
    keywordValidInLive = True
    keywordValidAfterLive =False
    autoNotifyPayEnable = False
    autoNotifyPayMessage = ""
    autoNotifyPayButton = ""
    autoNotifyPayTime = None
    stockEnable = False
    stockIime = None
    lowOfQuantityEnable = False
    lowOfQuantitySound = False
    lowOfQuantityQuantity = "1"
    has_interaction_message = ""
    has_interaction_message_button = ""
    no_interaction_message_first = ""
    second_message = ""
    first_message_button = ""
    second_message_button = " ️"
    need_send_message = True
    has_link = True
    startTime = None
    # endTime = datetime.datetime.now()+datetime.timedelta(days=3)
    endTime = None
    if "title" in data:
        title = data["title"]
    if "salesDescription" in data:
        title = data["salesDescription"]
    if "salesOwner" in data:
        salesOwner = data["salesOwner"]
    if "platform" in  data:
        platform = data["platform"]
    if "patternModel" in data:
        patternModel = data["patternModel"]
    if "keywordValidInLive" in data:
        keywordValidInLive = data["keywordValidInLive"]
    if "keywordValidAfterLive" in data:
        keywordValidAfterLive = data["keywordValidAfterLive"]

    if "autoNotifyPayEnable" in data:
        autoNotifyPayEnable = data["autoNotifyPayEnable"]
    if "autoNotifyPayMessage" in data:
        autoNotifyPayMessage = data["autoNotifyPayMessage"]
    if "autoNotifyPayButton" in data:
        autoNotifyPayButton = data["autoNotifyPayButton"]
    if "autoNotifyPayTime" in data:
        autoNotifyPayTime = data["autoNotifyPayTime"]

    if "stockEnable" in data:
        stockEnable = data["stockEnable"]
    if "stockIime" in data:
        stockIime = data["stockIime"]

    if "lowOfQuantityEnable" in data:
        lowOfQuantityEnable = data["lowOfQuantityEnable"]
    if "lowOfQuantitySound" in data:
        lowOfQuantitySound = data["lowOfQuantitySound"]
    if "lowOfQuantityQuantity" in data:
        lowOfQuantityQuantity = data["lowOfQuantityQuantity"]

    if "has_interaction_message" in data:
        has_interaction_message = data["has_interaction_message"]
    if "has_interaction_message_button" in data:
        has_interaction_message_button = data["has_interaction_message_button"]
    if "no_interaction_message_first" in data:
        no_interaction_message_first = data["no_interaction_message_first"]
    if "first_message_button" in data:
        first_message_button = data["first_message_button"]
    if "second_message" in data:
        second_message = data["second_message"]
    if "second_message_button" in data:
        second_message_button = data["second_message_button"]
    if "need_send_message" in data:
        need_send_message = data["need_send_message"]
    # if "message_button" in data:
    #     message_button = data["message_button"]
    if "has_link" in data:
        has_link = data["has_link"]
    # platform = platform.upper()
    body = {}
    if platform.lower() in ("fb_group","facebook","instagram"):
        body = {
        "sales": {
            "title": title,
            "salesOwner": salesOwner,
            "salesDescription": salesDescription,
            "platforms": [
                platform
            ],
            "platformChannels": [],
            "startTime": startTime,
            "endTime": endTime
        },
        "salesConfig": {
            "patternModel": {
                "patternModel": patternModel,
                "keywordValidInLive": keywordValidInLive,
                "keywordValidAfterLive": keywordValidAfterLive
            },
            "autoNotifyPay": {
                "enable": autoNotifyPayEnable,
                "message": autoNotifyPayMessage,
                "button": autoNotifyPayButton
            },
            "stock": {
                "lockStock": stockEnable,
                "salesStockLockExpireTime": stockIime
            },
            "lowOfQuantity": {
                "enable": lowOfQuantityEnable,
                "sound": lowOfQuantitySound,
                "quantity": lowOfQuantityQuantity
            }
            },
            "postConfigMap": {
                platform: {
                    "message": {
                        "needSendMessage": need_send_message,
                        "hasInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": has_interaction_message
                            },
                            "messageButton": has_interaction_message_button
                        },
                        "hasLink": has_link,
                        "noInteractionMessage": {
                            "firstMessageTemplate": {
                                "topMessage": no_interaction_message_first
                            },
                            "firstMessageButton": first_message_button,
                            "secondMessageTemplate": {
                                "topMessage": second_message
                            },
                            "secondMessageButton": second_message_button
                        },
                        "messageType": "MESSAGE"
                    }
                }
            }
        }
    elif platform in ("pl&fb" ,"obc&fb") :
        platformSubType = platform.split("&")[0].upper()
        data["platform"] = "FACEBOOK"
        res = get_channel(data)
        body = {
        "sales": {
            "title": title,
            "salesOwner": salesOwner,
            "salesDescription": salesDescription,
            "platforms": [
                "SHOPLINE",
                "FACEBOOK"
            ],
            "platformSubType": platformSubType,
            "platformChannels": [
                res["data"][0]
            ],
            "startTime":startTime ,
            "endTime": endTime
        },
        "salesConfig": {
            "patternModel": {
                "patternModel": patternModel,
                "keywordValidInLive": keywordValidInLive,
                "keywordValidAfterLive": keywordValidAfterLive
            },
            "autoNotifyPay": {
                "enable": autoNotifyPayEnable,
                "message": autoNotifyPayMessage,
                "button": autoNotifyPayButton,
                "notifyTime": autoNotifyPayTime
            },
            "stock": {
                "lockStock": stockEnable,
                "salesStockLockExpireTime": stockIime
            },
            "lowOfQuantity": {
                "enable": lowOfQuantityEnable,
                "sound": lowOfQuantitySound,
                "quantity": lowOfQuantityQuantity
            }
        },
        "postConfigMap": {
            "FACEBOOK": {
                "message": {
                    "needSendMessage": need_send_message,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": has_interaction_message
                        },
                        "messageButton": has_interaction_message_button
                    },
                    "hasLink": has_link,
                    "noInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": no_interaction_message_first
                        },
                        "firstMessageButton": first_message_button,
                        "secondMessageButton": second_message_button,
                        "secondMessageTemplate": {
                            "topMessage": second_message
                        }
                    },
                    "messageType": "MESSAGE"
                }
            },
            "SHOPLINE": {
                "message": {
                    "needSendMessage": need_send_message,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": has_interaction_message
                        },
                        "messageButton": has_interaction_message_button
                    },
                    "hasLink": has_link,
                    "noInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": no_interaction_message_first
                        },
                        "firstMessageButton": first_message_button,
                        "secondMessageButton": second_message_button,
                        "secondMessageTemplate": {
                            "topMessage": second_message
                        }
                    },
                    "messageType": "MESSAGE"
                    }
                }
            }
        }
    elif platform in ("pl","obc"):
        platformSubType = platform.upper()
        platform = "SHOPLINE"
        body = {
        "sales": {
            "title": title,
            "salesOwner": salesOwner,
            "salesDescription": salesDescription,
            "platforms": [
                platform
            ],
            "platformChannels": [],
            "startTime": startTime,
            "endTime": endTime,
            "platformSubType":platformSubType
        },
        "salesConfig": {
            "patternModel": {
                "patternModel": patternModel,
                "keywordValidInLive": keywordValidInLive,
                "keywordValidAfterLive": keywordValidAfterLive
            },
            "autoNotifyPay": {
                "enable": autoNotifyPayEnable,
                "message": autoNotifyPayMessage,
                "button": autoNotifyPayButton
            },
            "stock": {
                "lockStock": stockEnable,
                "salesStockLockExpireTime": stockIime
            },
            "lowOfQuantity": {
                "enable": lowOfQuantityEnable,
                "sound": lowOfQuantitySound,
                "quantity": lowOfQuantityQuantity
            }
            },
            "postConfigMap":{}
        }
    response = requests.post(url,headers=headers,json=body).json()
    # print(json.dumps(body))
    print(response)
    sales_id = response["data"]["sales"]["id"]
    return sales_id


def add_live(data):
    """fb——group 链接帖文"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s/addLive"%(env,sales_id)
    pageId = data["page_id"]
    relationUrl = data["relationUrl"]

    body = {
        "pageId": pageId,
        "platform": "FB_GROUP",
        "relationUrl": relationUrl
    }
    response = requests.post(url,headers=headers,json=body).json()
    return response


def get_live_info(data):
    """查询直播间信息"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s" % (env, sales_id)
    response = requests.get(url,headers=headers).json()
    return response

def edit_live_info(data):
    """
    直播前编辑直播间信息:prepare
    直播中编辑直播间信息:progress
    """
    stamp = int(time.time())
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/live/sales/%s" % (env, sales_id)
    title = "接口编辑的直播活动名称%d" % stamp
    salesDescription = "接口编辑的直播活动介绍%d" % stamp
    salesOwner = "接口编辑的直播主%d" % stamp
    patternModel = "INCLUDE_MATCH"
    keywordValidInLive = True
    keywordValidAfterLive = False
    autoNotifyPayEnable = False
    autoNotifyPayMessage = ""
    autoNotifyPayButton = ""
    autoNotifyPayTime = None
    stockEnable = False
    stockPreTime = None
    stockExpireTime = None
    lowOfQuantityEnable = False
    lowOfQuantitySound = False
    lowOfQuantityQuantity = "1"
    has_interaction_message = ""
    has_interaction_message_button = ""
    no_interaction_message_first = ""
    second_message = ""
    first_message_button = ""
    second_message_button = " ️"
    need_send_message = True
    has_link = True
    commentIntent = True
    #无库存讯息
    allOutOfStockMessage = ""
    allOutOfStockEnable = True
    #欢迎讯息
    welcomeMessage = ""
    welcomeMessageEnable = True
        # 欢迎comment
    welcomeComment = ""
    welcomeCommentEnable = True
    productRecommendMessage = ""
    productRecommendMessageEnable = True
    platform = "FB_GROUP"
    type = "prepare"
    if "type" in data:
        type = data["type"]
    if "title" in data:
        title = data["title"]
    if "salesDescription" in data:
        title = data["salesDescription"]
    if "salesOwner" in data:
        title = data["salesOwner"]
    if "platform" in data:
        platform = data["platform"]
    if "patternModel" in data:
        patternModel = data["patternModel"]
    if "keywordValidInLive" in data:
        keywordValidInLive = data["keywordValidInLive"]
    if "keywordValidAfterLive" in data:
        keywordValidAfterLive = data["keywordValidAfterLive"]
    if "autoNotifyPayEnable" in data:
        autoNotifyPayEnable = data["autoNotifyPayEnable"]
    if "autoNotifyPayMessage" in data:
        autoNotifyPayMessage = data["autoNotifyPayMessage"]
    if "autoNotifyPayButton" in data:
        autoNotifyPayButton = data["autoNotifyPayButton"]
    if "autoNotifyPayTime" in data:
        autoNotifyPayTime = data["autoNotifyPayTime"]
    if "stockEnable" in data:
        stockEnable = data["stockEnable"]
    if "stockExpireTime" in data:
        stockExpireTime = data["stockExpireTime"]
    if "lowOfQuantityEnable" in data:
        lowOfQuantityEnable = data["lowOfQuantityEnable"]
    if "lowOfQuantitySound" in data:
        lowOfQuantitySound = data["lowOfQuantitySound"]
    if "lowOfQuantityQuantity" in data:
        lowOfQuantityQuantity = data["lowOfQuantityQuantity"]
    if "has_interaction_message" in data:
        has_interaction_message = data["has_interaction_message"]
    if "has_interaction_message_button" in data:
        has_interaction_message_button = data["has_interaction_message_button"]
    if "no_interaction_message_first" in data:
        no_interaction_message_first = data["no_interaction_message_first"]
    if "first_message_button" in data:
        first_message_button = data["first_message_button"]
    if "second_message" in data:
        second_message = data["second_message"]
    if "second_message_button" in data:
        second_message_button = data["second_message_button"]
    if "need_send_message" in data:
        need_send_message = data["need_send_message"]
    # if "message_button" in data:
    #     message_button = data["message_button"]
    if "has_link" in data:
        has_link = data["has_link"]
    if "commentIntent" in data:
        commentIntent = data["commentIntent"]
    if "allOutOfStockMessage" in data:
        allOutOfStockMessage = data["allOutOfStockMessage"]
    if "allOutOfStockEnable" in data:
        allOutOfStockEnable = data["allOutOfStockEnable"]
    if "welcomeMessage" in data:
        welcomeMessage = data["welcomeMessage"]
    if "welcomeMessageEnable" in data:
        welcomeMessageEnable = data["welcomeMessageEnable"]
    if "welcomeComment" in data:
        welcomeComment = data["welcomeComment"]
    if "welcomeCommentEnable" in data:
        welcomeCommentEnable = data["welcomeCommentEnable"]
    if "productRecommendMessage" in data:
        productRecommendMessage = data["productRecommendMessage"]
    if "productRecommendMessageEnable" in data:
        productRecommendMessageEnable = data["productRecommendMessageEnable"]
    platformChannels = []
    startTime = None
    endTime = None
    body = {}
    if type=="progress":
        #进行中不允许修改基础设置、关键子下单设置、保留库存、
        res = get_live_info(data)
        title = res["data"]["sales"]["post_sales_title"]
        salesOwner = res["data"]["sales"]["post_sales_owner"]
        salesDescription = res["data"]["sales"]["post_sales_title"]
        patternModel = res["data"]["salesConfig"]["patternModel"]["patternModel"]
        keywordValidInLive = res["data"]["salesConfig"]["patternModel"]["keywordValidInLive"]
        keywordValidAfterLive = res["data"]["salesConfig"]["patternModel"]["keywordValidAfterLive"]
        if "start_time_timestamp" in res["data"]["sales"]:
            startTime = res["data"]["sales"]["start_time_timestamp"]
        if "end_time_timestamp" in res["data"]["sales"]:
            endTime = res["data"]["sales"]["end_time_timestamp"]
        relatedPostList = res["data"]["relatedPostList"]
        for relatedPost in relatedPostList:
            platformChannelName = relatedPost["page_name"]
            platformChannelId = relatedPost["page_id"]
            platformChannel = {
                    "platformChannelName": platformChannelName,
                    "platformChannelId": platformChannelId,
                    "platform": platform
                }
            platformChannels.append(platformChannel)
    if platform.upper()=="FB_GROUP":
        body = {
        "sales": {
            "title": title,
            "salesOwner": salesOwner,
            "salesDescription": salesDescription,
            "platforms": [
                platform
            ],
            "platformSubType": "",
            "platformChannels": [],
            "archivedStreamVisibleTime": None
        },
        "salesConfig": {
            "patternModel": {
                "patternModel": patternModel,
                "keywordValidInLive": keywordValidInLive,
                "keywordValidAfterLive": keywordValidAfterLive
            },
            "autoNotifyPay": {
                "enable": autoNotifyPayEnable,
                "notifyTime": autoNotifyPayTime,
                "message": autoNotifyPayMessage,
                "button": autoNotifyPayButton
            },
            "stock": {
                "lockStock": stockEnable,
                "salesStockLockExpireTime": stockExpireTime,
                "salesStockLockPreTime": stockPreTime
            },
            "commentIntent": {
                "enabled": commentIntent
            },
            "variationToggleOn": {
                "enable": True
            },
            "productSort": {
                "productSort": "NEW_TO_OLD"
            },
            "lowOfQuantity": {
                "enable": lowOfQuantityEnable,
                "sound": lowOfQuantitySound,
                "quantity": lowOfQuantityQuantity
            },
            "notice": None,
            "frontLive": None,
            "liveViewSdk": None,
            "runningLightsConfig": None,
            "fbGroupSettingConfig": {
                "scGroupPmCommentId": True,
                "scGroupWebhook": True
            },
            "productPinningStyle": None
        },
        "postConfigMap": {
            platform: {
                "message": {
                    "needSendMessage": need_send_message,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": has_interaction_message
                        },
                        "messageButton": has_interaction_message_button
                    },
                    "hasLink": has_link,
                    "noInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": no_interaction_message_first
                        },
                        "firstMessageButton": first_message_button,
                        "secondMessageTemplate": {
                            "topMessage": second_message
                        },
                        "secondMessageButton": second_message_button
                    },
                    "messageType": "MESSAGE"
                },
                "allOutOfStockMessage": {
                    "needSendMessage": allOutOfStockEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": allOutOfStockMessage
                        }
                    },
                    "messageType": "ALL_OUT_OF_STOCK"
                },
                "welcomeMessage": {
                    "needSendMessage": welcomeMessageEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": welcomeMessage
                        }
                    },
                    "messageType": "WELCOME_MESSAGE"
                },
                "productRecommendMessage": {
                    "needSendMessage": productRecommendMessageEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "message": productRecommendMessage
                        }
                    },
                    "messageType": "PRODUCT_RECOMMEND_FB_MESSAGE"
                },
                "welcomeMessageComment": {
                    "needSendMessage": welcomeCommentEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": welcomeComment
                        }
                    },
                    "messageType": "WELCOME_MESSAGE_COMMENT"
                },
                "showNumberOfViewers": None,
                "showShareButton": None
            }
            }
        }
    elif platform.lower() in ("facebook","instagram"):
        body = {
        "sales": {
            "title": title,
            "salesOwner": salesOwner,
            "salesDescription": salesDescription,
            "platforms": [
                platform
            ],
            "platformSubType": "",
            "platformChannels": platformChannels,
            "archivedStreamVisibleTime": None,
            "startTime":startTime,
            "endtTime":endTime
        },
        "salesConfig": {
            "patternModel": {
                "patternModel": patternModel,
                "keywordValidInLive": keywordValidInLive,
                "keywordValidAfterLive": keywordValidAfterLive
            },
            "autoNotifyPay": {
                "enable": autoNotifyPayEnable,
                "notifyTime": autoNotifyPayTime,
                "message": autoNotifyPayMessage,
                "button": autoNotifyPayButton
            },
            "stock": {
                "lockStock": stockEnable,
                "salesStockLockExpireTime": stockExpireTime,
                "salesStockLockPreTime": stockPreTime
            },
            "commentIntent": {
                "enabled": commentIntent
            },
            "variationToggleOn": {
                "enable": True
            },
            "productSort": {
                "productSort": "NEW_TO_OLD"
            },
            "lowOfQuantity": {
                "enable": lowOfQuantityEnable,
                "sound": lowOfQuantitySound,
                "quantity": lowOfQuantityQuantity
            },
            "notice": None,
            "frontLive": None,
            "liveViewSdk": None,
            "runningLightsConfig": None,
            "fbGroupSettingConfig": None,
            "productPinningStyle": None
        },
        "postConfigMap": {
            "FACEBOOK": {
                "message": {
                    "needSendMessage": need_send_message,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": has_interaction_message
                        },
                        "messageButton": has_interaction_message_button
                    },
                    "hasLink": has_link,
                    "noInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": no_interaction_message_first
                        },
                        "firstMessageButton": first_message_button,
                        "secondMessageTemplate": {
                            "topMessage": second_message
                        },
                        "secondMessageButton": second_message_button
                    },
                    "messageType": "MESSAGE"
                },
                "allOutOfStockMessage": {
                    "needSendMessage": allOutOfStockEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": allOutOfStockMessage
                        }
                    },
                    "messageType": "ALL_OUT_OF_STOCK"
                },
                "welcomeMessage": {
                    "needSendMessage": welcomeMessageEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": welcomeMessage
                        }
                    },
                    "messageType": "WELCOME_MESSAGE"
                },
                "productRecommendMessage": {
                    "needSendMessage": productRecommendMessageEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "message": productRecommendMessage
                        }
                    },
                    "messageType": "PRODUCT_RECOMMEND_FB_MESSAGE"
                },
                "welcomeMessageComment": {
                    "needSendMessage": welcomeCommentEnable,
                    "hasInteractionMessage": {
                        "firstMessageTemplate": {
                            "topMessage": welcomeComment
                        }
                    },
                    "messageType": "WELCOME_MESSAGE_COMMENT"
                },
                "showNumberOfViewers": None,
                "showShareButton": None
            }
            }
        }
    response = requests.put(url, headers=headers, json=body).json()
    return response


def save_global_config(data):
    "保存直播间通用配置"
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales/global/LIVE"%env
    patternModel = "INCLUDE_MATCH"
    keywordValidInLive = True
    keywordValidAfterLive = False
    autoNotifyPayEnable = False
    autoNotifyPayMessage = ""
    autoNotifyPayButton = ""
    autoNotifyPayTime = None
    stockEnable = False
    stockPreTime = None
    stockExpireTime = None
    lowOfQuantityEnable = False
    lowOfQuantitySound = False
    lowOfQuantityQuantity = "1"
    has_interaction_message = ""
    has_interaction_message_button = ""
    no_interaction_message_first = ""
    second_message = ""
    first_message_button = ""
    second_message_button = " ️"
    need_send_message = True
    has_link = True
    commentIntent = True
    # 无库存讯息
    allOutOfStockMessage = ""
    allOutOfStockEnable = True
    # 欢迎讯息
    welcomeMessage = ""
    welcomeMessageEnable = True
    # 欢迎comment
    welcomeComment = ""
    welcomeCommentEnable = True
    #推荐讯息
    fbProductRecommendMessage = ""
    igProductRecommendMessage = ""
    slProductRecommendMessage = ""
    # productRecommendMessageEnable = True
    #视频观看人数
    show_number = True
    show_share = True

    if "title" in data:
        title = data["title"]
    if "salesDescription" in data:
        title = data["salesDescription"]
    if "salesOwner" in data:
        title = data["salesOwner"]
    if "platform" in data:
        platform = data["platform"]
    if "patternModel" in data:
        patternModel = data["patternModel"]
    if "keywordValidInLive" in data:
        keywordValidInLive = data["keywordValidInLive"]
    if "keywordValidAfterLive" in data:
        keywordValidAfterLive = data["keywordValidAfterLive"]

    if "autoNotifyPayEnable" in data:
        autoNotifyPayEnable = data["autoNotifyPayEnable"]
    if "autoNotifyPayMessage" in data:
        autoNotifyPayMessage = data["autoNotifyPayMessage"]
    if "autoNotifyPayButton" in data:
        autoNotifyPayButton = data["autoNotifyPayButton"]
    if "autoNotifyPayTime" in data:
        autoNotifyPayTime = data["autoNotifyPayTime"]

    if "stockEnable" in data:
        stockEnable = data["stockEnable"]
    if "stockExpireTime" in data:
        stockExpireTime = data["stockExpireTime"]

    if "lowOfQuantityEnable" in data:
        lowOfQuantityEnable = data["lowOfQuantityEnable"]
    if "lowOfQuantitySound" in data:
        lowOfQuantitySound = data["lowOfQuantitySound"]
    if "lowOfQuantityQuantity" in data:
        lowOfQuantityQuantity = data["lowOfQuantityQuantity"]

    if "has_interaction_message" in data:
        has_interaction_message = data["has_interaction_message"]
    if "has_interaction_message_button" in data:
        has_interaction_message_button = data["has_interaction_message_button"]
    if "no_interaction_message_first" in data:
        no_interaction_message_first = data["no_interaction_message_first"]
    if "first_message_button" in data:
        first_message_button = data["first_message_button"]
    if "second_message" in data:
        second_message = data["second_message"]
    if "second_message_button" in data:
        second_message_button = data["second_message_button"]
    if "need_send_message" in data:
        need_send_message = data["need_send_message"]
    # if "message_button" in data:
    #     message_button = data["message_button"]
    if "has_link" in data:
        has_link = data["has_link"]
    if "commentIntent" in data:
        commentIntent = data["commentIntent"]

    if "allOutOfStockMessage" in data:
        allOutOfStockMessage = data["allOutOfStockMessage"]
    if "allOutOfStockEnable" in data:
        allOutOfStockEnable = data["allOutOfStockEnable"]

    if "welcomeMessage" in data:
        welcomeMessage = data["welcomeMessage"]
    if "welcomeMessageEnable" in data:
        welcomeMessageEnable = data["welcomeMessageEnable"]

    if "welcomeComment" in data:
        welcomeComment = data["welcomeComment"]
    if "welcomeCommentEnable" in data:
        welcomeCommentEnable = data["welcomeCommentEnable"]

    if "show_number" in data:
        show_number = data["show_number"]
    if "show_share" in data:
        show_share = data["show_share"]

    if "fbProductRecommendMessage" in data:
        fbProductRecommendMessage = data["fbProductRecommendMessage"]
    if "igProductRecommendMessage" in data:
        igProductRecommendMessage = data["igProductRecommendMessage"]
    if "slProductRecommendMessage" in data:
        slProductRecommendMessage = data["slProductRecommendMessage"]


    body = {
    "saveList": [
        {
            "configKey": "PATTERN_MODEL",
            "configValue": {
                "patternModel": patternModel,
                "keywordValidInLive": keywordValidInLive,
                "keywordValidAfterLive": keywordValidAfterLive
            }
        },
        {
            "configKey": "STOCK",
            "configValue": {
                "lockStock": stockEnable,
                "salesStockLockExpireTime": stockExpireTime
            }
        },
        {
            "configKey": "LOW_OF_QUANTITY",
            "configValue": {
                "enable": lowOfQuantityEnable,
                "sound": lowOfQuantitySound,
                "quantity": lowOfQuantityQuantity
            }
        },
        {
            "configKey": "MESSAGE",
            "configValue": {
                "needSendMessage": need_send_message,
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "topMessage": has_interaction_message
                    },
                    "messageButton": has_interaction_message_button
                },
                "hasLink": has_link,
                "noInteractionMessage": {
                    "firstMessageTemplate": {
                        "topMessage": no_interaction_message_first
                    },
                    "firstMessageButton": first_message_button,
                    "secondMessageTemplate": {
                        "topMessage": second_message
                    },
                    "secondMessageButton": second_message_button
                },
                "messageType": "MESSAGE"
            }
        },
        {
            "configKey": "WELCOME_MESSAGE",
            "configValue": {
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "topMessage": welcomeMessage
                    }
                },
                "needSendMessage": welcomeMessageEnable,
                "messageType": "WELCOME_MESSAGE"
            }
        },
        {
            "configKey": "WELCOME_MESSAGE_COMMENT",
            "configValue": {
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "topMessage": welcomeComment
                    }
                },
                "needSendMessage": welcomeCommentEnable,
                "messageType": "WELCOME_MESSAGE_COMMENT"
            }
        },
        {
            "configKey": "PRODUCT_RECOMMEND_FB_MESSAGE",
            "configValue": {
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "message": fbProductRecommendMessage
                    }
                },
                "messageType": "PRODUCT_RECOMMEND_FB_MESSAGE"
            }
        },
        {
            "configKey": "PRODUCT_RECOMMEND_IG_MESSAGE",
            "configValue": {
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "message": igProductRecommendMessage
                    }
                },
                "messageType": "PRODUCT_RECOMMEND_IG_MESSAGE"
            }
        },
        {
            "configKey": "PRODUCT_RECOMMEND_SHOP_LINE_MESSAGE",
            "configValue": {
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "message": slProductRecommendMessage
                    }
                },
                "messageType": "PRODUCT_RECOMMEND_SHOP_LINE_MESSAGE"
            }
        },
        {
            "configKey": "ALL_OUT_OF_STOCK",
            "configValue": {
                "hasInteractionMessage": {
                    "firstMessageTemplate": {
                        "topMessage": allOutOfStockMessage
                    }
                },
                "needSendMessage": allOutOfStockEnable,
                "messageType": "ALL_OUT_OF_STOCK"
            }
        },
        {
            "configKey": "AUTO_NOTIFY_PAY",
            "configValue": {
                "enable": autoNotifyPayEnable,
                "message": autoNotifyPayMessage,
                "button": autoNotifyPayButton
            }
        },
        {
            "configKey": "COMMENT_INTENT",
            "configValue": {
                "enabled": commentIntent
            }
        },
        {
            "configKey": "SHOW_NUMBER_OF_VIEWERS",
            "configValue": {
                "enabled": show_number
            }
        },
        {
            "configKey": "SHOW_SHARE_BUTTON",
            "configValue": {
                "enabled": show_share
            }
        }
    ]
}
    response = requests.post(url, headers=headers, json=body).json()
    return response


def get_global_config(data):
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/post/sales/global/LIVE" % env
    response = requests.get(url,headers=headers).json()
    # print(response)
    return response




outOfStock = {
        "en":"The following product(s) doesn't have enough stock, please select other products, thanks!\n❗️{products}".replace("️{products}","ffddd"),
        "zh-cn":"以下商品库存不足，请选购其他商品，谢谢！\n❗️{products}".replace("️{products}","ffddd"),
        "zh-hant":"以下商品庫存不足，請選購其他商品，謝謝！\n❗️{products}".replace("️{products}","ffddd")
        }



def remove_live_product(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    product_id = data["product_id"]
    url = "%s/api/posts/post/sales/%s/product/%s"%(env,sales_id,product_id)
    response = requests.delete(url,headers=headers).json()
    return response


def change_keyword_status(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    product_id = data["product_id"]
    status = "true"
    if "status" in data:
        status = data["status"]
    url = "%s/api/posts/post/sales/%s/product/keyword/status/%s"%(env,sales_id,status)
    body = {
    "spuIdList": [
        product_id
        ]
     }
    response = requests.put(url, headers=headers,json=body).json()
    return response

def delete_product_set(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    product_id = data["product_id"]
    url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set"%(env,sales_id)
    body = {
    "ids": [
            product_id
        ]
    }
    res = requests.delete(url,headers=headers,json=body).json()
    return res
#查询普通商品列表
def get_live_product(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    query = ""
    if "query" in data:
        query = data["query"]
    url = "%s/api/posts/post/sales/%s/product/v2" % (env, sales_id)
    params = {"salesId":sales_id,"pageIndex":1,"pageSize":25,}
    if query!="":
        params["queryType"] = "PRODUCT_NAME"
        params["query"] = query
    response = requests.get(url, headers=headers,params=params).json()
    return response

def search_product_set(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    query = ""
    if "query" in data:
        query = data["query"]
    url = "%s/admin/api/bff-web/live/sale/%s/sale_list/product_set"%(env,sales_id)
    param = {"pageNum":1,"pageSize":10,"query":query,"queryType":"PRODUCT_NAME"}
    # print(param)
    res = requests.get(url,headers=headers,params=param).json()
    return res

def get_sales_keyword(data):
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/admin/api/bff-web/live/sale/%s/keyword/list"%(env,sales_id)
    res = requests.get(url, headers=headers).json()
    return res

def get_stock_product_set(res,type="stock"):
    list_data = res["data"]["list"]
    if type=="stock":
        for i in list_data:
            combinationList = i["combinationList"]
            for combination in combinationList:
                products = combination["products"]
                for product in products:
                    count = product["count"]
                    quantity = product["quantity"]
                    if quantity==-1:
                        # print("库存无限数量")
                        pass
                    elif quantity<count:
                        break
                    keyword = combination["keywords"][0]
                    product_id = i["id"]
                    return keyword, product_id, list_data
    elif type=="out":
        for i in list_data:
            combinationList = i["combinationList"]
            for combination in combinationList:
                products = combination["products"]
                for product in products:
                    count = product["count"]
                    quantity = product["quantity"]
                    if quantity != -1 and quantity < count:
                        keyword = combination["keywords"][0]
                        product_id = i["id"]
                        return keyword, product_id, list_data





if __name__=="__main__":
    data = {
    "success": True,
    "code": "SUCCESS",
    "message": "success",
    "data": {
        "pageInfo": {
            "pageNum": 1,
            "pageSize": 10,
            "total": 4,
            "lastPage": True
        },
        "list": [
            {
                "id": "673c889f3dc982185de87d1c",
                "image": "https://shoplineimg.com/61a87c9763b70c005106fbd0/673c889b52b9d600110bfc1c/50xf.webp?source_format=png&cheap_resize=1",
                "title": "ffsssdsfsfsf",
                "recommend": {
                    "isActivity": True,
                    "recommendTime": None
                },
                "effectiveKey": True,
                "defaultKey": "",
                "combinationList": [
                    {
                        "id": "46df6fa5b6af8bcbec7aa28db26f1eae",
                        "price": {
                            "originCents": 455,
                            "origin": "455 ₫",
                            "salesCents": 55,
                            "sales": "55 ₫"
                        },
                        "keywords": [
                            "组合商品关键字1732346557"
                        ],
                        "products": [
                            {
                                "spuId": "673c311f52b9d659d30bf878",
                                "skuId": "673c311f52b9d659d30bf878",
                                "count": 2,
                                "name": "inbox自定义商品",
                                "quantity": -1,
                                "unlimitedQuantity": True
                            },
                            {
                                "spuId": "673c2e5a3dc982185de87b57",
                                "skuId": "673c2e5a3dc982185de87b57",
                                "count": 2,
                                "name": "自定义商品哈哈哈",
                                "quantity": 9999,
                                "unlimitedQuantity": True
                            }
                        ],
                        "buyerProductCount": 0
                    }
                ],
                "availableStartTime": None,
                "availableEndTime": None,
                "tempPrice": {
                    "originCents": 455,
                    "origin": "455 ₫",
                    "salesCents": 55,
                    "sales": "55 ₫"
                },
                "childrenInfo": {
                    "673c2e5a3dc982185de87b57": {
                        "necessaryQuantity": 2,
                        "variations": []
                    },
                    "673c311f52b9d659d30bf878": {
                        "necessaryQuantity": 2,
                        "variations": []
                    }
                },
                "status": "active"
            },
            {
                "id": "670f8a6c7fb2d15f7b8f6431",
                "image": "https://shoplineimg.com/61a87c9763b70c005106fbd0/670f8a57b7b2cb000a26a9f6/50xf.webp?source_format=jpeg&cheap_resize=1",
                "title": "dyy超长的组合商品yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
                "recommend": {
                    "isActivity": True,
                    "recommendTime": None
                },
                "effectiveKey": True,
                "defaultKey": "",
                "combinationList": [
                    {
                        "id": "c536c6eaffa7364a1dac2743aeff518a",
                        "price": {
                            "originCents": 100,
                            "origin": "100 ₫",
                            "salesCents": 90,
                            "sales": "90 ₫"
                        },
                        "keywords": [
                            "LYQYH1730649250892"
                        ],
                        "products": [
                            {
                                "spuId": "670f8a48b7b2cb384126a9bc",
                                "skuId": "670f8a48db1762000bcedfc8",
                                "count": 2,
                                "name": "dyy超长的商品yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy(dyy超长的商品yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy)",
                                "quantity": -1,
                                "unlimitedQuantity": True
                            },
                            {
                                "spuId": "670f84314149e400117b3c6a",
                                "skuId": "670f84314bd7dd001035d0ea",
                                "count": 51,
                                "name": "多规格商品名称1729070129(红)",
                                "quantity": 50,
                                "unlimitedQuantity": True
                            }
                        ],
                        "buyerProductCount": 0
                    }
                ],
                "availableStartTime": None,
                "availableEndTime": None,
                "tempPrice": {
                    "originCents": 100,
                    "origin": "100 ₫",
                    "salesCents": 90,
                    "sales": "90 ₫"
                },
                "childrenInfo": {
                    "670f84314149e400117b3c6a": {
                        "necessaryQuantity": 1,
                        "variations": [
                            "670f84314bd7dd001035d0ea"
                        ]
                    },
                    "670f8a48b7b2cb384126a9bc": {
                        "necessaryQuantity": 2,
                        "variations": [
                            "670f8a48db1762000bcedfc8",
                            "670f8a48db1762000bcedfc9"
                        ]
                    }
                },
                "status": "active"
            },
            {
                "id": "670fc1bbb7b2cb161826a9c6",
                "image": "https://shoplineimg.com/61a87c9763b70c005106fbd0/670fc196b7b2cbbdac26a7e2/50xf.webp?source_format=jpeg&cheap_resize=1",
                "title": "dyy组合商品变动- 子商品从多规格 变成 无规格",
                "recommend": {
                    "isActivity": True,
                    "recommendTime": None
                },
                "effectiveKey": True,
                "defaultKey": "",
                "combinationList": [
                    {
                        "id": "e869f56d1d94901903a3c6b5e775d37b",
                        "price": {
                            "originCents": 100,
                            "origin": "100 ₫",
                            "salesCents": 90,
                            "sales": "90 ₫"
                        },
                        "keywords": [
                            "DDAASS"
                        ],
                        "products": [
                            {
                                "spuId": "670fc182b7b2cb001026ab78",
                                "skuId": "670fc182b7b2cb001026ab78",
                                "count": 2,
                                "name": "dyy商品从多规格 变成 无规格",
                                "quantity": -1,
                                "unlimitedQuantity": True
                            },
                            {
                                "spuId": "670fbb5227a445000f12b050",
                                "skuId": "670fbb517e0510001fd941c9",
                                "count": 3,
                                "name": "模式4接口自动化添加的多规格商品1729084241(红,M)",
                                "quantity": 55,
                                "unlimitedQuantity": False
                            }
                        ],
                        "buyerProductCount": 0
                    },
                    {
                        "id": "f266f67781aa371f8348d331ffc77565",
                        "price": {
                            "originCents": 100,
                            "origin": "100 ₫",
                            "salesCents": 90,
                            "sales": "90 ₫"
                        },
                        "keywords": [
                            "MMM"
                        ],
                        "products": [
                            {
                                "spuId": "670fc182b7b2cb001026ab78",
                                "skuId": "670fc182b7b2cb001026ab78",
                                "count": 2,
                                "name": "dyy商品从多规格 变成 无规格",
                                "quantity": -1,
                                "unlimitedQuantity": True
                            },
                            {
                                "spuId": "670fbb5227a445000f12b050",
                                "skuId": "670fbb517e0510001fd941ca",
                                "count": 3,
                                "name": "模式4接口自动化添加的多规格商品1729084241(红, L)",
                                "quantity": 1,
                                "unlimitedQuantity": False
                            }
                        ],
                        "buyerProductCount": 0
                    }
                ],
                "availableStartTime": None,
                "availableEndTime": None,
                "tempPrice": {
                    "originCents": 100,
                    "origin": "100 ₫",
                    "salesCents": 90,
                    "sales": "90 ₫"
                },
                "childrenInfo": {
                    "670fbb5227a445000f12b050": {
                        "necessaryQuantity": 3,
                        "variations": [
                            "670fbb517e0510001fd941c9",
                            "670fbb517e0510001fd941ca",
                            "670fbb517e0510001fd941cb",
                            "670fbb517e0510001fd941cc"
                        ]
                    },
                    "670fc182b7b2cb001026ab78": {
                        "necessaryQuantity": 2,
                        "variations": []
                    }
                },
                "status": "active"
            },
            {
                "id": "670fc567b7b2cb000a26ab86",
                "image": "https://shoplineimg.com/61a87c9763b70c005106fbd0/670fc54eb7b2cbbdac26a7e3/50xf.webp?source_format=jpeg&cheap_resize=1",
                "title": "组合商品下的子商品被删除了",
                "recommend": {
                    "isActivity": False,
                    "recommendTime": "2024-11-18T20:31:57+08:00"
                },
                "effectiveKey": True,
                "defaultKey": "",
                "combinationList": [
                    {
                        "id": "ea4838a97018ddd345099847945ac38b",
                        "price": {
                            "originCents": 100,
                            "origin": "100 ₫",
                            "salesCents": 90,
                            "sales": "90 ₫"
                        },
                        "keywords": [
                            "FFDDD",
                            "GGSS"
                        ],
                        "products": [
                            {
                                "spuId": "670fc53eb7b2cbfe9926a836",
                                "skuId": "670fc53eb7b2cbfe9926a836",
                                "count": 2,
                                "name": "dyy这个商品是要被删除的额",
                                "quantity": -1,
                                "unlimitedQuantity": True
                            }
                        ],
                        "buyerProductCount": 0
                    }
                ],
                "availableStartTime": None,
                "availableEndTime": None,
                "tempPrice": {
                    "originCents": 100,
                    "origin": "100 ₫",
                    "salesCents": 90,
                    "sales": "90 ₫"
                },
                "childrenInfo": {
                    "670fc53eb7b2cbfe9926a836": {
                        "necessaryQuantity": 2,
                        "variations": []
                    }
                },
                "status": "active"
            }
        ]
    },
    "traceId": "13f3a0b22dc91017817f0f74756031cf"
}
    keyword,spuid,__ = get_stock_product_set(data,"out")
    print(keyword)