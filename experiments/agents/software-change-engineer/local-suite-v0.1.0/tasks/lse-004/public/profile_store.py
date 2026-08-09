"""Small in-memory profile repository."""


class ProfileStore:
    def __init__(self):
        self._profiles = {}

    def create_profile(self, profile_id, name, email, created_at):
        if profile_id in self._profiles:
            raise ValueError("profile already exists")
        profile = {
            "profile_id": profile_id,
            "name": name,
            "email": email,
            "created_at": created_at,
        }
        self._profiles[profile_id] = profile
        return profile.copy()

    def get_profile(self, profile_id):
        try:
            return self._profiles[profile_id].copy()
        except KeyError:
            raise KeyError(f"unknown profile: {profile_id}") from None
