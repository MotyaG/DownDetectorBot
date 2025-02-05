from bot import run
from database import Database
import asyncio

db = Database("database.db")
db.create_db()

async def main():
    await run()

if __name__ == "__main__":
    asyncio.run(main())
