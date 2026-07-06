import asyncio

from sqlalchemy import select

from app.core.config import settings
from app.core.security import hash_password
from app.database.session import AsyncSessionLocal
from app.models.device_type import DeviceType
from app.models.organization import Organization
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.snmp_profile import SNMPProfile
from app.models.user import User
from app.models.user_role import UserRole
from app.models.vendor import Vendor


DEFAULT_PERMISSIONS = [
    "user.read",
    "user.write",
    "device.read",
    "device.write",
    "device.delete",
    "snmp.read",
    "snmp.write",
    "topology.read",
    "alarm.read",
    "alarm.write",
    "settings.read",
    "settings.write",
]

DEFAULT_ROLES = [
    "Super Admin",
    "Administrator",
    "Operator",
    "Viewer",
]

DEFAULT_VENDORS = [
    "Cisco",
    "Huawei",
    "MikroTik",
    "Fortinet",
    "Juniper",
    "HPE Aruba",
    "Dell",
    "F5",
    "Linux",
    "Windows",
]

DEFAULT_DEVICE_TYPES = [
    ("Router", "network"),
    ("Switch", "network"),
    ("Firewall", "security"),
    ("Server", "compute"),
    ("Wireless Controller", "wireless"),
    ("Access Point", "wireless"),
    ("UPS", "power"),
]


async def get_or_create(session, model, defaults=None, **filters):
    result = await session.execute(select(model).filter_by(**filters))
    obj = result.scalar_one_or_none()

    if obj:
        return obj

    data = dict(filters)
    if defaults:
        data.update(defaults)

    obj = model(**data)
    session.add(obj)
    await session.flush()
    return obj


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        org = await get_or_create(
            session,
            Organization,
            name="SISTECH",
            code="SISTECH",
            defaults={"description": "Default organization"},
        )

        permissions = []
        for permission_name in DEFAULT_PERMISSIONS:
            permission = await get_or_create(
                session,
                Permission,
                name=permission_name,
                defaults={"description": permission_name},
            )
            permissions.append(permission)

        super_admin_role = await get_or_create(
            session,
            Role,
            name="Super Admin",
            defaults={"description": "Full system access"},
        )

        for role_name in DEFAULT_ROLES:
            await get_or_create(
                session,
                Role,
                name=role_name,
                defaults={"description": role_name},
            )

        for permission in permissions:
            await get_or_create(
                session,
                RolePermission,
                role_id=super_admin_role.id,
                permission_id=permission.id,
            )

        admin_user = await get_or_create(
            session,
            User,
            username=settings.FIRST_SUPERUSER_USERNAME,
            defaults={
                "organization_id": org.id,
                "email": settings.FIRST_SUPERUSER_EMAIL,
                "full_name": settings.FIRST_SUPERUSER_FULL_NAME,
                "password_hash": hash_password(settings.FIRST_SUPERUSER_PASSWORD),
                "is_active": True,
                "is_superuser": True,
            },
        )

        await get_or_create(
            session,
            UserRole,
            user_id=admin_user.id,
            role_id=super_admin_role.id,
        )

        for vendor_name in DEFAULT_VENDORS:
            await get_or_create(
                session,
                Vendor,
                name=vendor_name,
                defaults={"description": vendor_name},
            )

        for name, category in DEFAULT_DEVICE_TYPES:
            await get_or_create(
                session,
                DeviceType,
                name=name,
                defaults={
                    "category": category,
                    "description": name,
                },
            )

        await get_or_create(
            session,
            SNMPProfile,
            name="Default SNMP v2c",
            defaults={
                "version": "v2c",
                "community": "public",
                "port": 161,
                "timeout": 3,
                "retries": 2,
                "is_active": True,
            },
        )

        await session.commit()

    print("Seed completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed())