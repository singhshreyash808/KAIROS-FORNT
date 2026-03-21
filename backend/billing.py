PLAN_LIMITS = {
    "free": {"ingest": 5, "preprocess": 5, "fuse": 5, "analytics": 5},
    "pro": {"ingest": 100, "preprocess": 100, "fuse": 100, "analytics": 100},
    "enterprise": {"ingest": 10000, "preprocess": 10000, "fuse": 10000, "analytics": 10000},
}

def check_quota(store, user_id, action):
    user = store.get_user_by_id(user_id)
    plan = user["plan"]
    used = store.get_usage(user_id, action)
    limit = PLAN_LIMITS.get(plan, {}).get(action, 0)
    return used < limit

def record_usage(store, user_id, action):
    store.increment_usage(user_id, action)
