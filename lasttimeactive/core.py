#
# core.py
#
# Copyright (C) 2009 Marc Marquez S. <mmsa1994@gmail.com>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#
from deluge._libtorrent import lt as libtorrent
from twisted.internet.task import LoopingCall
from deluge.log import LOG as log
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export
import deluge.common as common

DEFAULT_PREFS = {
    "test":"NiNiNi"
}

class Core(CorePluginBase):
    def enable(self):
        self.config = deluge.configmanager.ConfigManager("lasttimeactive.conf", DEFAULT_PREFS)
        self.torrents_status =  {}
        self.update_status_timer = LoopingCall(self.update_stats)
        self.update_status_timer.start(2)
        component.get("CorePluginManager").register_status_field("time_since_upload", self.get_torrent_upload_status)
        component.get("CorePluginManager").register_status_field("time_since_download", self.get_torrent_download_status)
    def disable(self):
        self.update_status_timer.stop()

    def update(self):
        pass

    def update_stats(self):
        self.torrents = component.get("Core").get_torrents_status({},[])
        for torrent_id in self.torrents.keys():
            # print torrent_id
            time_since_upload = component.get("Core").torrentmanager[torrent_id].handle.status().time_since_upload
            time_since_download = component.get("Core").torrentmanager[torrent_id].handle.status().time_since_download
            # print "Time since upload: ",time_since_upload
            # print "Time since download: ",time_since_download
            self.torrents_status[torrent_id]={"time_since_upload" : time_since_upload, "time_since_download" : time_since_download}
        # print self.torrents_status

    @export
    def set_config(self, config):
        """Sets the config dictionary"""
        for key in config.keys():
            self.config[key] = config[key]
        self.config.save()

    @export
    def get_config(self):
        """Returns the config dictionary"""
        return self.config.config

    def get_torrent_download_status(self, torrent_id):
        # response = str(self.torrents_status[torrent_id]["time_since_upload"])
        response = common.ftime(self.torrents_status[torrent_id]["time_since_upload"])
        # print response
        return response or ""

    def get_torrent_upload_status(self, torrent_id):
        # response = str(self.torrents_status[torrent_id]["time_since_download"])
        response = common.ftime(self.torrents_status[torrent_id]["time_since_download"])
        # print response
        return response or ""
