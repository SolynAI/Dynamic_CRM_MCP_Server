from mcp.types import Resource, Tool, TextContent

# 线索相关操作
DYNAMICS365_CREATE_LEAD = "create_lead"
DYNAMICS365_GET_ALL_LEADS = "get_all_leads"

# 客户操作
DYNAMICS365_CREATE_CONTACT = "create_contact"
DYNAMICS365_GET_ALL_CONTACTS = "get_all_contacts"
# 联系人操作
DYNAMICS365_CREATE_ACCOUNT = "create_account"
DYNAMICS365_GET_all_ACCOUNTS = "get_all_accounts"

# 活动管理
DYNAMICS365_CREATE_APPOINTMENT = 'create_appointment'
DYNAMICS365_GET_ALL_ACTIVITIES = "get_all_activities"

# 获取实体id
DYNAMICS365_FIND_ENTITY_ID = "find_entity_id"
DYNAMICS365_QUERY_ENTITY = "query_entity"

# 市场活动
DYNAMICS365_GET_ALL_CAMPAIGNS = 'get_all_campaigns'

# 商机(Opportunity)操作
DYNAMICS365_CREATE_OPPORTUNITY = "create_opportunity"
DYNAMICS365_GET_ALL_OPPORTUNITIES = "get_all_opportunities"

# 订单(SalesOrder)操作
DYNAMICS365_CREATE_SALES_ORDER = "create_sales_order"
DYNAMICS365_GET_ALL_SALES_ORDERS = "get_all_sales_orders"

# 案例(Incident)操作
DYNAMICS365_CREATE_INCIDENT = "create_incident"
DYNAMICS365_GET_ALL_INCIDENTS = "get_all_incidents"

# 产品(Product)操作
DYNAMICS365_GET_ALL_PRODUCTS = "get_all_products"

# 价目表项(ProductPriceLevel)操作
DYNAMICS365_GET_product_PRICELEVELS = "get_all_product_pricelevels"

# 邮件操作
DYNAMICS365_GET_ALL_EMAILS = "get_all_emails"

