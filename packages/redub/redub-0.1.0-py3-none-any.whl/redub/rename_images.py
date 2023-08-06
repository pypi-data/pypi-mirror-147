from pathlib import Path
import shutil
from timeit import timeit
import re

import pandas as pd
import PySimpleGUI as sg

# TODO: Options to add:
# Option to copy files to a different directory
# Get session name, input dir, and output dir from user
# Radio select "Landmark" or "Actual Folio"
# Radio select moving moving "Actual Folio" files into separate folders (FRONTMATTER, TEXT, BACKMATTER)
# If rename in place, first get all new names and ensure they don't already exist in folder. Raise dialogue if they do.
# convert versions to use square brackets and update our procedures from no on
###
# TOKENS: need to allow for complex renaming so that we can accomodate institution desires
###

def display_skipped_files(skipped: list, naming_convention: str):
    sg.set_options(dpi_awareness=True)
    layout = (
        (sg.Text(f'Failed to locate a corresponding {naming_convention} for the following:'),),
        (sg.Listbox(skipped, expand_y=True, expand_x=True, ),),
        (sg.Button('Okay'),)
    )
    window = sg.Window('Skipped Files', layout=layout, size=(800, 400))
    window.read()
    window.close()

def get_spreadsheet_data(excel_file: str):
    if not Path(excel_file).is_file():
        raise FileExistsError
    df = pd.read_excel(excel_file)
    df = df.fillna('')
    list_of_dicts = df.to_dict('records')
    return tuple(list_of_dicts)

def create_rename_dict(guide: tuple[dict[str, int | str]], naming_convention: str, prefix_in, prefix_out: str):
    '''Create and return a dictionary that has the input name as the key and the output name as the value.'''
    renaming_dict = {}
    used_landmarks = set()
    for row in guide:
        image_number = f'{row["Image #"]}'.zfill(4)
        image_number = f'{prefix_in}{image_number}'
        name = row[naming_convention].replace('p. ', 'p').replace(' ', '_')
        if naming_convention == 'Landmark':
            if not name.startswith('f') and re.match(r'\d+[abrv]', name):
                name = f'f{name}'
            name, used_landmarks, renaming_dict = version_new_name(used_landmarks, name, renaming_dict, prefix_out)
        if not name:
            name = row['Landmark'].replace(' ', '_')
        renaming_dict[image_number] = f'{prefix_out}{name}'
    return renaming_dict

def version_new_name(used_names: set, new_name: str, rename_dict: dict[str, str], prefix: str):
    if new_name not in used_names:
            used_names.add(new_name)
    else:
        for k, v in rename_dict.items():
            if v == f'{prefix}{new_name}':
                rename_dict[k] = f'{prefix}{new_name}[a]'
        for i in (
            'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z'
            ):
            if f'{new_name}_[{i}]' not in used_names:
                new_name = f'{new_name}[{i}]'
                used_names.add(new_name)
                version = i
                break
    return new_name, used_names, rename_dict

def get_image_version(stem: str):
    if '.' in stem:
        name, version = tuple(stem.split('.'))
        return name, f'_[{version}]'
    return stem, ''

def get_images_dir(dir_path: str):
    image_dir = image_dir = Path(dir_path).absolute().resolve()
    if not image_dir.is_dir():
        sg.popup_ok(f"{dir_path} either isn't a directory (folder), or it doesn't exist. Please select a valid directory which contains the JPEGs or TIFFs to rename.")
        return
    return image_dir

def rename_file(f: Path, image_dir: Path, new_name: str, image_version: str, extension: str):
    new_path = image_dir.joinpath(f'{new_name}{image_version}{extension}')
    try:
        f.rename(new_path)
    except FileExistsError:
        sg.popup_ok(f'Cannot rename {f.stem} to {new_name} because {new_name} already exists. Continuing on...', 'File Already Exists')
        return
    except Exception as e:
        sg.popup_ok(f'Failed to rename {f.stem} to {new_name} because:\n{e}')
        return
    return True

def copy_and_rename(f: Path, output: str, new_name: str, image_version: str, extension: str):
    output_dir = Path(output)
    if not output_dir.is_dir():
        sg.popup_ok(f"It doesn't seem that {output} is a valid folder.", title='Bad Output Folder')
        return
    new_path = output_dir.joinpath(f'{new_name}{image_version}{extension}')
    try:
        shutil.copyfile(f, new_path)
    except Exception as e:
        sg.popup_ok(f'Failed to rename {f.stem} to {new_name} because:\n{e}')
        return
    return True

def rename_all_files_in_dir(dir_path: str, excel_path: str, use: str, prefix_in: str, prefix_out: str, rename_in_place: bool, output_dir: str):
    '''use = "Landmark" | "Actual Folio"'''
    skipped_image_names = []
    if not (image_dir := get_images_dir(dir_path)):
        sg.popup(f'It seems that {image_dir} is not a valid folder. Please reselect the folder which contains the image files.', title='Bad Directory')
        return
    try:
        guide = get_spreadsheet_data(excel_path)
    except FileExistsError:
        sg.popup(f'It seems that {excel_path} does not exist. Please select a .xlsx file.', 'Bad Excel File')
        return
    except Exception as e:
        sg.popup_ok(f'Failed to load spreadsheet. See error:\n{e}')
        return
    rename_dict = create_rename_dict(guide, use, prefix_in, prefix_out)


    for f in image_dir.glob('*.[jt][pi][gf]*'): # this patter matches both "jpg*" and "tif*" [and theoretically, jpj, jpf, jig, jif, tpf, tpf, tig -- shouldn't be an issue (famous last words?)]
        extension = f.suffix
        image_stem, image_version = get_image_version(f.stem)
        new_name = rename_dict.get(image_stem)
        if not new_name:
            skipped_image_names.append(f.name)
            continue
        if rename_in_place:
            if not rename_file(f, image_dir, new_name, image_version, extension):
                return
        else:
            if not copy_and_rename(f, output_dir, new_name, image_version, extension):
                return
            
    if len(skipped_image_names) > 0:
        display_skipped_files(skipped_image_names, use)

    return True


# TEST PARAMS
# DIR_PATH = 'images'
# EXCEL = 'MS1176_GA471.xlsx'
# USE = 'Landmark'
# PREFIX_IN = 'M_NT_GRC_GA471_20220405'
# PREFIX_OUT = 'MS1176'
# RENAME_IN_PLACE = False
# OUTPUT = 'output'

# main(DIR_PATH, EXCEL, USE, PREFIX_IN, PREFIX_OUT, RENAME_IN_PLACE, OUTPUT)

