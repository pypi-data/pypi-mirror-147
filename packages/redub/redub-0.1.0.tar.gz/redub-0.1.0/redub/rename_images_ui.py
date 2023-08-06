import PySimpleGUI as sg

import redub.rename_images as ri

sg.set_options(dpi_awareness=True)

def valid(values: dict):
    for input_field in ('dir_path', 'excel_path', 'prefix_in', 'prefix_out'):
        if values[input_field] == '':
            sg.popup_ok('None of the following fields can be blank:\nImage Folder\nSpreadsheet\nInput Prefix\nOutput Prefix', title='Missing Field')
            return
    if values['diff_folder'] and values['output_dir'] == '':
        sg.popup_ok('If "Copy and rename files to different folder" is selected, then "Output Folder" cannot be blank.', title='Missing Field')
        return
    return True

def layout():
    label_size = (20, 1)
    return (
        (sg.Text('Image Folder', size=label_size), sg.Input('', expand_x=True, key='dir_path', disabled=True), sg.FolderBrowse()),
        (sg.Text('Spreadsheet', size=label_size), sg.Input('', expand_x=True, key='excel_path', disabled=True), sg.FileBrowse(file_types=(('Excel Files', '*.xlsx'),))),
        (sg.Text('Input Prefix', size=label_size), sg.Input('', expand_x=True, key='prefix_in')),
        (sg.Text('Output Prefix', size=label_size), sg.Input('', expand_x=True, key='prefix_out')),
        (sg.Text('Rename using', size=label_size), sg.Radio('Landmark', 'naming', key='landmark'), sg.Radio('Actual Folio', 'naming', key='actual', default=True)),
        (sg.Text('Files and Folders', size=label_size), sg.Radio('Rename files in place', 'folder_pref', key='in_place', default=True), sg.Radio('Copy and rename files to different folder', 'folder_pref', key='diff_folder')),
        (sg.Text('Output Folder', size=label_size), sg.Input('', expand_x=True, key='output_dir', disabled=True), sg.FolderBrowse()),
        (sg.Button('Rename All Images', key='rename'), sg.Stretch(), sg.Button('Exit'))
    )

def main():
    window = sg.Window('Rename Images', layout=layout())
    while True:
        event, values = window.read()
        if event in (sg.WIN_X_EVENT, sg.WIN_CLOSED, None, 'Exit'):
            break
        elif event == 'rename':
            if not valid(values):
                continue
            if values['actual']:
                naming_convention = 'Actual Folio'
            else:
                naming_convention = 'Landmark'
            if ri.rename_all_files_in_dir(
                values['dir_path'], values['excel_path'], naming_convention,
                values['prefix_in'], values['prefix_out'],
                values['in_place'], values['output_dir']
                    ):
                sg.popup_ok('Renaming is Complete', title='All Done')
            else:
                sg.popup_ok('Renaming was aborted before it was completed.', title='Stopped')
    window.close()

if __name__ == '__main__':
    main()
