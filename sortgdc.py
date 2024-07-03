import pandas as pd
import argparse
import os
import shutil
import sys
import time
from collections import defaultdict

"""
This script should be ran from the same directory as the downloaded GDC files (directories).
It will organize data by Data Category, and then by Data Type.
Each filename will be prefixed with the sample name.

Simple usage:

# Dummy run (no action performed)
python3 sortgdc.py -m gdc_manifest.2024-07-03.txt -s gdc_sample_sheet.2024-07-03.tsv


The dummy check will create a md5 checksums file, after which you can run,
md5sum -c allfiles.md5 | grep -v "OK$"
to verify all files.

# Copy files to the organized directories
python3 sortgdc.py -m gdc_manifest.2024-07-03.txt -s gdc_sample_sheet.2024-07-03.tsv -a 'copy'

"""


def load_data(manifest, samplesheet):
    '''
    Loads the initial data.

    Parameters
    ----------
    manifest : str
        The GDC manifest file name (and path if not in the current one).
    samplesheet : str
        The GDC samplesheet file name (and path if not in the current one).
    
    Returns
    -------
    samplesheet_df : pandas.DataFrame
        A DataFrame containing all the information from the sample sheet, plus:
        - the md5 from the manifest
        - a 'path' column with the relative file path.
        In column names, spaces are substituted by underscores.
    '''

    print("Loading info...")
    # Load the sample sheet file into a DataFrame
    samplesheet_df = pd.read_csv(samplesheet, sep='\t')
    samplesheet_df.columns = [x.replace(" ", "_") for x in samplesheet_df.columns]
    for column in ["Data_Category", "Data_Type"]:
        samplesheet_df[column] = samplesheet_df[column].apply(lambda x: x.replace(" ", "_"))

    # Add MD5 info from the manifest file
    manifest_df = pd.read_csv(manifest, sep='\t')
    samplesheet_df = pd.merge(samplesheet_df, manifest_df[["id", "md5"]], left_on="File_ID", right_on="id")

    # Add file path
    samplesheet_df["path"] = "./" + samplesheet_df["File_ID"] + "/" + samplesheet_df["File_Name"]

    return samplesheet_df


def check_data(df):
    '''
    Checks whether all the data was downloaded prior to any further action.

    Parameters
    ----------
    df : pandas.DataFrame
        Samplesheet DataFrame created by load_data().
    
    Returns
    -------
    None
        (Prints to screen.)
    '''
    print("Checking if filenames are present:")
    df["ok"] = False
    dirs = os.listdir()
    for line in df.index:
        dir = df.loc[line, "File_ID"]
        file = df.loc[line, "File_Name"]
        if dir in dirs:
            if file in os.listdir(dir):
                df.at[line, "ok"] = True
    ok = sum(df["ok"])
    nok = df.shape[0] - ok
    print("OK:", ok)
    print("Not OK:", nok)
    assert nok == 0


