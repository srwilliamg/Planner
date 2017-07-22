from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from planner.models import User


def RedirectToHome(user):
    rol_homes = {
        "R": "/admin",
        "A": "home_admin",
        "S": "home_agricultor"
    }
    view = rol_homes.get(user.role, None)
    return redirect(view)


def try_cast_int(val, fail=None):
    try:
        return int(val)
    except ValueError:
        return fail
