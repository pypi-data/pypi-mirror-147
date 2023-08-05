# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/empty_workspace_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EmptyWorkspaceWidget(object):
    def setupUi(self, EmptyWorkspaceWidget):
        EmptyWorkspaceWidget.setObjectName("EmptyWorkspaceWidget")
        EmptyWorkspaceWidget.resize(325, 108)
        self.verticalLayout = QtWidgets.QVBoxLayout(EmptyWorkspaceWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_icon = IconLabel(EmptyWorkspaceWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_icon.sizePolicy().hasHeightForWidth())
        self.label_icon.setSizePolicy(sizePolicy)
        self.label_icon.setMinimumSize(QtCore.QSize(80, 80))
        self.label_icon.setMaximumSize(QtCore.QSize(80, 80))
        self.label_icon.setText("")
        self.label_icon.setPixmap(QtGui.QPixmap(":/icons/images/material/folder_open.svg"))
        self.label_icon.setScaledContents(True)
        self.label_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.label_icon.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_icon.setProperty("color", QtGui.QColor(187, 187, 187))
        self.label_icon.setObjectName("label_icon")
        self.horizontalLayout_3.addWidget(self.label_icon)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(20, 12, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(EmptyWorkspaceWidget)
        QtCore.QMetaObject.connectSlotsByName(EmptyWorkspaceWidget)

    def retranslateUi(self, EmptyWorkspaceWidget):
        _translate = QtCore.QCoreApplication.translate
        EmptyWorkspaceWidget.setWindowTitle(_translate("EmptyWorkspaceWidget", "Form"))
from guardata.client.gui.custom_widgets import IconLabel
