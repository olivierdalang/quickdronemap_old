from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

try:
    import PIL
except ModuleNotFoundError:
    print("PIL not installed. Trying to auto-install using pip...")
    import pip
    pip.main(['install','pillow'])
    import PIL
    print("Done !")

from .resources import *
from .quick_drone_map_dialog import QuickDroneMapDialog
from .qdm import DroneMap

class QuickDroneMap:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface

        # Create the dialog (after translation) and keep reference
        self.dlg = QuickDroneMapDialog()

        # Declare instance attributes
        self.menu_name = '&Quick Drone Map'
        self.toolbar = self.iface.addToolBar(u'QuickDroneMap')
        self.toolbar.setObjectName(u'QuickDroneMap')


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon = QIcon(':/plugins/quick_drone_map/icon.png')
        self.action = QAction(icon, 'Run Quick Drone Map', self.iface.mainWindow())
        self.action.triggered.connect(self.run)

        self.toolbar.addAction(self.action)

        self.iface.addPluginToMenu(self.menu_name, self.action)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.iface.removePluginMenu(self.menu_name, self.action)
        self.iface.removeToolBarIcon(self.action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        result = self.dlg.exec_()
        
        if result:
            drone_map = DroneMap(self.iface, self.dlg.pathLineEdit.text())
            drone_map.process(
                step_guess_orientation=self.dlg.orientationCheckBox.isChecked(),
                step_advanced_alignement=self.dlg.advancedAlignementCheckBox.isChecked(),
                step_gen_worldfiles=self.dlg.genWorldfileCheckBox.isChecked(),
                step_load_worldfiles=self.dlg.loadWorldFileCheckBox.isChecked(),
                step_gen_vrts=self.dlg.genVRTCheckBox.isChecked(),
                step_load_vrts=self.dlg.loadVRTCheckBox.isChecked(),
                step_load_debug=self.dlg.loadDebugCheckBox.isChecked(),
            )
