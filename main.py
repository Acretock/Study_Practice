import sys
import os.path
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

mandelbrot = 'mandelbrot.gif'
julia = 'julia_set.gif'

class LoadingGif(object):
    def __init__(self,name):
        self.gif_name = name

    def mainUI(self, FrontWindow):
        FrontWindow.setObjectName("FTwindow")
        FrontWindow.resize(1900, 1000)
        self.centralwidget = QtWidgets.QWidget(FrontWindow)
        self.centralwidget.setObjectName("main-widget")

        # Label Create
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1000, 1000))
        self.label.setMinimumSize(QtCore.QSize(250, 250))
        self.label.setMaximumSize(QtCore.QSize(2500, 2500))
        self.label.setObjectName("lb1")
        FrontWindow.setCentralWidget(self.centralwidget)
        # Loading the GIF
        self.movie = QMovie(self.gif_name)
        self.label.setMovie(self.movie)

        self.startAnimation()

        # Start Animation

    def startAnimation(self):
        self.movie.start()

    # Stop Animation(According to need)
    def stopAnimation(self):
        self.movie.stop()

class TestApp:
    def __init__(self,useDefault=True,restart=False):
        self.useDefault = useDefault
        fileName =  'input.txt' if useDefault else  'default.txt'
        with open(fileName, mode='r') as f:
            lines = f.readlines()
        dataMan = list(map(float,lines[0].split(';')[0:-1]))
        dataJul = list(map(float,lines[1].split(';')[0:-1]))
        print(*dataJul)
        print(*dataMan)
        if not os.path.exists(mandelbrot) or restart:
            self.setupMandelbrot(dataMan)
        if not os.path.exists(julia) or restart:
            self.setupJulia(dataJul)
        f.close()
        print('setups done')
        app = QtWidgets.QApplication(sys.argv)
        mainWin = QtWidgets.QWidget()
        mainWin.resize(400, 400)
        mainWin.setWindowTitle('Main menu')
        mainBox = QtWidgets.QVBoxLayout()

        exitButton = QtWidgets.QPushButton('&exit all')
        #exitButton.resize(140, 100)
        exitButton.clicked.connect(app.quit)
        exitButton3 = QtWidgets.QPushButton('&Exit application')
        #exitButton.resize(140, 100)
        exitButton3.clicked.connect(app.quit)

        mandelbrotGifWindow = QtWidgets.QMainWindow()
        mandelbrotGifWindow.setWindowTitle("Animation")

        mandelbrotGif = LoadingGif(mandelbrot)
        mandelbrotGif.mainUI(mandelbrotGifWindow)


        stopMandelbrotGifButton = QtWidgets.QPushButton('&stop animation')
        #stopMandelbrotGifButton.resize(140, 100)
        stopMandelbrotGifButton.clicked.connect(mandelbrotGif.stopAnimation)

        startMandelbrotGifButton = QtWidgets.QPushButton('&start animation')
        #startMandelbrotGifButton.resize(140, 100)
        startMandelbrotGifButton.clicked.connect(mandelbrotGif.startAnimation)

        mControlsBox = QtWidgets.QVBoxLayout()
        mControlsBox.addWidget(stopMandelbrotGifButton)
        mControlsBox.addWidget(startMandelbrotGifButton)
        mControlsBox.addWidget(exitButton)

        controlsWindowMandelbrot = QtWidgets.QWidget()
        controlsWindowMandelbrot.resize(500, 400)
        controlsWindowMandelbrot.move(1000,200)

        def startMander():
            mandelbrotGifWindow.show()
            controlsWindowMandelbrot.show()
            mainWin.hide()

        julianGifWindow = QtWidgets.QMainWindow()
        julianGifWindow.setWindowTitle("Animation")

        julianGif = LoadingGif(julia)
        julianGif.mainUI(julianGifWindow)

        stopJulianGifButton = QtWidgets.QPushButton('&stop animation')
        stopJulianGifButton.resize(140, 100)
        stopJulianGifButton.clicked.connect(julianGif.stopAnimation)

        startJulianGifButton = QtWidgets.QPushButton('&start animation')
        startJulianGifButton.resize(140, 100)
        startJulianGifButton.clicked.connect(julianGif.startAnimation)

        exitButton2 = QtWidgets.QPushButton('&exit all')
        exitButton2.resize(140, 100)
        exitButton2.clicked.connect(app.quit)

        jControlsBox = QtWidgets.QVBoxLayout()
        jControlsBox.addWidget(stopJulianGifButton)
        jControlsBox.addWidget(startJulianGifButton)
        jControlsBox.addWidget(exitButton2)

        controlsWindowJulian = QtWidgets.QWidget()
        controlsWindowJulian.resize(500, 400)
        controlsWindowJulian.move(1000,200)

        def startJulia():
            julianGifWindow.show()
            controlsWindowJulian.show()
            mainWin.hide()

        startJuliaButton = QtWidgets.QPushButton('Start Julia')
        startJuliaButton.clicked.connect(startJulia)
        startMandelbrotButton = QtWidgets.QPushButton('Start Mandelbrot')
        startMandelbrotButton.clicked.connect(startMander)

        def returnMainMenu():
            julianGifWindow.hide()
            controlsWindowJulian.hide()
            mandelbrotGifWindow.hide()
            controlsWindowMandelbrot.hide()
            mainWin.show()


        returnButton = QtWidgets.QPushButton('&return to main menu')
        #returnButton.resize(140, 100)
        returnButton.clicked.connect(returnMainMenu)
        returnButton2 = QtWidgets.QPushButton('&return to main menu')
        #returnButton2.resize(140, 100)
        returnButton2.clicked.connect(returnMainMenu)
        jControlsBox.addWidget(returnButton2)
        mControlsBox.addWidget(returnButton)
        controlsWindowJulian.setLayout(jControlsBox)
        controlsWindowMandelbrot.setLayout(mControlsBox)

        mainBox.addWidget(startJuliaButton)
        mainBox.addWidget(startMandelbrotButton)
        mainBox.addWidget(exitButton3)
        mainWin.setLayout(mainBox)
        mainWin.show()
        sys.exit(app.exec_())

    def mandelbrot(self,x, y, threshold):
        """Calculates whether the number c = x + i*y belongs to the
        Mandelbrot set. In order to belong, the sequence z[i + 1] = z[i]**2 + c
        must not diverge after 'threshold' number of steps. The sequence diverges
        if the absolute value of z[i+1] is greater than 4.

        :param float x: the x component of the initial complex number
        :param float y: the y component of the initial complex number
        :param int threshold: the number of iterations to considered it converged
        """
        # initial conditions
        c = complex(x, y)
        z = complex(0, 0)

        for i in range(threshold):
            z = z ** 2 + c
            if abs(z) > 4.:  # it diverged
                return i

        return threshold - 1  # it didn't diverge

    def setupMandelbrot(self, data):
        xStartM, yStartM, widthM, heightM, dpiM = data
        #xStartM,yStartM  = -2, -1.5  # an interesting region starts here
        #width,height  = 3, 3  # for 3 units up and right
        #dpi = 250  # how many pixels per unit

        # real and imaginary axis
        re = np.linspace(xStartM, xStartM + widthM, math.floor(widthM * dpiM))
        im = np.linspace(yStartM, yStartM + heightM, math.floor(heightM * dpiM))

        fig = plt.figure(figsize=(10, 10))  # instantiate a figure to draw
        ax = plt.axes()  # create an axes object

        def animate(i):
            ax.clear()  # clear axes object
            ax.set_xticks([], [])  # clear x-axis ticks
            ax.set_yticks([], [])  # clear y-axis ticks

            X = np.empty((len(re), len(im)))  # re-initialize the array-like image
            threshold = round(1.15 ** (i + 1))  # calculate the current threshold

            # iterations for the current threshold
            for i in range(len(re)):
                for j in range(len(im)):
                    X[i, j] = self.mandelbrot(re[i], im[j], threshold)

            # associate colors to the iterations with an interpolation
            img = ax.imshow(X.T, interpolation="bicubic", cmap='magma')
            return [img]

        anim = animation.FuncAnimation(fig, animate, frames=45, interval=120, blit=True)
        anim.save(mandelbrot, writer='imagemagick')

    def julia_quadratic(self,zx, zy, cx, cy, threshold):
            """Calculates whether the number z[0] = zx + i*zy with a constant c = x + i*y
            belongs to the Julia set. In order to belong, the sequence
            z[i + 1] = z[i]**2 + c, must not diverge after 'threshold' number of steps.
            The sequence diverges if the absolute value of z[i+1] is greater than 4.

            :param float zx: the x component of z[0]
            :param float zy: the y component of z[0]
            :param float cx: the x component of the constant c
            :param float cy: the y component of the constant c
            :param int threshold: the number of iterations to considered it converged
            """
            # initial conditions
            z = complex(zx, zy)
            c = complex(cx, cy)

            for i in range(threshold):
                z = z ** 2 + c
                if abs(z) > 4.:  # it diverged
                    return i

            return threshold - 1  # it didn't diverge

    def setupJulia(self, data):
        xStartJ, yStartJ, widthJ, heightJ, dpiJ = data
        #x_start, y_start = -2, -2  # an interesting region starts here
        #width, height = 4, 4  # for 4 units up and right
        #density_per_unit = 200  # how many pixels per unit

        # real and imaginary axis
        reJulia = np.linspace(xStartJ, xStartJ + widthJ, math.floor(widthJ * dpiJ))
        imJulia = np.linspace(yStartJ, yStartJ + heightJ, math.floor(heightJ * dpiJ))

        threshold = 20  # max allowed iterations
        frames = 100  # number of frames in the animation

        # we represent c as c = r*cos(a) + i*r*sin(a) = r*e^{i*a}
        r = 0.7885
        a = np.linspace(0, 2 * np.pi, frames)

        figJulia = plt.figure(figsize=(10, 10))  # instantiate a figure to draw
        axJulia = plt.axes()  # create an axes object

        def animateJulia(i):
            axJulia.clear()  # clear axes object
            axJulia.set_xticks([], [])  # clear x-axis ticks
            axJulia.set_yticks([], [])  # clear y-axis ticks

            XJulia = np.empty((len(reJulia), len(imJulia)))  # the initial array-like image
            cx, cy = r * np.cos(a[i]), r * np.sin(a[i])  # the initial c number

            # iterations for the given threshold
            for i in range(len(reJulia)):
                for j in range(len(imJulia)):
                    XJulia[i, j] = self.julia_quadratic(reJulia[i], imJulia[j], cx, cy, threshold)

            img = axJulia.imshow(XJulia.T, interpolation="bicubic", cmap='magma')
            return [img]

        animJ = animation.FuncAnimation(figJulia, animateJulia, frames=frames, interval=50, blit=True)
        animJ.save(julia, writer='imagemagick')


if __name__ == '__main__':
    print('Input I for non default input')
    a = str(input()).lower()
    restart = False
    test = TestApp(a == 'i',restart)

