# bonds/urls.py
from django.urls import path

from .views import (
    hello,
    realtime_bond_market,
    basic_bonds,
    upcoming_bonds,
    upcoming_adjust_bonds,
    proposed_adjust_bonds,
    upcoming_adjust_condition_bonds,
    upcoming_mandatory_redeem_bonds,
    mandatory_redeem_condition_bonds,
    redeem_announced_bonds,
    upcoming_natural_expire_bonds,
)
urlpatterns = [
    path('hello/', hello, name='hello'),
    path('realtime_bond_market/', realtime_bond_market, name='realtime_bond_market'),
    path('basic_bonds/', basic_bonds, name='basic_bonds'),
    path('upcoming_bonds/', upcoming_bonds, name='upcoming_bonds'),
    path('upcoming_adjust_bonds/', upcoming_adjust_bonds, name='upcoming_adjust_bonds'),
    path('proposed_adjust_bonds/', proposed_adjust_bonds, name='proposed_adjust_bonds'),
    path('upcoming_adjust_condition_bonds/', upcoming_adjust_condition_bonds, name='upcoming_adjust_condition_bonds'),
    path('upcoming_mandatory_redeem_bonds/', upcoming_mandatory_redeem_bonds, name='upcoming_mandatory_redeem_bonds'),
    path('mandatory_redeem_condition_bonds/', mandatory_redeem_condition_bonds, name='mandatory_redeem_condition_bonds'),
    path('redeem_announced_bonds/', redeem_announced_bonds, name='redeem_announced_bonds'),
    path('upcoming_natural_expire_bonds/', upcoming_natural_expire_bonds, name='upcoming_natural_expire_bonds'),
]
