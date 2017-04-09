import sys
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QProgressBar, QFileDialog, \
	QApplication, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, Qt
from data import localStorage, refreshMatch, reqUserAvatar, updateHeroRanking, heroid_dict
from functools import partial
import time

import qdarkstyle

class WebAccessThread(QThread):
	status_update = pyqtSignal(str)
	progressbar_init = pyqtSignal()
	progressbar_update = pyqtSignal(int)
	ava_update = pyqtSignal(int, QPixmap)
	label_update = pyqtSignal(int, str)
	grid_update = pyqtSignal(int, int, QPixmap, str)

	def __init__(self):
		super().__init__()
		#self.input_text = input_text

	def run(self):
		global Ginput_text
		self.input_text = Ginput_text
		_, id_to_hero = heroid_dict()
		set_progress_number = 0
		self.progressbar_init.emit()
		status, rlist = refreshMatch(self.input_text)
		self.status_update.emit(status)
		try:
			for i in range(10):
				if rlist[i][0] != 0:
					name = rlist[i][0]
					ava = rlist[i][1]
				else:
					name = 'player' + str(i + 1)
					ava = 0
				ava_return = reqUserAvatar(ava)
				ava_pixmap = QPixmap()
				ava_pixmap.loadFromData(ava_return)
				self.ava_update.emit(i, ava_pixmap)

				#update_label = '<a href=\"https://opendota.com/players/'+str(rlist[i][5])+'\" style=\"color:white;\">'+str(name)+'</a>' + ' mmr estimation: ' + str(rlist[i][2]) + ' solo mmr: ' + str(
					#rlist[i][3]) + ' party mmr: ' + str(rlist[i][4])
				update_label = '<a href=\"https://opendota.com/players/' + str(
					rlist[i][5]) + '\" style=\"color:white;\">' + str(name) + '</a>' + ' <img src=\"media/esti_mmr.png\"> ' + str(
					rlist[i][2]) + ' <img src=\"media/solo_mmr.png\"> ' + str(
					rlist[i][3]) + ' <img src=\"media/team_mmr.png\"> ' + str(rlist[i][4])
				self.label_update.emit(i, update_label)

				hero_ranking = updateHeroRanking(rlist[i][5])
				if hero_ranking[0]['win']!=0:
					for k in range(10):
						temp_icon = hero_ranking[k]['hero_id']
						temp_icon = id_to_hero[int(temp_icon)]
						temp_icon = temp_icon.replace(' ', '_')
						temp_icon = 'hero_icon/' + temp_icon + '_icon.png'
						temp_icon = QPixmap(temp_icon)
						if hero_ranking[k]['games']!=0:
							temp_text = int(hero_ranking[k]['win']) / int(hero_ranking[k]['games'])
							temp_text = "{0:.0%}".format(temp_text)
							temp_text = temp_text+'/'+str(hero_ranking[k]['games'])
						else:
							temp_text = '0%'
						self.grid_update.emit(i, k, temp_icon, temp_text)

				set_progress_number += 10
				self.progressbar_update.emit(set_progress_number)
		except:
			set_progress_number = 100
			self.progressbar_update.emit(set_progress_number)

