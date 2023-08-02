12306py

## 功能介绍
```
    在火车票预售当天，自动抢票。
    典型的场景是抢列车的卧铺票。

```

## Usage
### 1、加入待购票乘车人信息到登录账号
```
    乘客姓名需要提前在12306账号中设置联系人信息。
```

### 2、修改配置
```
修改.env文件
```
### 3、运行
```
	python3 app.py
```

### 4、输入短信验证码 
```
等待跳出浏览器页面，手动完成短信验证码输入，点击确定。
（如果无短信验证，则忽略这一步）
```
### 5、完成支付
```
等待自动完成选票、提交订单，完成后自行支付订单
```

## 环境说明
### Python版本 3.X
### 依赖包
```
pip install -r requirements.txt
```
### chromedriver
```
请参见：https://chromedriver.chromium.org/home

```