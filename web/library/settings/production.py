from ._base import *
DEBUG = False
DATABASES = {
    "default": {
        "ENGINE": "mysql.connector.django",
        "NAME": environ["DB_NAME"],
        "HOST": environ["DB_HOST"],
        "PORT": environ["DB_PORT"],
        "USER": environ["DB_USER"],
        "PASSWORD": environ["DB_PASSWORD"],
    }
}
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = [
    "rest_framework.throttling.AnonRateThrottle",
    "rest_framework.throttling.UserRateThrottle",
],
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "anon": "5/minute",
    "user": "30/minute",
},
