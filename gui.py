# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# vim: set foldmethod=marker commentstring=\ \ #\ %s :
#
# Author:    Taishi Matsumura
# Created:   2017-05-01
#
# Copyright (C) 2017 Taishi Matsumura
#
from os import listdir
from os.path import join as os_path_join
import sys
import PyQt4.QtGui
import PyQt4.QtCore
from PyQt4 import uic
from brian2.units import *
from numpy import load as np_load
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
from raster import RasterFigure
from synamat import SynapseMatrix


class MainForm(PyQt4.QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.ui = uic.loadUi('./main_window.ui')
        self.establishConnection()

    def establishConnection(self):
        self.ui.OpenDialogButton.clicked.connect(self.pushOpenDialogButton)
        # tab1
        self.ui.PeriodCB.activated.connect(self.activatePeriodCB)
        self.ui.TrialCB.activated.connect(self.activateTrialCB)
        self.ui.GmaxCB.activated.connect(self.activateGmaxCB)
        self.ui.FlucCB.activated.connect(self.activateFlucCB)
        self.ui.JitterCB.activated.connect(self.activateJitterCB)
        self.ui.AmpCB.activated.connect(self.activateAmpCB)
        self.ui.FreqCB.activated.connect(self.activateFreqCB)
        self.ui.PeriodCB.highlighted.connect(self.activatePeriodCB)
        self.ui.TrialCB.highlighted.connect(self.activateTrialCB)
        self.ui.GmaxCB.highlighted.connect(self.activateGmaxCB)
        self.ui.FlucCB.highlighted.connect(self.activateFlucCB)
        self.ui.JitterCB.highlighted.connect(self.activateJitterCB)
        self.ui.AmpCB.highlighted.connect(self.activateAmpCB)
        self.ui.FreqCB.highlighted.connect(self.activateFreqCB)
        self.ui.RasterDrawButton.clicked.connect(self.pushRasterDrawButton)
        self.ui.MatrixDrawButton.clicked.connect(self.pushMatrixDrawButton)
        # tab2
        self.ui.PeriodCB_2.activated.connect(self.activatePeriodCB_2)
        self.ui.TrialCB_2.activated.connect(self.activateTrialCB_2)
        self.ui.GmaxCB_2.activated.connect(self.activateGmaxCB_2)
        self.ui.JitterCB_2.activated.connect(self.activateJitterCB_2)
        self.ui.AmpCB_2.activated.connect(self.activateAmpCB_2)
        self.ui.PeriodCB_2.highlighted.connect(self.activatePeriodCB_2)
        self.ui.TrialCB_2.highlighted.connect(self.activateTrialCB_2)
        self.ui.GmaxCB_2.highlighted.connect(self.activateGmaxCB_2)
        self.ui.JitterCB_2.highlighted.connect(self.activateJitterCB_2)
        self.ui.AmpCB_2.highlighted.connect(self.activateAmpCB_2)
        self.ui.MapDrawButton.clicked.connect(self.pushMapDrawButton)
        # tab3
        self.ui.PeriodCB_3.activated.connect(self.activatePeriodCB_3)
        self.ui.TrialCB_3.activated.connect(self.activateTrialCB_3)
        self.ui.GmaxCB_3.activated.connect(self.activateGmaxCB_3)
        self.ui.JitterCB_3.activated.connect(self.activateJitterCB_3)
        self.ui.AmpCB_3.activated.connect(self.activateAmpCB_3)
        self.ui.FreqCB_3_1.activated.connect(self.activateFreqCB_3_1)
        self.ui.FreqCB_3_2.activated.connect(self.activateFreqCB_3_2)
        self.ui.PeriodCB_3.highlighted.connect(self.activatePeriodCB_3)
        self.ui.TrialCB_3.highlighted.connect(self.activateTrialCB_3)
        self.ui.GmaxCB_3.highlighted.connect(self.activateGmaxCB_3)
        self.ui.JitterCB_3.highlighted.connect(self.activateJitterCB_3)
        self.ui.AmpCB_3.highlighted.connect(self.activateAmpCB_3)
        self.ui.FreqCB_3_1.highlighted.connect(self.activateFreqCB_3_1)
        self.ui.FreqCB_3_2.highlighted.connect(self.activateFreqCB_3_2)
        self.ui.TuningCurveDrawButton.clicked.connect(self.pushTuningCurveDrawButton)

    def pushOpenDialogButton(self):
        selected_dir = PyQt4.QtGui.QFileDialog.getExistingDirectory(self, 'Select Directory', '../network/')
        self.ui.DirEditor.setText(selected_dir)
        self.initComboBoxes()
        self.initComboBoxes_2()
        self.initComboBoxes_3()

    # tab1
    def initComboBoxes(self):
        self.dirs = []
        self.dirs.append(unicode(self.ui.DirEditor.text()))
        self.dirs.append('Data')
        files = listdir(os_path_join(*self.dirs))
        self.ui.PeriodCB.clear()
        self.ui.PeriodCB.addItems(files)
        self.ui.PeriodCB.setEnabled(True)
        self.ui.TrialCB.setEnabled(False)
        self.ui.GmaxCB.setEnabled(False)
        self.ui.FlucCB.setEnabled(False)
        self.ui.JitterCB.setEnabled(False)
        self.ui.AmpCB.setEnabled(False)
        self.ui.FreqCB.setEnabled(False)
        self.ui.RasterDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activatePeriodCB()

    def activatePeriodCB(self):
        del self.dirs[2:]
        self.dirs.append(unicode(self.ui.PeriodCB.currentText()))
        files = listdir(os_path_join(*self.dirs))
        self.ui.TrialCB.clear()
        self.ui.TrialCB.addItems(files)
        self.ui.TrialCB.setEnabled(True)
        self.ui.GmaxCB.setEnabled(False)
        self.ui.FlucCB.setEnabled(False)
        self.ui.JitterCB.setEnabled(False)
        self.ui.AmpCB.setEnabled(False)
        self.ui.FreqCB.setEnabled(False)
        self.ui.RasterDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateTrialCB()

    def activateTrialCB(self):
        del self.dirs[3:]
        self.dirs.append(unicode(self.ui.TrialCB.currentText()))
        files = listdir(os_path_join(*self.dirs))
        self.ui.GmaxCB.clear()
        self.ui.GmaxCB.addItems(files)
        self.ui.TrialCB.setEnabled(True)
        self.ui.GmaxCB.setEnabled(True)
        self.ui.FlucCB.setEnabled(False)
        self.ui.JitterCB.setEnabled(False)
        self.ui.AmpCB.setEnabled(False)
        self.ui.FreqCB.setEnabled(False)
        self.ui.RasterDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateGmaxCB()

    def activateGmaxCB(self):
        del self.dirs[4:]
        self.dirs.append(unicode(self.ui.GmaxCB.currentText()))
        files = listdir(os_path_join(*self.dirs))
        self.ui.FlucCB.clear()
        self.ui.FlucCB.addItems(files)
        self.ui.TrialCB.setEnabled(True)
        self.ui.GmaxCB.setEnabled(True)
        self.ui.FlucCB.setEnabled(True)
        self.ui.JitterCB.setEnabled(False)
        self.ui.AmpCB.setEnabled(False)
        self.ui.FreqCB.setEnabled(False)
        if len(files) == 1:
            self.activateFlucCB()

    def activateFlucCB(self):
        del self.dirs[5:]
        self.dirs.append(unicode(self.ui.FlucCB.currentText()))
        files = listdir(os_path_join(*self.dirs))
        self.ui.JitterCB.clear()
        self.ui.JitterCB.addItems(files)
        self.ui.TrialCB.setEnabled(True)
        self.ui.GmaxCB.setEnabled(True)
        self.ui.FlucCB.setEnabled(True)
        self.ui.JitterCB.setEnabled(True)
        self.ui.AmpCB.setEnabled(False)
        self.ui.FreqCB.setEnabled(False)
        self.ui.RasterDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateJitterCB()

    def activateJitterCB(self):
        del self.dirs[6:]
        self.dirs.append(unicode(self.ui.JitterCB.currentText()))
        files = listdir(os_path_join(*self.dirs))
        self.ui.AmpCB.clear()
        self.ui.AmpCB.addItems(files)
        self.ui.TrialCB.setEnabled(True)
        self.ui.GmaxCB.setEnabled(True)
        self.ui.FlucCB.setEnabled(True)
        self.ui.JitterCB.setEnabled(True)
        self.ui.AmpCB.setEnabled(True)
        self.ui.FreqCB.setEnabled(False)
        self.ui.RasterDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateAmpCB()

    def activateAmpCB(self):
        del self.dirs[7:]
        self.dirs.append(unicode(self.ui.AmpCB.currentText()))
        files = listdir(os_path_join(*self.dirs))
        self.ui.FreqCB.clear()
        self.ui.FreqCB.addItems(files)
        self.ui.TrialCB.setEnabled(True)
        self.ui.GmaxCB.setEnabled(True)
        self.ui.FlucCB.setEnabled(True)
        self.ui.JitterCB.setEnabled(True)
        self.ui.AmpCB.setEnabled(True)
        self.ui.FreqCB.setEnabled(True)
        self.ui.RasterDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateFreqCB()

    def activateFreqCB(self):
        del self.dirs[8:]
        self.dirs.append(unicode(self.ui.FreqCB.currentText()))
        self.load_path = os_path_join(*self.dirs)
        self.ui.RasterDrawButton.setEnabled(True)
        self.ui.MatrixDrawButton.setEnabled(True)

    def pushRasterDrawButton(self):
        raster_window = RasterWindow(self.dirs[:], parent=self)
        raster_window.ui.show()

    def pushMatrixDrawButton(self):
        synapse_matrix_window = SynapseMatrixWindow(self.dirs[:], parent=self)
        synapse_matrix_window.ui.show()

    # tab2
    def initComboBoxes_2(self):
        self.dirs2 = []
        self.dirs2.append(unicode(self.ui.DirEditor.text()))
        self.dirs2.append('Data')
        files = listdir(os_path_join(*self.dirs2))
        self.ui.PeriodCB_2.clear()
        self.ui.PeriodCB_2.addItems(files)
        self.ui.PeriodCB_2.setEnabled(True)
        self.ui.TrialCB_2.setEnabled(False)
        self.ui.GmaxCB_2.setEnabled(False)
        self.ui.JitterCB_2.setEnabled(False)
        self.ui.AmpCB_2.setEnabled(False)
        self.ui.MapDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activatePeriodCB_2()

    def activatePeriodCB_2(self):
        del self.dirs2[2:]
        self.dirs2.append(unicode(self.ui.PeriodCB_2.currentText()))
        files = listdir(os_path_join(*self.dirs2))
        self.ui.TrialCB_2.clear()
        self.ui.TrialCB_2.addItems(files)
        self.ui.TrialCB_2.setEnabled(True)
        self.ui.GmaxCB_2.setEnabled(False)
        self.ui.JitterCB_2.setEnabled(False)
        self.ui.AmpCB_2.setEnabled(False)
        self.ui.MapDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateTrialCB_2()

    def activateTrialCB_2(self):
        del self.dirs2[3:]
        self.dirs2.append(unicode(self.ui.TrialCB_2.currentText()))
        files = listdir(os_path_join(*self.dirs2))
        self.ui.GmaxCB_2.clear()
        self.ui.GmaxCB_2.addItems(files)
        self.ui.TrialCB_2.setEnabled(True)
        self.ui.GmaxCB_2.setEnabled(True)
        self.ui.JitterCB_2.setEnabled(False)
        self.ui.AmpCB_2.setEnabled(False)
        self.ui.MapDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateGmaxCB_2()

    def activateGmaxCB_2(self):
        del self.dirs2[4:]
        self.dirs2.append(unicode(self.ui.GmaxCB_2.currentText()))
        self.dirs2.append(listdir(os_path_join(*self.dirs2))[0])
        files = listdir(os_path_join(*self.dirs2))
        self.ui.JitterCB_2.clear()
        self.ui.JitterCB_2.addItems(files)
        self.ui.TrialCB_2.setEnabled(True)
        self.ui.GmaxCB_2.setEnabled(True)
        self.ui.JitterCB_2.setEnabled(True)
        self.ui.AmpCB_2.setEnabled(False)
        self.ui.MapDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateJitterCB_2()

    def activateJitterCB_2(self):
        del self.dirs2[6:]
        self.dirs2.append(unicode(self.ui.JitterCB_2.currentText()))
        files = listdir(os_path_join(*self.dirs2))
        self.ui.AmpCB_2.clear()
        self.ui.AmpCB_2.addItems(files)
        self.ui.TrialCB_2.setEnabled(True)
        self.ui.GmaxCB_2.setEnabled(True)
        self.ui.JitterCB_2.setEnabled(True)
        self.ui.AmpCB_2.setEnabled(True)
        self.ui.MapDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateAmpCB_2()

    def activateAmpCB_2(self):
        del self.dirs2[7:]
        self.dirs2.append(unicode(self.ui.AmpCB_2.currentText()))
        self.dirs2.append(listdir(os_path_join(*self.dirs2))[0])
        self.load_path = os_path_join(*self.dirs2)
        self.ui.MapDrawButton.setEnabled(True)

    def pushMapDrawButton(self):
        window = DirectivityMapWindow(self.dirs2[:], parent=self)
        window.ui.show()

    # tab3
    def initComboBoxes_3(self):
        self.dirs3 = []
        self.dirs3.append(unicode(self.ui.DirEditor.text()))
        self.dirs3.append('Data')
        files = listdir(os_path_join(*self.dirs3))
        self.ui.PeriodCB_3.clear()
        self.ui.PeriodCB_3.addItems(files)
        self.ui.PeriodCB_3.setEnabled(True)
        self.ui.TrialCB_3.setEnabled(False)
        self.ui.GmaxCB_3.setEnabled(False)
        self.ui.JitterCB_3.setEnabled(False)
        self.ui.AmpCB_3.setEnabled(False)
        self.ui.FreqCB_3_1.setEnabled(False)
        self.ui.FreqCB_3_2.setEnabled(False)
        self.ui.TuningCurveDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activatePeriodCB_3()

    def activatePeriodCB_3(self):
        del self.dirs3[2:]
        self.dirs3.append(unicode(self.ui.PeriodCB_3.currentText()))
        files = listdir(os_path_join(*self.dirs3))
        self.ui.TrialCB_3.clear()
        self.ui.TrialCB_3.addItems(files)
        self.ui.TrialCB_3.setEnabled(True)
        self.ui.GmaxCB_3.setEnabled(False)
        self.ui.JitterCB_3.setEnabled(False)
        self.ui.AmpCB_3.setEnabled(False)
        self.ui.FreqCB_3_1.setEnabled(False)
        self.ui.FreqCB_3_2.setEnabled(False)
        self.ui.TuningCurveDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateTrialCB_3()

    def activateTrialCB_3(self):
        del self.dirs3[3:]
        self.dirs3.append(unicode(self.ui.TrialCB_3.currentText()))
        files = listdir(os_path_join(*self.dirs3))
        self.ui.GmaxCB_3.clear()
        self.ui.GmaxCB_3.addItems(files)
        self.ui.TrialCB_3.setEnabled(True)
        self.ui.GmaxCB_3.setEnabled(True)
        self.ui.JitterCB_3.setEnabled(False)
        self.ui.AmpCB_3.setEnabled(False)
        self.ui.FreqCB_3_1.setEnabled(False)
        self.ui.FreqCB_3_2.setEnabled(False)
        self.ui.TuningCurveDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateGmaxCB_3()

    def activateGmaxCB_3(self):
        del self.dirs3[4:]
        self.dirs3.append(unicode(self.ui.GmaxCB_3.currentText()))
        self.dirs3.append(listdir(os_path_join(*self.dirs3))[0])
        files = listdir(os_path_join(*self.dirs3))
        self.ui.JitterCB_3.clear()
        self.ui.JitterCB_3.addItems(files)
        self.ui.TrialCB_3.setEnabled(True)
        self.ui.GmaxCB_3.setEnabled(True)
        self.ui.JitterCB_3.setEnabled(True)
        self.ui.AmpCB_3.setEnabled(False)
        self.ui.FreqCB_3_1.setEnabled(False)
        self.ui.FreqCB_3_2.setEnabled(False)
        self.ui.TuningCurveDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateJitterCB_3()

    def activateJitterCB_3(self):
        del self.dirs3[6:]
        self.dirs3.append(unicode(self.ui.JitterCB_3.currentText()))
        files = listdir(os_path_join(*self.dirs3))
        self.ui.AmpCB_3.clear()
        self.ui.AmpCB_3.addItems(files)
        self.ui.TrialCB_3.setEnabled(True)
        self.ui.GmaxCB_3.setEnabled(True)
        self.ui.JitterCB_3.setEnabled(True)
        self.ui.AmpCB_3.setEnabled(True)
        self.ui.FreqCB_3_1.setEnabled(False)
        self.ui.FreqCB_3_2.setEnabled(False)
        self.ui.TuningCurveDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateAmpCB_3()

    def activateAmpCB_3(self):
        del self.dirs3[7:]
        self.dirs3.append(unicode(self.ui.AmpCB_3.currentText()))
        files = listdir(os_path_join(*self.dirs3))
        self.ui.FreqCB_3_1.clear()
        self.ui.FreqCB_3_1.addItems(files)
        self.ui.TrialCB_3.setEnabled(True)
        self.ui.GmaxCB_3.setEnabled(True)
        self.ui.JitterCB_3.setEnabled(True)
        self.ui.AmpCB_3.setEnabled(True)
        self.ui.FreqCB_3_1.setEnabled(True)
        self.ui.FreqCB_3_2.setEnabled(False)
        self.ui.TuningCurveDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateFreqCB_3_1()

    def activateFreqCB_3_1(self):
        del self.dirs3[8:]
        files = listdir(os_path_join(*self.dirs3))
        self.ui.FreqCB_3_2.clear()
        self.ui.FreqCB_3_2.addItems(files)
        self.dirs3.append(unicode(self.ui.FreqCB_3_1.currentText()))
        self.ui.TrialCB_3.setEnabled(True)
        self.ui.GmaxCB_3.setEnabled(True)
        self.ui.JitterCB_3.setEnabled(True)
        self.ui.AmpCB_3.setEnabled(True)
        self.ui.FreqCB_3_1.setEnabled(True)
        self.ui.FreqCB_3_2.setEnabled(True)
        self.ui.TuningCurveDrawButton.setEnabled(False)
        if len(files) == 1:
            self.activateFreqCB_3_2()

    def activateFreqCB_3_2(self):
        del self.dirs3[9:]
        self.dirs3.append(unicode(self.ui.FreqCB_3_2.currentText()))
        self.load_path = os_path_join(*self.dirs3)
        self.ui.TuningCurveDrawButton.setEnabled(True)

    def pushTuningCurveDrawButton(self):
        freq1 = int(self.dirs3[8][5:-4]) * Hz
        freq2 = int(self.dirs3[9][5:-4]) * Hz
        params_path = os_path_join(*self.dirs3[:9] + ['params.pkl'])
        params = np_load(params_path)
        profile_root = self.dirs3[0] + '/'
        period = params['period']
        gmax_rec = params['gmax_rec']
        a = params['a']
        jitter = params['jitter']
        trials = xrange(3)
        FLUCs = range(0, 1100000, 100000) * (uA ** 2 / ms)
        tuning_curve_figure = TuningCurveFigure()
        tuning_curve_figure.plot(profile_root, period, trials, gmax_rec, FLUCs, a, freq1, freq2, jitter)
        tuning_curve_figure.show()


class RasterWindow(PyQt4.QtGui.QMainWindow):
    def __init__(self, dirs, parent=None):
        super(RasterWindow, self).__init__(parent)
        self.ui = uic.loadUi('./raster_window.ui')
        self.establishConnection()

        dirs.append('params.pkl')
        params_path = os_path_join(*dirs)
        params = np_load(params_path)
        profile_root = dirs[0] + '/'
        period = params['period']
        trial = params['trial']
        gmax_rec = params['gmax_rec']
        FLUC = params['FLUC']
        a = params['a']
        freq = params['freq']
        jitter = params['jitter']
        self.raster_figure = RasterFigure()
        self.raster_figure.plot(profile_root, period, trial, gmax_rec, FLUC, a, freq, jitter)

        self.canvas = Canvas(self.raster_figure.fig, parent=self.ui.centralwidget)
        toolbar = NavigationToolbar2QT(self.canvas, self.ui.centralwidget)
        self.ui.VLayout.addWidget(self.canvas)
        self.ui.VLayout.addWidget(toolbar)
        self.ui.XlimDurationSB.setValue(self.raster_figure.ax1.get_xlim()[1])

    def establishConnection(self):
        self.ui.ApplyButton.clicked.connect(self.pushApplyButton)

    def pushApplyButton(self):
        self.updateXlim()
        self.canvas.updateFigure()

    def updateXlim(self):
        xlim_start = self.ui.XlimStartSB.value()
        xlim_end = xlim_start + self.ui.XlimDurationSB.value()
        self.raster_figure.ax1.set_xlim([xlim_start, xlim_end])
        self.raster_figure.ax2.set_xlim([xlim_start, xlim_end])


class SynapseMatrixWindow(PyQt4.QtGui.QMainWindow):
    def __init__(self, dirs, parent=None):
        super(SynapseMatrixWindow, self).__init__(parent)
        self.ui = uic.loadUi('./matrix_window.ui')
        self.establishConnection()

        dirs.append('params.pkl')
        params_path = os_path_join(*dirs)
        params = np_load(params_path)
        profile_root = dirs[0] + '/'
        period = params['period']
        trial = params['trial']
        gmax_rec = params['gmax_rec']
        FLUC = params['FLUC']
        a = params['a']
        freq = params['freq']
        jitter = params['jitter']
        self.matrix_figure = SynapseMatrix(profile_root, period, trial, gmax_rec, FLUC, a, freq, jitter)
        self.matrix_figure.plot_synamat()

        self.canvas = Canvas(self.matrix_figure.fig, parent=self.ui.centralwidget)
        toolbar = NavigationToolbar2QT(self.canvas, self.ui.centralwidget)
        self.ui.VLayout.addWidget(self.canvas)
        self.ui.VLayout.addWidget(toolbar)

    def establishConnection(self):
        self.ui.ApplyButton.clicked.connect(self.pushApplyButton)

    def pushApplyButton(self):
        self.canvas.updateFigure()


class Canvas(FigureCanvasQTAgg):
    def __init__(self, fig, parent=None):
        super(Canvas, self).__init__(fig)
        self.setParent(parent)
        FigureCanvasQTAgg.setSizePolicy(self,
                                   PyQt4.QtGui.QSizePolicy.Expanding,
                                   PyQt4.QtGui.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def updateFigure(self):
        self.draw()


if __name__ == '__main__':
    app = PyQt4.QtGui.QApplication(sys.argv)

    main_form = MainForm()
    main_form.ui.show()

    sys.exit(app.exec_())
