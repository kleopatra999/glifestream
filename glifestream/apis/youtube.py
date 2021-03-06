#  gLifestream Copyright (C) 2009, 2010, 2011, 2013, 2015 Wojciech Polak
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

from django.utils.translation import ugettext as _
from glifestream.stream import media
from glifestream.apis import webfeed


class API (webfeed.API):
    name = 'YouTube API v2'
    limit_sec = 3600

    def get_urls(self):
        if self.service.url.startswith('http://'):
            return (self.service.url,)
        else:
            h = 'http://gdata.youtube.com/feeds/api/users/%s' % self.service.url
            return ('%s/favorites?v=2' % h,
                    '%s/uploads?v=2' % h)

    def custom_process(self, e, ent):
        if 'yt_videoid' in ent:
            vid = ent['yt_videoid']
        elif 'media_player' in ent and 'url' in ent['media_player']:
            vid = ent['media_player']['url'][22:]
        else:
            vid = None

        if vid and 'media_thumbnail' in ent and len(ent.media_thumbnail):
            tn = None
            for mt in ent.media_thumbnail:
                if 'name' in mt and mt['name'] == 'hqdefault':
                    tn = mt
                    tn['width'], tn['height'] = 200, 150
            if not tn:
                tn = ent.media_thumbnail[0]

            if self.service.public:
                tn['url'] = media.save_image(tn['url'], downscale=True,
                                             size=(200, 150))

            e.link = e.link.replace('&feature=youtube_gdata', '')
            e.content = """<table class="vc"><tr><td><div id="youtube-%s" class="play-video"><a href="%s" rel="nofollow"><img src="%s" width="%s" height="%s" alt="YouTube Video" /></a><div class="playbutton"></div></div></td></tr></table>""" % (
                vid, e.link, tn['url'], tn['width'], tn['height'])
        else:
            e.content = ent.get('yt_state', '<a href="%s">%s</a>' %
                                (ent.get('link', '#').replace(
                                    '&feature=youtube_gdata', ''), ent.get('title', '')))


def filter_title(entry):
    if 'favorite' in entry.guid:
        return _('Favorited %s') % ('<em>' + entry.title + '</em>')
    else:
        return _('Published %s') % ('<em>' + entry.title + '</em>')
