from utils.selector import DirSelector
from utils.logger import setup_logging
from service.batoperator import BatStrOperator
from logging import Logger
from pathlib import Path
import os

class Main:
    """
    アプリケーションのメイン処理クラス
    """
    def __init__(self):
        main_script_dir: str = os.path.dirname(os.path.abspath(__file__))
        log_dir: str = os.path.join(main_script_dir, 'logs')
        
        self.logger: Logger = setup_logging(log_dir)
        self.dir_selector = DirSelector(main_script_dir)
        self.bat_str_operator = BatStrOperator(logger=self.logger)
        self.logger.info('メインプロセス初期化完了')
        
    def main_process(self):
        self.logger.info('メインプロセス実行')
        bat_folder_str = self.dir_selector.select(title='batファイルを書くのしているフォルダを選択してください')
        
        if not bat_folder_str:
            self.logger.error('フォルダ選択がキャンセルされました。処理を終了します')
            return
        
        bat_folder = Path(bat_folder_str)
        
        target_str_list = []
        new_line_content_list = []
        
        if len(target_str_list) != len(new_line_content_list):
            self.logger.error('置換元と置換後で指定の数が一致しません。処理を終了します。')
            return
        
        for i in range(len(target_str_list)):
            target_str = target_str_list[i]
            new_line_content = new_line_content_list[i]
            
            self.bat_str_operator.replace(bat_folder, target_str, new_line_content)
            

if __name__ == '__main__':
    MAIN = Main()
    MAIN.main_process()
    


    