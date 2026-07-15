import configparser
import pathlib
import unittest


PLUGIN_ROOT = pathlib.Path(__file__).resolve().parents[1]


class Qgis4CompatibilityTests(unittest.TestCase):
    def test_metadata_declares_qgis_3_and_4_support(self):
        metadata = configparser.ConfigParser()
        metadata.read(PLUGIN_ROOT / "metadata.txt", encoding="utf-8")

        general = metadata["general"]
        self.assertEqual(general["qgisMinimumVersion"], "3.28")
        self.assertEqual(general["qgisMaximumVersion"], "4.99")
        self.assertNotIn("supportsQt6", general)

    def test_qaction_uses_qtgui(self):
        source = (PLUGIN_ROOT / "batch_layer_renamer.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("from qgis.PyQt.QtGui import QAction, QIcon", source)
        self.assertNotIn("QtWidgets import QAction", source)

    def test_legacy_unscoped_qt_enums_are_absent(self):
        source = (PLUGIN_ROOT / "batch_rename_dialog.py").read_text(
            encoding="utf-8"
        )
        legacy_names = (
            "Qt.Horizontal",
            "Qt.UserRole",
            "QFrame.StyledPanel",
            "QListWidget.ExtendedSelection",
            "QAbstractItemView.NoEditTriggers",
            "QHeaderView.Interactive",
            "QMessageBox.Yes",
            "QMessageBox.No",
        )
        for legacy_name in legacy_names:
            with self.subTest(legacy_name=legacy_name):
                self.assertNotIn(legacy_name, source)

    def test_python_sources_compile(self):
        for source_path in PLUGIN_ROOT.glob("*.py"):
            with self.subTest(source_path=source_path.name):
                compile(
                    source_path.read_text(encoding="utf-8"),
                    str(source_path),
                    "exec",
                )


if __name__ == "__main__":
    unittest.main()
