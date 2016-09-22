#
# gtkui.py
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

import gtk

from deluge.log import LOG as log
from deluge.ui.client import client
from deluge.plugins.pluginbase import GtkPluginBase
import deluge.component as component
import deluge.common

from common import get_resource

# def cell_data_label(column, cell, model, row, data):
#     cell.set_property('text', str(model.get_value(row, data)))

def cell_data_time(column, cell, model, row, data):
    """Display value as time, eg 1m10s"""
    time = model.get_value(row, data)
    if time <= 0:
        time_str = ""
    else:
        time_str = deluge.common.ftime(time)
    cell.set_property('text', time_str)

class GtkUI(GtkPluginBase):
    def enable(self):
        self.glade = gtk.glade.XML(get_resource("config.glade"))

        component.get("Preferences").add_page("lasttimeactive", self.glade.get_widget("prefs_box"))
        component.get("PluginManager").register_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").register_hook("on_show_prefs", self.on_show_prefs)
        view = deluge.component.get("TorrentView")
        view.add_func_column(_("Time since Uploading"),cell_data_time,"text", status_field=["time_since_upload"])
        view.add_func_column(_("Time since Downloading"),cell_data_time,"text", status_field=["time_since_download"])
        # view.add_text_column(_("Time since Downloading"), status_field=["time_since_download"])

    def disable(self):
        component.get("Preferences").remove_page("lasttimeactive")
        component.get("PluginManager").deregister_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").deregister_hook("on_show_prefs", self.on_show_prefs)
        view = deluge.component.get("TorrentView")
        view.remove_column(_("Time since Uploading"))
        view.remove_column(_("Time since Downloading"))

    def on_apply_prefs(self):
        log.debug("applying prefs for lasttimeactive")
        config = {
            "test":self.glade.get_widget("txt_test").get_text()
        }
        client.lasttimeactive.set_config(config)

    def on_show_prefs(self):
        client.lasttimeactive.get_config().addCallback(self.cb_get_config)

    def cb_get_config(self, config):
        "callback for on show_prefs"
        self.glade.get_widget("txt_test").set_text(config["test"])
