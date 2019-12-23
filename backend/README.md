# バックエンド
## `dev` 環境の構築
### DynamoDB local の準備
DynamoDB local のインストール
```
$ mkdir ./dynamolocal
$ cd ./dynamolocal
$ wget http://dynamodb-local.s3-website-us-west-2.amazonaws.com/dynamodb_local_latest.tar.gz
$ tar xzf dynamodb_local_latest.tar.gz
$ rm -f dynamodb_local_latest.tar.gz 
```
DynamoDB local の起動
```
$ cd dynamolocal
$ java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -port 8001
```
`schema.json` のあるディレクトリで下記を実行し、スキーマの定義
```
$ aws dynamodb create-table --cli-input-json file://schema.json --endpoint-url http://localhost:8001
```
初期データの投入
```
$ aws dynamodb batch-write-item --request-items file://initial-data.json --endopoint-url http://localhost:8001
$ aws dynamodb scan --table-name Todos --endpoint-url http://localhost:8001
```

### ローカルへのデプロイ
```
$ chalice deploy --stage dev
$ http http://127.0.0.1:8000/todos
```


## `prod` 環境の構築
### DynamoDB の準備
`schema.json` のあるディレクトリで下記を実行し、スキーマの定義
```
$ aws dynamodb create-table --cli-input-json file://schema.json
```
`initial-data.json` のあるディレクトリで下記を実行し、データを投入
```
$ aws dynamodb batch-write-item --request-item file://initial-data.json
```

### AWS 環境へのデプロイ
```
$ chalice deploy --stage prod
$ http http://<your-api-url>/todos
```

## CI/CD 環境の準備
chalise でCodeCommitの設定ファイルを作成する。
```
$ chalice generate-pipeline pipeline.json -b buildspec.yml
```
```
$ aws cloudformation deploy --stack-name backend-stack --template-name pipeline.json --capabilities CAPABILITIY_IAM
$ aws cloudformation describe --stack-name backend-stack
```
`OutputKey` が `SourceRepoURL` の要素で、その `OutputValue` がリポジトリの URL である
CodeCommit のリポジトリへAWSの認証情報を付与し、プッシュする
```
$ git init .
$ git config --global credential.helper '!aws codecommit credential-helper $@'
$ git config --global credential.UseHttpPath true
$ git add -A .
$ git commit -m "initial commit"
$ git remote add codecommit https://<backend-repo-url>
$ git push codecommit master
```

### バックエンドの動作確認
下記コマンドでステージング環境の `URL` を調べ、エンドポイント URL に対して API をコールする。
```
$ aws cloudformation describe-stacks --stack-name backendBetaStack
$ http https://<your-staging-api-url>/todos
```
## テスト
`pytest` を使ってユニットテストを実行します
```
pytest tests/unit
```