class DotaLawliet(QWidget):
	def __init__(self):
		super(DotaLawliet, self).__init__()

		root_box = QVBoxLayout()
		root_box.setAlignment(Qt.AlignTop)

		first_row = QHBoxLayout()
		root_box.addLayout(first_row)
		self.locate_txt_btn = QPushButton('locate server_log.txt')
		self.serlog_txt_input = QLineEdit()
		self.load_serlog_from_file()
		self.locate_txt_btn.clicked.connect(self.locate_txt_btn_func)
		first_row.addWidget(self.locate_txt_btn)
		first_row.addWidget(self.serlog_txt_input)

		second_row = QHBoxLayout()
		root_box.addLayout(second_row)
		self.refresh_btn = QPushButton('refresh match')
		second_row.addWidget(self.refresh_btn)
		self.status_label = QLabel('waiting for refreshing the match')
		second_row.addWidget(self.status_label)
		#refresh_thread = WebAccessThread(input_text=self.serlog_txt_input.text())
		refresh_thread = WebAccessThread()
		refresh_thread.progressbar_init.connect(self.resolveRMinitProgressbar)
		refresh_thread.progressbar_update.connect(self.resolveRMprogressbar)
		refresh_thread.status_update.connect(self.resolveRMstatus)
		refresh_thread.ava_update.connect(self.resolveRMava)
		refresh_thread.label_update.connect(self.resolveRMlabel)
		refresh_thread.grid_update.connect(self.resolveRMgrid)

		#self.refresh_btn.clicked.connect(self.refresh_btn_median)
		self.refresh_btn.clicked.connect(lambda: refresh_thread.start())

		self.progressBar = QProgressBar(self)
		self.progressBar.setRange(0, 100)
		root_box.addWidget(self.progressBar)

		third_row = QVBoxLayout()
		root_box.addLayout(third_row)
		radiant_label = QLabel('Radiant')
		radiant_label.setStyleSheet('QLabel{background:green;}')
		third_row.addWidget(radiant_label)
		dire_label = QLabel('Dire')
		dire_label.setStyleSheet('QLabel{background:red;color:black;}')

		""" example code for looping
		player0_box = QtWidgets.QVBoxLayout()
		player0_userBox = QtWidgets.QHBoxLayout()
		self.player0_label = QtWidgets.QLabel()
		self.player0_ava = QtWidgets.QLabel()
		self.player0_grid = QGridLayout()

		third_row.addLayout(player0_box)
		player0_box.addLayout(player0_userBox)
		player0_userbox.addWidget(self.player0_ava)
		player0_userbox.addWidget(self.player0_label)
		player0_box.addLayout(self.player0_grid)"""

		for i in range(10):
			locals()['player' + str(i) + '_box'] = QVBoxLayout()
			locals()['player' + str(i) + '_userbox'] = QHBoxLayout()
			setattr(self, 'player' + str(i) + '_label', QLabel())
			setattr(self, 'player' + str(i) + '_ava', QLabel())
			setattr(self, 'player' + str(i) + '_grid', QGridLayout())

			if i == 5:
				third_row.addWidget(dire_label)
			third_row.addLayout(locals()['player' + str(i) + '_box'])
			locals()['player' + str(i) + '_box'].addLayout(locals()['player' + str(i) + '_userbox'])
			locals()['player' + str(i) + '_userbox'].addWidget(getattr(self, 'player' + str(i) + '_ava'))
			locals()['player' + str(i) + '_userbox'].addWidget(getattr(self, 'player' + str(i) + '_label'))
			locals()['player' + str(i) + '_box'].addLayout(getattr(self, 'player' + str(i) + '_grid'))

		self.setLayout(root_box)
		self.setWindowTitle('DotaLawliet')
		self.show()
		sys.exit(app.exec_())

	def locate_txt_btn_func(self):
		serlog_addr = QFileDialog.getOpenFileName(self, 'Open server_log.txt')
		if serlog_addr[0]:
			global Ginput_text
			Ginput_text = serlog_addr[0]
			self.serlog_txt_input.setText(serlog_addr[0])
			localStorage('write', serlog_addr[0])
		else:
			pass

	def load_serlog_from_file(self):
		global Ginput_text
		x = localStorage('read', ' ')
		Ginput_text = x[0]
		self.serlog_txt_input.setText(x[0])

	def resolveRMinitProgressbar(self):
		for i in range(10):
			while True:
				item = getattr(self, 'player'+str(i)+'_grid').takeAt(0)
				if not item:
					break
				getattr(self, 'player' + str(i) + '_grid').removeWidget(item.widget())
				item.widget().deleteLater()

		self.progressBar.setValue(0)
		# disable the button for 20 seconds
		self.refresh_btn.setEnabled(False)

	def resolveRMstatus(self, status):
		self.status_label.setText(status)

	def resolveRMprogressbar(self, progress):
		self.progressBar.setValue(progress)
		if progress == 100 and str(self.status_label.text()) != 'invalid server_log.txt path!':
			QTimer.singleShot(20000, partial(self.refresh_btn.setEnabled, True))
		else:
			self.refresh_btn.setEnabled(True)

	def resolveRMava(self, i, ava_pixmap):
		getattr(self, 'player' + str(i) + '_ava').setPixmap(ava_pixmap)

	def resolveRMlabel(self, i, update_label):
		assignName = getattr(self, 'player' + str(i) + '_label')
		assignName.setStyleSheet("font: 10pt")
		assignName.setText(update_label)
		assignName.setOpenExternalLinks(True)

	def resolveRMgrid(self, i, k, temp_icon, temp_text):
		temp_icon_label = QLabel()
		temp_icon_label.setPixmap(temp_icon)
		temp_text_label = QLabel(str(temp_text))
		"""self.player0_grid.addWidget(icon, 0, 0)
		self.player0_grid.addWidget(text, 1, 0)"""
		getattr(self, 'player' + str(i) + '_grid').addWidget(temp_icon_label, 0, k)
		getattr(self, 'player' + str(i) + '_grid').addWidget(temp_text_label, 1, k)
		
# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
	# Print the error and traceback
	print(exctype, value, traceback)
	# Call the normal Exception hook after
	sys._excepthook(exctype, value, traceback)
	time.sleep(3)
	sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
main_window = DotaLawliet()
try:
	sys.exit(app.exec_())
except:
	print("Exiting")
