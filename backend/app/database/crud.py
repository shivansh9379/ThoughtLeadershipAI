import json

from backend.app.database.database import SessionLocal
from backend.app.database.models import UserProfileDB, ChatHistoryDB


# -------------------------
# USER PROFILE
# -------------------------

def save_profile(profile):

    db = SessionLocal()

    user = db.query(UserProfileDB).first()

    if user is None:
        user = UserProfileDB()
        db.add(user)

    user.name = profile.get("name")
    user.profession = profile.get("profession")
    user.goal = profile.get("goal")
    user.interests = json.dumps(profile.get("interests", []))

    db.commit()
    db.close()


def load_profile():

    db = SessionLocal()

    user = db.query(UserProfileDB).first()

    db.close()

    if user is None:
        return None

    return {
        "name": user.name,
        "profession": user.profession,
        "goal": user.goal,
        "interests": json.loads(user.interests or "[]")
    }


# -------------------------
# CHAT HISTORY
# -------------------------

def save_message(role, message):

    db = SessionLocal()

    chat = ChatHistoryDB(
        role=role,
        message=message
    )

    db.add(chat)

    db.commit()
    db.close()


def load_history():

    db = SessionLocal()

    chats = db.query(ChatHistoryDB).all()

    db.close()

    history = []

    for chat in chats:
        history.append({
            "role": chat.role,
            "message": chat.message
        })

    return history