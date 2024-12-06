# nmrstar_xml
Convert NMRSTAR to XML and back again

## XML to NMRSTAR
```
usage: xmlstar [-h] [-i INPUT] [-o OUTPUT]

Translate XML file to NMR-STAR

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        XML input file (default stdin)
  -o OUTPUT, --output OUTPUT
                        NMR-STAR output file (default stdout)
```

##  NMRSTAR to XML
```
usage: starxml [-h] [-i INPUT] [-o OUTPUT]

Translate NMR-STAR file to XML

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        NMR-STAR input file (default stdin)
  -o OUTPUT, --output OUTPUT
                        XML output file (default stdout)
```

## As Python module

```
with Translator(args.input,args.output) as tr:
        tr.xml_translate()

with Translator(args.input,args.output) as tr:
        tr.star_translate()
```

