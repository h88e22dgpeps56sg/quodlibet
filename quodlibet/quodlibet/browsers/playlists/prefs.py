# -*- coding: utf-8 -*-
# Copyright 2016 Nick Boultbee
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

from gi.repository import Gtk

from quodlibet.util import format_time_display, format_time_long,\
    format_size, tag
from quodlibet import ngettext
from quodlibet import qltk
from quodlibet.browsers._base import EditDisplayPatternMixin, FakeDisplayItem
from quodlibet.qltk import Button, Icons

_FOOTER = "<~tracks> (<~filesize> / <~length>)"
DEFAULT_PATTERN_TEXT = ("[b]<~name>[/b]\n"
                        "[small]<~tracks|%s|[i](%s)[/i]>[/small]"
                        % (_FOOTER, (_("empty"))))


class Preferences(qltk.UniqueWindow, EditDisplayPatternMixin):
    _A_SIZE = 127 * 1024 * 1024
    _SOME_PEOPLE = "\n".join(
            tag(t) for t in ["artist", "performer", "composer", "arranger"])

    _DEFAULT_PATTERN = DEFAULT_PATTERN_TEXT

    _PREVIEW_ITEM = FakeDisplayItem({
        "date": "2015-11-31",
        "~length": format_time_display(6319),
        "~long-length": format_time_long(6319),
        "~tracks": ngettext("%d track", "%d tracks", 27) % 27,
        "~#filesize": _A_SIZE,
        "~filesize": format_size(_A_SIZE),
        "~#rating": 0.75,
        "~name": _("Example Playlist"),
        "~people": _SOME_PEOPLE + "..."})

    def __init__(self, browser):
        if self.is_not_unique():
            return
        super(Preferences, self).__init__()
        self.set_border_width(12)
        self.set_title(_("Playlist Browser Preferences"))
        self.set_default_size(420, 240)
        self.set_transient_for(qltk.get_top_parent(browser))

        box = Gtk.VBox(spacing=6)
        edit_frame = self.edit_display_pane(browser, _("Playlist display"))
        box.pack_start(edit_frame, False, True, 12)

        main_box = Gtk.VBox(spacing=12)
        close = Button(_("_Close"), Icons.WINDOW_CLOSE)
        close.connect('clicked', lambda *x: self.destroy())
        b = Gtk.HButtonBox()
        b.set_layout(Gtk.ButtonBoxStyle.END)
        b.pack_start(close, True, True, 0)

        main_box.pack_start(box, True, True, 0)
        self.use_header_bar()

        if not self.has_close_button():
            main_box.pack_start(b, False, True, 0)
        self.add(main_box)

        close.grab_focus()
        self.show_all()
