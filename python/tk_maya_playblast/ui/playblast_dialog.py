# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'playblast_dialog.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_PlayblastDialog(object):
    def setupUi(self, PlayblastDialog):
        PlayblastDialog.setObjectName("PlayblastDialog")
        PlayblastDialog.resize(468, 67)
        self.gridLayout = QtGui.QGridLayout(PlayblastDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.cmbPercentage = QtGui.QComboBox(PlayblastDialog)
        self.cmbPercentage.setObjectName("cmbPercentage")
        self.gridLayout.addWidget(self.cmbPercentage, 0, 0, 1, 1)
        self.chbUploadToShotgun = QtGui.QCheckBox(PlayblastDialog)
        self.chbUploadToShotgun.setObjectName("chbUploadToShotgun")
        self.gridLayout.addWidget(self.chbUploadToShotgun, 0, 1, 1, 1)
        self.chbShowViewer = QtGui.QCheckBox(PlayblastDialog)
        self.chbShowViewer.setChecked(True)
        self.chbShowViewer.setObjectName("chbShowViewer")
        self.gridLayout.addWidget(self.chbShowViewer, 0, 2, 1, 1)
        self.btnPlayblast = QtGui.QPushButton(PlayblastDialog)
        self.btnPlayblast.setMinimumSize(QtCore.QSize(450, 0))
        self.btnPlayblast.setObjectName("btnPlayblast")
        self.gridLayout.addWidget(self.btnPlayblast, 1, 0, 1, 3)

        self.retranslateUi(PlayblastDialog)
        QtCore.QMetaObject.connectSlotsByName(PlayblastDialog)

    def retranslateUi(self, PlayblastDialog):
        PlayblastDialog.setWindowTitle(QtGui.QApplication.translate("PlayblastDialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))
        self.chbUploadToShotgun.setText(QtGui.QApplication.translate("PlayblastDialog", "Upload to Shotgun", None, QtGui.QApplication.UnicodeUTF8))
        self.chbShowViewer.setText(QtGui.QApplication.translate("PlayblastDialog", "Show Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.btnPlayblast.setText(QtGui.QApplication.translate("PlayblastDialog", "Playblast", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
