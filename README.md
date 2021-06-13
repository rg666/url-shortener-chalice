# url-shortener-chalice
## _A simple URL shortener app using AWS Chalice._

[![N|Solid](https://miro.medium.com/max/1025/1*_HK9snXXUHghoixLEQWwtA.png)](https://github.com/aws/chalice)


Please make sure your to configure your AWS credentials before starting with deploying things onto AWS. 
```sh
aws configure
```
Dependencies are included in the file:
```sh
requirements.txt
``` 

## Deployment steps:
```sh
aws cloudformation deploy --template-file .chalice\dynamodb_cf_template.yaml --stack-name "url-shortner-stack"
```
```sh
chalice deploy
```

## Testing steps screenshots:
![alt text](https://github.com/rg666/url-shortener-chalice/blob/main/tests/shorten-url.png?raw=true)
![alt text](https://github.com/rg666/url-shortener-chalice/blob/main/tests/use_short_url_2.png?raw=true)
![alt text](https://github.com/rg666/url-shortener-chalice/blob/main/tests/use_short_url_1.png?raw=true)
## Teardown steps:
```sh
chalice delete
```
```sh
aws cloudformation delete-stack --stack-name "url-shortner-stack"
```

