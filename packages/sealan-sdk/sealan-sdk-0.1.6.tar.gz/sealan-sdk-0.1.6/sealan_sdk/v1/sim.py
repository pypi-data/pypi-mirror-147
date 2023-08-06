# -*- coding: utf-8 -*-
from . import response
from . import client

class SimRequest(object):
    OPERATOR_CHINAMOBILE = 1
    OPERATOR_CHINAUNICOM = 2
    OPERATOR_CHINATELCOM = 3

    def __init__(self):
        return

    def get_package_list(self, page = 1, size = 20):
        params = client.RequestParam()
        params.method = params.GET
        params.payload = {
            "page": page,
            "size": size,
        }
        params.path = f"cardapi/package/list"
        return params

    def get_card_list(self, cardflag = 1, operator = None, order = None, page = 1, size = 20, sortfield = None, status = None):
        params = client.RequestParam()
        params.path = f"cardapi/card/list/"
        params.method = params.POST
        params.payload = {
            "cardFlag": cardflag,
            "operator": operator or self.OPERATOR_CHINAMOBILE,
            "order": order,
            "pageindex": page,
            "pagesize": size,
            "sortfield": sortfield,
        }
        return params

    def get_card(self, iccid = None):
        if iccid == None:
            return response.PARAM_ERROR

        params = client.RequestParam()
        params.method = params.GET
        params.path = f"cardapi/card/all/{iccid}/"

        return params

    def get_share_pool_list(self):
        params = client.RequestParam()
        params.path = f"cardapi/cardsharepool/list/"
        params.method = params.POST
        params.payload = {}
        return params

    def get_card_month_usage(self, iccid, month):
        params = client.RequestParam()
        params.path = f"cardapi/card_flow/month/"
        params.method = params.POST
        params.payload = {
            "iccid": iccid,
            "month": month,
        }
        return params

    
    def create_alert(self, name, webhook,event,flow,all,enable,status,iccids,description):
        """创建单个报警规则接口

        Params:
            name (string, require): 名称
            webhook (text, require): 接收警告接口
            flow (float, optional): 报警触发流量
            all (bool, optional): 是否是用户全部卡片
            enable (bool, optional): 规则开启关闭
            description (text, optional): 描述
            status (int, optional): 告警触发状态, 1可激活, 2已激活, 3已停用
            event (int, require): 规则类型分类, 1状态监控, 2流量值监控, 3流量比例监控
            iccids (array, optional): 卡iccid列表
        """
        params = client.RequestParam()
        params.path = f"cardapi/alert"
        params.method = params.POST
        params.payload = {
            'name': name,
            'webhook': webhook,
            'flow': flow,
            'all': all,
            'enable': enable,
            'description': description,
            'status': status,
            'event': event,
            'iccids': iccids,
        }
        return params

    def get_alert_list(self, page = 1, size = 20):
        params = client.RequestParam()
        params.method = params.GET
        params.payload = {
            "page": page,
            "size": size,
        }
        params.path = f"cardapi/alert/list"
        return params


    def get_alert(self, id = None):
        if id == None:
            return response.PARAM_ERROR

        params = client.RequestParam()
        params.method = params.GET
        params.path = f"cardapi/alert/{id}"

        return params

    def modify_alert(self, id, name, webhook,flow,enable,status,description):
        """修改单个报警规则接口

        Params:
            id (int, required): ID
            name (string, optional): 名称
            webhook (text, optional): 接收警告接口
            flow (float, optional): 报警触发流量
            all (bool, optional): 是否是用户全部卡片
            enable (bool, optional): 规则开启关闭
            description (text, optional): 描述
            status (int, optional): 告警触发状态, 1可激活, 2已激活, 3已停用
            event (int, optional): 规则类型分类, 1状态监控, 2流量值监控, 3流量比例监控
        """
        params = client.RequestParam()
        params.path = f"cardapi/alert/{id}"
        params.method = params.PUT
        params.payload = {
            'name': name,
            'webhook': webhook,
            'flow': flow,
            'enable': enable,
            'description': description,
            'status': status,
        }
        return params

    def delete_alert(self, ids):
        """delete删除多个报警规则接口

        Params:
            ids (list, require): 需要删除的报警规则ID主键列表，当包含关联子表时，会删除失败

        """
        params = client.RequestParam()
        params.path = f"cardapi/alert"
        params.method = params.DELETE
        params.payload = {
            'ids': ids,
        }
        return params
        