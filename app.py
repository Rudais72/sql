# app.py — the main startup file of the "Library" project.
# Run it with: python3 app.py (or python app.py on Windows).

import main
import terminal

if __name__ == "__main__":
    # 1) create the database and the data (main.py)
    # 2) open the menu (terminal.py)
    main.run()
    terminal.main()
