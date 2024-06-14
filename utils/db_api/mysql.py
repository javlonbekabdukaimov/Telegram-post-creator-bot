import aiomysql
from aiomysql import Pool, Connection
from typing import Union

from data import config

class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create_database(self):
        async with aiomysql.connect(
                host=config.DB_HOST,
                port=config.DB_PORT,
                user=config.DB_USER,
                password=config.DB_PASS
        ) as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}")

    async def create_pool(self):
        self.pool = await aiomysql.create_pool(host=config.DB_HOST,
                                               port=config.DB_PORT,
                                               user=config.DB_USER,
                                               password=config.DB_PASS,
                                               db=config.DB_NAME)

    async def create_table(self):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    CREATE TABLE IF NOT EXISTS info (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        user_id BIGINT,
                        address TEXT,
                        orientation TEXT,
                        price INT,
                        size INT,
                        no_of_rooms INT,
                        no_of_floors INT,
                        h_floor INT,
                        owner_phone TEXT,
                        extra_info TEXT,
                        photo_id TEXT
                    )
                """)

    async def insert_info(self, user_id, address, orientation, price, size, no_of_rooms, no_of_floors, h_floor, owner_phone, extra_info, photo_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO info (user_id, address, orientation, price, size, no_of_rooms, no_of_floors, h_floor, owner_phone, extra_info, photo_id)"
                                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                  (user_id, address, orientation, price, size, no_of_rooms, no_of_floors, h_floor, owner_phone, extra_info, photo_id))
                await conn.commit()

    async def get_info_by_criteria(self, address=None, min_price=None, max_price=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = "SELECT * FROM info WHERE 1=1"
                parameters = []

                if address is not None:
                    query += " AND address = %s"
                    parameters.append(address)
                if min_price is not None:
                    query += " AND price >= %s"
                    parameters.append(min_price)
                if max_price is not None:
                    query += " AND price <= %s"
                    parameters.append(max_price)

                await cur.execute(query, parameters)
                rows = await cur.fetchall()
                return rows
