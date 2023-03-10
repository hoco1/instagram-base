from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import List
from core.hashing import Hasher
class MongoManager:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str):
        self.client = AsyncIOMotorClient(
            path,
            maxPoolSize=10,
            minPoolSize=10)
        self.db = self.client[settings.DATABASE]
        
    async def close_database_connection(self):
        self.client.close()
        
    async def add_account(self,user):
        user['password'] = Hasher.get_password_hash(user['password'])
        await self.db[settings.TABLE_USERS].insert_one(user)
    
    async def get_account_info(self,username):
        user = await self.db[settings.TABLE_USERS].find_one({"username":username})
        return user
    
    async def get_cookie(self):
        cursor = self.db[settings.TABLE_INSTAGRAM_COOKIE].find().sort("_id",-1).limit(1)
        cookie = []
        async for i in cursor:
            cookie.append(i)
        cookie = cookie[0]
        del cookie['_id']
        return cookie
    
    async def add_instagram_account(self,username,password):
        await self.db[settings.TABLE_INSTAGRAM_ACCOUNTS].insert_one({'username':username,'pwd':password})
        
    async def add_cookie(self,cookie):
        await self.db[settings.TABLE_INSTAGRAM_COOKIE].insert_one(dict(cookie))
        
    
    async def add_follower(self,user):
        await self.db[settings.TABLE_INSTAGRAM_FOLLOWERS].insert_one(user)
        
    async def fetch_follower_data(self,username,limitation=15):
        list_followers = []
        followers =  self.db[settings.TABLE_INSTAGRAM_FOLLOWERS].find({'which_account':username}).limit(limitation)
        async for follower in followers:
            list_followers.append(follower)
        return list_followers
    
    async def add_following(self,user):
        await self.db[settings.TABLE_INSTAGRAM_FOLLOWING].insert_one(user)
        
    async def fetch_following_data(self,username,limitation=15):
        list_following = []
        following =  self.db[settings.TABLE_INSTAGRAM_FOLLOWING].find({'which_account':username}).limit(limitation)
        async for i in following:
            list_following.append(i)
        return list_following
        
    