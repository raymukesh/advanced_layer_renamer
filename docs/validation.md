# Validation

The Validation tab helps you identify potential naming issues before they cause problems in your workflow.

---

## Why Validate?

Layer names with certain characteristics can cause issues:

- **File export failures** - Invalid characters prevent saving
- **Database errors** - Special characters may conflict with SQL
- **Cross-platform issues** - Some characters aren't allowed on all operating systems
- **Sorting problems** - Names may not sort as expected
- **Display issues** - Very long names get truncated

---

## Using the Validation Tool

### Steps

1. Go to the **Validation** tab
2. Select layers to validate (or use Select All in the Main tab)
3. Click **Validate Selected Layers**
4. Review the results

### Understanding Results

Results are displayed with status indicators:

| Icon | Meaning |
|------|---------|
| :material-check-circle:{ style="color: green" } | Valid - No issues found |
| :material-alert:{ style="color: orange" } | Warning - Potential issues detected |

---

## Validation Checks

### Invalid Characters

The following characters are flagged as potentially problematic:

| Character | Name | Why It's Problematic |
|-----------|------|---------------------|
| `<` | Less than | Not allowed in Windows filenames |
| `>` | Greater than | Not allowed in Windows filenames |
| `:` | Colon | Not allowed in Windows filenames |
| `"` | Double quote | Not allowed in Windows filenames |
| `/` | Forward slash | Path separator in Unix/Mac |
| `\` | Backslash | Path separator in Windows |
| `\|` | Pipe | Not allowed in Windows filenames |
| `?` | Question mark | Not allowed in Windows filenames |
| `*` | Asterisk | Wildcard character |

!!! tip "Fix with Remove Special Characters"
    Enable **Remove special characters** in the Advanced Options to automatically remove these characters.

---

### Name Length

Names longer than **255 characters** are flagged.

**Why it matters:**

- Most file systems limit filenames to 255 characters
- Long names may be truncated when exporting
- Some databases have field length limits

---

### Empty or Whitespace Names

Names that are empty or contain only whitespace are flagged.

**Examples of problematic names:**

- `` (empty)
- `   ` (only spaces)
- `\t` (only tabs)

---

### Leading/Trailing Spaces

Names with spaces at the beginning or end are flagged.

| Original | Issue |
|----------|-------|
| ` Layer` | Leading space |
| `Layer ` | Trailing space |
| ` Layer ` | Both |

**Why it matters:**

- Can cause duplicate name issues
- May not display correctly
- Can cause matching/search problems

!!! tip "Fix with Clean Whitespace"
    Enable **Clean extra whitespace** in the Advanced Options to remove leading/trailing spaces.

---

## Common Issues Reference

The Validation tab includes a quick reference panel listing common naming issues:

```
Common Naming Issues to Check:
• Invalid characters: < > : " / \ | ? *
• Names starting/ending with spaces
• Very long names (>255 characters)
• Duplicate names
• Empty names
• Names with only numbers
• Special characters in file paths
```

---

## Validation Workflow

### Before Renaming

1. Open the plugin
2. Go to the **Validation** tab
3. Click **Validate Selected Layers**
4. Review any warnings
5. Go to **Main** tab and configure options to fix issues
6. Preview changes
7. Validate again if needed
8. Apply the rename

### After Importing Data

1. Import your data layers
2. Open the plugin
3. Validate all layers
4. Apply the **Clean Names** quick template if issues are found
5. Rename to fix issues

---

## Validation Examples

### Example 1: File Export Preparation

**Scenario:** Preparing layers for export to Shapefile

**Validation finds:**
```
⚠️ Layer<2024>: Invalid character '<', Invalid character '>'
⚠️ Data/Points: Invalid character '/'
✅ Clean_Layer: Valid
```

**Solution:**

1. Enable **Remove special characters**
2. Preview changes
3. Apply rename
4. Export files successfully

---

### Example 2: Database Import

**Scenario:** Preparing layers for PostGIS import

**Validation finds:**
```
⚠️ My Layer Name: Contains spaces (may need quoting in SQL)
⚠️ layer-with-dashes: Dashes may cause issues
✅ layer_underscore: Valid
```

**Solution:**

1. Use Find/Replace: Find ` ` (space), Replace `_`
2. Use Find/Replace: Find `-`, Replace `_`
3. Apply changes

---

### Example 3: Cleaning Imported Data

**Scenario:** Data imported with messy names

**Validation finds:**
```
⚠️  Layer Name : Leading/trailing spaces
⚠️ Layer  Name: Multiple consecutive spaces
⚠️ Layer (copy) (1): May indicate duplicate
✅ Clean_Layer: Valid
```

**Solution:**

1. Enable **Clean extra whitespace**
2. Use Find/Replace to remove "(copy)" text
3. Apply changes

---

## Best Practices

### Regular Validation

- :material-check: Validate before major exports
- :material-check: Validate after importing external data
- :material-check: Validate before database uploads

### Fixing Issues

- :material-check: Use **Remove special characters** for invalid chars
- :material-check: Use **Clean whitespace** for spacing issues
- :material-check: Use **Find/Replace** for specific patterns

### Prevention

- :material-check: Establish naming conventions for your team
- :material-check: Create templates that enforce clean names
- :material-check: Validate early and often

---

## Validation vs. Preview

| Feature | Purpose |
|---------|---------|
| **Validation** | Checks current names for issues |
| **Preview** | Shows what names will become after transformation |

Use both together:

1. **Validate** to identify current issues
2. Configure options to fix issues
3. **Preview** to verify the fixes
4. Apply the rename
