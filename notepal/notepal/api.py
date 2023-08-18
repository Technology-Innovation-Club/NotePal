from ninja import NinjaAPI
from note.api import note_router

api = NinjaAPI()

api.add_router("/note", note_router)