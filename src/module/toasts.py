from win10toast import ToastNotifier


def toastMessage(header, message):
    '''Display toast message to inform user

    Keyword arguments:
    header     -- header message to display in toast
    message    -- message to display in toast
    '''
    toaster = ToastNotifier()
    toaster.show_toast(header,
                    message,
                    icon_path="src/assets/python.ico",
                    duration=7)