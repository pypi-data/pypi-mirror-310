import requests
import hashlib
import datetime

from PIL import Image
from moviepy.editor import VideoFileClip

from os.path import join, dirname, abspath, basename, exists
from os import makedirs
from .types import *

class AnkerAutoTrainSDK:
    def __init__(self, url="https://dataloop.anker-in.com"):
        self.url = url

    def _calculate_md5(self, file_path: str) -> str:
        """计算文件的MD5哈希值"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
        except IOError as e:
            raise Exception(f"Error reading file {file_path}: {e}")
        return hash_md5.hexdigest()
    
    def _get_file_meta(self, file_path: str) -> FileMeta:
        """获取文件的宽度和高度，如果是视频，还返回时长"""
        try:
            # Try to open the file as an image
            with Image.open(file_path) as img:
                width, height = img.size
                resolution = Resolution(width=width, height=height)
                return FileMeta(resolution=resolution, tokenLength=0, duration=0)
        except IOError:
            # If it fails, try to open the file as a video
            try:
                with VideoFileClip(file_path) as video:
                    width, height = video.size
                    duration = int(video.duration)  # Convert duration to int
                    resolution = Resolution(width=width, height=height)
                    return FileMeta(resolution=resolution, tokenLength=0, duration=duration)
            except Exception as e:
                # If it fails, return a default FileMeta and log the error
                print(f"Error reading file {file_path}: {e}")
                return None
            
    def _query_origin_data(self, query_data: dict) -> dict:
        try:
            url = f"{self.url}/query_origin_data"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=query_data)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while querying origin data: {detail}")
            else:
                raise Exception(f"HTTP error occurred while querying origin data: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while querying origin data: {e}")
        
    def _summarize_and_download(self, dataset_name: str, dataset_version: str) -> SummaryAndDownloadDataSetResponse:
        try:
            url = f"{self.url}/data/annotation/summarize_and_download"
            headers = { 'accept': 'application/json', 'Content-Type': 'application/json' }
            dataset_list = [{"datasetName": dataset_name, "datasetVersion": dataset_version}]
            dataset_info = {"dataset": dataset_list}
            response = requests.post(url, headers=headers, json=dataset_info)
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return SummaryAndDownloadDataSetResponse(
                url=response.get("url", ""),
                bucket=response.get("bucketName", ""),
                object_name=response.get("objectName", "")
            )
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while summarizing and downloading dataset: {detail}")
            else:
                raise Exception(f"HTTP error occurred while summarizing and downloading dataset: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while summarizing and downloading dataset: {e}")
        
    def upload_file(self, file_path: str, directory: str = "") -> UploadFileResponse:
        # get upload url
        try:
            url = f"{self.url}/get_upload_url"
            file_name = basename(file_path)
            response = requests.post(url, params={"directory": directory, "file_name": file_name})
            response.raise_for_status()  # Check for HTTP errors
            response = response.json()
        except requests.exceptions.RequestException as e:
            detail = None
            if response is not None:
                try:
                    detail = response.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            print(f"HTTP error occurred while getting upload URL: {detail or str(e)}")
            raise Exception(f"HTTP error occurred while getting upload URL: {detail or str(e)}")
        except Exception as e:
            print(f"An error occurred while getting upload URL: {e}")
            raise Exception(f"An error occurred while getting upload URL: {e}")

        # upload file by url
        try:
            upload_url = response.get("url")  # Get the upload URL from the response
            if not upload_url:
                raise Exception("No upload URL found in the response.")
            file_md5 = self._calculate_md5(file_path)  # Calculate the file's MD5
            file_meta = self._get_file_meta(file_path)  # Get the file's metadata
            # Then put to this path
            with open(file_path, "rb") as f:
                res = requests.put(upload_url, data=f)
                res.raise_for_status()  # Check for HTTP errors
                return UploadFileResponse(
                    url=upload_url,
                    bucket=response.get("bucket", ""),
                    storage_id=response.get("storage_id", ""),
                    object_name=response.get("object_name", ""),
                    uid=file_md5,
                    meta=file_meta
                )
        except requests.exceptions.RequestException as e:
            detail = None
            if res is not None:
                try:
                    detail = res.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading file: {detail or str(e)}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading file: {e}")
        
    # def upload_file(self, file_path: str, directory: str = "") -> UploadFileResponse:
    #     try:
    #         url = f"{self.url}/get_upload_url"
    #         file_name = basename(file_path)
    #         response = requests.post(url, params={"directory": directory, "file_name": file_name})
    #         response.raise_for_status()  # 检查HTTP错误
    #         response = response.json()
    #     except requests.exceptions.RequestException as e:
    #         if response is None:
    #             raise Exception(f"HTTP error occurred while getting upload URL: {e}")
    #         detail = response.json().get("detail")
    #         raise Exception(f"HTTP error occurred while getting upload URL: {detail}")
    #     except ValueError as e:
    #         raise Exception(f"Error parsing JSON response: {e}")
    #     except Exception as e:
    #         raise Exception(f"An error occurred while getting upload URL: {e}")
    
        
    #     try:    
    #         upload_url = response.get("url")  # 从响应中获取上传URL
    #         if not upload_url:
    #             raise Exception("No upload URL found in the response.")
    #         file_md5 = self._calculate_md5(file_path)  # 计算文件的MD5
    #         # 然后put到这个路径
    #         with open(file_path, "rb") as f:
    #             res = requests.put(upload_url, data=f)
    #             res.raise_for_status()  # 检查HTTP错误
    #             return UploadFileResponse(
    #                 url=upload_url,
    #                 bucket=response.get("bucket", ""),
    #                 storage_id=response.get("storage_id", ""),
    #                 object_name=response.get("object_name", ""),
    #                 uid=file_md5
    #             )
    #     except requests.exceptions.RequestException as e:
    #         if res is None:
    #             raise Exception(f"HTTP error occurred while uploading file: {e}")
    #         detail = res.json().get("detail")
    #         raise Exception(f"HTTP error occurred while uploading file: {detail}")
    #     except Exception as e:
    #         raise Exception(f"An error occurred while uploading file: {e}")
    
    def upload_raw_data(self, raw_data: dict) -> UploadRawDataResponse:
        try:
            url = f"{self.url}/upload_raw_data"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            print(f"upload raw_data: {raw_data}")
            response = requests.post(url, headers=headers, json=raw_data)
            response.raise_for_status()  # 检查HTTP错误
            response_json = response.json()
            if response_json.get("raw_data_id") is None:
                print(f"Failed to upload raw data: {response_json.get('detail', 'No detail provided')}")
            return UploadRawDataResponse(
                raw_data_id=raw_data.get("raw_data_id", "")
            )
        except requests.exceptions.RequestException as e:
            detail = None
            if response is not None:
                try:
                    detail = response.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading raw data: {detail or str(e)}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading raw data: {e}")
        
    # def upload_raw_data(self, raw_data: dict) -> UploadRawDataResponse:
    #     try:
    #         url = f"{self.url}/upload_raw_data"
    #         headers = {
    #             'accept': 'application/json',
    #             'Content-Type': 'application/json'
    #         }  # 设置请求头
    #         response = requests.post(url, headers=headers, json=raw_data)
    #         response.raise_for_status()  # 检查HTTP错误
    #         response = response.json()
    #         return UploadRawDataResponse(
    #             raw_data_id=response.get("raw_data_id", "")
    #         )
    #     except requests.exceptions.RequestException as e:
    #         if response is None:
    #             raise Exception(f"HTTP error occurred while uploading raw data: {e}")
    #         detail = response.json().get("detail")
    #         raise Exception(f"HTTP error occurred while uploading raw data: {detail}")
    #     except ValueError as e:
    #         raise Exception(f"Error parsing JSON response: {e}")
    #     except Exception as e:
    #         raise Exception(f"An error occurred while uploading raw data: {e}")

    def upload_data_with_info(self, raw_data: dict, file_path: str, directory: str = "") -> UploadRawDataResponse:
        try:
            # 上传文件
            upload_file_response = self.upload_file(file_path, directory)
            raw_data["uid"] = upload_file_response.uid
            raw_data["storage"] = {"objectName": upload_file_response.object_name, "storageId": upload_file_response.storage_id, "bucket": upload_file_response.bucket}
            
            if upload_file_response.meta is not None:
                resolution = {"width": upload_file_response.meta.resolution.width, "height": upload_file_response.meta.resolution.height}
                fileMeta = {"resolution": resolution, "tokenLength": upload_file_response.meta.tokenLength, "duration": upload_file_response.meta.duration}
                raw_data["fileMeta"] = fileMeta

            if raw_data.get("securityLevel") is None:
                raw_data["securityLevel"] = "medium"

            if raw_data.get("fileState") is None:
                raw_data["fileState"] = 0

            extra = raw_data.setdefault("extra", {})
            if extra.get("localEventTime") is None:
                extra["localEventTime"] = datetime.datetime.now().strftime("%Y%m%d")

            upload_info_response = self.upload_raw_data(raw_data)
            # print(f"Raw data uploaded with file: {raw_data}")
            return upload_info_response
        except requests.exceptions.RequestException as e:
            detail = None
            if e.response is not None:
                try:
                    detail = e.response.json().get("detail", "No detail provided")
                except ValueError:
                    detail = "No detail provided"
            raise Exception(f"HTTP error occurred while uploading data with info: {detail or str(e)}")
        except Exception as e:
            raise Exception(f"Failed to upload data with info: {str(e)}")
        
    def upload_annotated_data(self, annotated_data: dict) -> UploadAnnotationDataResponse: 
        try:
            url = f"{self.url}/data/annotation"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=annotated_data)
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
            return UploadAnnotationDataResponse( 
                annotation_data_id=response.get("id", "")
            )
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while uploading annotated data: {detail}")
            else:
                raise Exception(f"HTTP error occurred while uploading annotated data: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading annotated data: {e}")


    def download_file_by_storage(self, storage_id: str, bucket: str, object_name: str, directory: str) -> str:
        try:
            url = f"{self.url}/get_download_url"
            response = requests.post(url, params={"storage_id": storage_id, "bucket": bucket, "object_name": object_name})
            response.raise_for_status()  # 检查HTTP错误
            response = response.json()
        except requests.exceptions.RequestException as e:
             if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while getting download URL: {detail}")
             else:
                raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")
        
        try:
            download_url = response.get("url")  # 从响应中获取下载URL
            if not download_url:
                raise Exception("No download URL found in the response.")
            response = requests.get(download_url)
            response.raise_for_status()  # 检查HTTP错误
            # 保存到本地
            save_path = join(directory, object_name)
            # 判断目录是否存在
            if not exists(dirname(save_path)):
                makedirs(dirname(save_path))
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while downloading file: {detail}")
            else:
                raise Exception(f"HTTP error occurred while downloading file: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while downloading file: {e}")
        
    def download_file_by_uid(self, uid: str, directory: str) -> str:
        try:
            query_origin_data = { "uid": uid }
            origin_data = self._query_origin_data(query_origin_data)

            if not origin_data:  # 检查origin_data是否为空
                raise Exception("No origin data found for the given UID.")
            records = origin_data.get("records")

            if not records or len(records) == 0:  # 检查records是否为空
                raise Exception("No origin data found for the given UID.")

            record = records[0]  # 获取第一个记录
            get_uid = record.get("uid")
            if not get_uid or get_uid != uid:
                raise Exception("UID mismatch.")
            storage = record.get("storage")
            storage_id = storage.get("storageId")
            bucket = storage.get("bucket")
            object_name = storage.get("objectName")
            if not storage_id or not bucket or not object_name:
                raise Exception("Missing storage_id, bucket or object_name in origin data.")
            return self.download_file_by_storage(storage_id, bucket, object_name, directory)  # 调用原始下载方法
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP error occurred while getting download URL: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while getting download URL: {e}")

    def create_dataset(self, dataset_info: dict) -> CreateDataSetResponse:
        try:
            url = f"{self.url}/data/annotation/version"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            response = requests.post(url, headers=headers, json=dataset_info)
            response.raise_for_status()  # 棃查HTTP错误
            response = response.json()
            return CreateDataSetResponse(
                dataset_id=response.get("dataset_version_id", "")
            )
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while creating dataset: {detail}")
            else:
                raise Exception(f"HTTP error occurred while creating dataset: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while creating dataset: {e}")
        
    def link_dataset(self, annotation_id_list: list, dataset_id: str) -> dict:
        try:
            # 去除annotation_id_list中的重复元素
            unique_annotation_id_list = list(set(annotation_id_list))
            
            url = f"{self.url}/data/annotation/link"
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }  # 设置请求头
            dataset_info = {
                "annotationIds": unique_annotation_id_list,
                "annotationVersionId": dataset_id
            }
            response = requests.post(url, headers=headers, json=dataset_info)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while linking dataset: {detail}")
            else:
                raise Exception(f"HTTP error occurred while linking dataset: {e}")
        except ValueError as e:
            raise Exception(f"Error parsing JSON response: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while linking dataset: {e}")
        
    def download_dataset(self, dataset_name: str, dataset_version: str, directory: str) -> str:
        try:
            download_response = self._summarize_and_download(dataset_name, dataset_version)

            download_url = download_response.url  # 从响应中获取下载URL
            download_object_name = download_response.object_name
            if not download_url:
                raise Exception("No download URL found in the download_dataset.")
            response = requests.get(download_url)
            response.raise_for_status()  # 检查HTTP错误
            # 保存到本地
            save_path = join(directory, download_object_name)
            # 判断目录是否存在
            if not exists(dirname(save_path)):
                makedirs(dirname(save_path))
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
        except requests.exceptions.RequestException as e:
            if response is not None:
                detail = response.json().get("detail", "No detail provided")
                raise Exception(f"HTTP error occurred while downloading dataset: {detail}")
            else:
                raise Exception(f"HTTP error occurred while downloading dataset: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while downloading dataset: {e}")