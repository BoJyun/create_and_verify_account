##  Getting Started
### Pull the docker image
```
$ docker pull bojyun/restful:1.1
```

### Execute inside docker container
```
$ docker run -d -p "$SERVER_IP":8000 bojyun/restful:1.1
```

#  API document
## Create Account

`POST` /account/api/user
### Parameters
|Name |Description|
|-----|--------|
|body |{"username":"string","password":"string"} |

### Response
|code |Description|
|-----|--------|
|200  |	successful operation {"success":true,"reason":"Account create success"} |
|400  |	Fail operation {"success":false,"reason":"Username is too short or too long"} |
|400  |	Fail operation {"success":false,"reason":"password is too short or too long"} |
|400  |	Fail operation {"success":false,"reason":"password must have at least 1 uppercase letter, 1 lowercase letter and 1 number"} |


## Verify Account and Password
`POST` /account/api/user/auth
### Parameters
|Name |Description|
|-----|--------|
|body |{"username":"string","password":"string"} |

### Response
|code |Description|
|-----|--------|
|200  |	successful operation {"success":true,"reason":"Account verify success"} |
|401  |	Fail operation {"success":false,"reason":"You may have entered the wrong username or password"} |
|423 |	Fail operation {"success":false,"reason":"This account has been locked, Please try again after one minute"} |
