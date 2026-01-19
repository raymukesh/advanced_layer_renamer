from qgis.PyQt.QtCore import Qt, QDateTime, QTimer
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QListWidget, QListWidgetItem, QLineEdit, QLabel, QGroupBox,
    QCheckBox, QMessageBox, QRadioButton, QButtonGroup, QTabWidget,
    QTextEdit, QComboBox, QSpinBox, QFileDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame, QScrollArea,
    QProgressBar, QApplication, QWidget, QAbstractItemView,
    QInputDialog, QTextBrowser, QDialogButtonBox, QSplitter
)
from qgis.PyQt.QtGui import QFont, QColor, QPalette
from qgis.core import QgsProject, QgsMapLayer
import re
import os
import json
from datetime import datetime
import webbrowser

class BatchRenameDialog(QDialog):
    def __init__(self, iface):
        super().__init__(None)
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__) if __file__ else ""
        self.presets_file = os.path.join(self.plugin_dir, 'presets.json') if self.plugin_dir else 'presets.json'
        self.history_file = os.path.join(self.plugin_dir, 'history.json') if self.plugin_dir else 'history.json'
        self.setupUi()
        self.populateLayers()
        self.loadPresets()
        self.setModal(False)
        
    def setupUi(self):
        self.setWindowTitle('Advanced Layer Renamer')
        self.setMinimumSize(1000, 700)
        self.resize(1100, 750)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Tab widget for organized sections
        tab_widget = QTabWidget()
        
        # Main renaming tab
        main_tab = self.create_main_tab()
        tab_widget.addTab(main_tab, "🔧 Main")
        
        # Templates tab
        templates_tab = self.create_templates_tab()
        tab_widget.addTab(templates_tab, "💾 Templates")
        
        # Validation tab
        validation_tab = self.create_validation_tab()
        tab_widget.addTab(validation_tab, "✅ Validation")
        
        main_layout.addWidget(tab_widget)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        # Help button
        help_btn = QPushButton("❓ Help")
        help_btn.clicked.connect(self.show_help)
        help_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3; 
                color: white; 
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        self.preview_btn = QPushButton("🔍 Preview Changes")
        self.preview_btn.clicked.connect(self.preview_changes)
        self.rename_btn = QPushButton("✅ Rename Layers")
        self.rename_btn.clicked.connect(self.rename_layers)
        self.rename_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.clicked.connect(self.close)
        
        button_layout.addWidget(help_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.preview_btn)
        button_layout.addWidget(self.rename_btn)
        button_layout.addWidget(cancel_btn)
        
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        
    def create_main_tab(self):
        """Create the main renaming interface"""
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # Style for bold group box titles
        groupbox_style = "QGroupBox { font-weight: bold; }"

        # Main splitter for resizable left/right panels
        main_splitter = QSplitter(Qt.Horizontal)

        # Left panel - Layers and controls
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setFrameStyle(QFrame.StyledPanel)
        
        # Layers section
        layers_group = QGroupBox("🎯 Available Layers")
        layers_group.setStyleSheet(groupbox_style)
        layers_layout = QVBoxLayout()
        
        # Layer selection controls
        select_layout = QHBoxLayout()
        self.refresh_layers_btn = QPushButton("🔄 Refresh")
        self.select_all_btn = QPushButton("✓ Select All")
        self.select_none_btn = QPushButton("✗ Select None")
        self.invert_selection_btn = QPushButton("⇄ Invert")

        self.refresh_layers_btn.clicked.connect(self.populateLayers)
        self.select_all_btn.clicked.connect(self.select_all_layers)
        self.select_none_btn.clicked.connect(self.select_no_layers)
        self.invert_selection_btn.clicked.connect(self.invert_selection)

        select_layout.addWidget(self.refresh_layers_btn)
        select_layout.addWidget(self.select_all_btn)
        select_layout.addWidget(self.select_none_btn)
        select_layout.addWidget(self.invert_selection_btn)
        select_layout.addStretch()
        layers_layout.addLayout(select_layout)
        
        # Layers list with alternating colors
        self.layers_list = QListWidget()
        self.layers_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.layers_list.setAlternatingRowColors(True)
        self.layers_list.itemSelectionChanged.connect(self.update_preview)
        layers_layout.addWidget(self.layers_list)
        layers_group.setLayout(layers_layout)
        left_layout.addWidget(layers_group)
        
        # Right panel - Options and preview
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_panel.setFrameStyle(QFrame.StyledPanel)
        
        # Options scroll area
        options_scroll = QScrollArea()
        options_scroll.setWidgetResizable(True)
        options_widget = QWidget()
        options_layout = QVBoxLayout(options_widget)
        
        # Numbering options
        numbering_group = QGroupBox("🔢 Numbering Options")
        numbering_group.setStyleSheet(groupbox_style)
        numbering_layout = QVBoxLayout()

        self.numbering_group = QButtonGroup()
        self.no_numbering_radio = QRadioButton("No numbering")
        self.sequential_radio = QRadioButton("Sequential (1, 2, 3...)")
        self.leading_zero_radio = QRadioButton("Leading zeros")

        self.numbering_group.addButton(self.no_numbering_radio)
        self.numbering_group.addButton(self.sequential_radio)
        self.numbering_group.addButton(self.leading_zero_radio)

        self.no_numbering_radio.setChecked(True)

        # Leading zeros count dropdown
        self.leading_zeros_combo = QComboBox()
        self.leading_zeros_combo.addItems(["1 (01, 02...)", "2 (001, 002...)", "3 (0001, 0002...)", "4 (00001, 00002...)", "5 (000001, 000002...)"])
        self.leading_zeros_combo.setEnabled(False)
        self.leading_zeros_combo.setFixedWidth(150)

        # Layout for leading zeros radio + combo
        leading_zero_layout = QHBoxLayout()
        leading_zero_layout.addWidget(self.leading_zero_radio)
        leading_zero_layout.addWidget(self.leading_zeros_combo)
        leading_zero_layout.addStretch()

        # Connect radio buttons to update preview and enable/disable combo
        self.no_numbering_radio.toggled.connect(self.update_preview)
        self.sequential_radio.toggled.connect(self.update_preview)
        self.leading_zero_radio.toggled.connect(self.update_preview)
        self.leading_zero_radio.toggled.connect(lambda checked: self.leading_zeros_combo.setEnabled(checked))
        self.leading_zeros_combo.currentIndexChanged.connect(self.update_preview)

        numbering_layout.addWidget(self.no_numbering_radio)
        numbering_layout.addWidget(self.sequential_radio)
        numbering_layout.addLayout(leading_zero_layout)
        numbering_group.setLayout(numbering_layout)
        options_layout.addWidget(numbering_group)
        
        # Basic renaming options
        basic_group = QGroupBox("📝 Basic Options")
        basic_group.setStyleSheet(groupbox_style)
        basic_layout = QGridLayout()

        # Prefix/Suffix
        basic_layout.addWidget(QLabel("Prefix:"), 0, 0)
        self.prefix_edit = QLineEdit()
        self.prefix_edit.setPlaceholderText("Enter prefix...")
        self.prefix_edit.textChanged.connect(self.update_preview)
        basic_layout.addWidget(self.prefix_edit, 0, 1)

        basic_layout.addWidget(QLabel("Suffix:"), 0, 2)
        self.suffix_edit = QLineEdit()
        self.suffix_edit.setPlaceholderText("Enter suffix...")
        self.suffix_edit.textChanged.connect(self.update_preview)
        basic_layout.addWidget(self.suffix_edit, 0, 3)

        # Find/Replace
        basic_layout.addWidget(QLabel("Find:"), 1, 0)
        self.find_pattern = QLineEdit()
        self.find_pattern.setPlaceholderText("Text to find...")
        self.find_pattern.textChanged.connect(self.update_preview)
        basic_layout.addWidget(self.find_pattern, 1, 1)

        basic_layout.addWidget(QLabel("Replace:"), 1, 2)
        self.replace_pattern = QLineEdit()
        self.replace_pattern.setPlaceholderText("Replacement text...")
        self.replace_pattern.textChanged.connect(self.update_preview)
        basic_layout.addWidget(self.replace_pattern, 1, 3)

        # Regex checkbox
        self.regex_check = QCheckBox("Use Regular Expressions")
        self.regex_check.toggled.connect(self.update_preview)
        basic_layout.addWidget(self.regex_check, 2, 0, 1, 2)

        # Case conversion
        case_layout = QHBoxLayout()
        self.uppercase_check = QCheckBox("UPPERCASE")
        self.lowercase_check = QCheckBox("lowercase")
        self.title_case_check = QCheckBox("Title Case")
        self.capitalized_check = QCheckBox("Capitalized")

        # Make case checkboxes mutually exclusive and connect to preview
        self.uppercase_check.toggled.connect(self.case_exclusive)
        self.lowercase_check.toggled.connect(self.case_exclusive)
        self.title_case_check.toggled.connect(self.case_exclusive)
        self.capitalized_check.toggled.connect(self.case_exclusive)
        self.uppercase_check.toggled.connect(self.update_preview)
        self.lowercase_check.toggled.connect(self.update_preview)
        self.title_case_check.toggled.connect(self.update_preview)
        self.capitalized_check.toggled.connect(self.update_preview)

        case_layout.addWidget(QLabel("Case:"))
        case_layout.addWidget(self.uppercase_check)
        case_layout.addWidget(self.lowercase_check)
        case_layout.addWidget(self.title_case_check)
        case_layout.addWidget(self.capitalized_check)
        case_layout.addStretch()
        basic_layout.addLayout(case_layout, 3, 0, 1, 4)

        basic_group.setLayout(basic_layout)
        options_layout.addWidget(basic_group)
        
        # Advanced options
        advanced_group = QGroupBox("⚙️ Advanced Options")
        advanced_group.setStyleSheet(groupbox_style)
        advanced_layout = QVBoxLayout()

        # Date stamping
        date_layout = QHBoxLayout()
        self.date_stamp = QCheckBox("Add date stamp")
        self.date_format_combo = QComboBox()
        self.date_format_combo.addItems(["YYYYMMDD", "YYYY-MM-DD", "DD-MM-YYYY"])
        self.date_format_combo.setEnabled(False)
        self.date_stamp.toggled.connect(lambda checked: self.date_format_combo.setEnabled(checked))
        self.date_stamp.toggled.connect(self.update_preview)
        self.date_format_combo.currentIndexChanged.connect(self.update_preview)
        date_layout.addWidget(self.date_stamp)
        date_layout.addWidget(self.date_format_combo)
        date_layout.addStretch()

        # Remove special chars
        self.remove_special_chars = QCheckBox("Remove special characters (keeps letters, numbers, space, _ - .)")
        self.remove_special_chars.toggled.connect(self.update_preview)

        # Clean whitespace
        self.clean_whitespace = QCheckBox("Clean extra whitespace")
        self.clean_whitespace.toggled.connect(self.update_preview)

        advanced_layout.addWidget(self.date_stamp)
        advanced_layout.addWidget(self.date_format_combo)
        advanced_layout.addWidget(self.remove_special_chars)
        advanced_layout.addWidget(self.clean_whitespace)

        advanced_group.setLayout(advanced_layout)
        options_layout.addWidget(advanced_group)
        
        # Test regex button
        test_regex_btn = QPushButton("🧪 Test Regex Pattern")
        test_regex_btn.clicked.connect(self.test_regex)
        options_layout.addWidget(test_regex_btn)
        
        options_layout.addStretch()
        options_scroll.setWidget(options_widget)
        right_layout.addWidget(options_scroll)
        
        # Preview section
        preview_group = QGroupBox("👁️ Preview Changes")
        preview_group.setStyleSheet(groupbox_style)
        preview_layout = QVBoxLayout()

        self.preview_table = QTableWidget(0, 3)
        self.preview_table.setHorizontalHeaderLabels(['Original Name', 'New Name', 'Status'])
        self.preview_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.preview_table.setAlternatingRowColors(True)
        # Make columns resizable by dragging
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.preview_table.horizontalHeader().setStretchLastSection(True)
        preview_layout.addWidget(self.preview_table)

        preview_group.setLayout(preview_layout)
        right_layout.addWidget(preview_group)

        # Add panels to splitter for resizable layout
        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([350, 750])  # Initial sizes

        layout.addWidget(main_splitter)

        return widget
        
    def create_templates_tab(self):
        """Create templates management interface"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Style for bold group box titles
        groupbox_style = "QGroupBox { font-weight: bold; }"

        # Template management
        template_group = QGroupBox("💾 Template Management")
        template_group.setStyleSheet(groupbox_style)
        template_layout = QVBoxLayout()
        
        # Template list
        self.template_list = QListWidget()
        self.template_list.setAlternatingRowColors(True)
        template_layout.addWidget(QLabel("Saved Templates:"))
        template_layout.addWidget(self.template_list)
        
        # Template controls
        template_btn_layout = QHBoxLayout()
        self.save_template_btn = QPushButton("💾 Save Current Settings")
        self.load_template_btn = QPushButton("📂 Load Selected Template")
        self.delete_template_btn = QPushButton("🗑️ Delete Template")
        
        self.save_template_btn.clicked.connect(self.save_current_template)
        self.load_template_btn.clicked.connect(self.load_selected_template)
        self.delete_template_btn.clicked.connect(self.delete_template)
        
        template_btn_layout.addWidget(self.save_template_btn)
        template_btn_layout.addWidget(self.load_template_btn)
        template_btn_layout.addWidget(self.delete_template_btn)
        template_layout.addLayout(template_btn_layout)
        
        # Quick templates
        quick_group = QGroupBox("⚡ Quick Templates")
        quick_group.setStyleSheet(groupbox_style)
        quick_layout = QVBoxLayout()
        
        quick_btn_layout = QHBoxLayout()
        self.template_date_prefix = QPushButton("📅 Date Prefix")
        self.template_clean_names = QPushButton("🧹 Clean Names")
        self.template_project_standard = QPushButton("📋 Project Standard")
        
        self.template_date_prefix.clicked.connect(self.apply_date_prefix_template)
        self.template_clean_names.clicked.connect(self.apply_clean_names_template)
        self.template_project_standard.clicked.connect(self.apply_project_standard_template)
        
        quick_btn_layout.addWidget(self.template_date_prefix)
        quick_btn_layout.addWidget(self.template_clean_names)
        quick_btn_layout.addWidget(self.template_project_standard)
        quick_btn_layout.addStretch()
        
        quick_layout.addLayout(quick_btn_layout)
        quick_layout.addWidget(QLabel("Apply common naming conventions quickly"))
        
        quick_group.setLayout(quick_layout)
        template_layout.addWidget(quick_group)
        
        template_group.setLayout(template_layout)
        layout.addWidget(template_group)
        layout.addStretch()
        
        return widget
        
    def create_validation_tab(self):
        """Create validation interface"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Style for bold group box titles
        groupbox_style = "QGroupBox { font-weight: bold; }"

        # Validation controls
        validation_group = QGroupBox("🔍 Validation Tools")
        validation_group.setStyleSheet(groupbox_style)
        validation_layout = QVBoxLayout()
        
        # Validate button
        validate_btn = QPushButton("🔍 Validate Selected Layers")
        validate_btn.clicked.connect(self.validate_layers)
        validation_layout.addWidget(validate_btn)
        
        # Validation results
        self.validation_results = QTextEdit()
        self.validation_results.setReadOnly(True)
        validation_layout.addWidget(QLabel("Validation Results:"))
        validation_layout.addWidget(self.validation_results)
        
        validation_group.setLayout(validation_layout)
        layout.addWidget(validation_group)
        
        # Common issues group
        issues_group = QGroupBox("⚠️ Common Issues")
        issues_group.setStyleSheet(groupbox_style)
        issues_layout = QVBoxLayout()
        
        issues_text = """
Common Naming Issues to Check:
• Invalid characters: < > : " / \\ | ? *
• Names starting/ending with spaces
• Very long names (>255 characters)
• Duplicate names
• Empty names
• Names with only numbers
• Special characters in file paths
        """
        
        issues_label = QLabel(issues_text)
        issues_label.setFont(QFont("Arial", 9))
        issues_layout.addWidget(issues_label)
        
        issues_group.setLayout(issues_layout)
        layout.addWidget(issues_group)
        layout.addStretch()
        
        return widget
        
    def show_help(self):
        """Show help by opening external documentation"""
        help_file = os.path.join(self.plugin_dir, 'help.html')
        if os.path.exists(help_file):
            try:
                webbrowser.open('file://' + help_file)
            except Exception as e:
                QMessageBox.warning(self, "Help Error", f"Could not open help file: {str(e)}")
        else:
            # Fallback to simple help message
            help_text = """
<b>Advanced Layer Renamer Help</b>

<h3>Quick Start:</h3>
1. Select layers to rename
2. Configure renaming options
3. Preview changes
4. Rename layers

<h3>Main Features:</h3>
• Numbering (sequential, leading zeros)
• Prefix/Suffix addition
• Find/Replace text
• Case conversion (UPPERCASE, lowercase, etc.)
• Date stamping
• Special character removal
• Template saving/loading

<h3>Tips:</h3>
• Always preview before renaming
• Use templates for consistent naming
• Validate names for potential issues
"""
            QMessageBox.information(self, "Help", help_text)
        
    # Rest of the methods remain the same...
    # [Include all the existing methods from the previous implementation]
    
    def case_exclusive(self):
        """Make case checkboxes mutually exclusive"""
        sender = self.sender()
        if sender.isChecked():
            if sender == self.uppercase_check:
                self.lowercase_check.setChecked(False)
                self.title_case_check.setChecked(False)
                self.capitalized_check.setChecked(False)
            elif sender == self.lowercase_check:
                self.uppercase_check.setChecked(False)
                self.title_case_check.setChecked(False)
                self.capitalized_check.setChecked(False)
            elif sender == self.title_case_check:
                self.uppercase_check.setChecked(False)
                self.lowercase_check.setChecked(False)
                self.capitalized_check.setChecked(False)
            elif sender == self.capitalized_check:
                self.uppercase_check.setChecked(False)
                self.lowercase_check.setChecked(False)
                self.title_case_check.setChecked(False)
    
    def select_all_layers(self):
        """Select all layers"""
        for i in range(self.layers_list.count()):
            self.layers_list.item(i).setSelected(True)
        self.update_preview()
    
    def select_no_layers(self):
        """Deselect all layers"""
        for i in range(self.layers_list.count()):
            self.layers_list.item(i).setSelected(False)
        self.update_preview()
    
    def invert_selection(self):
        """Invert layer selection"""
        for i in range(self.layers_list.count()):
            item = self.layers_list.item(i)
            item.setSelected(not item.isSelected())
        self.update_preview()
    
    def populateLayers(self):
        """Populate the layers list with current project layers"""
        self.layers_list.clear()
        layers = QgsProject.instance().mapLayers()
        
        # Sort layers by name
        sorted_layers = sorted(layers.items(), key=lambda x: x[1].name().lower())
        
        for layer_id, layer in sorted_layers:
            item = QListWidgetItem(f"{layer.name()}")
            item.setData(Qt.UserRole, layer_id)
                
            self.layers_list.addItem(item)
        
        # Select all by default
        self.select_all_layers()
        self.update_preview()
        
        # Populate templates
        self.loadPresets()
    
    def get_selected_layers(self):
        """Get selected layer IDs"""
        selected_items = self.layers_list.selectedItems()
        if not selected_items:
            # Return all layers if none selected
            return [self.layers_list.item(i).data(Qt.UserRole) 
                   for i in range(self.layers_list.count())]
        return [item.data(Qt.UserRole) for item in selected_items]
    
    def generate_new_name(self, original_name, index=None):
        """Generate new name based on all options"""
        new_name = original_name
        
        # Apply find/replace with regex support
        if self.find_pattern.text():
            try:
                if self.regex_check.isChecked():
                    new_name = re.sub(self.find_pattern.text(), self.replace_pattern.text(), new_name)
                else:
                    new_name = new_name.replace(self.find_pattern.text(), self.replace_pattern.text())
            except re.error:
                # If regex is invalid, treat as plain text
                new_name = new_name.replace(self.find_pattern.text(), self.replace_pattern.text())
        
        # Remove special characters if requested (keep only letters, numbers, space, underscore, dash, dot)
        if self.remove_special_chars.isChecked():
            new_name = re.sub(r'[^a-zA-Z0-9\s_.\-]', '', new_name)
        
        # Clean whitespace if requested
        if self.clean_whitespace.isChecked():
            new_name = ' '.join(new_name.split())
        
        # Add numbering if requested
        if index is not None and not self.no_numbering_radio.isChecked():
            if self.sequential_radio.isChecked():
                number_str = str(index)
            elif self.leading_zero_radio.isChecked():
                # Get number of digits from combo box (index 0 = 2 digits, index 1 = 3 digits, etc.)
                digits_needed = self.leading_zeros_combo.currentIndex() + 2
                number_str = str(index).zfill(digits_needed)
            else:
                number_str = str(index)

            # Add number to the beginning
            new_name = f"{number_str}_{new_name}"
        
        # Add date stamp if requested
        if self.date_stamp.isChecked():
            date_formats = {
                "YYYYMMDD": "%Y%m%d",
                "YYYY-MM-DD": "%Y-%m-%d",
                "DD-MM-YYYY": "%d-%m-%Y"
            }
            date_format = date_formats.get(self.date_format_combo.currentText(), "%Y%m%d")
            date_str = datetime.now().strftime(date_format)
            new_name = f"{date_str}_{new_name}"
        
        # Add prefix/suffix
        prefix = self.prefix_edit.text()
        suffix = self.suffix_edit.text()
        
        if prefix:
            new_name = prefix + new_name
        if suffix:
            new_name = new_name + suffix
            
        # Apply case conversion
        if self.uppercase_check.isChecked():
            new_name = new_name.upper()
        elif self.lowercase_check.isChecked():
            new_name = new_name.lower()
        elif self.title_case_check.isChecked():
            new_name = new_name.title()
        elif self.capitalized_check.isChecked():
            new_name = new_name.capitalize()
            
        return new_name
    
    def update_preview(self):
        """Update the preview table"""
        self.preview_table.setRowCount(0)
        
        layers_to_process = self.get_selected_layers()
        project = QgsProject.instance()
        
        row = 0
        for i, layer_id in enumerate(layers_to_process, 1):
            layer = project.mapLayer(layer_id)
            if layer:
                original_name = layer.name()
                new_name = self.generate_new_name(original_name, i if not self.no_numbering_radio.isChecked() else None)
                
                self.preview_table.insertRow(row)
                
                # Original name
                orig_item = QTableWidgetItem(original_name)
                self.preview_table.setItem(row, 0, orig_item)
                
                # New name
                new_item = QTableWidgetItem(new_name)
                if new_name == original_name:
                    new_item.setBackground(QColor(245, 245, 245))
                    status = "No Change"
                else:
                    new_item.setBackground(QColor(220, 255, 220))
                    status = "Will Change"
                self.preview_table.setItem(row, 1, new_item)
                
                # Status
                status_item = QTableWidgetItem(status)
                if status == "No Change":
                    status_item.setBackground(QColor(245, 245, 245))
                else:
                    status_item.setBackground(QColor(200, 255, 200))
                self.preview_table.setItem(row, 2, status_item)
                
                row += 1
    
    def preview_changes(self):
        """Show preview of name changes"""
        try:
            self.update_preview()
            QMessageBox.information(self, "Preview", "Preview updated in the table below")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating preview: {str(e)}")
    
    def rename_layers(self):
        """Perform the actual renaming"""
        try:
            layers_to_rename = self.get_selected_layers()
            if not layers_to_rename:
                QMessageBox.warning(self, "Warning", "No layers selected")
                return
                
            self.progress_bar.setVisible(True)
            self.progress_bar.setMaximum(len(layers_to_rename))
            self.progress_bar.setValue(0)
            
            renamed_count = 0
            unchanged_count = 0
            error_count = 0
            project = QgsProject.instance()
            
            for i, layer_id in enumerate(layers_to_rename, 1):
                QApplication.processEvents()  # Keep UI responsive
                self.progress_bar.setValue(i)
                
                try:
                    layer = project.mapLayer(layer_id)
                    if layer:
                        old_name = layer.name()
                        new_name = self.generate_new_name(old_name, i if not self.no_numbering_radio.isChecked() else None)
                        
                        if new_name != old_name:
                            layer.setName(new_name)
                            renamed_count += 1
                        else:
                            unchanged_count += 1
                except Exception as e:
                    error_count += 1
                    continue
            
            self.progress_bar.setVisible(False)
            
            # Show results summary
            message = f"Renaming completed!\n\n"
            message += f"✅ Successfully renamed: {renamed_count} layers\n"
            if unchanged_count > 0:
                message += f"➖ No changes needed: {unchanged_count} layers\n"
            if error_count > 0:
                message += f"❌ Errors: {error_count} layers\n"
            
            QMessageBox.information(self, "Success", message)
            
            # Refresh the preview
            self.populateLayers()
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            QMessageBox.critical(self, "Error", f"Error renaming layers: {str(e)}")
    
    def test_regex(self):
        """Test regex patterns"""
        try:
            test_string = "sample_layer_name_2023"
            pattern = self.find_pattern.text()
            replacement = self.replace_pattern.text()
            
            if pattern:
                if self.regex_check.isChecked():
                    result = re.sub(pattern, replacement, test_string)
                    QMessageBox.information(self, "Regex Test", 
                                          f"Input: {test_string}\nPattern: {pattern}\nResult: {result}")
                else:
                    result = test_string.replace(pattern, replacement)
                    QMessageBox.information(self, "Find/Replace Test", 
                                          f"Input: {test_string}\nFind: {pattern}\nResult: {result}")
            else:
                QMessageBox.information(self, "Test", "Please enter a pattern to test")
                
        except re.error as e:
            QMessageBox.warning(self, "Regex Error", f"Invalid regex: {str(e)}")
    
    # Template management
    def save_current_template(self):
        """Save current settings as template"""
        template_name, ok = QInputDialog.getText(self, "Save Template", "Template name:")
        if ok and template_name:
            template = {
                'prefix': self.prefix_edit.text(),
                'suffix': self.suffix_edit.text(),
                'find_pattern': self.find_pattern.text(),
                'replace_pattern': self.replace_pattern.text(),
                'use_regex': self.regex_check.isChecked(),
                'numbering_style': 'none' if self.no_numbering_radio.isChecked() else
                                 'sequential' if self.sequential_radio.isChecked() else
                                 'leading_zero',
                'leading_zeros_count': self.leading_zeros_combo.currentIndex(),
                'uppercase': self.uppercase_check.isChecked(),
                'lowercase': self.lowercase_check.isChecked(),
                'title_case': self.title_case_check.isChecked(),
                'capitalized': self.capitalized_check.isChecked(),
                'date_stamp': self.date_stamp.isChecked(),
                'date_format': self.date_format_combo.currentText(),
                'remove_special_chars': self.remove_special_chars.isChecked(),
                'clean_whitespace': self.clean_whitespace.isChecked()
            }
            
            self.save_template(template_name, template)
            QMessageBox.information(self, "Success", f"Template '{template_name}' saved!")
    
    def loadPresets(self):
        """Load saved templates"""
        self.template_list.clear()
        if os.path.exists(self.presets_file):
            try:
                with open(self.presets_file, 'r') as f:
                    presets = json.load(f)
                for name in presets.keys():
                    self.template_list.addItem(name)
            except:
                pass
    
    def save_template(self, name, template):
        """Save a template"""
        presets = {}
        if os.path.exists(self.presets_file):
            try:
                with open(self.presets_file, 'r') as f:
                    presets = json.load(f)
            except:
                pass
        
        presets[name] = template
        
        try:
            with open(self.presets_file, 'w') as f:
                json.dump(presets, f, indent=2)
        except:
            pass
        
        self.loadPresets()
    
    def load_selected_template(self):
        """Load selected template"""
        current_item = self.template_list.currentItem()
        if current_item:
            template_name = current_item.text()
            if os.path.exists(self.presets_file):
                try:
                    with open(self.presets_file, 'r') as f:
                        presets = json.load(f)
                    
                    if template_name in presets:
                        template = presets[template_name]
                        self.apply_template(template)
                        QMessageBox.information(self, "Success", f"Template '{template_name}' loaded!")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not load template: {str(e)}")
    
    def delete_template(self):
        """Delete selected template"""
        current_item = self.template_list.currentItem()
        if current_item:
            template_name = current_item.text()
            reply = QMessageBox.question(self, "Confirm Delete", 
                                       f"Delete template '{template_name}'?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                if os.path.exists(self.presets_file):
                    try:
                        with open(self.presets_file, 'r') as f:
                            presets = json.load(f)
                        
                        if template_name in presets:
                            del presets[template_name]
                            
                            with open(self.presets_file, 'w') as f:
                                json.dump(presets, f, indent=2)
                        
                        self.loadPresets()
                        QMessageBox.information(self, "Success", f"Template '{template_name}' deleted!")
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Could not delete template: {str(e)}")
    
    def apply_template(self, template):
        """Apply template settings to UI"""
        self.prefix_edit.setText(template.get('prefix', ''))
        self.suffix_edit.setText(template.get('suffix', ''))
        self.find_pattern.setText(template.get('find_pattern', ''))
        self.replace_pattern.setText(template.get('replace_pattern', ''))
        self.regex_check.setChecked(template.get('use_regex', False))
        
        # Numbering style
        numbering_style = template.get('numbering_style', 'none')
        if numbering_style == 'none':
            self.no_numbering_radio.setChecked(True)
        elif numbering_style == 'sequential':
            self.sequential_radio.setChecked(True)
        elif numbering_style == 'leading_zero':
            self.leading_zero_radio.setChecked(True)

        # Leading zeros count
        leading_zeros_count = template.get('leading_zeros_count', 0)
        self.leading_zeros_combo.setCurrentIndex(leading_zeros_count)

        self.uppercase_check.setChecked(template.get('uppercase', False))
        self.lowercase_check.setChecked(template.get('lowercase', False))
        self.title_case_check.setChecked(template.get('title_case', False))
        self.capitalized_check.setChecked(template.get('capitalized', False))
        self.date_stamp.setChecked(template.get('date_stamp', False))
        
        # Date format
        date_format = template.get('date_format', 'YYYYMMDD')
        index = self.date_format_combo.findText(date_format)
        if index >= 0:
            self.date_format_combo.setCurrentIndex(index)
            
        self.remove_special_chars.setChecked(template.get('remove_special_chars', False))
        self.clean_whitespace.setChecked(template.get('clean_whitespace', False))
    
    # Quick templates
    def apply_date_prefix_template(self):
        """Apply date prefix template"""
        self.date_stamp.setChecked(True)
        self.date_format_combo.setCurrentIndex(0)  # YYYYMMDD
        self.prefix_edit.setText("")
        self.suffix_edit.setText("")
        QMessageBox.information(self, "Template Applied", "Date prefix template applied!")
    
    def apply_clean_names_template(self):
        """Apply clean names template"""
        self.remove_special_chars.setChecked(True)
        self.clean_whitespace.setChecked(True)
        self.no_numbering_radio.setChecked(True)
        QMessageBox.information(self, "Template Applied", "Clean names template applied!")
    
    def apply_project_standard_template(self):
        """Apply project standard template"""
        self.leading_zero_radio.setChecked(True)
        self.clean_whitespace.setChecked(True)
        QMessageBox.information(self, "Template Applied", "Project standard template applied!")
    
    # Validation
    def validate_layers(self):
        """Validate layer names"""
        validation_results = []
        layers_to_check = self.get_selected_layers()
        project = QgsProject.instance()
        
        for layer_id in layers_to_check:
            layer = project.mapLayer(layer_id)
            if layer:
                name = layer.name()
                issues = self.validate_name(name)
                if issues:
                    validation_results.append(f"⚠️ {name}: {', '.join(issues)}")
                else:
                    validation_results.append(f"✅ {name}: Valid")
        
        self.validation_results.setText("\n".join(validation_results))
    
    def validate_name(self, name):
        """Validate a single name"""
        issues = []
        
        # Check for invalid characters
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            if char in name:
                issues.append(f"Invalid character '{char}'")
        
        # Check length
        if len(name) > 255:
            issues.append("Name too long (>255 chars)")
        
        # Check if empty
        if not name.strip():
            issues.append("Empty or whitespace-only name")
        
        # Check for leading/trailing spaces
        if name != name.strip():
            issues.append("Leading/trailing spaces")
        
        return issues
