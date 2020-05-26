class TempPrint:
    """ For printing on the same line by replacing previous output """

    def __init__(self, is_active=True):
        self.last_line = ""
        self.is_active = is_active

    def text(self, txt):
        if not self.is_active:
            return
        len_diff = len(self.last_line) - len(txt)
        self.last_line = txt
        txt += " " * len_diff
        print(txt, end="\r")

    def progress_bar(self, progress, length=50, label=None):
        done = round(progress * length)
        if label:
            label += "  "
        self.text(f'{label}[{"#" * done}{"-" * (length - done)}]')
