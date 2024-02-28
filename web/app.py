from flask import Flask, render_template, jsonify, request
import requests
import time
from tdx_proxy import TDXProxy
from urllib.error import URLError
from socket import timeout
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
# 請添加app_id 及 app_key
proxy = TDXProxy(app_id="", app_key="")
import json

app = Flask(__name__)

# 取得各城市 JSON 資料
def search_city(str):
    result = proxy.get(f'/v2/Road/Traffic/CCTV/City/{str}')
    json_data = json.loads(result.content)
    return json_data
def modify_resolution(src_url, new_resolution):
    # 解析 URL
    parsed_url = urlparse(src_url)

    # 取得查詢字串參數
    query_params = parse_qs(parsed_url.query)

    # 修改 resolution 參數
    query_params['resolution'] = [new_resolution]

    # 重新編碼查詢字串
    encoded_query = urlencode(query_params, doseq=True)

    # 構建新的 URL
    modified_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, encoded_query, parsed_url.fragment))
    print("modified_url: "+modified_url)
    return modified_url
def get_final_url(url):
    # 发送 HEAD 请求，捕获重定向前和重定向后的 URL
    try: 
        response = requests.head(url, allow_redirects=True, timeout=5)
        print(f"Reponse got{str(response.url)}")
        return response.url
    except ConnectionError:
        print("connetion error")
        return url
    except Exception as e:
        print(f"something went wrong{str(e)}")
        return url

# 測試
#src_url = "https://tcnvr3.taichung.gov.tw:7001/media/00-D0-89-18-98-35.mpjpeg?resolution=240p&amp;auth=cHVibGljdmlld2VyOjYwZTE2ZTNjZWZlZDg6YjU5ZDZiOWY5ZjlkODgzMmExN2NmOGIwY2RkNDZmNWQ"
new_resolution = "1080"


def fetch_url_with_timeout(url, timeout_seconds=5):
    try:
        response = urlopen(url, timeout=timeout_seconds)
        start_time = time.time()
        chunk_size = 2048 

        # 初始化
        data = b""

        while True:
            # 讀取快取
            chunk = response.read(chunk_size)

            # 時間超時自動中斷
            if time.time() - start_time > timeout_seconds:
                print("time out")
                raise timeout("Read operation timed out.")

            # 完成讀取後跳出
            if not chunk:
                print("read finished")
                break

            # 將數據導入緩存
            data += chunk

        return data
    except URLError as e:
        print(f"Error: {e}")
        return None
    except timeout as e:
        print(f"Timeout: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


# 設定初始 JSON 資料
initial_data = search_city("Taichung")
current_data = initial_data

@app.route('/')
def index():
    return render_template('index.html', data=current_data)

@app.route('/get_data/<city>')
def get_data(city):
    data = proxy.get(f'/v2/Road/Traffic/CCTV/City/{city}')
    json_data = json.loads(data.content)
    # data2 = json.loads(data2.content)
    # json_data = data1['CCTVs'] + data2['CCTVs']

    if json_data:
        return json_data
    else:
        print("city not found")
        return jsonify({"error": "City not found"})
@app.route('/get_road', methods=['GET'])
def get_road():
    city = request.args.get('city')
    road = request.args.get('road')
    # 判斷要求是否為普通公路
    if(road != "Road"):
        # 請求快速道路或高速公路
        data = proxy.get(f'v2/Road/Traffic/CCTV/{road}')
    else:
        data = proxy.get(f'/v2/Road/Traffic/CCTV/City/{city}')
    json_data = json.loads(data.content)
    # data2 = json.loads(data2.content)
    # json_data = data1['CCTVs'] + data2['CCTVs']

    if json_data:
        return json_data
    else:
        print("data not found")
        return jsonify({"error": "City not found"})
@app.route('/get_img_src', methods=['POST'])
# 將影片連結處理最佳化並回傳
def get_img_src():
    # 取得 POST 請求中的 JSON 資料
    data = request.json
    # 取得 video_url
    video_url = data.get('video_url', '')
    print("video_url: "+video_url)
    video_url = get_final_url(video_url)
    print("final_url: "+video_url)


    try:
        # 用 urlopen 獲取 HTML 內容
        print("processing html_content")
        html_content = fetch_url_with_timeout(video_url, 5)
        print(html_content)
        if(html_content==None):
            print("urlopen time out")
            img_src = modify_resolution(video_url, new_resolution)
            return jsonify({'img_src': img_src}) 
        print("read!")
        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 提取 img 標籤的 src 屬性值
        img_element = soup.find('img')
        img_src = img_element.get('src') if img_element else None
        img_src = modify_resolution(img_src, new_resolution)
        print("img_src: "+img_src)
        if(img_src!=""):
            # 回傳 img_src
            return jsonify({'img_src': img_src})
        else:
            print("img_src null")
            return jsonify({'img_src': video_url})
    except TypeError as e:
        print(f"Type error: img_src null  {e}")
        return jsonify({'img_src': video_url})           

    except Exception as e:
        # 處理可能的錯誤
        print("error: "+str(e))
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False)