# フロントエンド
## Amazon S3 での静的ウェブサイトのホスティング
 `Transcyript` をインストール
```
$ pip3 install -r requirements.txt
 ```
S3 でバケットを作成し、静的ウェブサイトのホスティングを有効にし、`bucket-policy.json` をもとにポリシーを設定
```
$ aws s3 mb s3://todo-frontend
$ aws s3 website s3://todo-frontend --index-document index.html
$ aws s3api put-bucket-policy --bucket todo-frontend --policy file://buvcket-policy.json
```
`Transcrypt` を使ってJavaScryptを生成し、S3 へファイルをアップロード。その際、deploy ディレクトリは下記のような構成とする。
```
$ cd ~/todo-app-aws/frontend/
$ transcrypt -b frontend
$ mkdir deploy
$ cp -r __traget__/ deploy/
$ aws s3 sync deploy s3://todo-frontend
```
Web ブラウザーで `http://<バケット名>.s3-website-<リージョン名>.amazonaws.com/` へアクセス

