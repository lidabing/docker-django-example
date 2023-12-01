# bonds/urls.py
from django.urls import path

from .views import basic_bonds
from .views import hello
from .views import mandatory_redeem_condition_bonds
from .views import proposed_adjust_bonds
from .views import realtime_bond_market
from .views import redeem_announced_bonds
from .views import upcoming_adjust_bonds
from .views import upcoming_adjust_condition_bonds
from .views import upcoming_bonds
from .views import upcoming_mandatory_redeem_bonds
from .views import upcoming_natural_expire_bonds

urlpatterns = [
    path("hello/", hello, name="hello"),
    path(
        "realtime_bond_market/",
        realtime_bond_market,
        name="realtime_bond_market",
    ),
    path("basic_bonds/", basic_bonds, name="basic_bonds"),
    path("upcoming_bonds/", upcoming_bonds, name="upcoming_bonds"),
    path(
        "upcoming_adjust_bonds/",
        upcoming_adjust_bonds,
        name="upcoming_adjust_bonds",
    ),
    path(
        "proposed_adjust_bonds/",
        proposed_adjust_bonds,
        name="proposed_adjust_bonds",
    ),
    path(
        "upcoming_adjust_condition_bonds/",
        upcoming_adjust_condition_bonds,
        name="upcoming_adjust_condition_bonds",
    ),
    path(
        "upcoming_mandatory_redeem_bonds/",
        upcoming_mandatory_redeem_bonds,
        name="upcoming_mandatory_redeem_bonds",
    ),
    path(
        "mandatory_redeem_condition_bonds/",
        mandatory_redeem_condition_bonds,
        name="mandatory_redeem_condition_bonds",
    ),
    path(
        "redeem_announced_bonds/",
        redeem_announced_bonds,
        name="redeem_announced_bonds",
    ),
    path(
        "upcoming_natural_expire_bonds/",
        upcoming_natural_expire_bonds,
        name="upcoming_natural_expire_bonds",
    ),
]
