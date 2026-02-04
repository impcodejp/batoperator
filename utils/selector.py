import os
import tkinter as tk
from tkinter import filedialog

class DirSelector:
    """
    フォルダ選択用のダイアログを開くヘルパーくらすです。
    """
    def __init__(self, default_dir=None):
        # 指定されたディレクトリが存在するか確認し、なければカレントディレクトリをデフォルトにします
        if default_dir and os.path.exists(default_dir):
            self.default_dir = default_dir
        else:
            self.default_dir = os.getcwd()
            
    def select(self, title="フォルダを選択してください"):
        """
        ダイアログを開き、指定されたパスを返します。
        ユーザーがキャンセルした場合は None を返します。
        """
        root = tk.Tk()
        root.withdraw()  
        
        root.attributes('-topmost', True)

        selected_path = filedialog.askdirectory(
            initialdir=self.default_dir,
            title=title
        )

        root.destroy()

        return selected_path if selected_path else None