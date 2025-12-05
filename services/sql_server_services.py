import pyodbc
from datetime import datetime
from models.UserInformation import UserInformation
from models.ChatHistory import ChatHistory
from configs.config_loader import load_config

config = load_config()
db = config["sql_server"]

def get_database_connection():
    conn = pyodbc.connect(
        f"DRIVER={{{db['driver']}}};"
        f"SERVER={db['server']};"
        f"DATABASE={db['database']};"
        f"UID={db['username']};"
        f"PWD={db['password']};"
    )

    return conn

def get_user_by_mobile(mobile: str) -> UserInformation | None:

    conn = get_database_connection()
    cursor = conn.cursor()
    query = """
        SELECT [Id]
            ,[FullName]
            ,[CompanyName]
            ,[Role]
            ,[TelegramId]
            ,[Mobile]
            ,[Email]
        FROM [dbo].[Customer]
        WHERE Mobile = ?
    """

    cursor.execute(query, (mobile,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return UserInformation(
            user_id = row.Id,
            full_name = row.FullName,
            company = row.CompanyName,
            mobile = row.Mobile,
            role = row.Role
        )
    else:
        return None



def get_last_chat_history(user_id: int, platform: str, limit: int = 10) -> list[ChatHistory]:
    """
    Returns the last N chat history records for a given user.
    """
    conn = get_database_connection()
    cursor = conn.cursor()

    query = f"""
        SELECT TOP {limit} [ChatMessage].* FROM [ChatMessage]
        INNER JOIN [Chat] ON [ChatMessage].[ChatId] = Chat.Id
        WHERE
            [Chat].[CustomerId] = {user_id} AND
            [Chat].[Platform] = '{platform}'
        ORDER BY [ChatMessage].Id DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    history_list = []

    for row in rows:
        history_list.append(ChatHistory(
            chat_id=row.ChatId,
            role="User",
            message=row.Message
        ))
        history_list.append(ChatHistory(
            chat_id=row.ChatId,
            role="Assistant",
            message=row.ResponseMessage
        ))


    return history_list


def insert_chat_message(
        chat_id: int = None,
        type: str = None,
        message: str = None,
        dt: datetime = datetime.now(),
        response_message: str = None,
        response_type: str = None,
        response_dt: datetime = datetime.now(),
        response_status: str = None,
        elapsed: float = None,
        thinking: str = None
    ):

    query = """
        INSERT INTO ChatMessage
        (ChatId, Type, Message, Datetime, ResponseMessage, ResponseType, ResponseDatetime, ResponseStatus, TimeElapsed, Thinking)
        OUTPUT inserted.Id
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    conn = get_database_connection()
    cursor = conn.cursor()

    cursor.execute(query, (
        chat_id,
        type,
        message,
        dt,
        response_message,
        response_type,
        response_dt,
        response_status,
        elapsed,
        thinking
    ))

    inserted_id = cursor.fetchone()[0]
    conn.commit()

    cursor.close()
    conn.close()

    return inserted_id