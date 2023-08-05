## Kcaptcha API文档

---


Latest Version: 1.0.3

`pip install kcaptcha==1.0.3`

---
### 更新


#### 2022-04-18:

1. 修复打包时未能正确包含数据文件的问题。

#### 2022-04-17：

1. 已通过pypi发布。可通过`pip install kcaptcha`安装。（但是不想写文档！先忍一下[doge]）

   ```python
   from kcaptcha.core import SlideKiller
   
   
   slide_killer = SlideKiller()
   # test slide match mode
   with open('imgs/slide_match_target_1.jpg', 'rb') as f:
       test_match_target = f.read()
   with open('imgs/slide_match_bg_1.jpg', 'rb') as f:
       test_match_background = f.read()
   match_result = slide_killer.match(test_match_target, test_match_background, simple_target=True,
                                     target_threshold=(200, 300),
                                     method=4,
                                     background_threshold=(100, 200), debug=True, border=True)
   ```

   

2. 增加了debug参数，用来显示识别过程中各阶段的图片，方便调整阈值参数。

---

### 一、概述

通过 API 提供字符型验证码识别、滑块验证码的滑动距离识别、点选验证码的点击位置识别服务。

HOST： 192.168.0.155:9898

| 功能                        | URI                       | 备注                         |
| --------------------------- | ------------------------- | ---------------------------- |
| 通用字符型验证码识别        | /common/ocr/file          | 通过开源的onnx格式ai模型实现 |
| 通用点选验证码识别          | /common/det/file          | 通过开源的onnx格式ai模型实现 |
| 通用滑块验证码识别-匹配模式 | /common/slide-match/file  | 通过cv库实现                 |
| 通用滑块验证码识别-对比模式 | /common/slide-match/file  | 通过cv库实现                 |
| 极验文字点选验证码识别      | /geetest/order-click/file | 通过cv库及ai模型实现         |

可以处理的验证码示例如下：

