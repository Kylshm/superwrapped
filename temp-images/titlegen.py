from pyfiglet import Figlet

breaker = "\n\n\n═══════════════════════════════════════════════════════════════════\n\n\n\n\n"
font = Figlet(font="ansi_shadow")
print(breaker)
print(font.renderText("super\nwrapped"))
print(breaker)