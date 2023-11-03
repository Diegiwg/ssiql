from ..database import db_manager
from .views import ViewController, ViewModel

view_controller = ViewController(db_manager())
