 
from flask import render_template
from flask import Flask, request

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "accept-encoding":"gzip, deflate, br" ,
    # "accept-language": "en-US,en;q=0.9",
    "cookie": '_zap=b3cd2c55-aef6-4791-aba5-1c6280b3ef9f; d_c0="AJAjCKW-6A6PTsGydGbpl5mO3U6D2MhBl1I=|1548917401"; q_c1=60a46aafdae64c02b27ff21482d74fd6|1548917402000|1548917402000; _xsrf=85c3dd82-65b1-4259-ae76-07789ce0dffb; l_n_c=1; n_c=1; __utma=51854390.522950587.1549803059.1549803059.1549803059.1; __utmc=51854390; __utmz=51854390.1549803059.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|3=entry_date=20190131=1; tgw_l7_route=a37704a413efa26cf3f23813004f1a3b; capsion_ticket="2|1:0|10:1549807660|14:capsion_ticket|44:ZDJjMjYzODg5Mjk5NDY2YWE5MWMyZWVjNTY1NTZmMWI=|9e4caf93acca83e7df9ad6d79499a87688b89f1d3d6d059a90e6ae42c25c92a3"; r_cap_id="OTA0MTk5YWYzMjkwNGU5MmJmMjM2MTg1N2YyNmQ3NWM=|1549807669|074a353152ff940a4cd0e014dd762a0c0068318a"; cap_id="YThkMjgxZmM1ZjZkNGExZmFkZDQ3NTIyMTJmZTUzNzM=|1549807669|9bb448d09071ce613bc6ee97504ea1b5757d3493"; l_cap_id="Y2FiYWNkNTYxNjI0NDM5MmJhMGFlMDY0MTRkNzIzNTg=|1549807669|5bfbe708cb0d50ce7bc40b5814e3510c51d76e3f"; z_c0=Mi4xZVJuRkFRQUFBQUFBa0NNSXBiN29EaGNBQUFCaEFsVk5SMzVOWFFEN2ktVFdzdTVSTTdtQi0tM3dVcVBMbWJTeWN3|1549807687|51926ae8fcb9f49ad8178ec6d79560d1712e8c3b; tst=r',
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"
}
def get_chinese(check_str):
    res = ""
    tmp = ""
    repeat_num = 0
    for ch in check_str:
        
        
        if u'\u4e00' <= ch <= u'\u9fff' or ch in "，！。,.":
            if tmp == ch:
                repeat_num+=1
                print(ch,end=" ")
            else:
                repeat_num = 0

            if repeat_num < 2:
                res += ch
    
    return res


@app.route("/")
def pass_url():
    return render_template("pass_url.html")
start_tag = ",,,,,..,,,,,,,,,,,,,,,"
start_tag_len = len(start_tag)
@app.route("/content")
def get_content():
    url = request.args.get('url')
    
    r = requests.get(url,headers= headers)
    soup = BeautifulSoup(r.content,features="html.parser")
    res = get_chinese(str(soup))
    try:
        start = res.index(start_tag) + start_tag_len
    except:
        start = 0
    
    res = res[start:]
    with open('./content/'+url.split("/")[-1]+".html", "w+" ) as f:
        f.write(res)
    return res
    

app.run(host="0.0.0.0", port=80)