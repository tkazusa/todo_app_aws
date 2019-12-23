# Amazon Web Service を活用した ToDo 管理アプリ
## 概要
[ほぼPythonだけでサーバーレスアプリをつくろう（技術の泉シリーズ）](https://nextpublishing.jp/book/10940.html) を参考にしました。

## 利用したサービス
- [AWS Chalice](https://github.com/aws/chalice)
- [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
- [AWS CodeCommit](https://aws.amazon.com/codecommit/)
- [AWS CodeBuild](https://aws.amazon.com/codebuild/)
- [AWS CodePipeline](https://aws.amazon.com/codepipeline/)

## Requirements
- Python 3.7.3
- AdoptOoenJDK 11.0.3+7
- Chalice 1.9.185
- Transcrypt 3.7.16
- Boto3 1.9.185
- pytest 5.3.1
- Requests 2.22.0

## 手順
### OpoenJDK 11(LTS)のインストール
[OpoenJDK 11(LTS)](https://openjdk.java.net/projects/jdk/11/)をインストール。
```bash
$ sudo apt install openjdk-11-jdk
```

### HTTPie のインストール
[HTTPie](https://httpie.org/) をインストール。
```bash
$ sudo apt install httpie
$ http httpie.org
```

### AWSユーザー の Access key IDと Secret access key を取得
[AWS マネジメントコンソール上](https://aws.amazon.com/jp/console/)で IAMユーザー を設定。「プログラムによるアクセス」を選択し、既存の「AdministratorAccess」ポリシーをアタッチしたユーザーを作成。Access key と Secret access key を保存。

### Python パッケージのインストール
Chalice をインストールする際に、`pip3`のバージョンが低いと`pip3` を破壊する可能性がある。
```bash
$ pip3 install --upgrade pip
$ pip3 install -r requirements.txt
```

### AWS CLI のインストールと認証情報の設定
```bash
$ aws configure
```

### バックエンド
詳細は[こちら](https://github.com/tkazusa/todo_app_aws/tree/master/backend)を確認下さい。

### フロントエンド
詳細は[こちら](https://github.com/tkazusa/todo_app_aws/tree/master/frontend)を確認下さい。

