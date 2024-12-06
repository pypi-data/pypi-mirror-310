import aiohttp
import os

class Route:
    def __init__(self, path):
        self.path = path


class BotHttp:
    def __init__(self):
        self.base_url = "http://localhost:3000"

    async def send_group_request(self, route, payload, headers, method):
        url = f"{self.base_url}{route.path}"
        async with aiohttp.ClientSession() as session:
            data = {"group_id": payload["group_id"], "message": []}
            if method == "POST":
                if payload["at"] is not None and payload["reply"] is None:
                    data["message"].append({"type":"at","data":{"qq":payload["at"]}})
                    if payload["text"] is not None:
                        data["message"].append({"type":"text","data":{"text":payload["text"]}})

                    if payload["image"] is not None:
                        # 往payload的message中添加{"type":"image","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["image]}
                        data["message"].append({"type":"image","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["image"]}})

                    if payload["face"] is not None:
                        data["message"].append({"type":"face","data":{"id":payload["face"]}})

                    if payload["jsoner"] is not None:
                        data["message"].append({"type":"json","data":{"data":payload["jsoner"]}})

                    if payload["recode"] is not None:
                        data["message"].append({"type":"reply","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["recode"]}})

                    if payload["video"] is not None:
                        data["message"].append({"type":"video","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["video"]}})

                    if payload["dic"]:
                        print("error: 错误的使用")

                    if payload["rps"]:
                        print("error: 错误的使用")

                if payload["reply"] is not None and payload["at"] is None:
                    data["message"].append({"type":"reply","data":{"id":payload["reply"]}})
                    if payload["text"] is not None:
                        data["message"].append({"type":"text","data":{"text":payload["text"]}})

                    if payload["image"] is not None:
                        # 往payload的message中添加{"type":"image","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["image]}
                        data["message"].append({"type":"image","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["image"]}})

                    if payload["face"] is not None:
                        data["message"].append({"type":"face","data":{"id":payload["face"]}})

                    if payload["jsoner"] is not None:
                        data["message"].append({"type":"json","data":{"data":payload["jsoner"]}})

                    if payload["recode"] is not None:
                        data["message"].append({"type":"reply","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["recode"]}})

                    if payload["video"] is not None:
                        data["message"].append({"type":"video","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["video"]}})

                    if payload["dic"]:
                        print("error: 错误的使用")

                    if payload["rps"]:
                        print("error: 错误的使用")

                if payload["at"] is None and payload["reply"] is None:
                    if payload["text"] is not None:
                        data["message"].append({"type":"text","data":{"text":payload["text"]}})

                    if payload["image"] is not None:
                        # 往payload的message中添加{"type":"image","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["image]}
                        data["message"].append({"type":"image","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["image"]}})

                    if payload["face"] is not None:
                        data["message"].append({"type":"face","data":{"id":payload["face"]}})

                    if payload["jsoner"] is not None:
                        data["message"].append({"type":"json","data":{"data":payload["jsoner"]}})

                    if payload["recode"] is not None:
                        data["message"].append({"type":"reply","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["recode"]}})

                    if payload["video"] is not None:
                        data["message"].append({"type":"video","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["video"]}})

                    if payload["dic"]:
                        print("error: 错误的使用")

                    if payload["rps"]:
                        print("error: 错误的使用")

                if payload["dic"]:
                    data["message"].append({"type":"dice"})

                if payload["rps"]:
                    data["message"].append({"type":"rps"})
                async with session.post(url, headers=headers, json=data) as response:
                    return await response.json()
            elif method == "GET":
                async with session.get(url, headers=headers, params=payload) as response:
                    return await response.json()
            else:
                raise ValueError("Unsupported HTTP method")

    async def send_private_request(self, route, payload, headers, method):
        url = f"{self.base_url}{route.path}"
        async with aiohttp.ClientSession() as session:
            data = {"user_id": payload["user_id"], "message": []}
            if method == "POST":
                if payload["reply"] is not None:
                    data["message"].append({"type":"reply","data":{"id":payload["reply"]}})
                    if payload["text"] is not None:
                        data["message"].append({"type":"text","data":{"text":payload["text"]}})

                    if payload["image"] is not None:
                        # 往payload的message中添加{"type":"image","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["image]}
                        data["message"].append({"type":"image","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["image"]}})

                    if payload["face"] is not None:
                        data["message"].append({"type":"face","data":{"id":payload["face"]}})

                    if payload["jsoner"] is not None:
                        data["message"].append({"type":"json","data":{"data":payload["jsoner"]}})

                    if payload["recode"] is not None:
                        data["message"].append({"type":"reply","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["recode"]}})

                    if payload["video"] is not None:
                        data["message"].append({"type":"video","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["video"]}})

                    if payload["dic"]:
                        print("error: 错误的使用")

                    if payload["rps"]:
                        print("error: 错误的使用")

                if payload["reply"] is None:
                    if payload["text"] is not None:
                        data["message"].append({"type":"text","data":{"text":payload["text"]}})

                    if payload["image"] is not None:
                        # 往payload的message中添加{"type":"image","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["image]}
                        data["message"].append({"type":"image","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["image"]}})

                    if payload["face"] is not None:
                        data["message"].append({"type":"face","data":{"id":payload["face"]}})

                    if payload["jsoner"] is not None:
                        data["message"].append({"type":"json","data":{"data":payload["jsoner"]}})

                    if payload["recode"] is not None:
                        data["message"].append({"type":"reply","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["recode"]}})

                    if payload["video"] is not None:
                        data["message"].append({"type":"video","data":{"file":"file://"+os.getcwd().replace('\\', '\\\\')+"\\"+payload["video"]}})

                    if payload["dic"]:
                        pass

                    if payload["rps"]:
                        pass

                if payload["dic"]:
                    data["message"].append({"type":"dice"})

                if payload["rps"]:
                    data["message"].append({"type":"rps"})
                async with session.post(url, headers=headers, json=data) as response:
                    return await response.json()
            elif method == "GET":
                async with session.get(url, headers=headers, params=payload) as response:
                    return await response.json()
            else:
                raise ValueError("Unsupported HTTP method")