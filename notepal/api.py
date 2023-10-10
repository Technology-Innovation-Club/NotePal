from ninja import NinjaAPI
from note.api import note_router
from chat.api import chat_router


api = NinjaAPI(csrf=True)


api.add_router("/note", note_router)
api.add_router("/chat", chat_router)
