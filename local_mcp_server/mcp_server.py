import asyncio
from mcp.server.fastmcp import FastMCP
from database_suppliers.suppliers_utils import search_top_k_suppliers

mcp = FastMCP("supply-chain-mcp",
               host="0.0.0.0",
               port=9090)

@mcp.tool()
async def search_suppliers(query: str) -> dict:
    """Fetch suppliers from database
    Args: query:
    Output: 
    """
    return search_top_k_suppliers(query, k=5)

@mcp.tool()
async def get_product_info(product_id: int) -> dict:
    """
    fetch products from database
    """

    products = {
        101: {
            "name": "Rice – Hashemi",
            "category": "Food",
            "brand": "Local Farm",
            "price": 320000,
            "unit": "1 kg",
            "in_stock": True
        },
        102: {
            "name": "Olive Oil",
            "category": "Food",
            "brand": "Golden Olive",
            "price": 450000,
            "unit": "1 liter",
            "in_stock": False
        },
        103: {
            "name": "Tea – Ceylon",
            "category": "Beverages",
            "brand": "Royal Leaf",
            "price": 280000,
            "unit": "500 g",
            "in_stock": True
        },
        104: {
            "name": "Saffron",
            "category": "Spices",
            "brand": "Khorasan Gold",
            "price": 1500000,
            "unit": "4.6 g",
            "in_stock": True
        }
    }

    return products[product_id]

if __name__ == "__main__":
    asyncio.run(mcp.run(transport="streamable-http"))


# http://localhost:9090/mcp