tool_list = [
    Tool(
        name=DYNAMICS365_CREATE_LEAD,
        description="在Dynamics CRM中创建新的潜在客户记录",
        inputSchema={
            "type": "object",
            "properties": {
                "subject": {
                    "description": "主题",
                    "type": "string",
                    "examples": ["新潜在客户 - 张三"]
                },
                "firstname": {
                    "description": "潜在客户的名字",
                    "type": "string",
                    "examples": ["张"]
                },
                "lastname": {
                    "description": "潜在客户的姓氏",
                    "type": "string",
                    "examples": ["三"]
                },
                "jobtitle": {
                    "description": "潜在客户的职务",
                    "type": "string",
                    "examples": ["CEO"]
                },
                "mobilephone": {
                    "description": "潜在客户的移动电话",
                    "type": "string",
                    "examples": ["+86 13849986547"]
                },
                "emailaddress1": {
                    "description": "潜在客户的主要电子邮件地址",
                    "type": "string",
                    "examples": ["zhangsan@example.com"]
                },
                "companyname": {
                    "description": "与潜在客户关联的公司名称",
                    "type": "string",
                    "examples": ["示例公司"]
                },
                "telephone1": {
                    "description": "潜在客户的主要电话号码",
                    "type": "string",
                    "examples": ["+86-138-1234-5678"]
                },
                "address1_postalcode": {
                    "description": "潜在客户的邮政编码",
                    "type": "string",
                    "examples": ["785556"]
                },
                "address1_country": {
                    "description": "潜在客户的国家",
                    "type": "string",
                    "examples": ["中华人民共和国"]
                },
                "address1_stateorprovince": {
                    "description": "潜在客户的省/直辖市/自治区",
                    "type": "string",
                    "examples": ["河南省"]
                },
                "address1_city": {
                    "description": "潜在客户的市/县",
                    "type": "string",
                    "examples": ["洛阳市"]
                },
                "address1_line1": {
                    "description": "潜在客户的街道",
                    "type": "string",
                    "examples": ["秦岭路"]
                }
            },
            "required": ["subject", "lastname"],
            "title": "创建潜在客户请求"
        }
    ),
    Tool(
        name=DYNAMICS365_GET_ALL_LEADS,
        description="获取所有潜在客户列表",
        inputSchema={
            "type": "object",
            "properties": {
                "top": {
                    "description": "返回记录数量",
                    "type": "integer",
                    "default": 1000
                }
            },
            "title": "获取所有潜在客户请求"
        }
    ),
    Tool(
        name=DYNAMICS365_GET_ALL_ACTIVITIES,
        description="获取当前账号下的所有客户活动(包括会议、电话、邮件、任务等)，支持按类型和时间范围筛选",
        inputSchema={
            "type": "object",
            "properties": {
                "top": {
                    "description": "返回记录数量限制(1-1000)",
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 1000,
                    "default": 100
                }
            },
            "title": "获取客户活动请求"
        }
    ),
    Tool(
        name=DYNAMICS365_CREATE_CONTACT,
        description="创建新的联系人记录",
        inputSchema={
            "type": "object",
            "properties": {
                "firstname": {
                    "description": "联系人的名字",
                    "type": "string",
                    "examples": ["李"]
                },
                "lastname": {
                    "description": "联系人的姓氏",
                    "type": "string",
                    "examples": ["四"]
                },
                "emailaddress1": {
                    "description": "主要电子邮件地址",
                    "type": "string",
                    "examples": ["lisi@example.com"]
                },
                "telephone1": {
                    "description": "主要电话号码",
                    "type": "string",
                    "examples": ["+86-139-8765-4321"]
                },
                "jobtitle": {
                    "description": "职位名称",
                    "type": "string",
                    "examples": ["销售经理"]
                },
                "address1_postalcode": {
                    "description": "邮政编码",
                    "type": "string",
                    "examples": ["785556"]
                },
                "address1_country": {
                    "description": "国家",
                    "type": "string",
                    "examples": ["中华人民共和国"]
                },
                "address1_stateorprovince": {
                    "description": "省/直辖市/自治区",
                    "type": "string",
                    "examples": ["河南省"]
                },
                "address1_city": {
                    "description": "市/县",
                    "type": "string",
                    "examples": ["洛阳市"]
                },
                "address1_line1": {
                    "description": "街道",
                    "type": "string",
                    "examples": ["秦岭路"]
                }
            },
            "required": ["lastname"],
            "title": "创建联系人请求"
        }
    ),
    Tool(
        name=DYNAMICS365_GET_ALL_CONTACTS,
        description="获取联系人信息",
        inputSchema={
            "type": "object",
            "properties": {
                "top": {
                    "description": "返回结果数量限制",
                    "type": "integer",
                    "default": 1000
                }
            }
        }
    ),
    Tool(
        name=DYNAMICS365_CREATE_ACCOUNT,
        description="创建新的客户(公司)记录，并可关联主联系人和附加联系人",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "description": "客户公司名称",
                    "type": "string",
                    "examples": ["示例有限公司"]
                },
                "primarycontactid": {
                    "description": "主联系人ID(可选)",
                    "type": "string",
                    "examples": ["00000000-0000-0000-0000-000000000000"]
                },
                "other_contact_ids": {
                    "description": "其他关联联系人ID列表(可选)",
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "examples": [["00000000-0000-0000-0000-000000000000", "00000000-0000-0000-0000-000000000001"]]
                },
                "industrycode": {
                    "description": "行业代码(可选)",
                    "type": "integer",
                    "examples": [1]
                },
                "revenue": {
                    "description": "年收入(可选)",
                    "type": "number",
                    "examples": [1000000]
                },
                "telephone1": {
                    "description": "主要电话(可选)",
                    "type": "string",
                    "examples": ["123-456-7890"]
                },
                "websiteurl": {
                    "description": "网站URL(可选)",
                    "type": "string",
                    "examples": ["https://www.example.com"]
                },
                "address1_line1": {
                    "description": "地址行1(可选)",
                    "type": "string",
                    "examples": ["123 Main St"]
                },
                "address1_city": {
                    "description": "城市(可选)",
                    "type": "string",
                    "examples": ["New York"]
                },
                "address1_stateorprovince": {
                    "description": "州/省(可选)",
                    "type": "string",
                    "examples": ["NY"]
                },
                "address1_postalcode": {
                    "description": "邮编(可选)",
                    "type": "string",
                    "examples": ["10001"]
                },
                "address1_country": {
                    "description": "国家(可选)",
                    "type": "string",
                    "examples": ["USA"]
                },
                "description": {
                    "description": "客户描述信息(可选)",
                    "type": "string",
                    "examples": ["这是一家专注于IT解决方案的公司"]
                },
                "transactioncurrencyid": {
                    "description": "货币id",
                    "type": "string",
                    "examples": ["5fd825f9-2ddd-ef11-8eea-000d3ac7f225"]
                }
            },
            "required": ["name"],
            "title": "创建客户请求"
        }
    ),
    Tool(
        name=DYNAMICS365_FIND_ENTITY_ID,
        description="根据条件查询实体ID，支持精确/模糊匹配和分页",
        inputSchema={
            "type": "object",
            "properties": {
                "entity_name": {
                    "description": "实体类型(contacts/accounts/leads等)",
                    "type": "string",
                    "enum": ["contacts", "accounts", "leads"],
                    "examples": ["contacts"]
                },
                "search_criteria": {
                    "description": "查询条件字典(字段: 值)",
                    "type": "object",
                    "examples": [{"emailaddress1": "test@example.com"}]
                },
                "exact_match": {
                    "description": "是否全局精确匹配",
                    "type": "boolean",
                    "default": False
                }
            },
            "required": ["entity_name", "search_criteria"],
            "title": "实体ID查询请求"
        }
    ),
    # 市场活动操作
    Tool(
        name=DYNAMICS365_GET_ALL_CAMPAIGNS,
        description="查询当前账号下正在执行的市场活动",
        inputSchema={
            "type": "object",
            "properties": {
                "top": {
                    "description": "返回结果数量限制",
                    "type": "integer",
                    "default": 1000
                }
            },
            "title": "获取进行中的市场活动请求"
        }
    ),
    Tool(
        name=DYNAMICS365_CREATE_APPOINTMENT,
        description="在Dynamics CRM中创建新的拜访记录(Appointment)",
        inputSchema={
            "type": "object",
            "properties": {
                "subject": {
                    "description": "拜访主题",
                    "type": "string",
                    "examples": ["客户季度业务回顾"]
                },
                "scheduledstart": {
                    "description": "计划开始时间(ISO格式)",
                    "type": "string",
                    "format": "date-time",
                    "examples": ["2023-06-15T14:00:00"]
                },
                "scheduledend": {
                    "description": "计划结束时间(ISO格式)",
                    "type": "string",
                    "format": "date-time",
                    "examples": ["2023-06-15T15:00:00"]
                },
                "location": {
                    "description": "拜访地点",
                    "type": "string",
                    "examples": ["客户办公室"]
                },
                "description": {
                    "description": "拜访详细描述",
                    "type": "string",
                    "examples": ["讨论下季度合作计划和业务增长机会"]
                },
                "regardingobjectid_account": {
                    "description": "关联的客户ID(可选)",
                    "type": "string",
                    "examples": ["12345678-1234-1234-1234-123456789abc"]
                },
                "regardingobjectid_contact": {
                    "description": "关联的联系人ID(可选)",
                    "type": "string",
                    "examples": ["87654321-4321-4321-4321-987654321abc"]
                },
                "prioritycode": {
                    "description": "优先级代码(1=低, 2=中, 3=高)",
                    "type": "integer",
                    "enum": [1, 2, 3],
                    "default": 2
                },
                "category": {
                    "description": "活动类别",
                    "type": "string",
                    "examples": ["客户拜访"]
                },
                "isalldayevent": {
                    "description": "是否全天事件",
                    "type": "boolean",
                    "default": False
                }
            },
            "required": ["subject", "scheduled_start", "scheduled_end"],
            "title": "创建拜访记录请求"
        }
    ),
    Tool(
        name=DYNAMICS365_GET_all_ACCOUNTS,
        description="获取客户信息",
        inputSchema={
            "type": "object",
            "properties": {
                "top": {
                    "description": "返回结果数量限制",
                    "type": "integer",
                    "default": 1000
                }
            }
        }
    ),
    Tool(
        name=DYNAMICS365_CREATE_OPPORTUNITY,
        description="创建新的商机(项目)",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "商机主题"
                },
                "budgetamount": {
                    "type": "number",
                    "description": "预算金额"
                },
                "parentcontactid": {
                    "type": "string",
                    "description": "关联联系人ID"
                },
                "description": {
                    "type": "string",
                    "description": "商机描述"
                }
            },
            "required": ["name", "budgetamount"]
        }
    ),
    Tool(
        name=DYNAMICS365_GET_ALL_OPPORTUNITIES,
        description="获取商机关联的产品列表",
        inputSchema={
            "type": "object",
            "properties": {
                "top": {
                    "description": "返回结果数量限制",
                    "type": "integer",
                    "default": 1000
                }
            },
            "required": []
        }
    ),
    Tool(
        name=DYNAMICS365_CREATE_SALES_ORDER,
        description="创建新的订单",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "订单名称"
                },
                "customerid": {
                    "type": "string",
                    "description": "客户ID"
                },
                "description": {
                    "type": "string",
                    "description": "订单描述"
                }
            },
            "required": ["name", "customerid"]
        }
    ),
    Tool(
        name=DYNAMICS365_GET_ALL_SALES_ORDERS,
        description="获取订单明细项",
        inputSchema={
            "type": "object",
            "properties": {
                "top": {
                    "description": "返回结果数量限制",
                    "type": "integer",
                    "default": 1000
                }
            },
            "required": []
        }
    ),
    Tool(
        name=DYNAMICS365_CREATE_INCIDENT,
        description="创建新的服务案例",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "案例标题"
                },
                "customerid": {
                    "type": "string",
                    "description": "客户ID"
                },
                "description": {
                    "type": "string",
                    "description": "案例详细描述"
                }
            },
            "required": ["title", "customerid"]
        }
    ),
    Tool(
        name=DYNAMICS365_GET_ALL_INCIDENTS,
        description="获取当前账号下的所有服务案例",
        inputSchema={
            "type": "object",
            "properties": {
                "top": {
                    "description": "返回结果数量限制",
                    "type": "integer",
                    "default": 1000
                }
            },
            "required": []
        }
    ),
    Tool(
        name=DYNAMICS365_GET_ALL_PRODUCTS,
        description="获取所有产品信息",
        inputSchema={
            "type": "object",
            "properties": {
                "filter": {
                    "type": "string",
                    "description": "过滤条件(OData格式)"
                },
                "top": {
                    "type": "integer",
                    "description": "返回数量限制",
                    "default": 1000
                }
            }
        }
    ),
    Tool(
        name=DYNAMICS365_GET_product_PRICELEVELS,
        description="获取价目表项(价格体系)",
        inputSchema={
            "type": "object",
            "properties": {
                "top": {
                    "description": "返回结果数量限制",
                    "type": "integer",
                    "default": 1000
                }
            },
            "required": []
        }
    ),
    Tool(
        name=DYNAMICS365_GET_ALL_EMAILS,
        description="获取当前帐号下的邮件记录",
        inputSchema={
            "type": "object",
            "properties": {
                "top": {
                    "description": "返回结果数量限制",
                    "type": "integer",
                    "default": 1000
                }
            },
            "required": []
        }
    ),
    Tool(
        name=DYNAMICS365_QUERY_ENTITY,
        description="通用实体查询方法",
        inputSchema={
            "type": "object",
            "properties": {
                "entity_name": {
                    "type": "string",
                    "description": "实体名称(如accounts,contacts等)"
                },
                "filter": {
                    "type": "string",
                    "description": "过滤条件(OData格式)"
                },
                "select": {
                    "type": "string",
                    "description": "选择返回字段"
                },
                "expand": {
                    "type": "string",
                    "description": "扩展关联实体"
                },
                "top": {
                    "type": "integer",
                    "description": "返回数量限制"
                },
                "orderby": {
                    "type": "string",
                    "description": "排序字段"
                }
            },
            "required": ["entity_name"]
        }
    )
]
