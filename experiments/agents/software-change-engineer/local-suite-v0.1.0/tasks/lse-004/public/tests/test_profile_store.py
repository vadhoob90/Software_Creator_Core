import unittest

from profile_store import ProfileStore


class ProfileStoreTests(unittest.TestCase):
    def test_create_and_read_returns_copies(self):
        store = ProfileStore()
        created = store.create_profile("p-1", "Ada", "ada@example.test", "2026-01-02T03:04:05Z")
        created["name"] = "mutated"
        self.assertEqual(store.get_profile("p-1")["name"], "Ada")


if __name__ == "__main__":
    unittest.main()
