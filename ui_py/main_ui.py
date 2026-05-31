# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QProgressBar, QPushButton,
    QSizePolicy, QTabWidget, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(940, 580)
        self.tabWidget = QTabWidget(Widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(9, 9, 921, 561))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(9, 9, 901, 81))
        self.button_open_image_dir = QPushButton(self.groupBox)
        self.button_open_image_dir.setObjectName(u"button_open_image_dir")
        self.button_open_image_dir.setGeometry(QRect(11, 26, 88, 25))
        self.label_image_dir_path = QLabel(self.groupBox)
        self.label_image_dir_path.setObjectName(u"label_image_dir_path")
        self.label_image_dir_path.setGeometry(QRect(11, 57, 851, 16))
        self.groupBox_2 = QGroupBox(self.tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(9, 92, 901, 293))
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.selector_match_type = QComboBox(self.groupBox_2)
        self.selector_match_type.addItem("")
        self.selector_match_type.addItem("")
        self.selector_match_type.setObjectName(u"selector_match_type")

        self.gridLayout.addWidget(self.selector_match_type, 0, 1, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)

        self.input_nfeatures = QLineEdit(self.groupBox_2)
        self.input_nfeatures.setObjectName(u"input_nfeatures")

        self.gridLayout.addWidget(self.input_nfeatures, 0, 3, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 4, 1, 1)

        self.input_match_distance_thresh = QLineEdit(self.groupBox_2)
        self.input_match_distance_thresh.setObjectName(u"input_match_distance_thresh")

        self.gridLayout.addWidget(self.input_match_distance_thresh, 0, 5, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 6, 1, 1)

        self.input_similarity_thresh = QLineEdit(self.groupBox_2)
        self.input_similarity_thresh.setObjectName(u"input_similarity_thresh")

        self.gridLayout.addWidget(self.input_similarity_thresh, 0, 7, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.input_start_point_x = QLineEdit(self.groupBox_2)
        self.input_start_point_x.setObjectName(u"input_start_point_x")
        self.input_start_point_x.setMaxLength(32767)

        self.horizontalLayout.addWidget(self.input_start_point_x)

        self.input_start_point_y = QLineEdit(self.groupBox_2)
        self.input_start_point_y.setObjectName(u"input_start_point_y")

        self.horizontalLayout.addWidget(self.input_start_point_y)

        self.input_end_point_x = QLineEdit(self.groupBox_2)
        self.input_end_point_x.setObjectName(u"input_end_point_x")

        self.horizontalLayout.addWidget(self.input_end_point_x)

        self.input_end_point_y = QLineEdit(self.groupBox_2)
        self.input_end_point_y.setObjectName(u"input_end_point_y")

        self.horizontalLayout.addWidget(self.input_end_point_y)

        self.button_add_rect = QPushButton(self.groupBox_2)
        self.button_add_rect.setObjectName(u"button_add_rect")

        self.horizontalLayout.addWidget(self.button_add_rect)

        self.button_image_picker = QPushButton(self.groupBox_2)
        self.button_image_picker.setObjectName(u"button_image_picker")

        self.horizontalLayout.addWidget(self.button_image_picker)

        self.button_del_rect = QPushButton(self.groupBox_2)
        self.button_del_rect.setObjectName(u"button_del_rect")

        self.horizontalLayout.addWidget(self.button_del_rect)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 8)

        self.listWidget_rect = QListWidget(self.groupBox_2)
        self.listWidget_rect.setObjectName(u"listWidget_rect")

        self.gridLayout.addWidget(self.listWidget_rect, 2, 0, 1, 8)

        self.groupBox_3 = QGroupBox(self.tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 390, 901, 122))
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.button_export_images = QPushButton(self.groupBox_3)
        self.button_export_images.setObjectName(u"button_export_images")
        self.button_export_images.setEnabled(False)

        self.gridLayout_2.addWidget(self.button_export_images, 2, 2, 1, 1)

        self.button_pause = QPushButton(self.groupBox_3)
        self.button_pause.setObjectName(u"button_pause")
        self.button_pause.setEnabled(False)

        self.gridLayout_2.addWidget(self.button_pause, 1, 2, 1, 2)

        self.button_stop = QPushButton(self.groupBox_3)
        self.button_stop.setObjectName(u"button_stop")
        self.button_stop.setEnabled(False)

        self.gridLayout_2.addWidget(self.button_stop, 1, 4, 1, 1)

        self.input_match_quantity = QLineEdit(self.groupBox_3)
        self.input_match_quantity.setObjectName(u"input_match_quantity")

        self.gridLayout_2.addWidget(self.input_match_quantity, 2, 4, 1, 1)

        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 3, 1, 1)

        self.button_start = QPushButton(self.groupBox_3)
        self.button_start.setObjectName(u"button_start")
        self.button_start.setEnabled(False)

        self.gridLayout_2.addWidget(self.button_start, 1, 0, 1, 2)

        self.button_remove_image = QPushButton(self.groupBox_3)
        self.button_remove_image.setObjectName(u"button_remove_image")
        self.button_remove_image.setEnabled(False)

        self.gridLayout_2.addWidget(self.button_remove_image, 2, 0, 1, 1)

        self.checkBox_remove_image_match_prefix = QCheckBox(self.groupBox_3)
        self.checkBox_remove_image_match_prefix.setObjectName(u"checkBox_remove_image_match_prefix")

        self.gridLayout_2.addWidget(self.checkBox_remove_image_match_prefix, 2, 1, 1, 1)

        self.progressBar = QProgressBar(self.groupBox_3)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout_2.addWidget(self.progressBar, 0, 0, 1, 5)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.groupBox_4 = QGroupBox(self.tab_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 0, 901, 71))
        self.layoutWidget = QWidget(self.groupBox_4)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 20, 454, 28))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.button_select_skewed_image = QPushButton(self.layoutWidget)
        self.button_select_skewed_image.setObjectName(u"button_select_skewed_image")

        self.horizontalLayout_2.addWidget(self.button_select_skewed_image)

        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_2.addWidget(self.label_6)

        self.input_skewed_image_width = QLineEdit(self.layoutWidget)
        self.input_skewed_image_width.setObjectName(u"input_skewed_image_width")

        self.horizontalLayout_2.addWidget(self.input_skewed_image_width)

        self.label_7 = QLabel(self.layoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_2.addWidget(self.label_7)

        self.input_skewed_image_height = QLineEdit(self.layoutWidget)
        self.input_skewed_image_height.setObjectName(u"input_skewed_image_height")

        self.horizontalLayout_2.addWidget(self.input_skewed_image_height)

        self.button_start_conv_images = QPushButton(self.groupBox_4)
        self.button_start_conv_images.setObjectName(u"button_start_conv_images")
        self.button_start_conv_images.setEnabled(False)
        self.button_start_conv_images.setGeometry(QRect(500, 20, 88, 26))
        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Widget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.groupBox.setTitle(QCoreApplication.translate("Widget", u"\u8bbe\u7f6e", None))
        self.button_open_image_dir.setText(QCoreApplication.translate("Widget", u"\u6253\u5f00\u56fe\u7247\u76ee\u5f55", None))
        self.label_image_dir_path.setText(QCoreApplication.translate("Widget", u"\u8bf7\u5148\u9009\u62e9\u56fe\u7247\u76ee\u5f55", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Widget", u"\u5206\u7c7b\u914d\u7f6e", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"\u5339\u914d\u7c7b\u578b", None))
        self.selector_match_type.setItemText(0, QCoreApplication.translate("Widget", u"\u5ffd\u7565\u9009\u533a", None))
        self.selector_match_type.setItemText(1, QCoreApplication.translate("Widget", u"\u5339\u914d\u9009\u533a", None))

#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><p>ORB \u6700\u5927\u7279\u5f81\u70b9\u6570\u91cf</p><p>\u5982\u679c\u4f60\u4f20\u5165 <span style=\" font-family:'Courier New';\">nfeatures=500</span>\uff0cORB \u7b97\u6cd5\u5c31\u4f1a\u5728\u56fe\u7247\u91cc\u8fdb\u884c\u7b5b\u9009\uff0c<span style=\" font-weight:700;\">\u53ea\u4fdd\u7559\u6700\u660e\u663e\u7684\u3001\u8d28\u91cf\u6700\u9ad8\u7684 500 \u4e2a\u7279\u5f81\u70b9</span>\u3002</p><p><span style=\" font-weight:700;\">\u4e3a\u4ec0\u4e48\u8981\u9650\u5236\u6570\u91cf\uff1f</span> \u5982\u679c\u7279\u5f81\u70b9\u592a\u591a\uff08\u6bd4\u5982\u51e0\u4e07\u4e2a\uff09\uff0c\u540e\u9762\u7684\u6bd4\u5bf9\u901f\u5ea6\u4f1a\u53d8\u5f97\u6781\u6162\uff1b\u5982\u679c\u592a\u5c11\uff0c\u53c8\u53ef\u80fd\u6bd4\u5bf9\u4e0d\u51c6\u3002\u9650\u5236\u5728\u8fd9\u4e2a\u6570\u91cf\uff0c\u662f\u5728\u201c\u51c6\u786e\u5ea6\u201d\u548c\u201c\u8fd0\u884c\u901f\u5ea6\u201d\u4e4b\u95f4\u627e\u4e00\u4e2a\u5b8c\u7f8e\u7684\u5e73\u8861\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Widget", u"nfeatures", None))
        self.input_nfeatures.setText(QCoreApplication.translate("Widget", u"2000", None))
#if QT_CONFIG(tooltip)
        self.label_4.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><p>\u8868\u793a\u4e24\u4e2a\u6307\u7eb9\u7684<span style=\" font-weight:700;\">\u5dee\u8ddd\uff08\u8ddd\u79bb\uff09</span>\u3002\u6570\u503c\u8d8a\u5c0f\uff0c\u8bf4\u660e\u8fd9\u4e24\u4e2a\u70b9\u957f\u5f97\u8d8a\u50cf</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("Widget", u"match_distance_thresh", None))
        self.input_match_distance_thresh.setText(QCoreApplication.translate("Widget", u"45", None))
#if QT_CONFIG(tooltip)
        self.label_5.setToolTip(QCoreApplication.translate("Widget", u"<html><head/><body><p>\u771f\u6b63\u5339\u914d\u6210\u529f\u7684\u201c\u597d\u8fde\u7ebf\u201d\u6709\u591a\u5c11\u6761\u3002</p><p>\u5982\u679c\u597d\u8fde\u7ebf\u7684\u6570\u91cf\u8d85\u8fc7\u4e86\u6211\u4eec\u8bbe\u5b9a\u7684\u53ca\u683c\u7ebf\uff08<span style=\" font-family:'Courier New';\">similarity_thresh</span>\uff09\uff0c\u8bf4\u660e\u4e24\u5f20\u56fe\u76f8\u4f3c\u5ea6\u5f88\u9ad8</p><p><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#7a7e85;\"># </span><span style=\" font-family:'Courier New','monospace'; font-size:9.8pt; color:#7a7e85;\">\u76f8\u4f3c\u5339\u914d\u9608\u503c<br/></span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#7a7e85;\"># </span><span style=\" font-family:'Courier New','monospace'; font-size:9.8pt; color:#7a7e85;\">\u6ce8\u610f\uff1a\u5982\u679c\u662f</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#7a7e85;\"> 'only_scan' </span><span style=\" font-family:'Courier New','monospa"
                        "ce'; font-size:9.8pt; color:#7a7e85;\">\u5c40\u90e8\uff0c\u63d0\u53d6\u70b9\u8f83\u5c11\uff0c\u9608\u503c\u5efa\u8bae\u8bbe\u4f4e\u70b9\uff08\u5982</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#7a7e85;\"> 30~50</span><span style=\" font-family:'Courier New','monospace'; font-size:9.8pt; color:#7a7e85;\">\uff09\uff1b<br/></span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#7a7e85;\"># </span><span style=\" font-family:'Courier New','monospace'; font-size:9.8pt; color:#7a7e85;\">\u5982\u679c\u662f</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#7a7e85;\"> 'ignore' </span><span style=\" font-family:'Courier New','monospace'; font-size:9.8pt; color:#7a7e85;\">\u4ec5\u62a0\u9664\u4e00\u5c0f\u5757\uff0c\u5927\u90e8\u5206\u5168\u56fe\u90fd\u88ab\u626b\u63cf\uff0c\u9608\u503c\u53ef\u4ee5\u8bbe\u9ad8\u70b9\uff08\u5982</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#7a"
                        "7e85;\"> 400~1000</span><span style=\" font-family:'Courier New','monospace'; font-size:9.8pt; color:#7a7e85;\">\uff09\u3002</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("Widget", u"similarity_thresh", None))
#if QT_CONFIG(tooltip)
        self.input_similarity_thresh.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.input_similarity_thresh.setText(QCoreApplication.translate("Widget", u"1200", None))
        self.input_start_point_x.setInputMask("")
        self.input_start_point_x.setText("")
        self.input_start_point_x.setPlaceholderText(QCoreApplication.translate("Widget", u"\u8d77\u70b9x\u8f74", None))
        self.input_start_point_y.setPlaceholderText(QCoreApplication.translate("Widget", u"\u8d77\u70b9y\u8f74", None))
        self.input_end_point_x.setPlaceholderText(QCoreApplication.translate("Widget", u"\u7ec8\u70b9x\u8f74", None))
        self.input_end_point_y.setInputMask("")
        self.input_end_point_y.setPlaceholderText(QCoreApplication.translate("Widget", u"\u7ec8\u70b9y\u8f74", None))
        self.button_add_rect.setText(QCoreApplication.translate("Widget", u"\u624b\u52a8\u6dfb\u52a0\u70b9\u4f4d", None))
        self.button_image_picker.setText(QCoreApplication.translate("Widget", u"\u56fe\u7247\u5750\u6807\u62fe\u53d6\u5668", None))
        self.button_del_rect.setText(QCoreApplication.translate("Widget", u"\u5220\u9664\u70b9\u4f4d", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Widget", u"\u4efb\u52a1", None))
        self.button_export_images.setText(QCoreApplication.translate("Widget", u"\u5bfc\u51fa\u56fe\u7247", None))
        self.button_pause.setText(QCoreApplication.translate("Widget", u"\u6682\u505c/\u6062\u590d", None))
        self.button_stop.setText(QCoreApplication.translate("Widget", u"\u505c\u6b62", None))
        self.input_match_quantity.setText(QCoreApplication.translate("Widget", u"3", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"\u6700\u5927\u5339\u8f93\u51fa\u573a\u666f\u6570", None))
        self.button_start.setText(QCoreApplication.translate("Widget", u"\u5f00\u59cb", None))
        self.button_remove_image.setText(QCoreApplication.translate("Widget", u"\u79fb\u9664\u76f8\u540c\u540d\u79f0\u7684\u56fe\u7247", None))
        self.checkBox_remove_image_match_prefix.setText(QCoreApplication.translate("Widget", u"\u6a21\u7cca\u5339\u914d", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Widget", u"\u56fe\u7247\u5206\u7c7b", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Widget", u"\u56fe\u7247\u900f\u89c6\u8f6c\u5316", None))
        self.button_select_skewed_image.setText(QCoreApplication.translate("Widget", u"\u5f85\u900f\u89c6\u7684\u6587\u4ef6", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"\u8f93\u51fa\u7684\u5bbd\u5ea6", None))
        self.label_7.setText(QCoreApplication.translate("Widget", u"\u8f93\u51fa\u7684\u9ad8\u5ea6", None))
        self.button_start_conv_images.setText(QCoreApplication.translate("Widget", u"\u5f00\u59cb", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Widget", u"\u5de5\u5177", None))
    # retranslateUi

