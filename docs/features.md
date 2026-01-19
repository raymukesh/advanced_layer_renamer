# Features

A comprehensive guide to all the renaming features available in Advanced Layer Renamer.

---

## Numbering Options

Add sequential numbers to your layer names.

### No Numbering

The default option. Layer names are transformed without adding numbers.

### Sequential (1, 2, 3...)

Adds simple sequential numbers as prefixes.

| Original | Result |
|----------|--------|
| Layer A | 1_Layer A |
| Layer B | 2_Layer B |
| Layer C | 3_Layer C |

### Leading Zeros

Adds numbers with leading zeros for consistent sorting. Choose the number of zeros:

| Setting | Example Output |
|---------|----------------|
| 1 (01, 02...) | 01, 02, 03... 99 |
| 2 (001, 002...) | 001, 002, 003... 999 |
| 3 (0001, 0002...) | 0001, 0002... 9999 |
| 4 (00001, 00002...) | 00001, 00002... 99999 |
| 5 (000001, 000002...) | 000001, 000002... 999999 |

!!! tip "Why use leading zeros?"
    Leading zeros ensure layers sort correctly in alphabetical order:

    - Without: 1, 10, 11, 2, 3...
    - With: 01, 02, 03... 10, 11...

---

## Basic Options

### Prefix

Add text to the beginning of layer names.

| Prefix | Original | Result |
|--------|----------|--------|
| `2024_` | Layer | 2024_Layer |
| `Project_` | Data | Project_Data |

### Suffix

Add text to the end of layer names.

| Suffix | Original | Result |
|--------|----------|--------|
| `_final` | Layer | Layer_final |
| `_v2` | Data | Data_v2 |

### Find & Replace

Replace specific text within layer names.

**Simple Text Replacement:**

| Find | Replace | Original | Result |
|------|---------|----------|--------|
| `old` | `new` | old_layer | new_layer |
| `_` | `-` | my_layer | my-layer |
| `copy` | `` | layer (copy) | layer () |

### Regular Expressions

Enable **Use Regular Expressions** for powerful pattern matching.

!!! info "What are Regular Expressions?"
    Regular expressions (regex) are patterns used to match character combinations in strings.

**Common Regex Examples:**

| Pattern | Description | Example |
|---------|-------------|---------|
| `\d+` | Match numbers | `layer123` → `layer` (if replaced with empty) |
| `\s+` | Match whitespace | `my  layer` → `my_layer` (if replaced with `_`) |
| `^old_` | Match "old_" at start | `old_layer` → `new_layer` |
| `_v\d$` | Match version suffix | `layer_v1` → `layer` |
| `\(.*\)` | Match parentheses content | `layer (copy)` → `layer ` |

**Test Your Regex:**

Click the **Test Regex Pattern** button to test your pattern against a sample string before applying.

---

## Case Conversion

Convert the case of layer names. Only one option can be selected at a time.

| Option | Original | Result |
|--------|----------|--------|
| **UPPERCASE** | My Layer | MY LAYER |
| **lowercase** | My Layer | my layer |
| **Title Case** | my layer name | My Layer Name |
| **Capitalized** | my layer name | My layer name |

!!! note
    Case conversion is applied after all other transformations (prefix, suffix, find/replace, etc.)

---

## Advanced Options

### Date Stamping

Automatically add the current date to layer names.

**Available Formats:**

| Format | Example |
|--------|---------|
| YYYYMMDD | 20240115 |
| YYYY-MM-DD | 2024-01-15 |
| DD-MM-YYYY | 15-01-2024 |

The date is added as a prefix:

```
Layer Name  →  20240115_Layer Name
```

### Remove Special Characters

Removes all characters except:

- Letters (a-z, A-Z)
- Numbers (0-9)
- Spaces
- Underscores (_)
- Dashes (-)
- Dots (.)

**Example:**

| Original | Result |
|----------|--------|
| `Layer <v1>` | `Layer v1` |
| `Data: 2024` | `Data 2024` |
| `file/path` | `filepath` |
| `name@domain` | `namedomain` |

!!! warning "Characters Removed"
    The following characters are removed: `< > : " / \ | ? * @ # $ % ^ & ( ) + = { } [ ] ; ' , ~`

### Clean Extra Whitespace

Removes leading/trailing spaces and collapses multiple spaces into one.

| Original | Result |
|----------|--------|
| `  Layer  ` | `Layer` |
| `My    Layer` | `My Layer` |
| `Data  Name  Here` | `Data Name Here` |

---

## Transformation Order

When multiple options are enabled, they are applied in this order:

1. **Find/Replace** (with or without regex)
2. **Remove Special Characters**
3. **Clean Whitespace**
4. **Add Numbering** (sequential or with zeros)
5. **Add Date Stamp**
6. **Add Prefix**
7. **Add Suffix**
8. **Apply Case Conversion**

!!! example "Example with Multiple Options"

    **Settings:**

    - Find: `old` → Replace: `new`
    - Prefix: `Project_`
    - Numbering: Leading zeros (01, 02...)
    - Case: UPPERCASE

    **Transformation:**
    ```
    old_layer
    ↓ Find/Replace
    new_layer
    ↓ Add Numbering
    01_new_layer
    ↓ Add Prefix
    Project_01_new_layer
    ↓ Case Conversion
    PROJECT_01_NEW_LAYER
    ```

---

## Preview Table

The preview table shows the effect of your settings in real-time:

| Column | Description |
|--------|-------------|
| **Original Name** | Current layer name |
| **New Name** | Result after transformation |
| **Status** | "Will Change" (green) or "No Change" (gray) |

- **Green background:** Name will be changed
- **Gray background:** Name will remain the same

!!! tip
    Columns are resizable - drag the column headers to adjust widths.

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Select all layers | Click **Select All** |
| Multi-select | ++ctrl++ + Click |
| Range select | ++shift++ + Click |
