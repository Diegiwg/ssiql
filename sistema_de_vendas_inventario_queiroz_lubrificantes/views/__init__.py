from ..database import API
from .views import ViewController, ViewModel

view_controller = ViewController(API())
