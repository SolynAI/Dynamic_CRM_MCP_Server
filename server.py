import asyncio
import logging
import os
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent
from dynamics_365_client import Dynamics365Client
from tools import tool_list
import tools
import json
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("dynamics_365_mcp_server")


def get_crm_config():
    """Get CRM configuration from environment variables."""
    config = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "tenant_id": os.getenv("TENANT_ID"),
        "resource": os.getenv("RESOURCE")
    }

    if not all(config.values()):
        logger.error("Missing required CRM configuration. Please check environment variables:")
        logger.error("CLIENT_ID, CLIENT_SECRET, TENANT_ID and RESOURCE are required")
        raise ValueError("Missing required CRM configuration")

    return config


# Initialize server
app = Server("dynamics_365_crm_server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available Dynamics 365 CRM tools."""
    logger.info("Listing all CRM tools...")
    return tool_list


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute Dynamics 365 CRM tool operation"""
    config = get_crm_config()
    logger.info(f"Calling tool: {name} with arguments: {arguments}")
    client = Dynamics365Client(**config)

    try:
        match name:
            # 线索相关操作
            case tools.DYNAMICS365_CREATE_LEAD:
                result = client.create_lead(**arguments)
            case tools.DYNAMICS365_GET_ALL_LEADS:
                result = client.get_all_leads(**arguments)

            # 客户操作
            case tools.DYNAMICS365_CREATE_CONTACT:
                result = client.create_contact(**arguments)
            case tools.DYNAMICS365_GET_ALL_CONTACTS:
                result = client.get_all_contacts(**arguments)

            # 联系人操作
            case tools.DYNAMICS365_CREATE_ACCOUNT:
                result = client.create_account(**arguments)
            case tools.DYNAMICS365_GET_all_ACCOUNTS:
                result = client.get_all_accounts(**arguments)

            # 活动管理
            case tools.DYNAMICS365_CREATE_APPOINTMENT:
                result = client.create_appointment(**arguments)
            case tools.DYNAMICS365_GET_ALL_ACTIVITIES:
                result = client.get_all_activities(**arguments)

            # 获取实体id
            case tools.DYNAMICS365_FIND_ENTITY_ID:
                result = client.find_entity_id(**arguments)
            # 实体查询
            case tools.DYNAMICS365_QUERY_ENTITY:
                result = client.query_entity(**arguments)

            # 市场活动
            case tools.DYNAMICS365_GET_ALL_CAMPAIGNS:
                result = client.get_all_campaigns(**arguments)

            # 商机操作
            case tools.DYNAMICS365_CREATE_OPPORTUNITY:
                result = client.create_opportunity(**arguments)
            case tools.DYNAMICS365_GET_ALL_OPPORTUNITIES:
                result = client.get_all_opportunities(**arguments)

            # 订单操作
            case tools.DYNAMICS365_CREATE_SALES_ORDER:
                result = client.create_sales_order(**arguments)
            case tools.DYNAMICS365_GET_ALL_SALES_ORDERS:
                result = client.get_all_sales_orders(**arguments)

            # 案例操作
            case tools.DYNAMICS365_CREATE_INCIDENT:
                result = client.create_incident(**arguments)
            case tools.DYNAMICS365_GET_ALL_INCIDENTS:
                result = client.get_all_incidents(**arguments)

            # 产品操作
            case tools.DYNAMICS365_GET_ALL_PRODUCTS:
                result = client.get_all_products(**arguments)

            # 价目表项(ProductPriceLevel)操作
            case tools.DYNAMICS365_GET_product_PRICELEVELS:
                result = client.get_all_product_pricelevels(**arguments)

            # 邮件操作
            case tools.DYNAMICS365_GET_ALL_EMAILS:
                result = client.get_all_emails(**arguments)

            # 其他未匹配的工具
            case _:
                logger.warning(f"Unknown tool name: {name}")
                return [TextContent(type="text", text=f"Error: Unsupported tool operation '{name}'")]

        logger.info(result)
        result = str(result)
        return [TextContent(type="text", text=result)]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}", exc_info=True)
        return [TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")]


async def main():
    """Main entry point to run the MCP server."""
    from mcp.server.stdio import stdio_server

    logger.info("Starting Dynamics 365 CRM MCP server...")
    config = get_crm_config()
    logger.info(f"CRM config loaded: {config}")

    async with stdio_server() as (read_stream, write_stream):
        try:
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
        except Exception as e:
            logger.error(f"Server error: {str(e)}", exc_info=True)
            raise


if __name__ == "__main__":
    asyncio.run(main())