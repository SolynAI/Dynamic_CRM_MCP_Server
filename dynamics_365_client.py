import json
import requests
import msal
from datetime import datetime, timedelta
import logging


class Dynamics365Client:
    def __init__(self, client_id, client_secret, tenant_id, resource):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.TENANT_ID = tenant_id
        self.RESOURCE = resource
        self.AUTHORITY = f'https://login.microsoftonline.com/{self.TENANT_ID}'
        self.API_URL = f'{self.RESOURCE}/api/data/v9.1'
        self.access_token = self._get_access_token()
        self.user_id = self._get_current_user_id()
        logging.info(f'user_id= {self.user_id}')

    def _get_current_user_id(self):
        """获取当前token关联的用户ID"""
        # 调用WhoAmI API获取当前用户信息
        response = requests.get(
            f'{self.API_URL}/WhoAmI',
            headers=self._get_headers()
        )
        result = self._response_to_json(response)
        if isinstance(result, dict) and 'UserId' in result:
            return result['UserId']
        else:
            raise ValueError("无法获取当前用户ID")

    def _get_access_token(self):
        """获取Dynamics 365访问令牌"""
        app = msal.ConfidentialClientApplication(
            self.CLIENT_ID,
            authority=self.AUTHORITY,
            client_credential=self.CLIENT_SECRET
        )
        result = app.acquire_token_for_client(scopes=[f'{self.RESOURCE}/.default'])

        if 'access_token' not in result:
            error_msg = f"Failed to acquire access token: {result.get('error')} - {result.get('error_description')}"
            raise ConnectionError(error_msg)

        return result['access_token']

    def _get_headers(self):
        """获取标准请求头"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8'
        }

    def _format_entity_references(self, data):
        """
        增强版：智能格式化实体关联引用
        现在支持所有标准实体类型的关联字段自动转换
        """
        if not data:
            return data

        formatted = data.copy()

        # 通用实体引用映射表（支持所有标准实体）
        reference_mappings = {
            # 标准关联字段
            'regardingobjectid': self._detect_entity_type,
            'objectid': self._detect_entity_type,
            'customerid': self._detect_entity_type,
            'parentcustomerid': self._detect_entity_type,
            'primarycontactid': lambda x: ('contacts', x),

            # 明确指定的关联字段（实体类型_字段名）
            'regardingobjectid_account': ('accounts', None),
            'regardingobjectid_contact': ('contacts', None),
            'regardingobjectid_lead': ('leads', None),
            'objectid_account': ('accounts', None),
            'objectid_contact': ('contacts', None),
            'objectid_lead': ('leads', None),
            'customerid_account': ('accounts', None),
            'customerid_contact': ('contacts', None),
        }

        for field, value in list(formatted.items()):
            if field in reference_mappings:
                mapping = reference_mappings[field]

                # 如果是可调用函数，则动态检测实体类型
                if callable(mapping):
                    entity_type, entity_id = mapping(value)
                else:
                    entity_type, _ = mapping
                    entity_id = value

                if entity_type and entity_id:
                    formatted[f"{field}@odata.bind"] = f"/{entity_type}({entity_id})"
                    del formatted[field]

            # 自动处理所有objectid_*和regardingobjectid_*格式的字段
            elif any(field.startswith(prefix) for prefix in ['objectid_', 'regardingobjectid_', 'customerid_']):
                entity_type = field.split('_')[-1]
                formatted[f"{field}@odata.bind"] = f"/{entity_type}s({value})"
                del formatted[field]

        return formatted

    def _detect_entity_type(self, entity_id):
        """
        智能检测实体类型（简化版，实际使用可能需要更复杂的逻辑）
        这里假设entity_id有前缀标识，如：
        'account:07fc9dd5-d90a-f011-bae3-6045bd21ddb0'
        """
        if not entity_id:
            return (None, None)

        # 如果有明确的类型前缀
        if ':' in entity_id:
            entity_type, guid = entity_id.split(':', 1)
            return (f"{entity_type}s", guid)

        # 默认返回account类型（实际项目应根据业务逻辑调整）
        return ('accounts', entity_id)

    def _response_to_result(self, response):
        if response.status_code in [200, 201, 204]:
            msg = {
                "status": "success",
                "message": "Operation completed successfully."
            }
            return response.content if response.content else f'{msg}'
        else:
            msg = {
                "status": "error",
                "status_code": response.status_code,
                "message": "API request failed",
                "response": response.text
            }
            return f'{msg}'
    def _response_to_json(self, response):
        """统一处理API响应"""
        if response.status_code in [200, 201, 204]:
            return response.json() if response.content else {
                "status": "success",
                "message": "Operation completed successfully."
            }
        else:
            return {
                "status": "error",
                "status_code": response.status_code,
                "message": "API request failed",
                "response": response.text
            }

    # ========== 通用获取方法 ==========
    def _get_all_entities(self, entity_name, top=1000, order_by="createdon desc", filter_id=True):
        """通用方法：获取当前用户下的所有实体数据"""
        if filter_id:
            params = {
                '$filter': f"_owninguser_value eq {self.user_id}",
                '$top': top,
                '$orderby': order_by
            }
        else:
            params = {
                '$top': top,
                '$orderby': order_by
            }

        response = requests.get(
            f'{self.API_URL}/{entity_name}',
            headers=self._get_headers(),
            params=params
        )
        return self._response_to_result(response)
    # ========== 线索相关 ==========
    def create_lead(self, **data):
        data = self._format_entity_references(data or {})
        response = requests.post(
            f'{self.API_URL}/leads',
            headers=self._get_headers(),
            json=data
        )
        return self._response_to_result(response)

    def get_all_leads(self, top=1000):
        return self._get_all_entities("leads", top)
    # ========== 客户/联系人操作 ==========



    # ========== 客户(Account)操作 ==========
    def create_contact(self, **data):
        data = {
            'firstname': data.get('firstname'),
            'lastname': data.get('lastname'),
            'emailaddress1': data.get('emailaddress1'),
            'telephone1': data.get('telephone1'),
            'jobtitle': data.get('jobtitle'),
        }
        data = self._format_entity_references(data or {})
        response = requests.post(
            f'{self.API_URL}/contacts',
            headers=self._get_headers(),
            json=data
        )
        return self._response_to_result(response)
    def get_all_accounts(self, top=1000):
        """获取当前用户下的所有客户"""
        return self._get_all_entities("accounts", top)

    # ========== 联系人(Contact)操作 ==========
    def create_account(self, **data):
        """
        创建客户(公司)记录，并可关联到联系人

        参数:
            name (str): 公司名称(必需)
            primarycontactid (str): 主联系人ID(可选)
            other_contact_ids (list): 其他关联联系人ID列表(可选)
            industrycode (int): 行业代码(可选)
            revenue (float): 年收入(可选)
            telephone1 (str): 主要电话(可选)
            websiteurl (str): 网站URL(可选)
            address_*: 各种地址字段(可选)

        返回:
            创建结果，包含新创建的客户ID或错误信息
        """
        # 提取联系人相关字段
        primary_contact_id = data.pop('primarycontactid', None)
        other_contact_ids = data.pop('other_contact_ids', [])

        # 格式化基本数据
        account_data = {
            'name': data.get('name'),
            'industrycode': data.get('industrycode'),
            'revenue': data.get('revenue'),
            'telephone1': data.get('telephone1'),
            'websiteurl': data.get('websiteurl'),
            'address1_line1': data.get('address1_line1'),
            'address1_city': data.get('address1_city'),
            'address1_stateorprovince': data.get('address1_stateorprovince'),
            'address1_postalcode': data.get('address1_postalcode'),
            'address1_country': data.get('address1_country'),
            'description': data.get('description')
        }

        # 关联主联系人
        if primary_contact_id:
            account_data['primarycontactid'] = primary_contact_id

        # 格式化实体引用
        account_data = self._format_entity_references(account_data)

        # 创建客户记录
        response = requests.post(
            f'{self.API_URL}/accounts',
            headers=self._get_headers(),
            json=account_data
        )
        result = self._response_to_json(response)
        # 如果创建成功且需要关联其他联系人
        if 'status' in result and result['status'] == 'success' and other_contact_ids:
            account_id = response.headers['OData-EntityId'].split('(')[1].split(')')[0]

            # 关联其他联系人
            for contact_id in other_contact_ids:
                self._associate_contact_to_account(account_id, contact_id)

            # 返回结果中包含关联信息
            result['associated_contacts'] = {
                'primary': primary_contact_id,
                'additional': other_contact_ids
            }
        return json.dumps(result)


    def _associate_contact_to_account(self, account_id, contact_id):
        """
        内部方法：将联系人关联到客户

        参数:
            account_id (str): 客户ID
            contact_id (str): 联系人ID
        """
        # 使用N:1关系将联系人关联到客户
        update_data = {
            'parentcustomerid@odata.bind': f'/accounts({account_id})'
        }

        response = requests.patch(
            f'{self.API_URL}/contacts({contact_id})',
            headers=self._get_headers(),
            json=update_data
        )
        return self._response_to_result(response)
    def get_all_contacts(self, top=1000):
        """获取当前用户下的所有联系人"""
        return self._get_all_entities("contacts", top)

    # ========== 活动管理 ==========
    def create_appointment(self, **data):
        """
        创建拜访记录（Appointment）

        参数:
            subject (str): 拜访主题
            scheduled_start (datetime): 计划开始时间
            scheduled_end (datetime): 计划结束时间
            **kwargs: 其他可选参数，包括:
                - location (str): 地点
                - description (str): 详细描述
                - regardingobjectid (str): 关联的实体ID（如客户、联系人等）
                - regardingobjectid_account (str): 明确关联到客户的ID
                - regardingobjectid_contact (str): 明确关联到联系人的ID
                - prioritycode (int): 优先级代码
                - category (str): 类别

        返回:
            创建结果
        """
        scheduled_start = datetime.fromisoformat(data['scheduledstart'])
        scheduled_end = datetime.fromisoformat(data['scheduledend'])
        subject = data['subject']
        # 计算持续时间（分钟）
        duration = int((scheduled_end - scheduled_start).total_seconds() / 60)

        # 基础数据
        appointment_data = {
            'subject': subject,
            'scheduledstart': scheduled_start.isoformat(),
            'scheduledend': scheduled_end.isoformat(),
            'actualdurationminutes': duration,
            'location': data.get('location'),
            'description': data.get('description'),
            'prioritycode': data.get('prioritycode', 1),  # 默认普通优先级
            'category': data.get('category'),
            'isalldayevent': data.get('isalldayevent', False)
        }

        # 处理关联实体
        appointment_data = self._format_entity_references(appointment_data)

        # 设置默认所有者（当前用户）
        if 'ownerid' not in appointment_data:
            appointment_data['ownerid@odata.bind'] = f'/systemusers({self.user_id})'

        # 创建拜访记录
        response = requests.post(
            f'{self.API_URL}/appointments',
            headers=self._get_headers(),
            json=appointment_data
        )

        return self._response_to_result(response)

    def get_all_activities(self, top=1000):
        """
        获取格式化后的客户活动信息（包含主题/相关实体/时间/持续时间/备注）
        改进点：
        1. 扁平化返回数据结构
        2. 确保获取关联实体信息
        3. 处理空结果情况
        4. 优化时间显示格式
        """
        return self._get_all_entities('appointments', top)
        params = {
            '$top': top,
            '$filter': f"_owninguser_value eq {self.user_id}"
        }
        response = requests.get(
            f'{self.API_URL}/appointments',
            headers=self._get_headers(),
            params=params,
            timeout=15
        )
        response_text = response.content  # 显式解码为 UTF-8
        return f"status: success, result: {response_text}"

    # 搜索实体id
    def find_entity_id(self, search_criteria, entity_name='contacts', exact_match=False):
        """
        通用方法：根据条件查找实体ID（增强版）
        :param search_criteria: 查询条件字典，如 {'emailaddress1': 'test@example.com'}
        :param entity_name: 实体名称(contacts/accounts/leads等)
        :param exact_match: 是否使用精确匹配（默认模糊匹配字符串字段）
        :return: 实体ID列表
        """
        if not search_criteria:
            raise ValueError("搜索条件不能为空")

        # 处理实体ID字段名称
        entity_id_field = f"{entity_name[:-1]}id" if entity_name.endswith('s') else f"{entity_name}id"

        # 构建过滤条件
        filter_parts = []
        for field, value in search_criteria.items():
            # 处理特殊字符
            safe_value = str(value).replace("'", "''") if isinstance(value, str) else value

            if isinstance(value, str) and not exact_match:
                filter_parts.append(f"contains({field}, '{safe_value}')")
            else:
                # 处理其他数据类型
                if isinstance(value, str):
                    operator = "eq"
                    formatted_value = f"'{safe_value}'"
                elif isinstance(value, datetime):
                    operator = "eq"
                    formatted_value = value.isoformat()
                else:
                    operator = "eq"
                    formatted_value = str(value)
                filter_parts.append(f"{field} {operator} {formatted_value}")

        filter_str = " and ".join(filter_parts)

        # 分页参数
        params = {
            # '$filter': filter_str,
            '$select': entity_id_field,
            '$top': 5000,
            '$count': 'true'
        }

        all_results = []
        while True:
            response = requests.get(
                f'{self.API_URL}/{entity_name}',
                headers=self._get_headers(),
                params=params,
                timeout=15
            )
            response.raise_for_status()

            result = self._response_to_json(response)

            if isinstance(result, dict) and 'value' in result:
                all_results.extend(result['value'])
                if '@odata.nextLink' in result:
                    params['$skiptoken'] = result['@odata.nextLink'].split('$skiptoken=')[1]
                else:
                    break
            else:
                break
        return [f'找到客户信息：{item[entity_id_field]}' for item in all_results if entity_id_field in item]

    # ========== 市场活动(Campaign)操作 ==========
    def get_all_campaigns(self, top=1000):
        return self._get_all_entities('campaigns', top)


    # ========== 商机(Opportunity)操作 ==========
    def create_opportunity(self, **data):
        """创建商机"""
        required_fields = ['name', 'budgetamount']
        if not all(field in data for field in required_fields):
            raise ValueError(f"缺少必填字段: {', '.join(required_fields)}")

        # 设置固定值
        data.setdefault('pricelevelid', '65029c08-f01f-eb11-a812-000d3a33e825')

        data = self._format_entity_references(data)
        response = requests.post(
            f'{self.API_URL}/opportunities',
            headers=self._get_headers(),
            json=data
        )
        return self._response_to_result(response)

    def get_all_opportunities(self, top=1000):
        """获取当前用户下的所有商机"""
        return self._get_all_entities("opportunities", top)

    # ========== 订单(SalesOrder)操作 ==========
    def create_sales_order(self, **data):
        """创建订单"""
        required_fields = ['name', 'customerid']
        if not all(field in data for field in required_fields):
            raise ValueError(f"缺少必填字段: {', '.join(required_fields)}")

        # 设置固定值
        data.setdefault('transactioncurrencyid', '5fd825f9-2ddd-ef11-8eea-000d3ac7f225')
        data.setdefault('pricelevelid', '65029c08-f01f-eb11-a812-000d3a33e825')

        data = self._format_entity_references(data)
        response = requests.post(
            f'{self.API_URL}/salesorders',
            headers=self._get_headers(),
            json=data
        )
        return self._response_to_result(response)

    def get_all_sales_orders(self, top=1000):
        """获取当前用户下的所有订单"""
        return self._get_all_entities("salesorders", top)

    # ========== 案例(Incident)操作 ==========
    def create_incident(self, **data):
        """创建服务案例"""
        required_fields = ['title', 'customerid']
        if not all(field in data for field in required_fields):
            raise ValueError(f"缺少必填字段: {', '.join(required_fields)}")

        # 设置固定值
        data.setdefault('subjectid', 'CA0EB44A-CEDC-EF11-8EEA-000D3AC7F225')

        data = self._format_entity_references(data)
        response = requests.post(
            f'{self.API_URL}/incidents',
            headers=self._get_headers(),
            json=data
        )
        return self._response_to_result(response)

    def get_all_incidents(self, top=1000):
        """获取当前用户下的所有案例"""
        return self._get_all_entities("incidents", top)

    # ========== 产品(Product)操作 ==========
    def get_all_products(self, filter=None, top=1000):
        """获取所有产品"""
        params = {'$top': top}
        if filter:
            params['$filter'] = filter

        response = requests.get(
            f'{self.API_URL}/products',
            headers=self._get_headers(),
            params=params
        )
        return self._response_to_result(response)

    # ========== 价目表项(ProductPriceLevel)操作 ==========
    def get_all_product_pricelevels(self, top=1000):
        """获取当前用户下的所有价目表项"""
        return self._get_all_entities("productpricelevels", top, filter_id=False)

    # ========== 邮件(Email)操作 ==========
    def get_all_emails(self, top=1000):
        """获取邮件"""
        return self._get_all_entities('emails', top)

    # ========== 通用查询增强 ==========
    def query_entity(self, entity_name, filter=None, select=None, expand=None, top=None, orderby=None):
        """通用实体查询方法"""
        params = {}
        if filter:
            params['$filter'] = filter
        if select:
            params['$select'] = select
        if expand:
            params['$expand'] = expand
        if top:
            params['$top'] = top
        if orderby:
            params['$orderby'] = orderby

        response = requests.get(
            f'{self.API_URL}/{entity_name}',
            headers=self._get_headers(),
            params=params
        )
        return self._response_to_result(response)


# if __name__ == '__main__':
#     client = Dynamics365Client(
#         client_id='9bcc6265-27d4-4843-b73b-b2666ab9b776',
#         client_secret='DuT8Q~h_rq3YtyeKb.9zv-SjnN.j4.bo7EmmDczN',
#         tenant_id='a40e4c7f-e1b4-4c80-a959-c81ad14d8133',
#         resource='https://orgbb73a388.crm5.dynamics.com/'
#     )
#     data = {
#         "subject": "拜访河南优文图新有限公司",
#         "scheduled_start": "2023-10-10T10:00:00",
#         "scheduled_end": "2023-10-10T11:00:00",
#         "location": "河南优文图新有限公司",
#         "description": "客户需求购买20台研磨机，5月前交付"
#     }
#     result = client.create_appointment(**data)
#     print(result)
if __name__ == '__main__':
    client_id = '9bcc6265-27d4-4843-b73b-b2666ab9b776'
    client_secret = 'DuT8Q~h_rq3YtyeKb.9zv-SjnN.j4.bo7EmmDczN'
    tenant_id = 'a40e4c7f-e1b4-4c80-a959-c81ad14d8133'
    resource = 'https://orgbb73a388.crm5.dynamics.com/'
    {'entity_name': 'contacts', 'search_criteria': {'emailaddress1': 'wxm2021@gmail.com'}}

    r = Dynamics365Client(client_id,
                      client_secret,
                      tenant_id,
                      resource).get_all_campaigns()
    print(r)