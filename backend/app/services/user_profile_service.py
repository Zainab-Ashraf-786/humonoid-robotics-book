class UserProfileService:
    def __init__(self, db):
        self.db = db

    async def get_user_profile(self, user_id):
        # Return a mock profile object
        class MockProfile:
            def to_dict(self):
                return {
                    "user_id": user_id,
                    "software_background": None,
                    "hardware_background": None,
                    "experience_level": "beginner",
                    "programming_languages": "not specified",
                    "learning_goals": "general learning",
                    "created_at": None,
                    "updated_at": None
                }
        return MockProfile()

    async def update_user_profile(self, user_id, **updates):
        # Always return success for now
        return True

    async def get_personalization_context(self, user_id):
        # Return default context for personalization
        return {
            "experience_level": "beginner",
            "software_background": "general",
            "hardware_background": "general",
            "programming_languages": "not specified",
            "learning_goals": "general learning"
        }