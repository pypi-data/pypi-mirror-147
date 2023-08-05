# pdf2image-cli
[pdf2image](https://github.com/Belval/pdf2image) port to a CLI version written in Python.

Designed to make PDF processing easier for those who like working through the terminal. After installing you will have the `pdf2image` command available to use.


## Installation
`pip install pdf2image-cli`

### Windows
For Windows you will need to install poppler for Windows. Here is a repo containing the binaries you will have to add to PATH. [@oschwartz10612/poppler-windows](https://github.com/oschwartz10612/poppler-windows)

### Mac
For MacOS you will need to install poppler for MacOS.

### Linux
Most distros have `pdftopppm` and/or `pdftocairo`. However if you do not have them installed in your machine please download `poppler-utils` from your distro's package manager.

## How to use it
The program can detect if you've chosen a directory or a file. In case you've chosen a directory, the program will extract images into separate folder for each PDF in it.

To begin, run the following command:
``` bash
$ pdf2image [path] 
```
The program will create an output folder in your current working directory. If you wish to change the output path run the command with the following flag.
``` bash
$ pdf2image [path] --output [output_path]
```

As defualt the program will extract the images in `jpeg` format. If you wish to change the format to `png` add the following flag.
``` bash
$ pdf2image [path] --file_type ["jpeg"|"png"]
```

## Acknowledgements
- Project based on [@Belval/pdf2image](https://github.com/Belval/pdf2image) API. For sponsorships, please visit [Github Sponsors](https://github.com/sponsors/Belval).

---
Developed with ❤️ by Carlos Valdez.