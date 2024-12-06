# **About**
hg2-item-parser is a Python package for parsing [Houkai Gakuen 2](https://houkai2nd.miraheze.org/wiki/Houkai_Gakuen_2_Wiki) items data.

## **Installation**
### **From PyPi**
```bash
pip install hg2-item-parser
```

## **Preparations**
To use this package, you will need a folder containing all item data, which can be downloaded and extracted using another package [hg2-data-extractor](https://github.com/xcvhmq33/hg2-data-extractor). It is recommended to use both packages in the same directory to avoid manually specifying folder paths, as they are designed to create and use directories with compatible names by default.

## **Commands Overview**

The CLI offers several commands for processing data. Below is a quick summary:

| Command        | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `check`        | Parses a single item by ID and prints to the console.                       |
| `parse`        | Parses a single item or a range of items by ID(s) and writes to a file.     |

---

## **Usage**
The CLI is invoked through a main entry point (e.g., `hg2-item-parser` or `python -m <module-name>`). Below are detailed examples for each command.

### **1. Check item**
Parses and displays details about a single in-game item by its ID.

```bash
hg2-item-parser check <item_id> --data-dir path/to/data/
```

| Option                | Description                                          | Default Value    |
|-----------------------|------------------------------------------------------|------------------|
| `<item_id>`           | The in-game ID of a single item to parse.            | `None`           |
| `--data-dir`, `-d`    | Path to the directory where data files are located.  | `extracted`      |

---

### **2. Parse item(s)**
Parses and writes a single item or a range of items by their in-game IDs to a file.

```bash
hg2-item-parser parse <item_id> --range from to
```

| Option            | Description                                                                                     | Default Value     |
|-------------------|-------------------------------------------------------------------------------------------------|-------------------|
| `<item_id>`       | The in-game ID of a single item to parse.                                                       | `None`            |
| `--range`, `-r`   | Specify a range of item IDs to parse. Provide two integers: the start and end IDs (inclusive).  | `None`            |

---

## **Examples**

### **1. Check item**
Display item with ID=200:

```bash
hg2-item-parser check 200 --data-dir extracted
```

### **2. Parse a single item**
Parse item with ID=200:

```bash
hg2-item-parser parse 200 --output items.txt --data-dir extracted
```

### **3. Parse a range of items**
Parse items with IDs from 1 to 200:

```bash
hg2-item-parser parse --range 1 200 --output items.txt --data-dir extracted
```