# 回流服务SDK

## 怎么使用

1. 初始化SDK

```PYTHON
from ankerautotrainsdk import AnkerAutoTrainSDK

# 这里url可以不传，默认是国外正式环境url=https://dataloop.anker-in.com
# 如果想使用国外测试环境url=https://dataloop-qa.anker-in.com
# 如果想使用国内环境url=http://172.16.19.68:8000
# 注意数据合规问题，选择恰当的环境url
client = AnkerAutoTrainSDK(url="https://dataloop.anker-in.com") 
```
2. 上传文件

### upload_file(file_path: str, directory: str) 

#### 参数 
file_path: str 本地文件路径(可以是视频或图片)

directory: str 上传到minio的目录前缀名，如果不知道这个是干啥的，留空就可以

返回值

{
    url: str
    bucket: str
    storage_id: str
    object_name: str
    uid: str
}

使用示例
```python
client.upload_image("test.jpeg", "test")
```
3. 上传文件信息
一个文件信息必须要对应一个文件

### upload_raw_data(raw_data: dict)

#### 参数 
raw_data: dict 上传的文件对应的文件信息

返回值

{
    raw_data_id: str
}

使用示例
```python
## 上传文件
upload_response = client.upload_image("test.jpeg", "test")

## 上传文件对应的信息
resolution = {"width": 1920, "height": 1080}
sourceType = "trigger"
localEventTime = "20241024"
storage = {"storageId": upload_response.storage_id, "bucket": upload_response.bucket, "objectName": upload_response.object_name}
raw_data = {
    "uid": upload_response.uid,
    "fileMeta": {"resolution": resolution},
    "type": "image",
    "region": "CN",
    "securityLevel": "low",
    "storage": storage,
    "bg": "ap",
    "owner": "ivan.liu",
    "extra": {"localEventTime": localEventTime},
    "sourceInfo":{"type": sourceType}
}
client.upload_raw_data(raw_data)
```

4. 上传文件标注
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
## 上传文件
upload_response = client.upload_image("test.jpeg", "test")

## 上传文件对应的标注
model_name = 'test_model'
labelInfo = [{"bbox_xyxy": [4307,1834,4462,1952],"label": "poop","score": 1,"labelType": 0}]
annotation_data = {
    "annotationType": "object",
    "bg": "ap",
    "owner": "name",
    "dataId": ["b20911d85ce768742def204b032a95c7"],
    "labelInfo": labelInfo,
    "labelMethod": "auto",
    "labelScope": ["wire"],
    "modelName": model_name,
    "modelVersion": "0.1"
}
annotation_response = client.upload_annotated_data(annotation_data)

## 返回标注的ID
annotation_response.annotation_data_id
```

5. 创建数据集
数据集用于组织上传的标注文件，所以上传标注文件返回的标注annotation_data_id必须保存为一个list[]

### create_dataset(dataset_info: dict)

#### 参数 
dataset_info: dict 创建数据集的信息

返回值

{
    dataset_id: str
}

使用示例
```python
## 创建数据集
create_dataset_info = {
    "annotationBy": [],
    "annotationType": "detection",
    "bg": "ap",
    "datasetName": "test dataset",
    "datasetVersion": "v2",
    "modelType": "teacher",
    "owner": "name",
    "remark": "This is a test dataset",
    "versionType": "train"
}
create_datast_response = client.create_dataset(create_dataset_info)

## 返回数据集的ID
create_datast_response.dataset_id
```

6. 链接数据集
创建完数据集后，需要将上传标注文件返回的标注annotation_data_id链接到这个数据集上。上传的所有标注annotation_data_id必须保存为一个list[]

### link_dataset(annotation_id_list: list, dataset_id: str)

#### 参数 
annotation_id_list: list 需要组织到这个数据集的所有标注annotation_data_id list
dataset_id: str 创建的数据集dataset_id

使用示例
```python
## 创建数据集
id_list = ["66f519f20c11b8a33cd2aa7b", "66f519f20c11b8a33cd2aa7b"]

link_response = client.link_dataset(annotation_id_list=id_list, dataset_version_id=create_datast_response.dataset_id)
```

7. 下载文件
下载文件有两种方式，第一种是通过文件储存信息下载
### download_file_by_storage(storage_id: str, bucket: str, object_name: str, directory: str)

参数 
- storage_id: str 上传文件返回的storage_id
- bucket: str 上传文件返回的bucket
- object_name: str 上传文件返回的object_name
- directory: str 下载到本地的路径

使用示例
```python
client.download_image("2vcrqyykgmaql", "data-sync-storage", "2024-10-24/cables_pack.jpg", "/home/save")
```

第二种是通过文件uid下载
### def download_file_by_uid(uid: str, directory: str)
参数 
- uid: str 上传文件返回的uid
- directory: str 下载到本地的路径

使用示例
```python
client.download_image("b20911d85ce768742def204b032a95c7", "/home/save")
```

8. 下载数据集
组织好的数据集会包含原始文件的信息和标注的信息，通过json文件包含在一起。可以通过本接口下载json文件
### download_dataset(dataset_name: str, dataset_version: str, directory: str)

参数 
- dataset_name: str 需要下载的数据集的名在
- dataset_version: str 需要下载的数据集的版本
- directory: str 下载到本地的路径

使用示例
```python
download_dataset_response = client.download_dataset(dataset_name="test dataset", dataset_version="v2", directory="/home/ivan")
```