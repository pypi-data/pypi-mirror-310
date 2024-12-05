import sys

from PySide6.QtGui import Qt, QColor
from PySide6.QtWidgets import QApplication

from qfluentwidgets import SettingCardGroup, FluentIcon, setTheme, Theme, InfoBarIcon
from FluentWidgets import ButtonCard, PrimaryButtonCard, TransparentButtonCard, \
    ToolButtonCard, PrimaryToolButtonCard, \
    TransparentToolButtonCard, SwitchButtonCard, CheckBoxCard, HyperLinkCard, ComboBoxCard, EditComboBoxCard, \
    DropDownCard, WinPngFluentIcon as WPFI, WinSvgFluentIcon as WSFI, \
    PrimaryDropDownCard, TransparentDropDownCard, DropDownToolCard, PrimaryDropDownToolCard, \
    TransparentDropDownToolCard, \
    SplitCard, PrimarySplitCard, SliderCard, ExpandGroupCard, OptionsCard, FolderListCard, MessageBox, ColorDialog

from FluentWidgets.widgets.acrylic_cards import AcrylicComboBoxCard, AcrylicEditComboBoxCard
from FluentWidgets import Dialog, UrlDialog, VerticalScrollWidget

from PyMyMethod.Method import FileControl


class Demo(VerticalScrollWidget):
    def __init__(self):
        super().__init__()
        self.fc = FileControl()
        self.girls = \
        dict(self.fc.readJsonFiles(r"C:\Projects\Items\Python\QT\QFluentWidget\Test\FlunetWindow\config\data.json"))[
            'girlName']

        self.initCard()
        self.initCardGroup()
        self.initLayout()
        self.initExpandCard()
        self.connectSignalSlots()

        # self.resize(1200, 700)
        # desktop = QApplication.primaryScreen().availableGeometry()
        # w, h = desktop.width(), desktop.height()
        # self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def initLayout(self):
        self.vLayout.addWidget(self.btCardGroup)
        self.vLayout.addWidget(self.tlBtCardGroup)
        self.vLayout.addWidget(self.switchBtCardGroup)
        self.vLayout.addWidget(self.comBoCardGroup)
        self.vLayout.addWidget(self.sliderCardGroup)
        self.vLayout.addWidget(self.expandCardGroup)

    def initCardGroup(self):
        self.btCardGroup = SettingCardGroup('标准按钮卡片组', self)
        self.btCardGroup.addSettingCards([
            self.btCard,
            self.prBtCard,
            self.trBtCard
        ])

        self.tlBtCardGroup = SettingCardGroup('工具按钮卡片', self)
        self.tlBtCardGroup.addSettingCards([
            self.tlBtCard,
            self.prTlBtCard,
            self.trTlBtCard
        ])

        self.switchBtCardGroup = SettingCardGroup("状态开关按钮", self)
        self.switchBtCardGroup.addSettingCards([
            self.switchBtCard,
            self.checkCard,
            self.linkBtCard
        ])

        self.comBoCardGroup = SettingCardGroup("下拉框卡片", self)
        self.comBoCardGroup.addSettingCards([
            self.comBoCard,
            self.edComBoCard,
            self.alcComBtCard,
            self.alcEditComBtCard,
            self.dnCard,
            self.prDnCard,
            self.trDnCard,
            self.dnTlCard,
            self.prDnTlCard,
            self.trDnTlCard,
            self.spCard,
            self.prSpCard
        ])

        self.sliderCardGroup = SettingCardGroup('滑动条', self)
        self.sliderCardGroup.addSettingCards([
            self.sliderCard
        ])

        self.expandCardGroup = SettingCardGroup('展开卡片', self)
        self.expandCard = ExpandGroupCard(
            FluentIcon.WIFI,
            "展开卡片",
            'Content',
            self
        )
        self.expandCardGroup.addSettingCards([
            self.expandCard,
            self.optionsCard,
            self.fls
        ])

    def initCard(self):
        """ 普通按钮 """
        self.btCard = ButtonCard(
            WSFI.HOME,
            '标准按钮卡片',
            'Content',
            '确定',
            FluentIcon.SEND,
            self
        )
        self.prBtCard = PrimaryButtonCard(
            FluentIcon.GITHUB,
            '主题色按钮卡片',
            'Content',
            '确定',
            parent=self
        )
        self.trBtCard = TransparentButtonCard(
            WPFI.DOWNLOAD_FOLDER,
            '透明按钮卡片',
            'Content',
            btIcon=FluentIcon.MORE,
            parent=self
        )
        #######################################################
        """工具按钮"""
        self.tlBtCard = ToolButtonCard(
            FluentIcon.BLUETOOTH,
            '工具按钮',
            'Content',
            WPFI.MORE,
            self
        )
        self.prTlBtCard = PrimaryToolButtonCard(
            WPFI.INFO,
            '主题色工具按钮',
            'Content',
            InfoBarIcon.SUCCESS,
            self
        )
        self.trTlBtCard = TransparentToolButtonCard(
            WPFI.EXPLORER,
            '透明工具按钮',
            'Content',
            parent=self
        )
        self.trTlBtCard.setButtonText('确定')
        #######################################################
        self.switchBtCard = SwitchButtonCard(
            WPFI.COLOR_WIFI,
            '状态开关按钮',
            'Content',
            parent=self

        )
        self.checkCard = CheckBoxCard(
            FluentIcon.MAIL,
            '复选框按钮',
            'Content',
            True,
            '同意',
            parent=self
        )
        self.linkBtCard = HyperLinkCard(
            'https://www.bilibili.com',
            WPFI.MUSIC_FOLDER,
            '超链接按钮',
            "Content",
            'BiliBili',
            FluentIcon.VIEW,
            self
        )
        #######################################################
        self.comBoCard = ComboBoxCard(
            WPFI.DROP_DOWN,
            "下拉框",
            'Content',
            self.girls,
            parent=self
        )
        self.edComBoCard = EditComboBoxCard(
            WPFI.SEND,
            '可编辑下拉框',
            'Content',
            self.girls,
            True,
            'Selected',
            self
        )
        self.alcComBtCard = AcrylicComboBoxCard(
            FluentIcon.MOVE,
            '亚力克下拉框',
            'Content',
            self.girls,
            True,
            '',
            self
        )
        self.alcEditComBtCard = AcrylicEditComboBoxCard(
            FluentIcon.CUT,
            '亚力克可编辑下拉框',
            'Content',
            self.girls,
            parent=self
        )
        self.dnCard = DropDownCard(
            WPFI.SETTING,
            '下拉按钮卡片',
            "Content",
            '更多',
            FluentIcon.MORE,
            ['复制', '粘贴', '撤销'],
            [FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.RETURN],
            parent=self
        )
        self.dnCard.button.setMenu(self.dnCard.menu)
        self.prDnCard = PrimaryDropDownCard(
            FluentIcon.MAIL,
            '主题色下拉按钮卡片',
            'Content',
            btIcon=WPFI.XIN_HAO,
            menuTexts=['复制', '粘贴', '撤销'],
            menuIcons=[FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.RETURN],
            triggered=[lambda: print('复制'), lambda: print('粘贴'), lambda: print('撤销')],
            parent=self
        )
        self.trDnCard = TransparentDropDownCard(
            FluentIcon.CARE_LEFT_SOLID,
            '透明下拉按钮卡片',
            'Content',
            '发送',
            WPFI.SEND,
            ['复制', '粘贴', '撤销'],
            [FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.RETURN],
            [lambda: print('复制'), lambda: print('粘贴'), lambda: print('撤销')],
            self
        )
        self.dnTlCard = DropDownToolCard(
            FluentIcon.QRCODE,
            '下拉工具按钮卡片',
            'Content',
            FluentIcon.MORE,
            ['复制', '粘贴', '撤销'],
            [FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.RETURN],
            parent=self
        )
        self.prDnTlCard = PrimaryDropDownToolCard(
            FluentIcon.GITHUB,
            '主题色下拉工具按钮卡片',
            'Content',
            FluentIcon.MORE,
            ['复制', '粘贴', '撤销'],
            [FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.RETURN],
            [lambda: print('复制'), lambda: print('粘贴'), lambda: print('撤销')],
            self
        )
        self.prDnTlCard.setButtonIcon()
        self.trDnTlCard = TransparentDropDownToolCard(
            WPFI.XIN_HAO,
            '透明下拉工具按钮卡片',
            "Content",
            FluentIcon.MORE,
            ['复制', '粘贴', '撤销'],
            [FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.RETURN],
            [lambda: print('复制'), lambda: print('粘贴'), lambda: print('撤销')],
            self
        )
        self.spCard = SplitCard(
            WSFI.MENU,
            '拆分下拉按钮',
            "Content",
            '确定',
            FluentIcon.MORE,
            ['复制', '粘贴', '撤销'],
            [FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.RETURN],
            [lambda: print('复制'), lambda: print('粘贴'), lambda: print('撤销')],
            self
        )
        self.prSpCard = PrimarySplitCard(
            FluentIcon.MAIL,
            '主题色拆分下拉按钮',
            "Content",
            '确定',
            FluentIcon.MORE,
            ['复制', '粘贴', '撤销'],
            [FluentIcon.COPY, FluentIcon.PASTE, FluentIcon.RETURN],
            [lambda: print('复制'), lambda: print('粘贴'), lambda: print('撤销')],
            self
        )
        self.sliderCard = SliderCard(
            FluentIcon.VOLUME,
            '滑动条卡片',
            'Content',
            (0.1, 114.5),
            24.7,
            parent=self
        )
        self.optionsCard = OptionsCard(
            FluentIcon.POWER_BUTTON,
            '电源选项',
            '设置当前电源模式',
            ['省电模式', '正常模式', '性能模式'],
            '正常模式',
            self
        )
        self.optionsCard.optionChanged.connect(
            lambda options: print(options.value)
        )
        self.fls = FolderListCard(
            "Folders",
            "Selected Folder",
            "/root",
            self,
            WPFI.DOWNLOAD_FOLDER,
            WPFI.FOLDER
        )

    def initExpandCard(self):
        self.expandCard.addGroupWidgets([
            SliderCard(FluentIcon.VOLUME, '音量', '设置当前音量', (0, 1145), 114, parent=self),
            ComboBoxCard(FluentIcon.REMOVE, "ComboBoxCard", 'Content', self.girls, parent=self),
        ])
        self.expandCard.addPrimaryButtonCard('AddPrimaryButton', FluentIcon.GITHUB, '确定')
        self.expandCard.addButtonCard("AddButton", FluentIcon.HOME, '确定', self)

    def connectSignalSlots(self):
        self.btCard.button.clicked.connect(
            lambda: Dialog('弹出窗口', 'This is View', self).exec()
        )
        self.prBtCard.button.clicked.connect(
            lambda: UrlDialog(self).exec()
        )
        self.trBtCard.button.clicked.connect(
            lambda: MessageBox("弹出窗口", '带遮罩的窗口', self).exec()
        )
        ######################################
        self.tlBtCard.button.clicked.connect(
            lambda: print(ColorDialog(QColor(255, 255, 255), "Title", self).getColor())
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(1200, 700)
    setTheme(Theme.AUTO)
    window.show()
    sys.exit(app.exec())
