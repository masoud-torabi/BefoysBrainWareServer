from fastmcp import FastMCP
from database_suppliers.suppliers_utils import search_top_k_suppliers

mcp = FastMCP("supply-chain-mcp")
def get_context_from_database(user_id: str) -> str:
    return f"""
    اطلاعات کاربر: {user_id}
    هتل آتنا امروز با کمبود مواد اولیه مواجه است.
    تامین‌کننده اصلی شرکت «بهار دشت» است.
    سفارش‌های جدید در وضعیت بررسی می‌باشند.
    """.strip()

@mcp.tool()
def get_context(query: str) -> str:
    """
    Returns dynamic supply chain context for a specific user.
    """
    return get_context_from_database(query)



@mcp.tool()
def search_suppliers(query: str) -> dict:
    return search_top_k_suppliers(query, k=5)

if __name__ == "__main__":
    mcp.run()
