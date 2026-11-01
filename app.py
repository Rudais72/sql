# app.py — главный файл запуска проекта "Библиотека".
# Запусти его: python3 app.py (или python app.py на Windows).

import main
import terminal

if __name__ == "__main__":
    # 1) создаём базу и данные (main.py)
    # 2) открываем меню (terminal.py)
    main.run()
    terminal.main()
