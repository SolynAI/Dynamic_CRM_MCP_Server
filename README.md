# solyn_dynamics365_mcp_server
# Overview
The Microsoft Dynamics 365 MCP Server is a MCP server that provides tools to interact with Microsoft Dynamics 365 using the Model Context Protocol(MCP) by Anthorpic. It allows users to perform various operations such as retrieving user information, accounts, opportunities associated with an account, create and update accounts from Claude Desktop.

# List of Tools 🛠️

| Tool Name                     | Description                                                                 | Input Parameters                                                                                                                                                                                                                                                                                                                                 | Output                     |
|-------------------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|
| `create_lead`                 | 在Dynamics CRM中创建新的潜在客户记录                                         | **Required:**<br>`subject` (string), `lastname` (string)<br>**Optional:**<br>`firstname`, `jobtitle`, `mobilephone`, `emailaddress1`, `companyname`, `telephone1`, `address1_postalcode`, `address1_country`, `address1_stateorprovince`, `address1_city`, `address1_line1`                                                                        | 创建的潜在客户记录详情     |
| `get_all_leads`               | 获取所有潜在客户列表                                                        | `top` (integer, default=1000)                                                                                                                                                                                                                                                                                                                   | 潜在客户列表(JSON格式)    |
| `get_all_activities`          | 获取当前账号下的所有客户活动(包括会议、电话、邮件、任务等)                   | `top` (integer, 1-1000, default=100)                                                                                                                                                                                                                                                                                                            | 客户活动列表(JSON格式)    |
| `create_contact`              | 创建新的联系人记录                                                          | **Required:**<br>`lastname` (string)<br>**Optional:**<br>`firstname`, `emailaddress1`, `telephone1`, `jobtitle`, `address1_postalcode`, `address1_country`, `address1_stateorprovince`, `address1_city`, `address1_line1`                                                                                                                         | 创建的联系人记录详情      |
| `get_all_contacts`            | 获取联系人信息                                                              | `top` (integer, default=1000)                                                                                                                                                                                                                                                                                                                   | 联系人列表(JSON格式)      |
| `create_account`              | 创建新的客户(公司)记录，并可关联主联系人和附加联系人                        | **Required:**<br>`name` (string)<br>**Optional:**<br>`primarycontactid`, `other_contact_ids`, `industrycode`, `revenue`, `telephone1`, `websiteurl`, `address1_line1`, `address1_city`, `address1_stateorprovince`, `address1_postalcode`, `address1_country`, `description`, `transactioncurrencyid`                                              | 创建的客户记录详情        |
| `find_entity_id`              | 根据条件查询实体ID，支持精确/模糊匹配和分页                                 | **Required:**<br>`entity_name` (enum: contacts/accounts/leads), `search_criteria` (object)<br>**Optional:**<br>`exact_match` (boolean, default=False)                                                                                                                                                                                            | 实体ID信息                |
| `get_all_campaigns`           | 查询当前账号下正在执行的市场活动                                            | `top` (integer, default=1000)                                                                                                                                                                                                                                                                                                                   | 市场活动列表(JSON格式)    |
| `create_appointment`          | 在Dynamics CRM中创建新的拜访记录(Appointment)                               | **Required:**<br>`subject` (string), `scheduledstart` (date-time), `scheduledend` (date-time)<br>**Optional:**<br>`location`, `description`, `regardingobjectid_account`, `regardingobjectid_contact`, `prioritycode` (1/2/3), `category`, `isalldayevent` (boolean)                                                                              | 创建的拜访记录详情        |
| `get_all_accounts`            | 获取客户信息                                                                | `top` (integer, default=1000)                                                                                                                                                                                                                                                                                                                   | 客户列表(JSON格式)        |
| `create_opportunity`          | 创建新的商机(项目)                                                          | **Required:**<br>`name` (string), `budgetamount` (number)<br>**Optional:**<br>`parentcontactid`, `description`                                                                                                                                                                                                                                   | 创建的商机记录详情        |
| `get_all_opportunities`       | 获取商机关联的产品列表                                                      | `top` (integer, default=1000)                                                                                                                                                                                                                                                                                                                   | 商机列表(JSON格式)        |
| `create_sales_order`          | 创建新的订单                                                                | **Required:**<br>`name` (string), `customerid` (string)<br>**Optional:**<br>`description`                                                                                                                                                                                                                                                        | 创建的订单详情            |
| `get_all_sales_orders`        | 获取订单明细项                                                              | `top` (integer, default=1000)                                                                                                                                                                                                                                                                                                                   | 订单列表(JSON格式)        |
| `create_incident`             | 创建新的服务案例                                                            | **Required:**<br>`title` (string), `customerid` (string)<br>**Optional:**<br>`description`                                                                                                                                                                                                                                                       | 创建的服务案例详情        |
| `get_all_incidents`           | 获取当前账号下的所有服务案例                                                | `top` (integer, default=1000)                                                                                                                                                                                                                                                                                                                   | 服务案例列表(JSON格式)    |
| `get_all_products`            | 获取所有产品信息                                                            | **Optional:**<br>`filter` (string), `top` (integer, default=1000)                                                                                                                                                                                                                                                                               | 产品列表(JSON格式)        |
| `get_all_product_pricelevels` | 获取价目表项(价格体系)                                                      | `top` (integer, default=1000)                                                                                                                                                                                                                                                                                                                   | 价目表项列表(JSON格式)    |
| `get_all_emails`              | 获取当前帐号下的邮件记录                                                    | `top` (integer, default=1000)                                                                                                                                                                                                                                                                                                                   | 邮件记录列表(JSON格式)    |
| `query_entity`                | 通用实体查询方法                                                            | **Required:**<br>`entity_name` (string)<br>**Optional:**<br>`filter`, `select`, `expand`, `top`, `orderby`                                                                                                                                                                                                                                       | 查询结果(JSON格式)        |

# Dynamics 365 MCP Server Integration

## Prerequisites 📝

Before setting up the project, ensure you have the following:

- **Python 3.10** or later
- Access to a **Dynamics 365 instance** with API permissions
- **Azure Active Directory (AAD)** application configured with Dynamics 365 API access
  - Application must have the following permissions:
    - Dynamics CRM user_impersonation
    - Office 365 Exchange Online

## Setup & Installation ⚙️

### 1. Clone Repository
```bash
git clone https://github.com/your-repo/dynamics365-mcp-server.git
cd dynamics365-mcp-server
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## Claude for Desktop Integration 🖥️
Add this configuration to your Claude settings file (settings.json):
```json
{
    "mcpServers": {
        "Dynamic_CRM_MCP_Server": {
            "command": "python",
            "args": ["Dynamic_CRM_MCP_Server/server.py"],
            "env": {
                "CLIENT_ID": "<your_client_id>",
                "CLIENT_SECRET": "<your_client_secret>",
                "TENANT_ID": "<your_tenant_id>",
                "RESOURCE": "<your_dynamics365_resource_url>"
            }
        }
    }
}
```

## Note
Replace values in <angle_brackets> with your actual credentials:

CLIENT_ID: Azure AD Application ID

CLIENT_SECRET: Azure AD Client Secret

TENANT_ID: Azure Directory (tenant) ID

RESOURCE: Dynamics 365 instance URL (e.g. https://orgname.crm.dynamics.com)
