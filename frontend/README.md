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

## CI/CD 環境の準備
ステージング用のバケットを用意
```
$ aws s3 mb s3://todo-frontend-staging
$ aws s3 website s3://todo-frontend-staging --index-document index.html
$ aws s3api put-bucket-policy --bucket todo-frontend-staging --policy file://bucket-policy-staging.json
```
CodeCommit のリポジトリを作成
```
$ aws codecommit create-repository --repository-name todo-frontend
```
CodePipeline用の IAM ロールとポリシーを作成、アタッチする
```
$ aws iam create-role --role-name frontend-deploy --assume-role-policy-document file://deploy-assume-role-policy.json
$ aws iam create-policy  --policy-name frontend-deploy-policy --policy-document file://deploy-policy.json
$ aws iam attach-role-policy --role-name frontend-deploy --policy-arn <your-policy-arn>
```

CodeBuild用の IAM ロールとポリシーを作成、アタッチする
```
$ aws iam create-role --role-name frontend-build --assume-role-policy-document file://build-assume-role-policy.json
$ aws iam create-policy  --policy-name frontend-build-policy --policy-document file://build-policy.json
$ aws iam attach-role-policy --role-name frontend-build --policy-arn <your-policy-arn>
```

CodePipelineに登録する
```
$ aws s3 mb s3://frontend-artifact
$ aws codepipeline create-pipeline --cli-input-json file://pipeline.json
$ aws codebuild create-projekut --cli-input-json file://project.json
```

### フロントエンドの動作確認
```
$ git init .
$ git config --global credential.helper '!aws codecommit credential-helper $@'
$ git config --global credential.UseHttpPath true
$ git add -A .
$ git commit -m "initial commit"
$ git remote add codecommit https://<frontend-repo-url>
$ git push codecommit master
```


