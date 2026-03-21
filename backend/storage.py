import uuid

class Storage:
    def __init__(self):
        self.users = {}          # email -> user dict
        self.users_by_id = {}    # id -> user dict
        self.usage = {}          # user_id -> action -> count
        self.fused = {}          # user_id -> latest fused
        self.geojson = {}        # user_id -> FeatureCollection

    def create_user(self, email, password, plan):
        if email in self.users:
            return self.users[email]
        user = {"id": str(uuid.uuid4()), "email": email, "password": password, "plan": plan}
        self.users[email] = user
        self.users_by_id[user["id"]] = user
        self.usage[user["id"]] = {}
        return user
    def find_user(self, email):
        return self.users.get(email)

    def get_user_by_id(self, uid):
        return self.users_by_id.get(uid)

    def get_usage(self, uid, action):
        return self.usage.get(uid, {}).get(action, 0)

    def increment_usage(self, uid, action):
        self.usage.setdefault(uid, {})
        self.usage[uid][action] = self.usage[uid].get(action, 0) + 1

    def save_fused(self, uid, fused):
        self.fused[uid] = fused
        # Build mock GeoJSON layer from fused grid
        features = []
        grid = fused.get("pixels", [])
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                features.append({
                    "type": "Feature",
                    "properties": {"value": val},
                    "geometry": {
                        "type": "Point",
                        "coordinates": [77.5 + j*0.001, 28.7 + i*0.001]
                    }
                })
        self.geojson[uid] = {"type": "FeatureCollection", "features": features}
def get_fused_geojson(self, uid):
        return self.geojson.get(uid)
