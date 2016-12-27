from django.conf.urls import url
from django.contrib import admin
from users.views import FightView, listing, Registration, Login, Logout
from lab6.User_file import NewFight


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^fights/$', listing),
    url(r'^registration/$', Registration, name='registration'),
    url(r'^login/$', Login, name='login'),
    url(r'^fight/(?P<id>\d+)$', FightView.as_view(), name='fight_url'),
    url(r'^logout$', Logout.as_view(), name='logout'),
    url(r'^newFight$', NewFight, name='NewFight'),
]
