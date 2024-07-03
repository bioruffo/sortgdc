# sortgdc

Organize and rename GDC files.

## Basic info

The script will take data from the GDC manifest and samplesheet files, traverse the download directories, and copy or move the files to new directories organized by 'Data Category' and 'Data Type'.
The files will also be renamed as to have the 'Case ID' as prefix, for easier identification.

The script will also create the following output files:
- `info_initial.tsv` containing all data from the samplesheet, plus the md5sum of each file;  
- `allfiles.md5` a file ready to be used as input to `md5sum -c`;  
- `info_final.tsv` containing all data from `info_initial.tsv` plus the destination path and filename.

The script has three --action modes:
- 'none': Only create the output files and perform a dummy check of the operation
- 'copy': Create the output files and **copy** the genomics data to the organized directories
- 'move': Create the output files and **move** the genomics data to the organized directories


## Requirements
 - pandas

## Installation

Clone/save the sortgdc.py file inside the directory where all the GDC file directories are located.

## Usage

#### Perform a dummy check and create `allfiles.md5` (and the other output files):
```
python3 sortgdc.py -m gdc_manifest.2024-07-03.txt -s gdc_sample_sheet.2024-07-03.tsv
```

#### Verify the md5sums (strongly suggested)
```
md5sum -c allfiles.md5 | grep -v "OK$"
```

#### Organize the files
```
python3 sortgdc.py -m gdc_manifest.2024-07-03.txt -s gdc_sample_sheet.2024-07-03.tsv -a 'copy'
```





