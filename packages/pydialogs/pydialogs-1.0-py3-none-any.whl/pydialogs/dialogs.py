import curses, textwrap

def display_alert(stdscr, title, message, width, height):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.curs_set(0)
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.clear()
    stdscr.refresh()

    max_height, max_width = stdscr.getmaxyx()
    start_x = (max_width // 2) - (width // 2)
    start_y = (max_height // 2) - (height // 2)

    shadow = curses.newwin(height, width, start_y + 1, start_x + 2)
    shadow.bkgd(' ', curses.color_pair(3))
    shadow.refresh()

    dialog = curses.newwin(height, width, start_y, start_x)
    dialog.bkgd(' ', curses.color_pair(2))
    dialog.border()

    dialog.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)

    for idx, line in enumerate(textwrap.wrap(message, width=width - 4)):
        if idx + 2 < height - 3:
            dialog.addstr(2 + idx, 2, line)

    return dialog

def display_select(stdscr, title, message, width, height, options):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.curs_set(0)
    stdscr.bkgd(' ', curses.color_pair(1))
    stdscr.clear()
    stdscr.refresh()

    max_height, max_width = stdscr.getmaxyx()
    start_x = (max_width // 2) - (width // 2)
    start_y = (max_height // 2) - (height // 2)

    shadow = curses.newwin(height, width, start_y + 1, start_x + 2)
    shadow.bkgd(' ', curses.color_pair(3))
    shadow.refresh()

    dialog = curses.newwin(height, width, start_y, start_x)
    dialog.bkgd(' ', curses.color_pair(2))
    dialog.border()

    dialog.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)

    for idx, line in enumerate(textwrap.wrap(message, width=width - 4)):
        if idx + 2 < height - 5:
            dialog.addstr(2 + idx, 2, line)

    selection = 0

    while True:
        start_x = (width - sum(len(opt) + 4 for opt in options) - 2) // 2

        for idx, option in enumerate(options):
            if idx == selection:
                dialog.addstr(height - 3, start_x, f"[ {option} ]", curses.A_REVERSE)
            else:
                dialog.addstr(height - 3, start_x, f"  {option}  ")
            start_x += len(option) + 4

        dialog.refresh()

        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            selection = (selection - 1) % len(options)
        elif key == curses.KEY_RIGHT:
            selection = (selection + 1) % len(options)
        elif key in (curses.KEY_ENTER, 10, 13):
            return options[selection]

def alert(title, message, width=50, height=10, button="OK"):
    def wrap(stdscr):
        window = display_alert(stdscr, title, message, width, height)
        btn = f"[ {button} ]"
        window.addstr(height - 3, (width - len(btn)) // 2, btn, curses.A_REVERSE)
        window.refresh()
        while True:
            key = stdscr.getch()
            if key in (curses.KEY_ENTER, 10, 13, 32):
                break
    curses.wrapper(wrap)

def select(title, message, width=50, height=10, options=None):
    if options is None:
        options = ["Yes", "No"]
    return curses.wrapper(display_select, title, message, width, height, options)
