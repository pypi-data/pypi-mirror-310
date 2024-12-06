# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2024-11-06 09:39:45
@LastEditTime: 2024-11-06 15:14:06
@LastEditors: HuangJianYi
@Description: 
"""

#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class StoreInfoModel(BaseModel):
    def __init__(self, db_connect_key='db_hk_cap', sub_table=None, db_transaction=None, context=None):
        super(StoreInfoModel, self).__init__(StoreInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class StoreInfo:

    def __init__(self):
        super(StoreInfo, self).__init__()
        self.id = 0  # id
        self.guid = None  # guid
        self.business_id = 0  # 商家标识
        self.platform_id = 0  # 平台标识
        self.store_name = ""  # 店铺名称
        self.store_icon = ""  # 店铺图标
        self.plat_store_id = ""  # 平台店铺标识
        self.store_status = 0  # 店铺状态
        self.plat_telephone_key = ""  # 平台手机号密钥
        self.prefix_status = 0  # 号段生成状态(0-未生成 1-已生成)
        self.prefix_path = ""  # 号段存储路径
        self.seller_nick = ""  # 店铺主账号
        self.buy_product_ids = "" # 订购产品列表
        self.crm_rawdata_sync_status = 0 # CRM数据同步状态
        self.cdp_rawdata_sync_status = 0 # CDP数据同步状态
        self.overdue_date = '1970-01-01 00:00:00.000' # 过期时间
        self.create_date = '1970-01-01 00:00:00.000' # 创建时间
        self.modify_date = '1970-01-01 00:00:00.000' # 修改时间
        

    @classmethod
    def get_field_list(self):
        return ['id', 'guid', 'business_id', 'platform_id', 'store_name', 'store_icon', 'plat_store_id', 'store_status', 'plat_telephone_key', 'prefix_status', 'prefix_path', 'seller_nick', 'buy_product_ids', 'crm_rawdata_sync_status', 'cdp_rawdata_sync_status', 'overdue_date', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "store_info_tb"
    