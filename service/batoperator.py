from logging import Logger
from pathlib import Path

class BatStrOperator:
    """
    バッチファイルの文字列操作を行うクラス
    """

    def __init__(self, logger: Logger):
        """
        コンストラクタ
        :param logger: ログ出力用インスタンス
        """
        self.logger = logger

    def replace(self, target_dir: Path, target_str: str, new_content: str) -> None:
        """
        指定ディレクトリ内のbatファイルを対象に、行単位で置換を行う
        
        :param target_dir: 対象のフォルダパス (Pathオブジェクト)
        :param target_str: 検索する行の開始文字列 (例: "SET DB_HOST=")
        :param new_content: 置換後の行の内容全体 (例: "SET DB_HOST=192.168.1.1")
        """
        
        # 処理開始ログ
        self.logger.info(f'置換処理開始: キーワード="{target_str}" -> 新内容="{new_content}"')

        # フォルダ内の.batファイルをすべて取得
        bat_files = list(target_dir.glob("*.bat"))

        if not bat_files:
            self.logger.warning(f'指定フォルダ内に.batファイルが見つかりません: {target_dir}')
            return

        # 各ファイルに対して処理を実行
        for file_path in bat_files:
            self._process_single_file(file_path, target_str, new_content)

    def _process_single_file(self, file_path: Path, target_str: str, new_content: str) -> None:
        """
        単一ファイルに対する読み込み・置換・保存処理
        """
        # バッチファイルの一般的なエンコーディング (cp932: Shift_JIS)
        # **注意** UTF-8等で記述されたbatファイルが含まれる場合別途対応必須です。混在処理はできません。
        
        encoding_type = "cp932" 

        try:
            content = file_path.read_text(encoding=encoding_type, errors="ignore")
            lines = content.splitlines()

            new_lines = []
            is_changed = False

            # 2. 行ごとのチェック
            for line in lines:
                # 行の先頭が target_str で始まるかチェック（大文字小文字を区別しない）
                if line.strip().upper().startswith(target_str.upper()):
                    new_lines.append(new_content)
                    is_changed = True
                    self.logger.debug(f'[{file_path.name}] 置換対象を検出: {line.strip()} -> {new_content}')
                else:

                    new_lines.append(line)

            if is_changed:
                file_path.write_text("\n".join(new_lines), encoding=encoding_type)
                self.logger.info(f'ファイルを更新しました: {file_path.name}')
            
        except Exception as e:
            self.logger.error(f'ファイル操作中にエラーが発生しました: {file_path.name}', exc_info=True)