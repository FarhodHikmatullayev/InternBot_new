from datetime import datetime, timedelta
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config
from data.config import DEVELOPMENT_MODE


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        print('DEVELOPMENT_MODE', DEVELOPMENT_MODE)
        if DEVELOPMENT_MODE:
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME
            )
        else:
            self.pool = await asyncpg.create_pool(
                dsn=config.DATABASE_URL
            )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def create_user(self, phone, username, full_name, telegram_id, role='user', joined_at=datetime.now()):
        sql = "INSERT INTO users (phone, username, full_name, telegram_id, role, joined_at) VALUES($1, $2, $3, $4, $5, $6) RETURNING *"
        return await self.execute(sql, phone, username, full_name, telegram_id, role, joined_at, fetchrow=True)

    async def select_user(self, user_id):
        sql = "SELECT * FROM users WHERE id = $1"
        return await self.execute(sql, user_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def select_users(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_users_last_week(self):
        # Hozirgi sanani olish
        today = datetime.now()
        # Bir hafta oldin sanani hisoblash
        one_week_ago = today - timedelta(days=7)

        sql = """
        SELECT * FROM users 
        WHERE joined_at <= $1 
          AND role = 'user'
        """
        return await self.execute(sql, one_week_ago, fetch=True)

    async def update_user(self, user_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE users SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), user_id, fetchrow=True)

    async def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id = $1 RETURNING *"
        return await self.execute(sql, user_id, fetchrow=True)

    # Department functions
    async def create_department(self, name):
        sql = "INSERT INTO department (name) VALUES($1) RETURNING *"
        return await self.execute(sql, name, fetchrow=True)

    async def select_department(self, department_id):
        sql = "SELECT * FROM department WHERE id = $1"
        return await self.execute(sql, department_id, fetchrow=True)

    async def select_departments(self, **kwargs):
        sql = "SELECT * FROM department WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_departments(self):
        sql = "SELECT * FROM department"
        return await self.execute(sql, fetch=True)

    async def update_department(self, department_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE department SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *list(kwargs.values()), department_id, fetchrow=True)

    async def delete_department(self, department_id):
        sql = "DELETE FROM department WHERE id = $1 RETURNING *"
        return await self.execute(sql, department_id, fetchrow=True)

    # TeacherProfile functions
    async def create_teacher_profile(self, user_id, department_id):
        sql = "INSERT INTO teacher_profile (user_id, department_id, created_at) VALUES($1, $2, $3) RETURNING *"
        return await self.execute(sql, user_id, department_id, datetime.now(), fetchrow=True)

    async def select_teacher_profile(self, profile_id):
        sql = "SELECT * FROM teacher_profile WHERE id = $1"
        return await self.execute(sql, profile_id, fetchrow=True)

    async def select_all_teacher_profiles(self):
        sql = "SELECT * FROM teacher_profile"
        return await self.execute(sql, fetch=True)

    async def select_teacher_profiles(self, **kwargs):
        sql = "SELECT * FROM teacher_profile WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_teacher_profile(self, profile_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE teacher_profile SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *list(kwargs.values()), profile_id, fetchrow=True)

    async def delete_teacher_profile(self, profile_id):
        sql = "DELETE FROM teacher_profile WHERE id = $1 RETURNING *"
        return await self.execute(sql, profile_id, fetchrow=True)

    # ChiefProfile functions
    async def create_chief_profile(self, user_id, department_id):
        sql = "INSERT INTO chief_profile (user_id, department_id, created_at) VALUES($1, $2, $3) RETURNING *"
        return await self.execute(sql, user_id, department_id, datetime.now(), fetchrow=True)

    async def select_chief_profile(self, profile_id):
        sql = "SELECT * FROM chief_profile WHERE id = $1"
        return await self.execute(sql, profile_id, fetchrow=True)

    async def select_all_chief_profiles(self):
        sql = "SELECT * FROM chief_profile"
        return await self.execute(sql, fetch=True)

    async def select_chief_profiles(self, **kwargs):
        sql = "SELECT * FROM chief_profile WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_chief_profile(self, profile_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE chief_profile SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *list(kwargs.values()), profile_id, fetchrow=True)

    async def delete_chief_profile(self, profile_id):
        sql = "DELETE FROM chief_profile WHERE id = $1 RETURNING *"
        return await self.execute(sql, profile_id, fetchrow=True)

    # HR Profile functions
    async def create_hr_profile(self, user_id):
        sql = "INSERT INTO hr_profile (user_id, created_at) VALUES($1, $2) RETURNING *"
        return await self.execute(sql, user_id, datetime.now(), fetchrow=True)

    async def select_hr_profile(self, profile_id):
        sql = "SELECT * FROM hr_profile WHERE id = $1"
        return await self.execute(sql, profile_id, fetchrow=True)

    async def select_all_hr_profiles(self):
        sql = "SELECT * FROM hr_profile"
        return await self.execute(sql, fetch=True)

    async def select_hr_profiles(self, **kwargs):
        sql = "SELECT * FROM hr_profile WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_hr_profile(self, profile_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE hr_profile SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *list(kwargs.values()), profile_id, fetchrow=True)

    async def delete_hr_profile(self, profile_id):
        sql = "DELETE FROM hr_profile WHERE id = $1 RETURNING *"
        return await self.execute(sql, profile_id, fetchrow=True)

    # Intern Profile functions
    async def create_intern_profile(self, user_id, teacher_id, department_id, internship_period):
        sql = "INSERT INTO intern_profile (user_id, teacher_id, department_id, internship_period, created_at, is_active) VALUES($1, $2, $3, $4, $5, $6) RETURNING *"
        return await self.execute(sql, user_id, teacher_id, department_id, internship_period, datetime.now(), True,
                                  fetchrow=True)

    async def select_intern_profile(self, profile_id):
        sql = "SELECT * FROM intern_profile WHERE id = $1"
        return await self.execute(sql, profile_id, fetchrow=True)

    async def select_all_intern_profiles(self):
        sql = "SELECT * FROM intern_profile WHERE is_active = TRUE"
        return await self.execute(sql, fetch=True)

    async def select_intern_profiles(self, **kwargs):
        sql = "SELECT * FROM intern_profile WHERE is_active = TRUE"

        if kwargs:
            sql += " AND "  # Qo'shimcha shartlar qo'shamiz
            sql, parameters = self.format_args(sql, parameters=kwargs)
        else:
            parameters = []

        return await self.execute(sql, *parameters, fetch=True)

    async def update_intern_profile(self, profile_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE intern_profile SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *list(kwargs.values()), profile_id, fetchrow=True)

    async def delete_intern_profile(self, profile_id):
        sql = "DELETE FROM intern_profile WHERE id = $1 RETURNING *"
        return await self.execute(sql, profile_id, fetchrow=True)

    # Mark functions
    async def create_mark(self, intern_id, muomala, kirishimlilik, chaqqonlik_va_malaka, masuliyat,
                          ozlashtirish_qobiliyati, ichki_tartibga_rioyasi, shaxsiy_intizomi, rated_by_id, description):
        sql = """
        INSERT INTO mark (intern_id, muomala, kirishimlilik, chaqqonlik_va_malaka, 
                          masuliyat, ozlashtirish_qobiliyati, ichki_tartibga_rioyasi, 
                          shaxsiy_intizomi, rated_by_id, description, created_at) 
        VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) 
        RETURNING *
        """
        return await self.execute(sql, intern_id, muomala, kirishimlilik, chaqqonlik_va_malaka,
                                  masuliyat, ozlashtirish_qobiliyati, ichki_tartibga_rioyasi,
                                  shaxsiy_intizomi, rated_by_id, description, datetime.now(), fetchrow=True)

    async def select_mark(self, mark_id):
        sql = "SELECT * FROM mark WHERE id = $1"
        return await self.execute(sql, mark_id, fetchrow=True)

    async def select_all_marks(self):
        sql = "SELECT * FROM mark"
        return await self.execute(sql, fetch=True)

    async def select_marks(self, **kwargs):
        sql = "SELECT * FROM mark WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_today_marks(self, intern_id, rated_by_id):
        # Bugungi sanani olish
        today = datetime.now().date()  # Faqat sanani olish uchun date() metodidan foydalaning

        sql = """
        SELECT * FROM mark 
        WHERE intern_id = $1 
          AND rated_by_id = $2
          AND created_at::date = $3
        """
        return await self.execute(sql, intern_id, rated_by_id, today, fetch=True)

    async def update_mark(self, mark_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE mark SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *list(kwargs.values()), mark_id, fetchrow=True)

    async def delete_mark(self, mark_id):
        sql = "DELETE FROM mark WHERE id = $1 RETURNING *"
        return await self.execute(sql, mark_id, fetchrow=True)

    # for pdf file
    async def select_all_information_pdfs(self):
        sql = "SELECT * FROM pdf_file"
        return await self.execute(sql, fetch=True)
