from abc import ABC, abstractmethod

from sqlalchemy import select, update, delete

from db.psql.connect import AsyncSessionMaker
from db.psql.enums.enums import Roles
from db.psql.models import User


class SqlService(ABC):
    @abstractmethod
    async def run(self):
        raise NotImplementedError


class ReadUsersByRole(SqlService):

    def __init__(self, roles: list[Roles] = None):
        self.roles = roles

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = select(User)
            if self.roles is not None:
                stmt = stmt.where(User.roles.in_(self.roles))
            users = await session.scalars(stmt)
            return users.all()
# --- Чтение по tg_id ---
class ReadUserByTgId(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            result = await session.scalar(select(User).where(User.tg_id == self.tg_id))
            return result


# --- Чтение по username ---
class ReadUserByUsername(SqlService):
    def __init__(self, username: str):
        self.username = username

    async def run(self):
        async with AsyncSessionMaker() as session:
            result = await session.scalar(select(User).where(User.username == self.username))
            return result


# --- Создание пользователя ---
class CreateUser(SqlService):
    def __init__(self, tg_id: int, username: str, first_name: str, last_name: str, roles: Roles = Roles.USER):
        self.tg_id = tg_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.roles = roles

    async def run(self):
        async with AsyncSessionMaker() as session:
            user = User(
                tg_id=self.tg_id,
                username=self.username,
                first_name=self.first_name,
                last_name=self.last_name,
                roles=self.roles,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user


# --- Обновление роли пользователя по tg_id ---
class UpdateUserRoleByTgId(SqlService):
    def __init__(self, tg_id: int, new_role: Roles):
        self.tg_id = tg_id
        self.new_role = new_role

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = (
                update(User)
                .where(User.tg_id == self.tg_id)
                .values(roles=self.new_role)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount  # количество обновлённых строк

# --- Обновление роли пользователя по username ---
class UpdateUserRoleByUsername(SqlService):
    def __init__(self, username: str, new_role: Roles):
        self.username = username
        self.new_role = new_role

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = (
                update(User)
                .where(User.username == self.username)
                .values(roles=self.new_role)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount  # количество обновлённых строк

# --- Удаление пользователя ---
class DeleteUser(SqlService):
    def __init__(self, tg_id: int):
        self.tg_id = tg_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            stmt = (
                delete(User)
                .where(User.tg_id == self.tg_id)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount  # количество удалённых строк

async def run_sql(runnable: SqlService):
    return await runnable.run()