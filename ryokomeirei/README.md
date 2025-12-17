# ryokomeirei

## summary

外部機関経費の出張
手続きの際に事務に提出するワードファイルを生成するためのスクリプト.
加えて, それを送付するときのカバーレターの文案も生成する.

`src/sample.txt` のようなファイルを作成し,
```
python3 ryokomeirei.py sample.txt
```
とやればよい.
細かいオプションは
`python3 ryokomeirei.py --help`
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
必要に応じてxlsxファイルを直接修正する必要があるかも知れない.

### Requirements

これを実行するには `python3`, `python-openpyxl`が必要になる.
`python-openpyxl` は,
```
pip install --user python-openpyxl
```
とかやれば簡単に入れられると思う.
Debianで管理権限があれば以下でも入れられる.
```
apt-get install  python3-openpyxl
````


### Change Log
2024年3月の様式改定に対応.
           
