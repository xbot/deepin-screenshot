#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Deepin, Inc.
#               2011 Hou Shaohui
#
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou ShaoHui <houshao55@gmail.com>
#             Long Changjin <admin@longchangjin.cn>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
from main import main
from window import get_screenshot_pixbuf
from optparse import OptionParser
from tipswindow import CountdownWindow
from utils import get_format_time, get_pictures_dir, parser_path
from constant import DEFAULT_FILENAME
from nls import _

save_filetype = "png"


def open_file_dialog(fullscreen=True, filetype='png'):
    '''
    Save file to file.
    @param fullscreen: if get the fullscreen snapshot.
    @parser filetype: the filetype to save
    '''
    pixbuf = get_screenshot_pixbuf(fullscreen)
    dialog = gtk.FileChooserDialog(
        "Save..",
        None,
        gtk.FILE_CHOOSER_ACTION_SAVE,
        (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
        gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT))
    dialog.set_default_response(gtk.RESPONSE_ACCEPT)
    dialog.set_position(gtk.WIN_POS_CENTER)
    dialog.set_local_only(True)
    dialog.set_current_folder(get_pictures_dir())
    dialog.set_current_name("%s%s.%s" % (_(DEFAULT_FILENAME), get_format_time(), "png"))

    response = dialog.run()
    if response == gtk.RESPONSE_ACCEPT:
        filename = dialog.get_filename()
        pixbuf.save(filename, save_filetype)
        print "Save snapshot to %s" % (filename)
    elif response == gtk.RESPONSE_REJECT:
        print 'Closed, no files selected'
    dialog.destroy()

def set_save_filetype(widget, filetype):
    global save_filetype
    widget.set_current_name("%s%s.%s" % (_(DEFAULT_FILENAME), get_format_time(), "png"))
    save_filetype =filetype
       

def processArguments():
    '''init process arguments '''
    parser = OptionParser(usage="Usage: deepin-screenshot [options] [arg]", version="deepin-screenshot v2.1")
    parser.add_option("-f", "--full", action="store_true", dest="fullscreen", help="Taking the fullscreen shot")
    parser.add_option("-w", "--window", action="store_true", dest="window", help="Taking the currently focused window")
    parser.add_option("-d", "--delay", dest="delay", type="int", help="wait NUM seconds before taking a shot", metavar="NUM")
    parser.add_option("-s", "--save", dest="save_file", help="save screenshot to FILE", metavar="FILE")
    #parser.add_option("-a", "--area", help="Grab an area of the screen instead of the entire screen", action="store_true")
    #parser.add_option("-e", "--border-effect", action="store_true", dest="border_effect", help="Effect to add to the border")
    #parser.add_option("-i", "--interactive", action="store_true", help="Interactively set options")
    #parser.add_option("-b", "--include-border", action="store_true", help="Include the window border with the screenshot")
    #parser.add_option("-B", "--remove-border", action="store_true", help="Remove the window border from the screenshot")
    #parser.add_option("-c", "--clipboard", help="Send the grab directly to the clipboard", action="store_true")
    
    (options, args) = parser.parse_args()

    if options.fullscreen and options.window:
        parser.error("options -f and -w are mutually exclusive")
    if options.delay:
        CountdownWindow(options.delay)
    if options.save_file:
        parserFile = parser_path(str(options.save_file))
        if options.fullscreen:
            pixbuf = get_screenshot_pixbuf(True)
            pixbuf.save(parserFile[0], parserFile[1])
        elif options.window:
            pixbuf = get_screenshot_pixbuf(False)
            pixbuf.save(parserFile[0], parserFile[1])
        else:    
            main(options.save_file)
    elif options.fullscreen:
        open_file_dialog()
    elif options.window:
        open_file_dialog(False)
    else:
        main()

if __name__ == '__main__':
    processArguments()
