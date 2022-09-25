from typing import List

from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> List[str]:
    return [
        """CREATE TABLE IF NOT EXISTS "subscription" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_setter_id" BIGINT NOT NULL,
    "server_id" BIGINT NOT NULL,
    "channel_id" BIGINT NOT NULL,
    "image_url" VARCHAR(255) NOT NULL,
    CONSTRAINT "uid_subscriptio_server__b9f9f8" UNIQUE ("server_id", "channel_id")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""
    ]


async def downgrade(db: BaseDBAsyncClient) -> List[str]:
    return []
