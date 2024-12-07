# 回流服务SDK

## 怎么使用

1. 初始化SDK

```PYTHON
from datalakesdk import DataLakeSDK

client = DataLakeSDK()
```
1. 同时上传文件和文件信息
在上传文件的同时上传文件信息

### upload_data_with_info(raw_data: dict, file_path: str, directory: str)

#### 参数 
raw_data: dict 上传的文件对应的文件信息

file_path: str 本地文件路径(可以是视频或图片)

directory: str 上传到minio的目录前缀名，如果不知道这个是干啥的，留空就可以

返回值

{
    raw_data_id: str
}

使用示例
```python
## 上传文件
upload_response = client.upload_data_with_info("test.jpeg", "test")

## 上传文件对应的信息
sourceType = "collect"
raw_data = {
    "type": "image",
    "region": "CN",
    "bg": "Appliances",
    "owner": "xxx.xx",
    "sourceInfo":{"type": sourceType},
    "meta": {}
}
client.upload_raw_data(raw_data)
```

2. 上传文件标注
一个文件标注必须要对应一个文件
多个文件标注可以对应一个文件

### upload_annotated_data(annotated_data: dict)

#### 参数 
annotated_data: dict 上传的文件对应的标注信息

返回值

{
    annotation_data_id: str
}

使用示例
```python
## 上传文件对应的标注
labelInfo = [{"bbox_xyxy": [4307,1834,4462,1952],"label": "shoes","score": 0.3,"labelType": 0}]
annotation_data = {
    "dataId": ["1b49483de4233df15fb5b92a05bebe8e"],
    "annotationType": "detection",
    "labelScope": ["shoes"],
    "labelInfo": labelInfo,
    "bg": "Appliances",
    "owner": "ivan.liu",
    "labelMethod": "auto",
    "modelName": "test_model",
    "modelVersion": "0.1",
    "processState": "student",
    "reviewed": 0,
    "modelType": "student"
}
annotation_response = client.upload_annotated_data(annotation_data)

## 返回标注的ID
annotation_response.annotation_data_id
```