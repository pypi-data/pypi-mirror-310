"""
skyview_frame.py

Satview frame class for PyGPSClient application.

This handles a frame containing a 2D plot of satellite visibility.

Created on 13 Sep 2020

:author: semuadmin
:copyright: 2020 SEMU Consulting
:license: BSD 3-Clause
"""

from operator import itemgetter
from tkinter import ALL, BOTH, YES, Canvas, Frame, font

from pygpsclient.globals import BGCOL, FGCOL, GNSS_LIST, WIDGETU1
from pygpsclient.helpers import cel2cart, col2contrast, snr2col

OL_WID = 2


class SkyviewFrame(Frame):
    """
    Skyview frame class.
    """

    def __init__(self, app, *args, **kwargs):
        """
        Constructor.

        :param Frame app: reference to main tkinter application
        :param args: optional args to pass to Frame parent class
        :param kwargs: optional kwargs to pass to Frame parent class
        """

        self.__app = app  # Reference to main application class
        self.__master = self.__app.appmaster  # Reference to root class (Tk)

        Frame.__init__(self, self.__master, *args, **kwargs)

        def_w, def_h = WIDGETU1
        self.width = kwargs.get("width", def_w)
        self.height = kwargs.get("height", def_h)
        self.bg_col = BGCOL
        self.fg_col = FGCOL
        self._body()

        self.bind("<Configure>", self._on_resize)

    def _body(self):
        """
        Set up frame and widgets.
        """

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.can_satview = Canvas(
            self, width=self.width, height=self.height, bg=self.bg_col
        )
        self.can_satview.pack(fill=BOTH, expand=YES)

    def init_frame(self):
        """
        Initialise satellite view
        """

        w, h = self.width, self.height
        axis_r = min(h, w) / 18
        resize_font = font.Font(size=min(int(w / 25), 8))
        self.can_satview.delete(ALL)
        maxr = min((h / 2), (w / 2)) - axis_r
        for r in (0.2, 0.4, 0.6, 0.8, 1):
            self.can_satview.create_circle(
                w / 2, h / 2, maxr * r, outline=self.fg_col, width=1
            )
        self.can_satview.create_line(w / 2, 0, w / 2, h, fill=self.fg_col)
        self.can_satview.create_line(0, h / 2, w, h / 2, fill=self.fg_col)
        self.can_satview.create_text(
            w - axis_r, h / 2, text="90\u00b0\n E", fill=self.fg_col, font=resize_font
        )
        self.can_satview.create_text(
            axis_r, h / 2, text="270\u00b0\n W", fill=self.fg_col, font=resize_font
        )
        self.can_satview.create_text(
            w / 2, axis_r, text="0\u00b0 N", fill=self.fg_col, font=resize_font
        )
        self.can_satview.create_text(
            w / 2, h - axis_r, text="180\u00b0 S", fill=self.fg_col, font=resize_font
        )

    def update_frame(self):
        """
        Plot satellites' elevation and azimuth position.
        """

        data = self.__app.gnss_status.gsv_data
        w, h = self.width, self.height
        axis_r = min(h, w) / 18
        maxr = min((h / 2), (w / 2)) - axis_r
        resize_font = font.Font(size=min(int(maxr / 10), 8))
        self.init_frame()

        for d in sorted(data.values(), key=itemgetter(4)):  # sort by ascending snr
            try:
                gnssId, prn, ele, azi, snr = d
                ele = int(ele)
                azi = (int(azi) - 90) % 360  # adjust so north is upwards
                x, y = cel2cart(ele, azi)
                x = x * maxr
                y = y * maxr
                if snr == "":
                    snr = 0
                else:
                    snr = int(snr)
                (_, ol_col) = GNSS_LIST[gnssId]
                prn = f"{int(prn):02}"
                bg_col = snr2col(snr)
                self.can_satview.create_circle(
                    x + (w / 2),
                    y + (h / 2),
                    (maxr / 10),
                    outline=ol_col,
                    fill=bg_col,
                    width=OL_WID,
                )
                self.can_satview.create_text(
                    x + (w / 2),
                    y + (h / 2),
                    text=prn,
                    fill=col2contrast(bg_col),
                    font=resize_font,
                )
            except ValueError:
                pass

        self.can_satview.update_idletasks()

    def _on_resize(self, event):  # pylint: disable=unused-argument
        """
        Resize frame

        :param event event: resize event
        """

        self.width, self.height = self.get_size()

    def get_size(self):
        """
        Get current canvas size.

        :return: window size (width, height)
        :rtype: tuple
        """

        self.update_idletasks()  # Make sure we know about any resizing
        width = self.can_satview.winfo_width()
        height = self.can_satview.winfo_height()
        return (width, height)
