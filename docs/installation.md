# Installation

This guide covers how to install the Advanced Layer Renamer plugin in QGIS.

## Method 1: QGIS Plugin Manager (Recommended)

The easiest way to install the plugin is through the QGIS Plugin Manager.

### Steps

1. Open QGIS
2. Go to **Plugins** > **Manage and Install Plugins...**
3. Click on the **All** tab
4. Search for `Advanced Layer Renamer`
5. Click **Install Plugin**

!!! success "Done!"
    The plugin is now installed and ready to use. You'll find it in the **Plugins** menu.

---

## Method 2: Manual Installation

If the plugin is not available in the repository or you want to install a development version:

### Steps

1. Download the plugin ZIP file from the [GitHub releases page](https://github.com/raymukesh/advanced_layer_renamer/releases)

2. Open QGIS and go to **Plugins** > **Manage and Install Plugins...**

3. Click on **Install from ZIP**

4. Browse to the downloaded ZIP file and click **Install Plugin**

!!! tip "Alternative: Direct Folder Installation"
    You can also extract the ZIP file directly to your QGIS plugins folder:

    === "Windows"
        ```
        C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
        ```

    === "macOS"
        ```
        ~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/
        ```

    === "Linux"
        ```
        ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
        ```

---

## Method 3: From Source (Development)

For developers who want to contribute or modify the plugin:

### Prerequisites

- Git installed on your system
- QGIS 3.0 or higher

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/raymukesh/advanced_layer_renamer.git
   ```

2. Create a symbolic link or copy the folder to your QGIS plugins directory

3. Restart QGIS

4. Enable the plugin in **Plugins** > **Manage and Install Plugins...**

---

## Enabling the Plugin

After installation, make sure the plugin is enabled:

1. Go to **Plugins** > **Manage and Install Plugins...**
2. Click on the **Installed** tab
3. Find **Advanced Layer Renamer** in the list
4. Check the box next to it to enable

---

## Verifying Installation

To verify the plugin is installed correctly:

1. Look for **Advanced Layer Renamer** in the **Plugins** menu
2. You should also see a new icon in the toolbar

!!! note "Toolbar Icon"
    If you don't see the toolbar icon, right-click on the toolbar area and ensure **Plugins Toolbar** is checked.

---

## Updating the Plugin

### Via Plugin Manager

1. Go to **Plugins** > **Manage and Install Plugins...**
2. Click on the **Upgradeable** tab
3. If an update is available, select the plugin and click **Upgrade Plugin**

### Manual Update

1. Download the latest version
2. Uninstall the current version (optional but recommended)
3. Install the new version using any of the methods above

---

## Uninstalling

To remove the plugin:

1. Go to **Plugins** > **Manage and Install Plugins...**
2. Click on the **Installed** tab
3. Select **Advanced Layer Renamer**
4. Click **Uninstall Plugin**

---

## Troubleshooting

### Plugin not appearing after installation

- Restart QGIS
- Check if the plugin is enabled in the Plugin Manager
- Verify the plugin folder is in the correct location

### Error messages on startup

- Check the QGIS Python console for error details
- Ensure you have QGIS 3.0 or higher
- Try reinstalling the plugin

### Need more help?

[:material-github: Open an Issue](https://github.com/raymukesh/advanced_layer_renamer/issues){ .md-button }
