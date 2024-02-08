from mcstatus import JavaServer
from mcstatus import BedrockServer
# 从flask包引入Flask类，通过实例化类创建程序对象app
from flask import Flask, send_file
from flask import render_template

from PIL import Image, ImageDraw, ImageFont

bdserver = JavaServer.lookup("p.bdcraft.cn:25565")
def mc_java_server_status(server):
    try:
        status = server.status()
        print("服务器版本：%s\n当前有 %s/%s 位玩家\n延迟为 %s ms\n" % (status.version.name, status.players.online, status.players.max, round(status.latency, 2)))
    except:
        status = {"players":{"online":0,"max":0},"version":{"name":"无法连接到服务器"},"description":{"text":"Unknown"},"latency":0}
    return status

bdbeserver = BedrockServer.lookup("www.mcd.blue:19132")
def mc_bedrock_server_status(server):
    try:
        status = server.status()
    except:
        status = {"players":{"online":0,"max":0},"version":{"name":"无法连接到服务器"},"description":{"text":"Unknown"},"latency":0}
    return status

app = Flask(__name__)

@app.route('/')
def index():   
    bdstatus = mc_java_server_status(bdserver)
    # bdbestatus = mc_bedrock_server_status(bdbeserver)
    return render_template('index.html',bdstatus=bdstatus)

@app.route('/infopic')
def get_mc_status():
    # 获取MC服务器在线状态
    server = JavaServer.lookup("p.bdcraft.cn:25565")
    status = server.status()
    online_players = status.players.online
    max_players = status.players.max

    # 创建一个图片
    img = Image.new('RGB', (480, 85), color = (179, 229, 252))
    
    # 打开BDLOGO
    bdlogo = Image.open("bd-logo-256.png").resize((80,80))
    img.paste(bdlogo,(2,2),bdlogo)

    # 在图片上绘制文字
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("zpix.ttf", 30)
    d.text((90,10), f"梦之蓝-正版纯净生存社区\n当前在线: {online_players}/{max_players}", fill=(26,35,126), font=font)

    # 保存图片
    img.save("mc_status.png")

    # 返回图片
    return send_file("mc_status.png", mimetype='image/png')
