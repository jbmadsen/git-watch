import os
import sys
from win10toast import ToastNotifier


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)    
    return os.path.join(os.path.abspath("."), relative_path)


def toastMessage(header, message):
    '''Display toast message to inform user

    Keyword arguments:
    header     -- header message to display in toast
    message    -- message to display in toast
    '''
    icon = resource_path(os.path.join('src', 'assets', 'icon.ico'))
    toaster = ToastNotifier()
    toaster.show_toast(header,
                    message,
                    icon_path=icon,
                    duration=7)
