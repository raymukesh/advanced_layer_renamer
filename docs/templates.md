# Templates

Templates allow you to save and reuse your renaming configurations. This is especially useful for maintaining consistent naming conventions across projects.

---

## Understanding Templates

A template saves all your current settings, including:

- Prefix and suffix
- Find/replace patterns
- Regex option
- Numbering style and leading zeros count
- Case conversion option
- Date stamping settings
- Special character and whitespace options

---

## Saving a Template

### Steps

1. Configure all your desired renaming options in the **Main** tab
2. Switch to the **Templates** tab
3. Click **Save Current Settings**
4. Enter a descriptive name for your template
5. Click **OK**

!!! tip "Naming Tips"
    Use descriptive names that indicate the purpose:

    - `Project_Standard_Numbering`
    - `Clean_Import_Layers`
    - `Archive_With_Date`

---

## Loading a Template

### Steps

1. Go to the **Templates** tab
2. Select a template from the **Saved Templates** list
3. Click **Load Selected Template**
4. Switch back to the **Main** tab to see the applied settings

!!! note
    Loading a template replaces all current settings with the saved configuration.

---

## Deleting a Template

### Steps

1. Go to the **Templates** tab
2. Select the template you want to remove
3. Click **Delete Template**
4. Confirm the deletion

!!! warning
    Deleted templates cannot be recovered.

---

## Quick Templates

The plugin includes three pre-configured quick templates for common use cases:

### :material-calendar: Date Prefix

Adds the current date as a prefix to layer names.

**Settings Applied:**

- Date stamp: Enabled
- Date format: YYYYMMDD

**Example Result:**
```
Layer_Name  →  20240115_Layer_Name
```

---

### :material-broom: Clean Names

Cleans up messy layer names by removing special characters and extra whitespace.

**Settings Applied:**

- Remove special characters: Enabled
- Clean extra whitespace: Enabled
- Numbering: None

**Example Result:**
```
My   Layer <copy>  →  My Layer copy
```

---

### :material-clipboard-list: Project Standard

Applies a professional numbering scheme with clean whitespace.

**Settings Applied:**

- Numbering: Leading zeros (01, 02...)
- Clean extra whitespace: Enabled

**Example Result:**
```
Layer A  →  01_Layer A
Layer B  →  02_Layer B
```

---

## Template Storage

Templates are stored in a JSON file located in the plugin directory:

```
presets.json
```

### Template File Format

```json
{
  "My Template": {
    "prefix": "Project_",
    "suffix": "",
    "find_pattern": "",
    "replace_pattern": "",
    "use_regex": false,
    "numbering_style": "leading_zero",
    "leading_zeros_count": 0,
    "uppercase": false,
    "lowercase": false,
    "title_case": false,
    "capitalized": false,
    "date_stamp": false,
    "date_format": "YYYYMMDD",
    "remove_special_chars": true,
    "clean_whitespace": true
  }
}
```

---

## Template Workflows

### Workflow 1: Standardizing Imported Data

**Scenario:** You frequently import data with inconsistent naming.

1. Create a template with:
    - Remove special characters: Enabled
    - Clean whitespace: Enabled
    - Case: Title Case
2. Save as `Clean_Imports`
3. Use whenever importing new data

---

### Workflow 2: Project Archiving

**Scenario:** You need to archive project layers with dates.

1. Create a template with:
    - Date stamp: Enabled (YYYY-MM-DD format)
    - Prefix: `Archive_`
    - Leading zeros numbering
2. Save as `Archive_Project`
3. Use when archiving completed projects

---

### Workflow 3: Team Standards

**Scenario:** Your team has specific naming conventions.

1. Create templates matching your team's standards
2. Share the `presets.json` file with team members
3. Everyone uses the same naming conventions

!!! tip "Sharing Templates"
    Copy the `presets.json` file from your plugin directory and share it with colleagues. They can place it in their plugin directory to use the same templates.

---

## Best Practices

### Do

- :material-check: Use descriptive template names
- :material-check: Create templates for recurring tasks
- :material-check: Test templates on a few layers before bulk application
- :material-check: Back up your `presets.json` file

### Don't

- :material-close: Create too many similar templates
- :material-close: Use generic names like "Template 1"
- :material-close: Forget to update templates when conventions change

---

## Troubleshooting

### Template not saving

- Check if you have write permissions to the plugin directory
- Try running QGIS as administrator (Windows)

### Template not loading correctly

- The template file may be corrupted
- Delete the problematic template and recreate it

### Templates missing after update

- Plugin updates may reset the presets file
- Always back up your `presets.json` before updating
