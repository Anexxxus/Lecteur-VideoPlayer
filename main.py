from PyQt5.QtCore import Qt, QUrl, QTime
from qt_material import apply_stylesheet
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QAction, QComboBox
from PyQt5.QtGui import QIcon, QMouseEvent, QPixmap
import sys, os

class Videoplayer(QMainWindow):
    def __init__(self, parent=None):
        super(Videoplayer, self).__init__(parent)
        self.setMinimumSize(800, 600)
        self.windowStateBeforeFullScreen = None
        self.setWindowIcon(QIcon('icons/app.png'))
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        videoWidget.setMouseTracking(True)
        videoarea = QWidget(self)
        self.setCentralWidget(videoarea)
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.pausebutton=QPushButton()
        self.pausebutton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.pausebutton.setEnabled(False)
        self.spaceAction = QAction(QIcon('icons/play_arrow.png'), 'Воспроизвести/Пауза', self)
        self.spaceAction.setShortcut('Space')
        self.spaceAction.triggered.connect(self.togglePlayPause)
        self.stopbutton=QPushButton()
        self.stopbutton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopbutton.setEnabled(False)
        self.stopbutton.clicked.connect(self.stop)
        self.currentTimeLabel = QLabel()
        self.currentTimeLabel.setVisible(False)
        self.timeSeparatorLabel = QLabel("/")
        self.timeSeparatorLabel.setVisible(False)
        self.totalTimeLabel = QLabel()
        self.totalTimeLabel.setVisible(False)
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setEnabled(False)
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeImageLabel = QLabel()
        self.updateVolumeImage()
        self.volumeSlider.valueChanged.connect(self.setVolume)
        self.volumeSlider.valueChanged.connect(self.updateVolume)
        self.volumeSlider.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.fullscreenButton = QPushButton()
        self.fullscreenButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.fullscreenButton.clicked.connect(self.toggleFullScreen)
        self.fullscreenAction = QAction(QIcon('icons/fullscreen.png'), 'Во весь экран', self)
        self.fullscreenAction.setShortcut('F')
        self.fullscreenAction.triggered.connect(self.toggleFullScreen)
        self.speedComboBox = QComboBox()
        self.speedComboBox.addItems(["0.25x", "0.5x", "0.75x", "1x", "1.25x", "1.5x", "1.75x", "2x"])
        self.speedComboBox.currentIndexChanged.connect(self.changePlaybackSpeed)
        self.speedComboBox.setCurrentIndex(3)
        self.backwardButton = QPushButton()
        self.backwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.backwardButton.setEnabled(False)
        self.backwardButton.clicked.connect(self.backward)
        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.forwardButton.setEnabled(False)
        self.forwardButton.clicked.connect(self.forward)
        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Создание вкладок для меню бара, а также привязка к нему горячих клавиш вместе с иконками
        openAction = QAction(QIcon('icons/open_file.png'), 'Открыть файл', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(self.openfile)
        exitAction = QAction(QIcon('icons/exit_app.png'), 'Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.exit)
        stopAction=QAction(QIcon('icons/stop.png'), 'Стоп', self)
        stopAction.setShortcut('S')
        stopAction.triggered.connect(self.stop)
        toggleMuteAction = QAction(QIcon('icons/tooglemute.png'), 'Включить/Отключить звук', self)
        toggleMuteAction.setShortcut('M')
        toggleMuteAction.triggered.connect(self.toggleMute)
        increaseVolumeAction = QAction(QIcon('icons/volume_up.png'), 'Увеличить громкость', self)
        increaseVolumeAction.setShortcut(Qt.Key_Up)
        increaseVolumeAction.triggered.connect(self.increaseVolume)
        decreaseVolumeAction = QAction(QIcon('icons/volume_down.png'), 'Уменьшить громкость', self)
        decreaseVolumeAction.setShortcut(Qt.Key_Down)
        decreaseVolumeAction.triggered.connect(self.decreaseVolume)
        backwardAction = QAction(QIcon('icons/backward.png'), 'Назад', self)
        backwardAction.setShortcut('Left')
        backwardAction.triggered.connect(self.backward)
        forwardAction = QAction(QIcon('icons/forward.png'), 'Вперед', self)
        forwardAction.setShortcut('Right')
        forwardAction.triggered.connect(self.forward)

        # Меню бар и добавление к нему вкладок
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('Медиа')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        Editmenu=menuBar.addMenu('Воспроизведение')
        Editmenu.addAction(self.spaceAction)
        Editmenu.addAction(stopAction)
        Editmenu.addAction(backwardAction)
        Editmenu.addAction(forwardAction)
        Audiomenu=menuBar.addMenu('Аудио')
        Audiomenu.addAction(toggleMuteAction)
        Audiomenu.addAction(increaseVolumeAction)
        Audiomenu.addAction(decreaseVolumeAction)
        VideoMenu=menuBar.addMenu('Видео')
        VideoMenu.addAction(self.fullscreenAction)

        # Создание макетов кнопок и расположение их
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.stopbutton)
        controlLayout.addWidget(self.currentTimeLabel)
        controlLayout.addWidget(self.timeSeparatorLabel)
        controlLayout.addWidget(self.totalTimeLabel)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.volumeImageLabel)
        controlLayout.addWidget(self.volumeSlider)
        controlLayout.addWidget(self.fullscreenButton)
        controlLayout.addWidget(self.speedComboBox)
        controlLayout.addWidget(self.backwardButton)
        controlLayout.addWidget(self.forwardButton)
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)
        videoarea.setLayout(layout)

        # Вызов виджетов для открытия выбора файла
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.detectionError)

    def openfile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Выберите видеофайл",  "", "Все файлы (*);;Видеофайл (*.mp4 *.avi *.wmv *.mov *.mkv *.3gp, *flv, *ogv, *webm)")
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromUserInput(fileName)))
            self.playButton.setEnabled(True)
            self.stopbutton.setEnabled(True)
            self.pausebutton.setEnabled(True)
            self.positionSlider.setEnabled(True)
            self.currentTimeLabel.setVisible(True)
            self.timeSeparatorLabel.setVisible(True)
            self.totalTimeLabel.setVisible(True)
            file_name = os.path.basename(fileName)
            file_name_without_ext = os.path.splitext(file_name)[0]
            self.setWindowTitle(f"Видеоплеер - {file_name_without_ext}")
            self.errorLabel.clear()
        else:
            self.detectionError()

    def exit(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
           self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def pause(self):
        self.mediaPlayer.pause()

    def togglePlayPause(self): #Кнопка пауза и воспроизвести
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def stop(self):
        self.mediaPlayer.stop()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.backwardButton.setEnabled(True)
            self.forwardButton.setEnabled(True)
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.backwardButton.setEnabled(True)
            self.forwardButton.setEnabled(True)

        playbackRate = self.mediaPlayer.playbackRate()
        speedText = f"{playbackRate}x"
        index = self.speedComboBox.findText(speedText)
        if index != -1:
            self.speedComboBox.setCurrentIndex(index)

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.currentTimeLabel.setText(self.formatTime(position))

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        self.totalTimeLabel.setText(self.formatTime(duration))

    def formatTime(self, milliseconds):
        duration = QTime(0, 0, 0, 0).addMSecs(milliseconds)
        return duration.toString('hh:mm:ss')

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def unmute(self):
        self.mediaPlayer.setMuted(False)
        if self.volumeSlider.value() == 0:
            self.volumeSlider.setValue(self.previousVolume)
        self.updateVolumeImage()

    def mute(self):
        self.mediaPlayer.setMuted(True)
        self.previousVolume = self.volumeSlider.value()
        self.volumeSlider.setValue(0)
        self.updateVolumeImage()

    def toggleMute(self):
        if self.mediaPlayer.isMuted():
            self.mediaPlayer.setMuted(False)
            if self.volumeSlider.value() == 0:
                self.volumeSlider.setValue(self.previousVolume)
            self.updateVolumeImage()
        else:
            self.mediaPlayer.setMuted(True)
            self.previousVolume = self.volumeSlider.value()
            self.volumeSlider.setValue(0)
            self.updateVolumeImage()

    def setVolume(self, volume):
        self.mediaPlayer.setVolume(volume)

    def updateVolume(self):
        volume = self.volumeSlider.value()
        if volume == 0:
            self.mediaPlayer.setMuted(True)
        else:
            self.mediaPlayer.setMuted(False)
            self.mediaPlayer.setVolume(volume)
        self.updateVolumeImage()

    def updateVolumeImage(self):
        volume = self.volumeSlider.value()
        if volume == 0:
            image = QPixmap('icons/volume_off.png').scaled(35, 35)
        elif volume <= 50:
            image = QPixmap('icons/volume_down.png').scaled(35, 35)
        else:
            image = QPixmap('icons/volume_up.png').scaled(35, 35)
        self.volumeImageLabel.setPixmap(image)

    def increaseVolume(self):
        volume = self.volumeSlider.value()
        if volume < 100:
            volume += 5
            self.volumeSlider.setValue(volume)

    def decreaseVolume(self):
        volume = self.volumeSlider.value()
        if volume > 0:
            volume -= 5
            self.volumeSlider.setValue(volume)

    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
            if self.windowStateBeforeFullScreen is not None:
                self.setWindowState(self.windowStateBeforeFullScreen)
            self.windowStateBeforeFullScreen = None
        else:
            self.windowStateBeforeFullScreen = self.windowState()
            self.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F:
            self.toggleFullScreen()
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.toggleFullScreen()
        elif event.key() == Qt.Key_Left:
            self.backward()
        elif event.key() == Qt.Key_Right:
            self.forward()
        else:
            super().keyPressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.toggleFullScreen()
        else:
            super().mouseDoubleClickEvent(event)

    def changePlaybackSpeed(self):
        speedText = self.speedComboBox.currentText()
        speed = float(speedText[:-1])
        self.mediaPlayer.setPlaybackRate(speed)

    def backward(self):
        position = self.mediaPlayer.position()
        self.mediaPlayer.setPosition(position - 10000)

    def forward(self):
        position = self.mediaPlayer.position()
        duration = self.mediaPlayer.duration()
        new_position = position + 10000
        if new_position > duration:
            new_position = duration
        self.mediaPlayer.setPosition(new_position)

    def detectionError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Ошибка: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Видеоплеер")
    apply_stylesheet(app, theme='light_cyan.xml')
    window = Videoplayer()
    window.show()
    sys.exit(app.exec_())