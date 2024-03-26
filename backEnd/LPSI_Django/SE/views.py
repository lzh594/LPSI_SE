import json
import os
from .ssh import *
from .models import *
from django.http import JsonResponse
from collections import Counter


# Create your views here.
def index(request):
    # return render(request, 'index.html')
    return JsonResponse({"para1": "Test"})


# 处理上传上来的文件路径
def handle_uploaded_file(f, fn):
    path = r'./file/'  # 图片保存路径
    print(f"filename={fn}")
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + fn, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return path + fn


def post_data(req):
    # 对二进制数据进行解码,解码得到json数据
    json_str = req.body.decode()
    # 将json数据转化成字典形式
    return json.loads(json_str)


# 处理交给后台的命令
def processCmd(filename, kwd, mode):
    with open(filename, "r") as f:
        dbdata = f.read().replace(" ", '').replace("\n", '')
        k = []

        for i in kwd:
            k.append(i["value"])

        keyword = []
        for i in k:
            keyword.append(i)
        for i in range(len(k), 8):
            keyword.append(None)

        KeywordsHistory.objects.create(Keyword1=keyword[0], Keyword2=keyword[1], Keyword3=keyword[2],
                                       Keyword4=keyword[3], Keyword5=keyword[4], Keyword6=keyword[5],
                                       Keyword7=keyword[6], Keyword8=keyword[7])

        k = str(k).replace(" ", '').replace('\'', '\"')

        command = "./SE " + "-d" + " '" + dbdata + "' -m " + mode + " -w '" + k + "'"

        return command_SSH(command)


def uploadFile(request):
    handle_uploaded_file(request.FILES.get("file"), str(request.FILES["file"]))
    return JsonResponse({"uploadFile": "uploadFile_test"})


def upload(request):
    query_data = post_data(request)
    return JsonResponse({"upload": "upload_test", "query_data": query_data})


# 进行搜索
def search(request):
    search_query = post_data(request)
    enc_result, result = processCmd(f"./file/{search_query['QueryDB']}.json", search_query["Keywords"],
                                    search_query["QueryMode"])

    # 解析enc_result（字典=>列表）
    id = 1
    search_data = []
    for (key, values) in enc_result.items():
        table = {"id": id, "keyword": key}
        length = len(values)
        for i in range(0, length):
            table[f"inv_idx{i + 1}"] = values[i]
        for i in range(length, 6):
            table[f"inv_idx{i + 1}"] = ""
        search_data.append(table)
        id += 1

    # 将查询结果写入数据库
    length = len(result)
    for i in range(length, 4):
        result.append("")
    PlainResult.objects.create(dec_inv_idx1=result[0], dec_inv_idx2=result[1], dec_inv_idx3=result[2],
                               dec_inv_idx4=result[3])
    return JsonResponse({"search": "search_test", "search_data": search_data})


# 查询搜索结果
def result(request):
    result_query = post_data(request)

    # 从数据库中读出该次查询的结果
    last_data = PlainResult.objects.last()

    result_data = [{"id": last_data.id, "dec_inv_idx1": last_data.dec_inv_idx1, "dec_inv_idx2": last_data.dec_inv_idx2,
                    "dec_inv_idx3": last_data.dec_inv_idx3, "dec_inv_idx4": last_data.dec_inv_idx4, }]

    return JsonResponse({"result": "result_test", "result_data": result_data})


# 进行词频统计
def countWords(request):
    # 拿到所有的搜索过的关键词
    all_data = KeywordsHistory.objects.all()
    print(all_data)
    # 将所有的词语写成列表
    all_words = []
    for data in all_data:
        # 获取该条查询的所有关键词
        attributes = data.__dict__
        attribute_values = []
        for attribute_name, attribute_value in attributes.items():
            if not attribute_name.startswith("_"):
                attribute_values.append(attribute_value)
        for ele in attribute_values:
            if ele is not None and isinstance(ele, str):
                all_words.append(ele)
    # 统计词频
    wordsFrequence = Counter(all_words)

    n = 5  # 取值最大的5个关键词
    wF = sorted(wordsFrequence.items(), key=lambda item: item[1], reverse=True)
    wF = wF[:n]  # 列表内容为元组(word, count)
    words, count = zip(*wF)

    return JsonResponse({"countWords": "countWords_test", "countWords_data": {"words": words, "count": count}})
