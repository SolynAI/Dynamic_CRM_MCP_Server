# solyn_dynamics365_mcp_server
List of Tools 🛠️

Tool Name	Description	Input	Output
create_lead	在Dynamics CRM中创建新的潜在客户记录	subject (string, required), firstname (string), lastname (string, required), jobtitle (string), mobilephone (string), emailaddress1 (string), companyname (string), telephone1 (string), address1_postalcode (string), address1_country (string), address1_stateorprovince (string), address1_city (string), address1_line1 (string)	创建的潜在客户记录详情
get_all_leads	获取所有潜在客户列表	top (integer, optional, default=1000)	潜在客户列表(JSON格式)
get_all_activities	获取当前账号下的所有客户活动(包括会议、电话、邮件、任务等)，支持按类型和时间范围筛选	top (integer, optional, 1-1000, default=100)	客户活动列表(JSON格式)
create_contact	创建新的联系人记录	firstname (string), lastname (string, required), emailaddress1 (string), telephone1 (string), jobtitle (string), address1_postalcode (string), address1_country (string), address1_stateorprovince (string), address1_city (string), address1_line1 (string)	创建的联系人记录详情
get_all_contacts	获取联系人信息	top (integer, optional, default=1000)	联系人列表(JSON格式)
create_account	创建新的客户(公司)记录，并可关联主联系人和附加联系人	name (string, required), primarycontactid (string, optional), other_contact_ids (array, optional), industrycode (integer, optional), revenue (number, optional), telephone1 (string, optional), websiteurl (string, optional), address1_line1 (string, optional), address1_city (string, optional), address1_stateorprovince (string, optional), address1_postalcode (string, optional), address1_country (string, optional), description (string, optional), transactioncurrencyid (string, optional)	创建的客户记录详情
find_entity_id	根据条件查询实体ID，支持精确/模糊匹配和分页	entity_name (string, required, enum: contacts/accounts/leads), search_criteria (object, required), exact_match (boolean, optional, default=False)	实体ID信息
get_all_campaigns	查询当前账号下正在执行的市场活动	top (integer, optional, default=1000)	市场活动列表(JSON格式)
create_appointment	在Dynamics CRM中创建新的拜访记录(Appointment)	subject (string, required), scheduledstart (string, format: date-time, required), scheduledend (string, format: date-time, required), location (string, optional), description (string, optional), regardingobjectid_account (string, optional), regardingobjectid_contact (string, optional), prioritycode (integer, optional, enum: 1/2/3, default=2), category (string, optional), isalldayevent (boolean, optional, default=False)	创建的拜访记录详情
get_all_accounts	获取客户信息	top (integer, optional, default=1000)	客户列表(JSON格式)
create_opportunity	创建新的商机(项目)	name (string, required), budgetamount (number, required), parentcontactid (string, optional), description (string, optional)	创建的商机记录详情
get_all_opportunities	获取商机关联的产品列表	top (integer, optional, default=1000)	商机列表(JSON格式)
create_sales_order	创建新的订单	name (string, required), customerid (string, required), description (string, optional)	创建的订单详情
get_all_sales_orders	获取订单明细项	top (integer, optional, default=1000)	订单列表(JSON格式)
create_incident	创建新的服务案例	title (string, required), customerid (string, required), description (string, optional)	创建的服务案例详情
get_all_incidents	获取当前账号下的所有服务案例	top (integer, optional, default=1000)	服务案例列表(JSON格式)
get_all_products	获取所有产品信息	filter (string, optional), top (integer, optional, default=1000)	产品列表(JSON格式)
get_all_product_pricelevels	获取价目表项(价格体系)	top (integer, optional, default=1000)	价目表项列表(JSON格式)
get_all_emails	获取当前帐号下的邮件记录	top (integer, optional, default=1000)	邮件记录列表(JSON格式)
query_entity	通用实体查询方法	entity_name (string, required), filter (string, optional), select (string, optional), expand (string, optional), top (integer, optional), orderby (string, optional)	查询结果(JSON格式)
