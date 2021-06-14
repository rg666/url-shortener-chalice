# url-shortener-chalice
## _A simple URL shortener app using AWS Chalice._

[![N|Solid](https://miro.medium.com/max/1025/1*_HK9snXXUHghoixLEQWwtA.png)](https://github.com/aws/chalice)


Please make sure you configure your AWS credentials using AWS CLI before starting with deploying things onto AWS. 
```sh
aws configure
```
Dependencies are included in the file:
```sh
requirements.txt
``` 

Do note the below chalice scheduler is configured to clean up the dynamo-db table entries every 24 hours.
![alt text](https://github.com/rg666/url-shortener-chalice/blob/main/images/periodic-db-clean-up.png?raw=true)

## Deployment steps:
```sh
aws cloudformation deploy --template-file .chalice\dynamodb_cf_template.yaml --stack-name "url-shortner-stack"
```
```sh
chalice deploy
```

## Testing steps screenshots:
![alt text](https://github.com/rg666/url-shortener-chalice/blob/main/images/shorten-url.png?raw=true)
![alt text](https://github.com/rg666/url-shortener-chalice/blob/main/images/use_short_url_2.png?raw=true)
![alt text](https://github.com/rg666/url-shortener-chalice/blob/main/images/use_short_url_1.png?raw=true)
## Teardown steps:
```sh
chalice delete
```
```sh
aws cloudformation delete-stack --stack-name "url-shortner-stack"
```

