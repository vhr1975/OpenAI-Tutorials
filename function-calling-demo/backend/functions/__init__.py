# Function registry
from .weather import get_weather
from .calendar import get_events
from .translation import translate

FUNCTIONS = {
    "get_weather": get_weather,
    "get_events": get_events,
    "translate": translate
}
