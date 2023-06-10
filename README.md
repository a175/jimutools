# jimutools

事務に提出する書類などのためのツール群


## kenshu

研修の手続きの際に事務に提出するワードファイルを生成するためのスクリプト.
加えて, それを送付するときのカバーレターの文案も生成する.

`sample.txt` のようなファイルを作成し,
```
python3 kenshu.py sample.txt
```
とやればよい.
細かいオプションは
`python3 kenshu.py --help`
でみることができる.

入力ファイルは,
テキストファイルだが,
コメントアウトできるので,
ワードファイルを直接編集するよりは便利だと思う.
また, 重複する項目はなるべく入力しなくて良いようになっているので,
入力ミスもある程度は防げると思う.


ただし,
実装をサボっているせいで,
日程表は6行以内でないといけないなどの制限はある.
必要に応じてdocxファイルを直接修正する必要があるかも知れない.

### Requirements

これを実行するには `python3`, `python-docx`が必要になる.
`python-docx` は,
```
pip install --user python-docx
```
とかやれば簡単に入れられると思う.

