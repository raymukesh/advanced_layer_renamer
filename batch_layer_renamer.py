from qgis.PyQt.QtCore import QCoreApplication, Qt
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QInputDialog
from qgis.PyQt.QtGui import QIcon
import os.path
from .batch_rename_dialog import BatchRenameDialog

class BatchLayerRenamer:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.dlg = None
        
    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
        else:
            icon = QIcon()
            
        self.action = QAction(
            icon,
            'Advanced Layer Renamer',
            self.iface.mainWindow()
        )
        self.action.setObjectName('advancedLayerRenamer')
        self.action.setStatusTip('Advanced layer renaming with templates and validation')
        self.action.triggered.connect(self.run)
        
        self.iface.addPluginToMenu('&Advanced Layer Renamer', self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removePluginMenu('&Advanced Layer Renamer', self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        if self.dlg is None:
            self.dlg = BatchRenameDialog(self.iface)

        # Refresh the layer list each time the dialog is opened
        self.dlg.populateLayers()

        self.dlg.show()
        self.dlg.raise_()
        self.dlg.activateWindow()
