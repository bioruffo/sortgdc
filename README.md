# sortgdc

Organize and rename GDC files.

## Basic info

The script will take data from the GDC manifest and samplesheet files, traverse the download directories, and either copy or move the files to new directories organized by 'Data Category' and 'Data Type'.
The files will also be renamed as to have the 'Case ID' as prefix, for easier identification.
The script can also just check what was already downloaded, and optionally verify the files' md5sums.

The script will create the following output files:
- `info_initial.tsv` containing all data from the samplesheet, plus the md5sum of each file, its 'downloaded' status, and the 'md5sum_ok' check if requested;  
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

## Options

`--manifest` (`-m`): manifest file name  

`--samplesheet` (`-s`): samplesheet file name  

`--action` (`-a`): action to perform with the files.  
- 'none' (default) will perform a dummy run and create the output files. Advised as initial test, followed by checking the expected file names in the 'info_final.tsv' table, and possibly re-verifying the files' md5sums. The dummy run should also be ran to identify possible issues.  
- 'copy' will copy the files to the organized folders.  
- 'move' will move the files instead (not recommended, only do this if you can't afford the copy space and are certain that all is ok).    

`--cut` (`-c`): comma-separated list of strings to remove as prefix, plus a number of characters to remove from the start of the filename.  
- The default is ',36' since the file names start with a 36-character ID.  
- If you want to leave the name as it is, use ',0'.
- Add any prefixes that you want removed from the file names. 
E.g. to remove also the "TARGET-ALL-P2." prefix from any filenames that start with it (even if others don't), use:  
`--cut 'TARGET-ALL-P2.,36'` 

`--verify` (`-v`): verify md5sums of all downloaded files. The result of the md5sum check will be added to `info_initial.tsv` even for dry runs.


## Usage

#### Check what was downloaded and verify the md5sums of all files:
```
python3 sortgdc.py -m gdc_manifest.2024-07-03.txt --verify
```
(View the 'md5sum_ok' column in `info_initial.tsv`)  

#### Just check what was downloaded:
```
python3 sortgdc.py -m gdc_manifest.2024-07-03.txt
```
You can then verify the md5sums externally via terminal:
```
md5sum -c allfiles.md5 | grep -v "OK$"
```

#### Copy the files to directories based on data type:
```
python3 sortgdc.py -m gdc_manifest.2024-07-03.txt -s gdc_sample_sheet.2024-07-03.tsv -a 'copy'
```

### Example terminal output

#### Command
```
python3 sortgdc.py -m gdc_manifest.2024-07-03.txt -s gdc_sample_sheet.2024-07-03.tsv -a 'copy' -c 'TARGET-ALL-P2.,36'
```

#### Terminal output
```
Loading info...
Checking if filenames are present:
Downloaded: 2797 / 2797

Saving expected md5sum values and file locations to 'allfiles.md5'

Saving the dataframe to 'info_initial.tsv', with download information

=== Dry run, no directory will actually be created ===
Creating folder Biospecimen
Creating subfolder Biospecimen
Creating folder Clinical
Creating subfolder Clinical
Creating folder Copy_Number_Variation
Creating subfolder Copy_Number_Variation
Creating subfolder Copy_Number_Variation
Creating folder Simple_Nucleotide_Variation
Creating subfolder Simple_Nucleotide_Variation
Creating subfolder Simple_Nucleotide_Variation
Creating subfolder Simple_Nucleotide_Variation
Creating folder Structural_Variation
Creating subfolder Structural_Variation
Creating folder Transcriptome_Profiling
Creating subfolder Transcriptome_Profiling
Creating subfolder Transcriptome_Profiling
Creating subfolder Transcriptome_Profiling

Copying files...
2797 / 2797
Copying from: ./a58bdb5b-74f7-46e1-8ac5-780901d4c16f/981e279f-a841-46ef-bf55-7b0160a0a29e_noid_Red.idat
To: DNA_Methylation/Masked_Intensities/TARGET-15-SJMPAL046470_5_noid_Red.idat
Saving the dataframe to 'info_final.tsv'
```


## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->