1. 通用字符型验证

   ![image-20220413093452270](https://s2.loli.net/2022/04/13/W5wjzcYBkJATotO.png)

2. 通用点选（不带语序，仅目标识别）

   ![image-20220413093634982](C:\Users\Administrator.WINDOWS-JFG3003\Desktop\common_click.png)![image-20220413093652372](https://s2.loli.net/2022/04/13/rQAme7yap9fdnsH.png)

3. 通用滑块-匹配模式

   适用于能获取滑块图片（target_img）及带缺口背景图(bg_img)的滑块验证码，返回滑块的位置

   ![image-20220413094037039](https://s2.loli.net/2022/04/13/RI2Ly9xzQ1TnwW3.png)![image-20220413094047235](https://s2.loli.net/2022/04/13/FQfCVJaZhqyMWXU.png)

4. 通用滑块-比较模式

   适用于能获取完整背景图及带缺口背景图的滑块验证码，返回滑动距离

   ![image-20220413094223146](C:\Users\Administrator.WINDOWS-JFG3003\Desktop\2.png)![image-20220413094212874](C:\Users\Administrator.WINDOWS-JFG3003\Desktop\2.png)
   
5. 极验文字点选验证码识别

   按顺序点选文字验证码，图标形式暂未实现。

   ![image-20220413094510796](C:\Users\Administrator.WINDOWS-JFG3003\Desktop\geetest_click.png)

---

### 二、通用字符型验证码

#### 1. 请求参数（POST）

| 名称 | 类型   | 必填 | 示例           | 描述                                                         |
| ---- | ------ | ---- | -------------- | ------------------------------------------------------------ |
| img  | String | 是   | 图片二进制文件 | 图片的二进制文件，调用时把图片二进制文件放入到HTTP body 中上传即可。 |

#### 2. 返回数据

| 名称    | 类型    | 示例   | 描述     |
| ------- | ------- | ------ | -------- |
| code    | Integer | 200    | 状态码   |
| msg     | String  | ""     | 状态描述 |
| results | String  | "jepv" | 识别结果 |

#### 3. 请求示例

```python
import requests

url = HOST + '/common/ocr/file'
img_file_path = {Your Img Filepath}
files = {
    'img': ('img', open(img_file_path, 'rb'))
}
response = requests.post(url, files=files)
```


#### 4. 响应示例

```python
{"code": 200, "results": "jepv", "msg": ""}
```

---

### 三、通用点选型验证码

#### 1. 请求参数（POST）

| 名称 | 类型   | 必填 | 示例           | 描述                                                         |
| ---- | ------ | ---- | -------------- | ------------------------------------------------------------ |
| img  | String | 是   | 图片二进制文件 | 图片的二进制文件，调用时把图片二进制文件放入到HTTP body 中上传即可。 |

#### 2. 返回数据

| 名称    | 类型    | 示例                                      | 描述                                                         |
| ------- | ------- | ----------------------------------------- | ------------------------------------------------------------ |
| code    | Integer | 200                                       | 状态码                                                       |
| msg     | String  | ""                                        | 状态描述                                                     |
| results | Array   | [[131, 53, 182, 103], [214, 52, 258, 96]] | 识别结果：列表每项为一个四元组，该四元组表示一个区域，分别为**左上x坐标、左上y坐标、右下x坐标、右下y坐标**。 |

#### 3. 请求示例

```python
import requests

url = HOST + '/common/det/file'
img_file_path = {Your Img Filepath}
files = {
    'img': ('img', open(img_file_path, 'rb'))
}
response = requests.post(url, files=files)
```

#### 4. 响应示例

```python
{"code": 200, "results": [[131, 53, 182, 103], [214, 52, 258, 96], [299, 105, 350, 154], [292, 17, 341, 65]], "msg": ""}
```

![image-20220413110345937](https://s2.loli.net/2022/04/13/4UB39GMf2qjgAlX.png)

---

### 四、通用滑块验证码识别-匹配模式

#### 1. 请求参数（POST）

| 名称                     | 类型    | 必填 | 示例           | 描述                                                         |
| :----------------------- | ------- | ---- | -------------- | ------------------------------------------------------------ |
| target_img               | String  | 是   | 图片二进制文件 | 滑块图片的二进制文件，调用时把图片二进制文件放入到HTTP body 中上传即可 |
| bg_img                   | String  | 是   | 图片二进制文件 | 带缺口背景图片的二进制文件，调用时把图片二进制文件放入到HTTP body 中上传即可 |
| method                   | Integer | 否   | 4              | 进行滑块匹配的算法模式，可选值为0~4，具体算法含义可参考cv2的文档 |
| target_threshold_min     | Integer | 否   | 100            | 滑块图二值化处理的最小阈值                                   |
| target_threshold_max     | Integer | 否   | 300            | 滑块图二值化处理的最大阈值                                   |
| background_threshold_min | Integer | 否   | 100            | 背景图二值化处理的最小阈值                                   |
| background_threshold_max | Integer | 否   | 130            | 背景图二值化处理的最大阈值                                   |
| border                   | Bool    | 否   | True           | 对滑块图片处理时是否添加边框                                 |

**注**：因各类滑块验证码存在差异，当发现识别准确率不高时，可尝试调整 method、target_threshold_min、target_threshold_max、background_threshold_min、background_threshold_max、border 参数

#### 2. 返回数据

| 名称    | 类型    | 示例                                            | 描述                                                         |
| ------- | ------- | ----------------------------------------------- | ------------------------------------------------------------ |
| code    | Integer | 200                                             | 状态码                                                       |
| msg     | String  | ""                                              | 状态描述                                                     |
| results | Object  | {"target_y": 0, "target": [191, 116, 259, 184]} | 识别结果：target_y 为Y轴方向上移动的距离；target 为缺口位置，以四元组表示，分别为**左上x坐标、左上y坐标、右下x坐标、右下y坐标**。 |

#### 3. 请求示例

```python
import requests

url = HOST + '/common/slide-match/file'
target_img_file_path = {Your Img Filepath}
bg_img_file_path = {Your Img Filepath}
data = {
    'method': 4,
    'target_threshold_min': 100,
    'target_threshold_max': 300,
    'background_threshold_min': 100,
    'background_threshold_max': 130,
    'border': True
}
files = {
    'target_img': ('img', open(target_img_file_path, 'rb')),
    'bg_img': ('img', open(bg_img_file_path, 'rb')),
}
response = requests.post(url, files=files, data=data)
```

#### 4. 响应示例

```python
{"code": 200, "results": {"target_y": 0, "target": [191, 116, 259, 184]}, "msg": ""}
```

![image-20220413110455633](https://s2.loli.net/2022/04/13/3mz8NIXwWKUtlQF.png)

---

### 五、通用滑块验证码识别-对比模式

#### 1. 请求参数（POST）

| 名称        | 类型   | 必填 | 示例           | 描述                                                         |
| :---------- | ------ | ---- | -------------- | ------------------------------------------------------------ |
| full_bg_img | String | 是   | 图片二进制文件 | 完整背景图片的二进制文件，调用时把图片二进制文件放入到HTTP body 中上传即可 |
| bg_img      | String | 是   | 图片二进制文件 | 带缺口背景图片的二进制文件，调用时把图片二进制文件放入到HTTP body 中上传即可 |

#### 2. 返回数据

| 名称    | 类型    | 示例                  | 描述                                                         |
| ------- | ------- | --------------------- | ------------------------------------------------------------ |
| code    | Integer | 200                   | 状态码                                                       |
| msg     | String  | ""                    | 状态描述                                                     |
| results | Object  | {'target': [124, 79]} | 识别结果：target 为缺口位置，以二元组表示，分别为缺口左侧距做边框的距离、纵坐标。 |

#### 3. 请求示例

```python
import requests

url = HOST + '/common/slide-compare/file'
full_bg_img_path = {Your Img Filepath}
bg_img_path = {Your Img Filepath}
files = {
    'full_bg_img': ('img', open(full_bg_img, 'rb')),
    'bg_img': ('img', open(bg_img_path, 'rb')),
}
response = requests.post(url, files=files)
```

#### 4. 响应示例

```python
{"code": 200, "results": {'target': [124, 79]}, "msg": ""}
```



![image-20220413105523331](https://s2.loli.net/2022/04/13/EjN2H4k7bVpd3IA.png)

---

### 六、极验文字点选验证码识别

#### 1. 请求参数（POST）

| 名称 | 类型   | 必填 | 示例           | 描述                                                         |
| ---- | ------ | ---- | -------------- | ------------------------------------------------------------ |
| img  | String | 是   | 图片二进制文件 | 图片的二进制文件，调用时把图片二进制文件放入到HTTP body 中上传即可。 |

#### 2. 返回数据

| 名称    | 类型    | 示例                                                         | 描述                                                         |
| ------- | ------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| code    | Integer | 200                                                          | 状态码                                                       |
| msg     | String  | ""                                                           | 状态描述                                                     |
| results | Array   | [{"char": "松", "target": [149, 125, 207, 182]}, {"char": "油", "target": [9, 242, 67, 300]}, {"char": "醇", "target": [94, 25, 156, 87]}] | 识别结果：按**顺序**返回识别结果，每项中char为识别的字，target为一个四元组，分别为**左上x坐标、左上y坐标、右下x坐标、右下y坐标**。 |

#### 3. 请求示例

```python
import requests

url = HOST + '/geetest/order-click/file'
img_file_path = {Your Img Filepath}
files = {
    'img': ('img', open(img_file_path, 'rb'))
}
response = requests.post(url, files=files)
```

#### 4. 响应示例

```python
{"code": 200, "results": [{"char": "松", "target": [149, 125, 207, 182]}, {"char": "油", "target": [9, 242, 67, 300]}, {"char": "醇", "target": [94, 25, 156, 87]}], "msg": ""}
```

![image-20220413111306739](https://s2.loli.net/2022/04/13/AkUcnFvabl93T8u.png)

---

## Todo:

- [x] 通过pypi发布，以提供更便捷的使用方式

- [x] 增加可选的debug功能：调用时可返回中间的过程图，方便调整阈值等参数提高准确率

- [ ] 极验图标点选验证

- [ ] 极验语序点选验证码

- [ ] 计算式验证码处理

  
