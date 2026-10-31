"""High-level Role-Based Access Control (RBAC) definitions for Search-Want."""

ROLE_USER = "USER"
ROLE_SHOP_OWNER = "SHOP_OWNER"
ROLE_ADMIN = "ADMIN"
ROLE_SUPER_ADMIN = "SUPER_ADMIN"

ALL_ROLES: tuple[str, ...] = (
    ROLE_USER,
    ROLE_SHOP_OWNER,
    ROLE_ADMIN,
    ROLE_SUPER_ADMIN,
)

ADMIN_ROLES: tuple[str, ...] = (
    ROLE_ADMIN,
    ROLE_SUPER_ADMIN,
)

ROLE_RANK: dict[str, int] = {
    ROLE_USER: 10,
    ROLE_SHOP_OWNER: 20,
    ROLE_ADMIN: 80,
    ROLE_SUPER_ADMIN: 100,
}

# Granular permission identifiers exposed to the frontend & enforced by backend dependencies
PERM_SHOP_CREATE = "shop:create"
PERM_SHOP_EDIT_OWN = "shop:edit_own"
PERM_SHOP_DELETE_OWN = "shop:delete_own"
PERM_ADMIN_MODERATE_SHOPS = "admin:moderate_shops"
PERM_ADMIN_VIEW_LOGS = "admin:view_logs"
PERM_SUPER_MANAGE_USERS = "super:manage_users"
PERM_SUPER_MANAGE_ADSENSE = "super:manage_adsense"
PERM_SUPER_SECURITY_AUDIT = "super:security_audit"
PERM_SUPER_DELETE_ANY_SHOP = "super:delete_any_shop"
PERM_SUPER_SEED_DEMO = "super:seed_demo"

ROLE_PERMISSIONS: dict[str, tuple[str, ...]] = {
    ROLE_USER: (
        PERM_SHOP_CREATE,
    ),
    ROLE_SHOP_OWNER: (
        PERM_SHOP_CREATE,
        PERM_SHOP_EDIT_OWN,
        PERM_SHOP_DELETE_OWN,
    ),
    ROLE_ADMIN: (
        PERM_SHOP_CREATE,
        PERM_SHOP_EDIT_OWN,
        PERM_SHOP_DELETE_OWN,
        PERM_ADMIN_MODERATE_SHOPS,
        PERM_ADMIN_VIEW_LOGS,
    ),
    ROLE_SUPER_ADMIN: (
        PERM_SHOP_CREATE,
        PERM_SHOP_EDIT_OWN,
        PERM_SHOP_DELETE_OWN,
        PERM_ADMIN_MODERATE_SHOPS,
        PERM_ADMIN_VIEW_LOGS,
        PERM_SUPER_MANAGE_USERS,
        PERM_SUPER_MANAGE_ADSENSE,
        PERM_SUPER_SECURITY_AUDIT,
        PERM_SUPER_DELETE_ANY_SHOP,
        PERM_SUPER_SEED_DEMO,
    ),
}


def get_permissions_for_role(role: str) -> list[str]:
    return list(ROLE_PERMISSIONS.get(role, ()))


def has_permission(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, ())

