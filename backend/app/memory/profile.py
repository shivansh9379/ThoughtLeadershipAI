from backend.app.database.crud import save_profile, load_profile


class UserProfile:

    def __init__(self):

        data = load_profile()

        if data:

            self.profile = data

        else:

            self.profile = {
                "name": None,
                "profession": None,
                "goal": None,
                "interests": []
            }

    def save(self):
        save_profile(self.profile)

    def set_name(self, name):
        self.profile["name"] = name
        self.save()

    def set_profession(self, profession):
        self.profile["profession"] = profession
        self.save()

    def set_goal(self, goal):
        self.profile["goal"] = goal
        self.save()

    def add_interest(self, interest):

        if interest not in self.profile["interests"]:
            self.profile["interests"].append(interest)
            self.save()

    def get_profile(self):
        return self.profile