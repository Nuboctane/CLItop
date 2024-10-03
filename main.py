import sys
import os
import curses

ascii_art = {
    "A": [
        "   A  ",
        "  A A ",
        " AAAAA",
        " A   A",
        " A   A"
    ],
    "B": [
        " BBBB ",
        " B   B",
        " BBBB ",
        " B   B",
        " BBBB "
    ],
    "C": [
        "  CCC ",
        " C   C",
        " C    ",
        " C   C",
        "  CCC "
    ],
    "D": [
        " DDDD ",
        " D   D",
        " D   D",
        " D   D",
        " DDDD "
    ],
    "E": [
        " EEEEE",
        " E    ",
        " EEE  ",
        " E    ",
        " EEEEE"
    ],
    "F": [
        " FFFFF",
        " F    ",
        " FFF  ",
        " F    ",
        " F    "
    ],
    "G": [
        "  GGG ",
        " G    ",
        " G  GG",
        " G   G",
        "  GGG "
    ],
    "H": [
        " H   H",
        " H   H",
        " HHHHH",
        " H   H",
        " H   H"
    ],
    "I": [
        " IIIII",
        "   I  ",
        "   I  ",
        "   I  ",
        " IIIII"
    ],
    "J": [
        " JJJJJ",
        "     J",
        "     J",
        " J   J",
        "  JJJ "
    ],
    "K": [
        " K   K",
        " K  K ",
        " KKK  ",
        " K  K ",
        " K   K"
    ],
    "L": [
        " L    ",
        " L    ",
        " L    ",
        " L    ",
        " LLLLL"
    ],
    "M": [
        " M   M",
        " MM MM",
        " M M M",
        " M   M",
        " M   M"
    ],
    "N": [
        " N   N",
        " NN  N",
        " N N N",
        " N  NN",
        " N   N"
    ],
    "O": [
        "  OOO ",
        " O   O",
        " O   O",
        " O   O",
        "  OOO "
    ],
    "P": [
        " PPPP ",
        " P   P",
        " PPPP ",
        " P    ",
        " P    "
    ],
    "Q": [
        "  QQQ ",
        " Q   Q",
        " Q   Q",
        " Q  QQ",
        "  QQQQ"
    ],
    "R": [
        " RRRR ",
        " R   R",
        " RRRR ",
        " R  R ",
        " R   R"
    ],
    "S": [
        "  SSS ",
        " S    ",
        "  SSS ",
        "     S",
        "  SSS "
    ],
    "T": [
        " TTTTT",
        "   T  ",
        "   T  ",
        "   T  ",
        "   T  "
    ],
    "U": [
        " U   U",
        " U   U",
        " U   U",
        " U   U",
        "  UUU "
    ],
    "V": [
        " V   V",
        " V   V",
        " V   V",
        "  V V ",
        "   V  "
    ],
    "W": [
        " W   W",
        " W   W",
        " W W W",
        " WW WW",
        " W   W"
    ],
    "X": [
        " X   X",
        "  X X ",
        "   X  ",
        "  X X ",
        " X   X"
    ],
    "Y": [
        " Y   Y",
        "  Y Y ",
        "   Y  ",
        "   Y  ",
        "   Y  "
    ],
    "Z": [
        " ZZZZZ",
        "    Z ",
        "   Z  ",
        "  Z   ",
        " ZZZZZ"
    ]
}

class CLItop:
    def __init__(self, args):
        self.args = args
        self.max_y = 0
        self.max_x = 0
        self.selected_idx = -1  # Track the currently selected index
        curses.wrapper(self.main)  # Wrap curses

    def main(self, stdscr):
        curses.curs_set(0)
        curses.start_color()
        
        # Initialize colors
        self.initialize_colors()
        
        items = self.get_desktop_items()
        if not items:
            stdscr.addstr(0, 0, "No items found on the desktop.")
            stdscr.refresh()
            stdscr.getch()
            return

        selected_idx = 0
        while True:
            self.draw_icons(stdscr, items, selected_idx)
            
            key = stdscr.getch()
            if key == curses.KEY_RIGHT and selected_idx < len(items) - 1:
                selected_idx += 1
            elif key == curses.KEY_LEFT and selected_idx > 0:
                selected_idx -= 1
            elif key == curses.KEY_DOWN:
                selected_idx += self.cols
                if selected_idx >= len(items):
                    selected_idx -= self.cols
            elif key == curses.KEY_UP:
                selected_idx -= self.cols
                if selected_idx < 0:
                    selected_idx += self.cols
            elif key == ord('\n'):
                os.startfile(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', items[selected_idx]))
            elif key == ord('q'):  # Add an option to quit
                break

    def get_desktop_items(self):
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        return os.listdir(desktop_path)

    def draw_icon(self, stdscr, icon_ascii, y, x, name, is_selected):
        # Draw the ASCII icon without highlight
        for row in range(len(icon_ascii)):
            for col in range(len(icon_ascii[row])):
                char = icon_ascii[row][col]
                if char != ' ':
                    color_pair = (ord(char) - ord('A') + 2) % 8 + 1  # Cycle through color pairs 1-8
                    stdscr.attron(curses.color_pair(color_pair))
                    stdscr.addstr(y + row, x + col, char)
                    stdscr.attroff(curses.color_pair(color_pair))
                else:
                    stdscr.addstr(y + row, x + col, char)
        
        # Ensure the name has at least one space at the start or end
        display_name = f" {name[:8]} " if len(name) > 8 else f" {name} "
        
        # Highlight the name if selected
        if is_selected:
            stdscr.attron(curses.color_pair(1))  # Highlight color
            stdscr.addstr(y + len(icon_ascii) + 1, x, display_name)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y + len(icon_ascii) + 1, x, display_name)

    def generate_ascii_icon(self, letter):
        # Use the predefined ascii_art dictionary
        return ascii_art.get(letter, ["     ", "     ", "     ", "     ", "     "])

    def draw_icons(self, stdscr, items, selected_idx):
        stdscr.clear()
        self.max_y, self.max_x = stdscr.getmaxyx()

        if self.max_x < 10 or self.max_y < 7:  # Adjusted for extra space
            stdscr.addstr(0, 0, "Window size is too small.")
            stdscr.refresh()
            stdscr.getch()
            return

        icon_width = 10
        icon_height = 7  # Adjusted for extra space
        self.cols = self.max_x // icon_width

        for idx, item in enumerate(items):
            y = (idx // self.cols) * icon_height
            x = (idx % self.cols) * icon_width

            letter = item[0].upper()  # Get the first letter of the item
            icon_ascii = self.generate_ascii_icon(letter)  # Generate ASCII art for the letter
            
            is_selected = (idx == selected_idx)
            self.draw_icon(stdscr, icon_ascii, y, x, item, is_selected)  # Draw the icon and name

        stdscr.refresh()

    def initialize_colors(self):
        # Add different color mappings using curses init_color and init_pair
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)  # Highlight color
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)

if __name__ == "__main__":
    CLItop(sys.argv)
