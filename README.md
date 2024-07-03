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

## Options

`--manifest` (`-m`): Manifest file name  

`--samplesheet` (`-s`): Samplesheet file name  

`--action` (`-a`): Action to perform with the files.  
- The default is 'none' which will perform a dummy run and create the output files.  
- 'copy' will copy the files to the organized folders.  
- 'move' will move the files instead (not recommended, only do this if you can't afford the copy space and are certain that all is ok).    

`--cut` (`-c`): Comma-separated list of strings to remove as prefix, plus a number of characters to remove from the start of the filename.  
- The default is ',36' since the file names start with a 36-character ID.  
- If you want to leave the name as it is, use ',0'.
- Add any prefixes that you want removed from the file names. 
E.g. to remove also the "TARGET-ALL-P2." prefix from any filenames that start with it (even if others don't), use:  
`--cut 'TARGET-ALL-P2.,36'`


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

### Example run

#### Command
```
python3 sortgdc.py -m gdc_manifest.2024-07-03.txt -s gdc_sample_sheet.2024-07-03.tsv -a 'copy' -c 'TARGET-ALL-P2.,36'
```

#### Terminal output
```
Loading info...
Checking if filenames are present:
OK: 2797
Not OK: 0
Saving md5sums to 'allfiles.md5'
Saving the dataframe to 'info_initial.tsv'
Creating folder Copy_Number_Variation
  Creating subfolder Allele-specific_Copy_Number_Segment
  Creating subfolder Gene_Level_Copy_Number
Creating folder DNA_Methylation
  Creating subfolder Masked_Intensities
  Creating subfolder Methylation_Beta_Value
Creating folder Simple_Nucleotide_Variation
  Creating subfolder Masked_Somatic_Mutation
Creating folder Transcriptome_Profiling
  Creating subfolder Gene_Expression_Quantification
  Creating subfolder Isoform_Expression_Quantification
  Creating subfolder miRNA_Expression_Quantification
Copying files...
2797 / 2797
Copying from: ./a58bdb5b-74f7-46e1-8ac5-780901d4c16f/981e279f-a841-46ef-bf55-7b0160a0a29e_noid_Red.idat
To: DNA_Methylation/Masked_Intensities/TARGET-15-SJMPAL046470_5_noid_Red.idat
Saving the dataframe to 'info_final.tsv'
```






