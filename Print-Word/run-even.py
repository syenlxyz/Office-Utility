from alive_progress import alive_it
from datetime import datetime
from pathlib import Path
from win32com.client import Dispatch
from win32print import SetDefaultPrinter

WdPrintOutPages = {
    'AllPages': 0,
    'EvenPagesOnly': 2,
    'OddPagesOnly': 1
}

def run():
    input_path = Path.cwd() / 'input'
    if not input_path.is_dir():
        input_path.mkdir()
    
    options = {
        'length': 70,
        'spinner': 'classic',
        'bar': 'classic2',
        'receipt_text': True,
        'dual_line': True
    }
    
    target_printer = 'EPSON L3150 Series'
    SetDefaultPrinter(target_printer)
    
    file_list = []
    path_list = list(input_path.glob('**/*'))
    for path in path_list:
        if path.suffix in ['.doc', '.docx']:
            file_list.append(path)
    
    results = alive_it(
        file_list, 
        len(file_list), 
        finalize=lambda bar: bar.text('Printing Word (Even Pages Only): done'),
        **options
    )
    
    params = {
        'Background': False,
        'Append': False,
        'Range': 0,
        'OutputFileName': '',
        'From': '',
        'To': '',
        'Item': 0,
        'Copies': 1,
        'Pages': '',
        'PageType': WdPrintOutPages['EvenPagesOnly'],
        'PrintToFile': False,
        'Collate': True
    }
    
    wrd = Dispatch('Word.Application')
    wrd.Visible = False
    wrd.Options.PrintReverse = True
    for file_path in results:
        results.text(f'Printing Word (Even Pages Only): {file_path.name}')
        wrd.Documents.Open(str(file_path))
        num_page = wrd.ActiveDocument.ComputeStatistics(Statistic=2)
        if num_page % 2:
            wrd.Selection.GoTo(3, -1)
            wrd.Selection.EndKey()
            wrd.Selection.InsertNewPage()
        wrd.ActiveDocument.PrintOut(**params)
        wrd.ActiveDocument.Close(SaveChanges=False)
    wrd.Options.PrintReverse = False
    wrd.Quit()

if __name__ == '__main__':
    print(f'Running {Path(__file__).parent.name}')
    start_time = datetime.now()
    run()
    end_time = datetime.now()
    run_time = end_time - start_time
    print(f'Execution time: {run_time}')