def organize(df, action, cut):
    """
    Sort the data in folders according to Data Category and Data Type.
    Add new path and new filename as columns to the dataframe.
    Perform the required action on the files ('none', 'copy' or 'move')

    Parameters
    ----------
    df : pandas.DataFrame
        Samplesheet DataFrame created by load_data().
    action : str
        action to be performed on the files ('none', 'copy' or 'move')
    cut : str
        Comma-separated strings to cut as prefixes. E.g. 'TARGET-ALL-P1,TARGET-ALL-P2'
    
    Returns
    -------
    None
        However, the dataframe will be modified in-place with the addition of the columns:
        - "unique_id": 'Case_ID' plus a suffix to guarantee name uniqueness
        - "newname": name of the file at the new directory (prepended with the sample name).
        - "newpath": relative path of the new file, including the new file name.
    """

    categories = sorted(df["Data_Category"].unique())
    df['unique_id'] = ""
    # Create organized folders, if not present
    # one top folder per category
    for cat in categories:
        if cat not in os.listdir():
            print("Creating folder", cat)
            if action in ('move', 'copy'):
                os.mkdir(cat)
            else:
                print(' (dummy run, no directory created)')
        datatypes = sorted(df[df["Data_Category"]==cat]["Data_Type"].unique())
        # Within the category, one subfolder per data type
        for datatype in datatypes:
            if (cat not in os.listdir() and action not in ('move', 'copy')) or datatype not in os.listdir(cat):
                print("  Creating subfolder", datatype)
                if action in ('move', 'copy'):
                    os.mkdir(os.path.join(cat, datatype))
                else:
                    print('   (dummy run, no directory created)')
            # Set unique IDs
            selection = df[(df["Data_Category"]==cat) & (df["Data_Type"]==datatype)]
            case_ids = defaultdict(int)
            for index in selection.index:
                case = list(set([x.strip() for x in selection.loc[index, "Case_ID"].split(",")]))
                assert len(case) == 1
                case = case[0]
                df.at[index, 'unique_id'] = f"{case}_{case_ids[case]}"
                case_ids[case] += 1
            selection = df[(df["Data_Category"]==cat) & (df["Data_Type"]==datatype)]
            assert len(selection["unique_id"].unique()) == selection.shape[0]

    
    # Copy or move data in folders
    df["newpath"] = ""
    df["newname"] = ""
    settings = dict()
    cut = cut.split(",") # Prefixes to remove
    skip = int(cut.pop(-1)) # The last item is the number of characters to remove
    for index in df.index:
        source = df.loc[index, "path"]
        case = df.loc[index, "unique_id"]
        keep = df.loc[index, "File_Name"]
        if cut:
            for prefix in cut:
                if keep.startswith(prefix):
                    keep=keep[len(prefix):]
        keep = keep[skip:]
        newname = case+keep 
        df.at[index, "newname"] = newname
        destination = os.path.join(df.loc[index, "Data_Category"], df.loc[index, "Data_Type"], newname)
        df.at[index, "newpath"] = destination
        settings[index] = {'from': source, 'to': destination}

    # Ok, let's proceed
    if action == 'move':
        execute = shutil.move 
        verb = "Moving"
    elif action == 'copy':
        execute = shutil.copy
        verb = "Copying"
    else:
        execute = dummy # default is do nothing
        verb = "Dummy check (no action)"
    

    print(f"{verb} files...")
    tot = df.shape[0]
    n = 0
    print("\n\n")

    for item in settings.values():
        source, destination = item.values()
        n += 1
        print(f"\033[3A", end='') # Back 3 lines
        print("\033[2K", end='') # Clear line
        print(f"{n} / {tot}")
        print("\033[2K", end='') # Clear line
        print(f"{verb} from: {source}")
        print("\033[2K", end='') # Clear line
        print(f"To: {destination}")
        execute(source, destination) 
    sys.stdout.flush()           


def dummy(*args, **kwargs):
    """
    Wait for a short time.
    """
    time.sleep(0.005)


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Load GDC manifest and sample sheet into pandas DataFrames.")
    parser.add_argument("-m", "--manifest", required=True, help="Path to the manifest file")
    parser.add_argument("-s", "--samplesheet", required=True, help="Path to the sample sheet file")
    parser.add_argument("-a", "--action", choices=['none', 'copy', 'move'], default='none', help="Action to perform with the files ('none', 'copy' or 'move')")
    parser.add_argument("-c", "--cut", default=',36', help="Comma-separated list of strings to remove as prefix, plus a number (default: ',36' == no string, but 36 characters)")

    args = parser.parse_args()

    # Load data
    df = load_data(args.manifest, args.samplesheet)

    # Check that all files are present
    check_data(df)

    # Save info
    print("Saving md5sums to 'allfiles.md5'")
    df[["md5", "path"]].to_csv("allfiles.md5", sep="\t", index=False, header=False)
    print("Saving the dataframe to 'info_initial.tsv'")
    df.to_csv("info_initial.tsv", sep="\t", index=False)

    # Organize
    organize(df, args.action, args.cut)

    # Save the final data
    print("Saving the dataframe to 'info_final.tsv'")
    df.to_csv("info_final.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
