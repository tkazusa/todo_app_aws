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

