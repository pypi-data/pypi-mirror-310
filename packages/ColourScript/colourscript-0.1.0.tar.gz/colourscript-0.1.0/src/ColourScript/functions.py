from time import sleep


class text:
    def __init__(self, message):
        self.message = message
        print(self.message)

    def reset() -> None:
        print('\033[0;0m')

    def plain(self):
        print('\033[0;0m' + str(self))

    def red(self):
        print('\033[31m' + str(self))

    def green(self):
        print('\033[32m' + str(self))

    def yellow(self):
        print('\033[33m' + str(self))

    def blue(self):
        print('\033[34m' + str(self))

    def purple(self):
        print('\033[35m' + str(self))

    def cyan(self):
        print('\033[36m' + str(self))

    def white(self):
        print('\033[38m' + str(self))

    def black(self):
        print('\033[30m' + str(self))

    def custom_octal(self, code):
        print(f"\033[{code}m" + str(self))

    def bold(self):
        print('\033[1m' + str(self))

    def underline(self):
        print('\033[4m' + str(self))

    def italic(self):
        print('\033[3m' + str(self))

    def strikethrough(self):
        print('\033[9m' + str(self))

    def orange(self):
        print('\033[38;5;202m' + str(self))

    # Functions for each HTML color (RGB)
    def AliceBlue(self):
        print('\033[38;5;153m' + str(self))

    def AntiqueWhite(self):
        print('\033[38;5;127m' + str(self))

    def Aqua(self):
        print('\033[38;5;51m' + str(self))

    def Aquamarine(self):
        print('\033[38;5;79m' + str(self))

    def Azure(self):
        print('\033[38;5;159m' + str(self))

    def Beige(self):
        print('\033[38;5;230m' + str(self))

    def Bisque(self):
        print('\033[38;5;223m' + str(self))

    def Black(self):
        print('\033[38;5;0m' + str(self))

    def BlanchedAlmond(self):
        print('\033[38;5;214m' + str(self))

    def Blue(self):
        print('\033[38;5;32m' + str(self))

    def BlueViolet(self):
        print('\033[38;5;57m' + str(self))

    def Brown(self):
        print('\033[38;5;94m' + str(self))

    def BurlyWood(self):
        print('\033[38;5;127m' + str(self))

    def CadetBlue(self):
        print('\033[38;5;61m' + str(self))

    def Chartreuse(self):
        print('\033[38;5;118m' + str(self))

    def Chocolate(self):
        print('\033[38;5;94m' + str(self))

    def Coral(self):
        print('\033[38;5;214m' + str(self))

    def CornflowerBlue(self):
        print('\033[38;5;32m' + str(self))

    def Cornsilk(self):
        print('\033[38;5;229m' + str(self))

    def Crimson(self):
        print('\033[38;5;196m' + str(self))

    def Cyan(self):
        print('\033[38;5;51m' + str(self))

    def DarkBlue(self):
        print('\033[38;5;19m' + str(self))

    def DarkCyan(self):
        print('\033[38;5;36m' + str(self))

    def DarkGoldenrod(self):
        print('\033[38;5;136m' + str(self))

    def DarkGray(self):
        print('\033[38;5;239m' + str(self))

    def DarkGreen(self):
        print('\033[38;5;22m' + str(self))

    def DarkKhaki(self):
        print('\033[38;5;143m' + str(self))

    def DarkMagenta(self):
        print('\033[38;5;91m' + str(self))

    def DarkOliveGreen(self):
        print('\033[38;5;100m' + str(self))

    def DarkOrange(self):
        print('\033[38;5;202m' + str(self))

    def DarkOrchid(self):
        print('\033[38;5;92m' + str(self))

    def DarkRed(self):
        print('\033[38;5;88m' + str(self))

    def DarkSalmon(self):
        print('\033[38;5;217m' + str(self))

    def DarkSeaGreen(self):
        print('\033[38;5;143m' + str(self))

    def DarkSlateBlue(self):
        print('\033[38;5;61m' + str(self))

    def DarkSlateGray(self):
        print('\033[38;5;23m' + str(self))

    def DarkTurquoise(self):
        print('\033[38;5;44m' + str(self))

    def DarkViolet(self):
        print('\033[38;5;90m' + str(self))

    def DeepPink(self):
        print('\033[38;5;198m' + str(self))

    def DeepSkyBlue(self):
        print('\033[38;5;63m' + str(self))

    def DimGray(self):
        print('\033[38;5;239m' + str(self))

    def DodgerBlue(self):
        print('\033[38;5;33m' + str(self))

    def Firebrick(self):
        print('\033[38;5;88m' + str(self))

    def FloralWhite(self):
        print('\033[38;5;255m' + str(self))

    def ForestGreen(self):
        print('\033[38;5;34m' + str(self))

    def Fuchsia(self):
        print('\033[38;5;13m' + str(self))

    def Gainsboro(self):
        print('\033[38;5;253m' + str(self))

    def GhostWhite(self):
        print('\033[38;5;15m' + str(self))

    def Gold(self):
        print('\033[38;5;220m' + str(self))

    def Goldenrod(self):
        print('\033[38;5;136m' + str(self))

    def Gray(self):
        print('\033[38;5;243m' + str(self))

    def Green(self):
        print('\033[38;5;28m' + str(self))

    def GreenYellow(self):
        print('\033[38;5;118m' + str(self))

    def Honeydew(self):
        print('\033[38;5;157m' + str(self))

    def HotPink(self):
        print('\033[38;5;198m' + str(self))

    def IndianRed(self):
        print('\033[38;5;167m' + str(self.text))

    def Indigo(self):
        print('\033[38;5;54m' + str(self))

    def Ivory(self):
        print('\033[38;5;255m' + str(self))

    def Khaki(self):
        print('\033[38;5;180m' + str(self))

    def Lavender(self):
        print('\033[38;5;159m' + str(self))

    def LavenderBlush(self):
        print('\033[38;5;219m' + str(self))

    def LawnGreen(self):
        print('\033[38;5;118m' + str(self))

    def LemonChiffon(self):
        print('\033[38;5;227m' + str(self))

    def LightBlue(self):
        print('\033[38;5;153m' + str(self))

    def LightCoral(self):
        print('\033[38;5;217m' + str(self))

    def LightCyan(self):
        print('\033[38;5;159m' + str(self))

    def LightGoldenrodYellow(self):
        print('\033[38;5;227m' + str(self))

    def LightGray(self):
        print('\033[38;5;250m' + str(self))

    def LightGreen(self):
        print('\033[38;5;120m' + str(self))

    def LightPink(self):
        print('\033[38;5;218m' + str(self))

    def LightSalmon(self):
        print('\033[38;5;214m' + str(self))

    def LightSeaGreen(self):
        print('\033[38;5;42m' + str(self))

    def LightSkyBlue(self):
        print('\033[38;5;117m' + str(self))

    def LightSlateGray(self):
        print('\033[38;5;145m' + str(self))

    def LightSteelBlue(self):
        print('\033[38;5;145m' + str(self))

    def LightYellow(self):
        print('\033[38;5;228m' + str(self))

    def Lime(self):
        print('\033[38;5;10m' + str(self))

    def LimeGreen(self):
        print('\033[38;5;48m' + str(self))

    def Linen(self):
        print('\033[38;5;230m' + str(self))

    def Magenta(self):
        print('\033[38;5;13m' + str(self))

    def Maroon(self):
        print('\033[38;5;88m' + str(self))

    def MediumAquaMarine(self: str):
        print('\033[38;5;79m' + str(self))

    def CustomRGB(red: int, green: int, blue: int, string: str):
        print(f'\033[{red};{green};{blue}m' + string)


class pause:
    def __init__(self, duration: float):
        self.duration = duration
        sleep(self.duration / 1000)  # Pause for the given milliseconds

    def secs(seconds: float):
        sleep(seconds)  # Pause for the given seconds

    def mins(minutes: float):
        sleep(minutes * 60)  # Pause for the given minutes
