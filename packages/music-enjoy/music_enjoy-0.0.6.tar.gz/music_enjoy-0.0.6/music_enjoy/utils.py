import requests

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
ORIGIN = 'https://www.bilibili.com'
REFERER = 'https://www.bilibili.com/'

def getPage(url, dest, encoding):
    headers = {
        'User-Agent': USER_AGENT,
    }
    response = requests.get(url=url, headers=headers).content.decode(encoding=encoding)
    print(response.status_code)
    fw = open(dest, 'w', encoding='utf-8')
    fw.write(response)
    fw.close()
    return

def download(url, dest):
    headers = {
        'User-Agent': USER_AGENT,
        "Origin": ORIGIN,
        "Referer": REFERER,
    }

    try:
        response = requests.get(url, headers=headers, stream=True, verify=True)
        print(response.status_code)
        with open(dest, 'wb') as fw:
            for chunk in response.iter_content(1024):
                fw.write(chunk)
                fw.flush()  # 清空缓存
    except Exception as e:
        print("url下载错误: %s" % url)
        print(e)

    return