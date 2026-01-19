# Frequently Asked Questions

Common questions and answers about the Advanced Layer Renamer plugin.

---

## General

### What QGIS versions are supported?

The plugin requires **QGIS 3.0 or higher**. It has been tested on QGIS 3.0 through 3.34.

---

### Does this rename the actual data files?

**No.** This plugin only renames the layers within your QGIS project. The underlying data files (shapefiles, GeoPackages, etc.) are not affected.

To rename actual files, you would need to:

1. Export the layer with a new name
2. Use your operating system's file manager

---

### Can I undo a rename?

Currently, there is no built-in undo feature. However:

- QGIS has a general undo function (++ctrl+z++) that may work in some cases
- You can close the project without saving to revert changes
- Consider saving your project before bulk renames

!!! tip "Best Practice"
    Always save a backup of your project before performing large batch renames.

---

### Will this work with layers in groups?

Yes! The plugin lists all layers regardless of their group structure. Layer groups themselves are not renamed, only the individual layers within them.

---

## Features

### How do I add numbers at the end instead of the beginning?

Currently, numbering is added as a prefix. As a workaround:

1. Leave numbering off
2. Add your number pattern as a suffix
3. Use a template for consistency

*Feature request: Numbering position is on our roadmap.*

---

### Can I start numbering from a specific number?

Not yet. Numbering always starts from 1. This is a planned feature for a future release.

**Workaround:** Add a calculated offset using find/replace with regex after the initial numbering.

---

### What regex flavor is used?

The plugin uses **Python's `re` module**, which implements Perl-compatible regular expressions.

Common patterns:

| Pattern | Matches |
|---------|---------|
| `\d` | Any digit |
| `\w` | Word character (letter, digit, underscore) |
| `\s` | Whitespace |
| `.` | Any character |
| `*` | Zero or more |
| `+` | One or more |
| `?` | Zero or one |
| `^` | Start of string |
| `$` | End of string |

---

### Why isn't my regex working?

Common issues:

1. **Escaping:** Special characters need backslashes (`\.` for a literal dot)
2. **Case sensitivity:** Patterns are case-sensitive by default
3. **Greedy matching:** `.*` matches as much as possible

Use the **Test Regex Pattern** button to debug your patterns.

---

### Can I use regex in the prefix/suffix fields?

No. The prefix and suffix fields only accept literal text. Use the Find/Replace fields for regex operations.

---

## Templates

### Where are templates stored?

Templates are stored in `presets.json` in the plugin directory:

=== "Windows"
    ```
    C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\batch_layer_renamer\presets.json
    ```

=== "macOS"
    ```
    ~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/batch_layer_renamer/presets.json
    ```

=== "Linux"
    ```
    ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/batch_layer_renamer/presets.json
    ```

---

### Can I share templates with colleagues?

Yes! Simply copy the `presets.json` file and share it. Recipients should place it in their plugin directory.

---

### My templates disappeared after updating. Why?

Plugin updates may sometimes reset the presets file. Always back up your `presets.json` before updating.

---

## Troubleshooting

### The plugin doesn't show any layers

**Possible causes:**

1. No layers are loaded in the project
2. Plugin opened before layers were added

**Solution:** Click the **Refresh** button to reload the layer list.

---

### The rename button doesn't do anything

**Check:**

1. Are any layers selected?
2. Does the preview show "Will Change" for any layers?
3. Are there any error messages?

If all names show "No Change," your settings aren't modifying the names.

---

### I get an error about invalid regex

Your regular expression pattern has a syntax error. Common mistakes:

- Unmatched parentheses: `(text` should be `(text)`
- Unescaped special chars: `file.txt` should be `file\.txt`
- Invalid quantifiers: `*+` is invalid

Use the **Test Regex Pattern** button to validate your pattern.

---

### The plugin is slow with many layers

The real-time preview updates with every change, which can be slow with hundreds of layers.

**Tips:**

- Select only the layers you need to rename
- Configure all settings, then click Preview Changes
- Disable real-time preview by making changes quickly

---

### Special characters aren't being removed

Ensure **Remove special characters** is checked in Advanced Options.

Note: This option keeps letters, numbers, spaces, underscores, dashes, and dots. Only other special characters are removed.

---

## Performance

### How many layers can I rename at once?

There's no hard limit, but performance may degrade with very large numbers:

| Layers | Performance |
|--------|-------------|
| 1-100 | Instant |
| 100-500 | Fast |
| 500-1000 | May take a few seconds |
| 1000+ | Consider batching |

---

### Why is the preview slow?

The preview regenerates for all selected layers whenever settings change. With many layers, this can take time.

**Optimization tips:**

- Select fewer layers at once
- Make multiple quick changes rather than pausing between each

---

## Feature Requests

### How do I request a new feature?

1. Check the [GitHub issues](https://github.com/raymukesh/advanced_layer_renamer/issues) to see if it's already requested
2. If not, [open a new issue](https://github.com/raymukesh/advanced_layer_renamer/issues/new) with the "enhancement" label
3. Describe your use case and desired functionality

---

### Can I contribute code?

Absolutely! The project is open source. See the GitHub repository for contribution guidelines.

---

## Still Have Questions?

[:material-github: Open an Issue](https://github.com/raymukesh/advanced_layer_renamer/issues){ .md-button .md-button--primary }
[:material-email: Email the Author](mailto:dr.raymukesh@gmail.com){ .md-button }
