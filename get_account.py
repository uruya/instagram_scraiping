from instaloader import Profile
import instaloader
import time

class GetAccountDetails:
    """アカウント詳細情報取得
    """
    # 今回取得する項目
    # ・プロフィールURL
    # ・ユーザー名
    # ・プロフィール文章
    # ・フォロワー数
    def __init__(self):
        self.account_list = []
        self.login = False
        self.session = False
        self.logout = False
        self.error_text = "取得失敗"
        self.instaloader = instaloader.Instaloader()

    def get_account_details(self, scraping, target_account_list):
        for account in target_account_list:
            self.info = {}
            if scraping:
                # スクレイピング(UI変わるのであまり使えない)
                pass
            else:
                self.exec_instaloader("", "", account)

    def exec_instaloader(self, login_name, login_password, target_account):
        # 初回ログイン
        if not self.login:
            try:
                # ログインなしでも可能だが、複数回行うと途中でログインが促される
                # ※2023年現在エラーになる
                self.instaloader.login(login_name, login_password)
            except Exception as e:
                print(f"instaloaderログイン失敗: {e}")
        if not self.login and not self.session:
            # ログイン失敗時、セッション読み込みした方がいいのか謎
            # セッション読み込み時、実行前にFireFoxでinstagramログイン状態で、session.py実行し、ファイルDLしておく
            try:
                self.instaloader.load_session_from_file(login_name, "")
            except Exception as e:
                print(f'instaloaderセッション読み込み失敗: {e}')


        try:
            # アカウント情報取得
            profile = Profile.from_username(self.instaloader.context, target_account)
            time.sleep(20)

            # 表示名取得
            # self.info["profile_name"] = profile.full_name
            # プロフィール文章
            self.info["description"] = profile.biography
            # ユーザー名
            self.info["username"] = profile.username
            # フォロワー数
            profile.followers
            # プロフィールURL
            f'https://www.instagram.com/{profile.username}/'

        except Exception as e:
            print(e)

        self.account_list.append(self.info)