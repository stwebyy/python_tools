import os
import sys
import random
import subprocess

import termcolor

random_int = random.randint(0, 4)
COMMUNICATION = ['作業の一区切りですか？', '粒度は細かいほうが良いですね。', '結果をコミット。', '継続は力なり。', 'お疲れ様です。']


class GitFlow(object):
    def __init__(self, communication=COMMUNICATION[random_int], color='yellow'):
        self.talk = communication
        self.caution = color

    def first_method(self):
        print(self.talk)
        self.git_add()

    def git_add(self):
        add_confirm = input('現在の状態でgit addをしても良いですか？\n良ければyかyesを入力してください。終了する場合は他のキーを入力してください。\n')
        if add_confirm.strip().lower() == 'y' or add_confirm.strip().lower() == 'yes':
            try:
                add_cmd = 'git add .'
                subprocess.run(add_cmd, shell=True, check=True)
            except subprocess.CalledProcessError:
                print('git addに失敗しました。')
                sys.exit(1)
            self.git_commit()
        else:
            end_msg = termcolor.colored('スクリプトを終了します。', self.caution)
            print(end_msg)
            sys.exit(1)

    def git_commit(self):
        count = 0
        while True:
            try:
                commit_text = input('コミットメッセージを入力してください。\n')
                if count == 4:
                    five_msg = termcolor.colored('5回目の入力エラーです。スクリプトを終了します。', self.caution)
                    print(five_msg)
                    sys.exit(1)
                elif len(commit_text) < 4:
                    caution_msg = termcolor.colored('入力文字数が少なすぎます。4文字以上入力してください。', self.caution)
                    print(caution_msg)
                    count += 1
                else:
                    break
            except KeyboardInterrupt:
                sys.exit(0)
        try:
            commit_cmd = 'git commit -m {}'.format(commit_text)
            commit_cmd_finish = subprocess.run(commit_cmd, shell=True, check=True, stderr=subprocess.STDOUT)
            commit_msg = termcolor.colored('コミットメッセージは' + commit_text + 'です。', self.caution)
            print(commit_msg)
        except subprocess.CalledProcessError:
            err_msg = termcolor.colored('エラーが発生しました。', self.caution)
            err_descript = termcolor.colored(commit_cmd_finish.stderr, self.caution)
            print(err_msg)
            print(err_descript)
            sys.exit(1)
        self.git_push()

    def git_push(self):
        push_confirm = input('git pushを行ってもよろしいですか？\n良ければyかyesを入力してください。中止する場合は他のキーを入力してください。\n')
        if push_confirm.strip().lower() == 'y' or push_confirm.strip().lower() == 'yes':
            get_current_branch_name_cmd = 'git symbolic-ref --short HEAD'
            branch_name = subprocess.run(get_current_branch_name_cmd, shell=True, stdout=subprocess.PIPE)
            while True:
                final_confirm = input('branch名は ' + branch_name + ' ですね？ このbranch名でgit pushします。'
                                                                  '実行して良いならば、yかyesを入力してください。\n'
                                                                  '修正する場合はcかchangeを入力してください。\n')
                if final_confirm.strip().lower() == 'y' or final_confirm.strip().lower() == 'yes':
                    try:
                        push_cmd = 'git push origin {}'.format(branch_name)
                        git_push_run = subprocess.run(push_cmd, shell=True, check=True, stderr=subprocess.STDOUT)
                        break
                    except subprocess.CalledProcessError:
                        faild_msg = termcolor.colored('git pushに失敗しました。', self.caution)
                        print(faild_msg)
                        push_err_msg = termcolor.colored(git_push_run, self.caution)
                        print(push_err_msg)
                        sys.exit(1)
                elif final_confirm.strip().lower() == 'c' or final_confirm.strip().lower() == 'change':
                    branch_change_msg = termcolor.colored('branch名を変更します。', self.caution)
                    print(branch_change_msg)
                    branch_name = input('branch名を入力してください。\n')
        else:
            end_msg = termcolor.colored('スクリプトを終了します。コミットまで完了しました。\nコミットメッセージ'
                                        'は ' + commit_text + ' です。', self.caution)
            print(end_msg)
            sys.exit(1)
        push_complete_msg = termcolor.colored('正常にgit pushが完了しました。', caution)
        print(push_complete_msg)
        sys.exit()


if __name__ == '__main__':
    git_flow = GitFlow()
    git_flow.first_method()
else:
    termcolor.colored('git_flow.pyから実行してください。', 'yellow')
