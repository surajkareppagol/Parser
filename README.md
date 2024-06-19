# XML to JSON

A python script which parses the XML and converts it into JSON.

```bash
python main.py <file-path> [options]
```

```bash
python main.py --help
```

Use `-o` option to pass the output file name.

```bash
python main.py example.xml -o output.json
```

Here is an example,

`XML File`,

![xml file](https://raw.githubusercontent.com/surajkareppagol/Assets/main/22%20-%20Parser/xml.png)

Converted `JSON File`,

![json file](https://raw.githubusercontent.com/surajkareppagol/Assets/main/22%20-%20Parser/json.png)

## NOTE

The file should not contain more than one tag with same name on same level.
