import motor.motor_asyncio
from config import DB_URL

class Rohit:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
        self.database = self.client["Cluster0"]  # your DB name stays same

    # ==========================
    #   VERIFY MODE FUNCTIONS
    # ==========================

    async def get_val(self, key: str):
        """Get value from settings collection."""
        data = await self.database["settings"].find_one({"_id": key})
        return data["value"] if data else False

    async def update_val(self, key: str, value):
        """Update or insert value inside settings."""
        await self.database["settings"].update_one(
            {"_id": key},
            {"$set": {"value": value}},
            upsert=True
        )

    # ============================================
    #   EXISTING CODE (DON'T TOUCH BELOW THIS)
    # ============================================

    async def add_user(self, user_id):
        user = await self.database.users.find_one({"user_id": user_id})
        if user:
            return
        return await self.database.users.insert_one({"user_id": user_id})

    async def is_user_exist(self, user_id):
        user = await self.database.users.find_one({"user_id": user_id})
        return True if user else False

    async def total_users_count(self):
        count = await self.database.users.count_documents({})
        return count

    async def get_all_users(self):
        return self.database.users.find({})
    
    async def add_banned_user(self, user_id):
        user = await self.database.banned_users.find_one({"user_id": user_id})
        if user:
            return
        return await self.database.banned_users.insert_one({"user_id": user_id})

    async def remove_banned_user(self, user_id):
        await self.database.banned_users.delete_one({"user_id": user_id})

    async def is_banned(self, user_id):
        user = await self.database.banned_users.find_one({"user_id": user_id})
        return True if user else False
        

# create global db object
db = Rohit()
