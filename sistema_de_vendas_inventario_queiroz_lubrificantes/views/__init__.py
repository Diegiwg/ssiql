from ..database import API
from .views import ViewController, ViewModel  # noqa: F401

view_controller = ViewController(API())
