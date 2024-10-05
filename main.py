# これはサンプルの Python スクリプトです。
import random
# Shift+F10 を押して実行するか、ご自身のコードに置き換えてください。
# Shift を2回押す を押すと、クラス/ファイル/ツールウィンドウ/アクション/設定を検索します。
import sys
from pytube import Search
import os
import os.path
from pytube import *
from pytube import YouTube
import qrcode
import urllib.request
from pytube import YouTube

import sqlite3
import shutil
import datetime
import share_db
from itertools import islice
from pytube import YouTube
from pytube import Channel

from flask import Flask,render_template,request,redirect,url_for,session,Response,make_response
app = Flask(__name__, static_folder="./static/")


#app = Flask(__name__)

#IMG_FOLDER = os.path.join("static", "./templates/images")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bbs_post/<surename>')
def bbs_post(surename):



    return render_template('toukou.html',titles=surename)


#コメント投稿
@app.route('/bbs_toukou', methods=['POST'])
def bbs_toukou():



    return render_template('toukou.html')


#QR発行
@app.route("/qr/<string:id>/<string:url>")
def qr(id,url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=4,
    )
    qr.add_data("https://www.youtube.com/"+url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("./static/images/qr.png")


    img_path = 'images/youtube.png'



    return render_template('qr.html',images=img_path)


#チャンネル情報
@app.route("/chinfo/<string:path>")
def chinfo(path):

    channel = YouTube("https://www.youtube.com/watch?v="+path)
    #チャンネルURL
    print(channel.channel_url)
    #動画タイトル
    print(channel.title)
    #動画視聴回数
    print(channel.views)
    #
    print(channel.author)
    #動画サムネイル
    print(channel.thumbnail_url)
    #チャンネルID
    print(channel.channel_id)
    #備考
    print(channel.description)


  #  print(channel.rating)



    return render_template('chinfo.html',chan=channel.channel_url,chan1=channel.title,chan2=channel.views,chan3=channel.author,chan4=channel.channel_id,chan5=channel.description,thmnail=channel.thumbnail_url,views=channel.views,chid=channel.channel_id)


@app.route("/kuchikomi")
def kuchikomi():


    conn = sqlite3.connect('share.db')
    #conn.row_factory = sqlite3.Row  # dict型を指定
    c = conn.cursor()

    # DBの中身を取得
    c.execute('select * from thread')
    results = c.fetchall()

    # 展開用に空リストを作成
    title = []
    date=[]
    s=[]
    index=0
    # リストに展開する処理
    for r in results:
        print(r[1])
        title.append(r[0])
        date.append(r[1])
        s.append(index)
        index+=1
    conn.close()

    return render_template("kuchikomi.html",l=zip(title,date,s))

    #スレッド検索
@app.route("/thread_search", methods=['POST'])
def thread_search():

    


    #文字列取得
    name = request.form.get('t1')
    

    conn = sqlite3.connect('share.db')
    #conn.row_factory = sqlite3.Row  # dict型を指定
    c = conn.cursor()

    # DBの中身を取得
    c.execute("SELECT * FROM thread WHERE title like ?",('%'+name+'%',))

    results = c.fetchall()

    # 展開用に空リストを作成
    titles = []
    dates=[]
    s=[]
    index=0

    # リストに展開する処理
    for r in results:
        print(r[1])
        titles.append(r[0])
        dates.append(r[1])
        s.append(index)
        index+=1
    conn.close()

    return render_template('kuchikomi.html',moji=name,index=5,l=zip(titles,dates,s))

#スレッド削除
@app.route("/thread_Delete/<id>")
def thread_Delete(id):


    

    conn = sqlite3.connect('share.db')
    #conn.row_factory = sqlite3.Row  # dict型を指定
    c = conn.cursor()

    # DBの中身を取得
  #  c.execute("SELECT * FROM thread WHERE title like ?",('%'+name+'%',))
  #  sql = """DELETE FROM Fruit WHERE title=? ;"""
    c.execute('DELETE FROM thread WHERE title=?', (id,))


    #c.execute("DELETE FROM thread WHERE title = "ojisan";")

    results = c.fetchall()


    conn.commit()


    conn.close()
    # 展開用に空リストを作成
    titles = []
    dates=[]
    s=[]
    index=0



    # リストに展開する処理
    for r in results:
        print(r[1])
        titles.append(r[0])
        dates.append(r[1])
        s.append(index)
        index+=1
    conn.close()



    html="<html><head><script>alert('削除しました')</script></head></html>"

    return html

#スレッド作成
@app.route("/thread_create/<id>")
def thread_create(id):



    ##スレッド作成

    ##DBにスレッド登録

    # データベース開く
    db = sqlite3.connect("share.db")

    c = db.cursor()

    # テーブル作成
    #c.execute('create table artoria (name text, atk int, hp int)')

    dt_now = datetime.datetime.now()
    # データ追加(レコード登録)
    sql = 'insert into thread (title,create_dt) values (?,?)'
    data = (id,dt_now)
    c.execute(sql, data)
    # コミット
    db.commit()



    #フィールド作成用SQL文
    db.execute("CREATE TABLE IF NOT EXISTS %s (name TEXT,date TEXT)" % id)


    # クローズ
    db.close()

    html="<html><head><script>alert('スレッド作成しました')</script></head></html>"
    #return render_template("toukou.html",title=id)


    return html

@app.route("/settings")
def settings():



    return render_template("settings.html")



@app.route("/hyouka_toukou", methods=['POST'])
def hyouka_toukou():

    name = request.form.get('n2')

    #チャンネル名
    chmei = request.form.get('n3')

    #評価書き込み

    con = sqlite3.connect('hyouka.db')
    cur = con.cursor()
    sql = 'INSERT INTO toukou (chmei,point) values (?,?)'
    data = [chmei,name]
    cur.execute(sql, data)
    con.commit()
    con.close()



    han = os.path.isfile("static/images/temp.png")
    if han:
        conn = sqlite3.connect("hyouka.db")
        os.remove("static/images/temp.png")
        c = conn.cursor()
        c.execute("select * from toukou")
        chanmei = []
        point = []
        for row in c:
            chanmei.append(row[0])
            point.append(row[1])
            plt.bar(chanmei, point)
            plt.title("Youtube チャンネル評価")
            plt.ylabel("Revenue (thousand USD)")
            plt.savefig("static/images/temp.png")
        c.close()

    else:
        conn = sqlite3.connect("hyouka.db")
        #os.remove("static/images/temp.png")
        c = conn.cursor()
        c.execute("select * from toukou")
        chanmei = []
        point = []
        for row in c:
            chanmei.append(row[0])
            point.append(row[1])
            plt.bar(chanmei, point)
            plt.title("Youtube チャンネル評価")
            plt.ylabel("Revenue (thousand USD)")
            plt.savefig("static/images/temp.png")
        c.close()

    html="<html><head><script>alert('投稿しました')</script></head><body></body></html>"



    return html


@app.route("/onsei/<ons>")
def onsei(ons):
    youtube = YouTube('https://www.youtube.com/watch?v='+ons)

    streams = youtube.streams.filter(only_audio=True)

    stream = streams.first()

    key = "HOME"
    folder = os.getenv(key)
    print(folder)


    desktop_path = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Downloads"
    print(desktop_path)


    ongakuname=stream.download(desktop_path)

    print(ongakuname.title())
    audio_clip = AudioFileClip(ongakuname)
    next=random.randint(0,100)
    audio_clip.write_audiofile(desktop_path+"\\"+str(next)+".mp3", codec="libmp3lame")

    return "<html><head><script>alert('ダウンロード完了')</script></head><body></html>"


@app.route("/dougaDL/<ids>/<mei>")
def dougaDL(ids,mei):

    desktop_path = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Downloads"

    try:

        yt = YouTube('https://www.youtube.com/watch?v='+ids)
        stream = yt.streams.first()
        stream.download()

        print(f"Downloaded '{yt.title}' successfully.")
    except Exception as e:
        print(f"Error downloading video: {e}")

    share_db.download_rireki(ids, mei)


    return "<html><head><script>alert('ダウンロード完了')</script></head><body></html>"








@app.route("/down_rireki")
def down_rireki():
    conn = sqlite3.connect("download.db")

    c = conn.cursor()

    c.execute("select * from rireki")
    id = []
    title = []
    for row in c:
        id.append(row[0])
        title.append(row[1])
    c.close()

    return render_template("rireki.html", data=zip(id,title))



@app.route("/shousai/<path>")
def shousai(path):

    you=YouTube("http://youtube.com/watch?v="+path)

    title=you.title
    view=you.views
    #動画の収益
    shueki=0.03*view

    churl=you.channel_url
    length=you.length
    doua_time=length/60
    desc=you.description

    chan=Channel(you.channel_url)
    #公開日
    publicdate=you.publish_date
    chanurl=you.channel_url

    chanid=you.channel_id
    author=you.author

    return render_template("down.html",id=path,titles=title,views=view,shousai=desc,nagasa=doua_time,koukai=publicdate,chan=chanurl,chanids=chanid,mone=shueki,auth=author)



@app.route("/domentdl/<ids>")
def comentdl(ids):
    downloader = YoutubeCommentDownloader()
    indexappend = []
    naiyou = []
    thmnails = []
    time = []
    chmei = []
    with open('coment.txt', 'w') as f:
        comments = downloader.get_comments_from_url('https://www.youtube.com/watch?v=' + ids, sort_by=SORT_BY_POPULAR)
        for comment in islice(comments, 10):
            naiyou.append(comment["text"])
            f.write(comment["text"])

    f.close()

    return "<html><head><script>alert('保存しました')</script></head><body></html>"



@app.route("/next_func/<string:path>/<string:dougamei>/<string:titlemei>")
def next_func(path,dougamei,titlemei):

    print(path)
    youtube="https://www.youtube.com/watch?v="+path



    return render_template('down.html',url=youtube,dougatitle=dougamei,chmei=titlemei,id=path)



@app.route('/download_pages')
def download_pages():


    return render_template("down_page.html")


@app.route('/post', methods=['POST'])
def post():
    name = request.form.get('HOGE')
    janru=request.form.get('n2')
    youtube="https://www.youtube.com"
    key = name
    qrcode = []

    title = []
    l_empty = []
    thmna = []
    chmei = []
    # チャンネルURL
    churl = []
    # videoid
    videoid = []
    # 公開日
    koukai = []
    # プロフィール
    desc = []
    # 動画サムネイル
    dougaimage = []
    # 再生回数
    saisei = []
    # info
    info = []
    # 視聴回数
    views = []
    search = Search(name+janru)
    # URLからhttps://削除

    customurls = []
    # print(len(search.results))
    videos, next_continuation = search.fetch_and_parse()
    for video in videos:
        title.append(video.watch_url)
        l_empty.append(video.title)
        my_video = YouTube(video.watch_url)
        chmei.append(my_video.author)
        churl.append(my_video.channel_url)

        videoid.append(my_video.video_id)
        views.append(my_video.rating)
        s = my_video.thumbnail_url
        urls = my_video.watch_url
        b = urls.strip("https://www.youtube.com/")
        print(b)
        customurls.append("w" + b)

    return render_template('index.html', data=zip(title, l_empty, chmei, churl, videoid, customurls, views),keyword=name,post_index=1)

if __name__ == "__main__":
    app.run(port=8000, debug=True)