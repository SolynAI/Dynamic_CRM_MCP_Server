# Solyn_dynamics365_mcp_server
# Overview
The Microsoft Dynamics 365 MCP Server is a MCP server that provides tools to interact with Microsoft Dynamics 365 using the Model Context Protocol(MCP) by Anthorpic. It allows users to perform various operations such as retrieving user information, accounts, opportunities associated with an account, create and update accounts from Claude Desktop.

`Solyn.AI` is an AI-Native application platform designed for generative artificial intelligence services (AIGS) to help enterprises achieve intelligent transformation. The platform is built on a large-scale model of hundreds of billions of units, providing customers in different industries and application scenarios with a variety of development options so that they can create AI native products that adapt to the era of large models.
Solyn.AI integrates the core technologies needed to build AI native applications, including support for hundreds of models, a user-friendly prompt word arrangement interface, a high-performance RAG (Retrieval-Augmented Generation) engine, and a flexibly configurable intelligent agent framework. In addition, Solyn also provides easy-to-use mobile solutions, allowing customers to focus more on innovation and meeting business needs, thereby promoting the development and growth of enterprises.
Find more: www.solyn.ai   

# List of Tools 🛠️

| Tool Name                          | Description                                                                 | Input                                                                                                                                                                                                 | Output                                                                 |
|------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| create_lead                        | 在Dynamics CRM中创建新的潜在客户记录                                         | subject (string, 必填), lastname (string, 必填), [其他可选字段：firstname, jobtitle, mobilephone, emailaddress1, companyname 等]                                                                       | 创建的潜在客户详情（JSON格式）                                        |
| get_all_leads                      | 获取所有潜在客户列表                                                        | top (integer, 可选, 默认1000)                                                                                                                                                                         | 潜在客户列表（JSON格式）                                              |
| get_all_activities                 | 获取当前账号下的所有客户活动                                                | top (integer, 可选, 默认100, 范围1-1000)                                                                                                                                                              | 客户活动列表（JSON格式）                                              |
| create_contact                     | 创建新的联系人记录                                                          | lastname (string, 必填), [其他可选字段：firstname, emailaddress1, telephone1, jobtitle 等地址信息]                                                                                                     | 创建的联系人详情（JSON格式）                                          |
| get_all_contacts                   | 获取联系人信息                                                              | top (integer, 可选, 默认1000)                                                                                                                                                                         | 联系人列表（JSON格式）                                                |
| create_account                     | 创建新的客户(公司)记录                                                      | name (string, 必填), [其他可选字段：primarycontactid, industrycode, revenue, telephone1, websiteurl 等公司信息]                                                                                        | 创建的客户详情（JSON格式）                                            |
| find_entity_id                     | 根据条件查询实体ID                                                          | entity_name (string, 必填, 枚举: contacts/accounts/leads), search_criteria (object, 必填), exact_match (boolean, 可选, 默认False)                                                                      | 匹配的实体ID列表（JSON格式）                                          |
| get_all_campaigns                  | 查询当前账号下正在执行的市场活动                                            | top (integer, 可选, 默认1000)                                                                                                                                                                         | 市场活动列表（JSON格式）                                              |
| create_appointment                 | 创建新的拜访记录                                                            | subject (string, 必填), scheduledstart (date-time, 必填), scheduledend (date-time, 必填), [其他可选字段：location, description, 关联ID等]                                                              | 创建的拜访记录详情（JSON格式）                                        |
| get_all_accounts                   | 获取客户信息                                                                | top (integer, 可选, 默认1000)                                                                                                                                                                         | 客户列表（JSON格式）                                                  |
| create_opportunity                 | 创建新的商机(项目)                                                          | name (string, 必填), budgetamount (number, 必填), [其他可选字段：parentcontactid, description]                                                                                                         | 创建的商机详情（JSON格式）                                            |
| get_all_opportunities              | 获取商机关联的产品列表                                                      | top (integer, 可选, 默认1000)                                                                                                                                                                         | 商机产品列表（JSON格式）                                              |
| create_sales_order                 | 创建新的订单                                                                | name (string, 必填), customerid (string, 必填), [可选字段：description]                                                                                                                               | 创建的订单详情（JSON格式）                                            |
| get_all_sales_orders               | 获取订单明细项                                                              | top (integer, 可选, 默认1000)                                                                                                                                                                         | 订单列表（JSON格式）                                                  |
| create_incident                    | 创建新的服务案例                                                            | title (string, 必填), customerid (string, 必填), [可选字段：description]                                                                                                                              | 创建的服务案例详情（JSON格式）                                        |
| get_all_incidents                  | 获取当前账号下的所有服务案例                                                | top (integer, 可选, 默认1000)                                                                                                                                                                         | 服务案例列表（JSON格式）                                              |
| get_all_products                   | 获取所有产品信息                                                            | filter (string, 可选, OData格式), top (integer, 可选, 默认1000)                                                                                                                                       | 产品列表（JSON格式）                                                  |
| get_all_product_pricelevels        | 获取价目表项(价格体系)                                                      | top (integer, 可选, 默认1000)                                                                                                                                                                         | 价目表项列表（JSON格式）                                              |
| get_all_emails                     | 获取当前帐号下的邮件记录                                                    | top (integer, 可选, 默认1000)                                                                                                                                                                         | 邮件记录列表（JSON格式）                                              |
| query_entity                       | 通用实体查询方法                                                            | entity_name (string, 必填), [可选参数：filter (OData格式), select, expand, top, orderby]                                                                                                               | 查询结果集（JSON格式）                                                |

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
