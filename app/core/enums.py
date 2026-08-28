from enum import StrEnum

class UserRole(StrEnum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    USER = "USER"

class RateLimitAlgorithm(StrEnum):
    FIXED_WINDOW = "FIXED_WINDOW"
    SLIDING_WINDOW = "SLIDING_WINDOW"
    TOKEN_BUCKET = "TOKEN_BUCKET"

class RuleScope(StrEnum):
    GLOBAL = "GLOBAL"
    PLAN = "PLAN"
    TENANT = "TENANT"
    USER = "USER"
    API_KEY = "API_KEY"
    IP = "IP"
    ENDPOINT = "ENDPOINT"