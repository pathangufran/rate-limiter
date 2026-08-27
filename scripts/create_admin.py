import asyncio
from sqlalchemy import select
from app.core.config import settings
from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.plan import Plan
from app.models.tenant import Tenant
from app.models.user import User

async def create_admin() -> None:
    if not settings.admin_email:
        raise RuntimeError(
            "ADMIN_EMAIL is not configured"
        )
    if not settings.admin_password:
        raise RuntimeError(
            "ADMIN_PASSWORD is not configured"
        )

    async with AsyncSessionLocal() as session:
        existing_user = await session.execute(
            select(User).where(
                User.email == settings.admin_email
            )
        )
        if existing_user.scalar_one_or_none():
            print("Admin already exists.")
            return 

        plan_result = await session.execute(
            select(Plan).where(
                Plan.name == "Admin"
            )
        )

        plan = plan_result.scalar_one_or_none()

        if plan is None:
            plan = Plan(
                name="Admin",
                description="Internal administration plan",
            )
            session.add(plan)
            await session.flush()

        tenant = Tenant(
            name="Platform Admin",
            slug="platform-admin",
            plan_id=plan.id,
        )
        session.add(tenant)
        await session.flush()

        user = User(
            tenant_id=tenant.id,
            email=settings.admin_email,
            password=hash_password(settings.admin_password),
            role="SUPER_ADMIN",
            is_active=True,
        )
        session.add(user)
        await session.commit()

        print(
            f"Created admin user: {settings.admin_email}"
        )

if __name__ == "__main__":
    asyncio.run(create_admin())