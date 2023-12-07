#coding:utf-8
from flask import Flask, request, Response
import requests
import json,os
from bs4 import BeautifulSoup
from flask_cors import CORS

workdir=os.path.abspath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(workdir, 'static', '_next')

app = Flask(__name__,static_url_path="/_next",static_folder=STATIC_ROOT)
# 允许所有域的请求
CORS(app,supports_credentials=True)

# 或者指定允许的域
# CORS(app, resources={r"/api/*": {"origins": "http://yourdomain.com"}})

def changeHtml(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    soup.h1.string  = 'Shared GPT!'
    h3_tags = soup.find_all('h3')
    for h3 in h3_tags:
        h3.decompose()
    li_tags = soup.find_all('li')
#    for li in li_tags:
#        if li.a is not None and 'plus' not in li.a.get('class'):
#            print (li.a.get('class'))
#            li.decompose()
    soup.title.string = "my gpt"
    # 找到 href 属性为 "link2" 的 <a> 标签
    specific_a_tag = soup.find('div', {'class': 'contributor-list'})
    specific_a_tag.decompose()
#    # 创建一个新的标签
#    new_tag = soup.new_tag('a')
#    # 给新标签设置属性
#    new_tag['href'] = 'http://example.com'
#    new_tag.string = 'Link Text'
#    # 将新标签插入到文档中
#    soup.div.append(new_tag)    
    return str(soup)


PROXY_URL="https://chat1.zhile.io"
PROXY_URL="https://chat-shared3.zhile.io/"
def _proxy(*args,**kwargs):
    print (request.host_url)
    print (request.method)
    print (request.url)
    resp = requests.request(
        method= request.method,
        url= request.url.replace(request.host_url,PROXY_URL),
        headers={key:value for (key,value) in request.headers if key not in ["Host","Accept-Encoding"] },
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        verify=False
    )
    exclouded_headers = ["Content-Encoding","Content-Length","Transfer-Encoding","Connection","X-Frame-Options","x-frame-options"]
    headers = [(key,value) for (key,value) in resp.raw.headers.items() if key not in exclouded_headers]
    headers.append(("X-Frame-Options","*"))
    headers.append(("Access-Control-Allow-Origin","http://127.0.0.1:9988"))
    headers.append(("Access-Control-Allow-Credentials","true"))
    headers.append(("Access-Control-Allow-Headers","Content-Type,Authorization"))
    headers.append(("Access-Control-Allow-Methods","POST,GET"))
    print(headers)
    if "/shared.html" in request.url and len(resp.content) > 2:
#        f = open("login.html","w")
#        f.write(resp.content)
#        f.close()
        return Response(changeHtml(resp.content), status=resp.status_code, headers=headers)
    return Response(resp.content, status=resp.status_code, headers=headers)

def getModels():
    headers = {}
    print(headers)
    req = requests.request(
        method="GET",
        url="http://121.37.96.230:8082/auth/login?next=%2F",
        params={},
        data={}
    )
    # req = requests.get("http://121.37.96.230:8082/auth/login?next=%2F", verify=False, headers = headers, allow_redirects = False)
    print(req.text)
    response = req.json()
    print(json.dumps(response,indent=2,ensure_ascii=False))
    return response

# getModels()

@app.route("/",defaults={'path':''})
@app.route("/<path:path>", methods=['GET', 'POST'])
def test(path):
    return _proxy()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
    
def readHtml():
    with open('login.html', 'r') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    soup.h1.string  = 'Hello World!'
    h3_tags = soup.find_all('h3')
    for h3 in h3_tags:
#        if "zhile.io" in h3.string:
#            h3.string = 'Hello World!'
#            print(h3)
#        else:
#            # 删除标签
#            h3.decompose()
        h3.decompose()
    soup.title.string = "my gpt"
    # 找到 href 属性为 "link2" 的 <a> 标签
    specific_a_tag = soup.find('div', {'class': 'contributor-list'})
    specific_a_tag.decompose()

    
    # 创建一个新的标签
    new_tag = soup.new_tag('a')

    # 给新标签设置属性
    new_tag['href'] = 'http://example.com'
    new_tag.string = 'Link Text'

    # 将新标签插入到文档中
    soup.div.append(new_tag) 
    li_tags = soup.find_all('li')
    for li in li_tags:
        
        print(li.a.get('class'))

   
    with open('login_after.html', 'w') as file:
        file.write(str(soup))
#readHtml()        
