#  gLifestream Copyright (C) 2010, 2013 Wojciech Polak
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your
#  option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from glifestream.usettings import views

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(url='services'), name='settings'),
    (r'api/(?P<cmd>[a-z\-]+)$', views.api),
    (r'services$', views.services),
    (r'services/import$', views.opml, {
     'cmd': 'import'}, 'opml-import'),
    (r'services/export$', views.opml, {
     'cmd': 'export'}, 'opml-export'),
    (r'lists$', views.lists),
    (r'lists/(?P<list>[a-z0-9\-]+)$', views.lists),
    (r'pshb$', views.pshb),
    (r'openid$', views.openid),
    (r'tools$', views.tools),
    (r'oauth/(?P<id>[0-9]+)$', views.oauth),
)
