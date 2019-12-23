## API テストの実行
### API テスト用の DynamoDB local の準備
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
$ aws dynamodb batch-write-item --request-items file://initial-data-api-test.json --endopoint-url http://localhost:8001
$ aws dynamodb scan --table-name Todos --endpoint-url http://localhost:8001
```

### ローカルへのデプロイ
```
$ chalice deploy --stage dev
$ http http://127.0.0.1:8000/todos
```
### API テスト用の仮想環境を用意
```
$ python -m venv ~/todo_app_aws/.venv/api-tests
```

### API テスト
```
$ pytest 
```

