# Getting Started

This guide will walk you through your first batch rename operation using the Advanced Layer Renamer plugin.

## Opening the Plugin

There are two ways to open the plugin:

1. **Menu:** Go to **Plugins** > **Advanced Layer Renamer**
2. **Toolbar:** Click the plugin icon in the toolbar

---

## The Interface

When you open the plugin, you'll see a dialog with three main tabs:

### Main Tab

The primary workspace divided into two resizable panels:

| Panel | Description |
|-------|-------------|
| **Left Panel** | Layer selection with Refresh, Select All, Select None, and Invert buttons |
| **Right Panel** | Renaming options and live preview |

### Templates Tab

Save and manage your renaming configurations for reuse.

### Validation Tab

Check layer names for potential issues before renaming.

---

## Your First Rename

Let's walk through a simple example: adding a prefix to all layers.

### Step 1: Select Layers

1. Open a QGIS project with some layers
2. Open the plugin
3. Your layers will appear in the left panel
4. Click **Select All** or manually select the layers you want to rename

!!! tip
    Use ++ctrl++ + click to select multiple individual layers, or ++shift++ + click to select a range.

### Step 2: Configure Options

1. In the **Basic Options** section, find the **Prefix** field
2. Enter your desired prefix, e.g., `Project_`

### Step 3: Preview Changes

The preview table updates automatically as you type! You'll see:

| Column | Description |
|--------|-------------|
| **Original Name** | The current layer name |
| **New Name** | What the name will become |
| **Status** | "Will Change" (green) or "No Change" (gray) |

### Step 4: Apply Changes

1. Review the preview to make sure everything looks correct
2. Click **Rename Layers**
3. A summary dialog will show how many layers were renamed

!!! success "Congratulations!"
    You've completed your first batch rename!

---

## Common Workflows

### Adding Sequential Numbers

1. In **Numbering Options**, select **Leading zeros**
2. Choose the number of digits from the dropdown (e.g., "2" for 001, 002...)
3. The numbers will be added as prefixes

**Example Result:**
```
Layer A  →  01_Layer A
Layer B  →  02_Layer B
Layer C  →  03_Layer C
```

### Find and Replace

1. In **Basic Options**, enter text in the **Find** field
2. Enter replacement text in the **Replace** field
3. Check **Use Regular Expressions** for pattern matching

**Example:** Replace all underscores with spaces
```
Find:    _
Replace: (space)

my_layer_name  →  my layer name
```

### Cleaning Up Names

1. In **Advanced Options**, check **Remove special characters**
2. Check **Clean extra whitespace**

This will:

- Remove characters like `< > : " / \ | ? *`
- Keep letters, numbers, spaces, underscores, dashes, and dots
- Collapse multiple spaces into single spaces

---

## Interface Tips

### Resizable Panels

Drag the divider between the left and right panels to resize them according to your preference.

### Resizable Columns

Drag the column headers in the preview table to adjust column widths.

### Real-time Preview

All options update the preview automatically - no need to click a button!

### Refresh Layers

If you add or remove layers in QGIS while the plugin is open, click **Refresh** to update the layer list.

---

## Next Steps

Now that you know the basics, explore more features:

- [Complete Feature Guide](features.md) - Learn about all available options
- [Using Templates](templates.md) - Save and reuse your configurations
- [Validation Tools](validation.md) - Check for naming issues

---

## Quick Reference

| Action | How To |
|--------|--------|
| Select all layers | Click **Select All** button |
| Deselect all | Click **Select None** button |
| Invert selection | Click **Invert** button |
| Refresh layer list | Click **Refresh** button |
| Preview changes | Automatic - just configure options |
| Apply changes | Click **Rename Layers** button |
| Get help | Click **Help** button |
