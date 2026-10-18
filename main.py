import threading
import datetime

import uvicorn
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QWidget,
    QGridLayout,
    QInputDialog
)

from dota_worker.dotabuff_parser import Hero, DotabuffParser
from dota_worker.gsi_server import ui_bridge
from dota_worker.evaluation import Map

app = QApplication([])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DotaCoach')
        self.setFixedSize(QSize(900, 500))
        central_widget = QWidget()
        self.nickname = ''
        self.setCentralWidget(central_widget)
        self.window_layout = QGridLayout(central_widget)
        self._hero_grid()
        start_button = QPushButton(central_widget)
        start_button.setIcon(QIcon('images/start_button.png'))
        start_button.setIconSize(QSize(245, 50))
        start_button.setFixedSize(QSize(245, 50))
        self.window_layout.addWidget(start_button, 0, 1,
                                    alignment=Qt.AlignmentFlag.AlignCenter)
        self.field = QInputDialog(central_widget)
        self.field.setLabelText('Enter a nickname:')
        self.field.textValueSelected.connect(self._nickname)
        self.field.show()
        start_button.show()
        start_button.clicked.connect(self._clicked)
        ui_bridge.hero_ban.connect(self._ban_hero)


    def _clicked(self):
        threading.Thread(target=uvicorn.run, args=('dota_worker.gsi_server:dota_worker',), kwargs={'port': 3000}).start()

    def _ban_hero(self, hero_id):
        self.labels[hero_id][0].setText('BAN')
        print(hero_id, 'banned')


    def _hero_grid(self):
        self.labels = Map()
        self.parser = DotabuffParser()
        scroll_area = QScrollArea(self)
        scroll_area.setFixedSize(QSize(142*4+16, 500))
        hero_grid = QWidget(scroll_area)
        self.hero_grid_layout = QGridLayout(hero_grid)
        hero_grid.setFixedSize(QSize(142*4, 188*(126//4+1)))
        row = 0
        col = 0
        for i in range(Hero.all_heroes_schema()[-1]['id']+1):
            picture = QPixmap()
            name = Hero.hero_name_by_id(i)
            if name is not None:
                picture.load(r'/home/algol83/PycharmProjects/DotaCoach/images/selection/panorama/images/heroes/selection/' + Hero.hero_name_by_id(i) + '_png.png')
                label = HeroCard(hero_grid, picture)
                if col == 4:
                    col = 0
                    row += 1
                self.hero_grid_layout.addWidget(label, row, col,
                                                alignment=Qt.AlignmentFlag.AlignCenter)
                self.parser.create_hero(i, name)
                self.labels[i] = [label, row, col]

                col += 1
        scroll_area.setWidget(hero_grid)
        self.window_layout.addWidget(scroll_area, 0, 0)

    def _nickname(self):
        self.nickname = self.field.textValue()
        
class HeroCard(QLabel):
    def __init__(self, parent, picture: QPixmap, text: str | None = None):
        super().__init__(parent)
        self.setFixedSize(QSize(142, 188))
        self.setPixmap(picture)

class Application:
    def __init__(self):
        self.time_in = datetime.datetime.now()

    def save_report(self, nickname):
        self.time_out = datetime.datetime.now()
        with open('data/report.txt', 'w') as report:
        
                report.write(f'''+------------------------------------+
        | login   |   time_in  |  time_out   |
        |---------|------------|-------------|
        |{nickname} | {self.time_in.strftime('%d.%m.%Y %H:%M:%S')} | {self.time_out.strftime('%d.%m.%Y %H:%M:%S')}  |
        +------------------------------------+''')


if __name__ == '__main__':
    application = Application()
    window = MainWindow()
    window.show()

    app.exec()
    nickname = window.nickname
    application.save_report(nickname)