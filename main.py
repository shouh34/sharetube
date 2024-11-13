# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, render_template, request
from GoogleNews import GoogleNews
import sqlite3
import os
import datetime
import pytube
from moviepy.editor import *
from moviepy.video.fx.all import *
import pytchat

import urllib.parse
import ffmpeg
from pytube import Search
from pytube import Channel
import qrcode
from itertools import islice
from yt_dlp import YoutubeDL
import pyttsx3
import yt_dlp
from youtube_comment_downloader import *
from moviepy.editor import *
from pytube import YouTube
#Flaskオブジェクトの生成
app = Flask(__name__)

app = Flask(__name__, static_folder="./static/")


#「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/shinki_input", methods=['GET', 'POST'])
def shinki_input():

    name=request.form.get('t1')

    password=request.form.get('t2')

    mail=request.form.get('t3')


    dbname = 'main.db'
    conn = sqlite3.connect(dbname)

    # SQLiteを操作するためのカーソルを作成
    cur = conn.cursor()

    # データ登録
    cur.execute("insert into users(name, pass,mail) values('{}', '{}','{}');".format(name,password,mail))

    conn.commit()

    conn.close()


    return render_template("index.html")


@app.route("/shinki")
def shinki():





    return render_template("shinki.html")
#フレンド検索処理
@app.route("/Frend_search", methods=['GET', 'POST'])
def Frend_search():
    frend=request.form.get('t1')



    dbname = 'main.db'
    conn = sqlite3.connect(dbname)

    # SQLiteを操作するためのカーソルを作成
    cur = conn.cursor()

    # データ登録
    cur.execute('INSERT INTO users values("kuwajima","2024/06/29")')


    conn.commit()

    conn.close()



    return render_template("Frend.html")


@app.route("/yomiage/<coment>")
def yomiage(coment):
    engine = pyttsx3.init()
    engine.say(coment)
    engine.runAndWait()

    html="<html><head><script>alert('読み上げ完了')</script></head><body></body></html>"

    return html



@app.route("/toukou", methods=['GET', 'POST'])
def toukou():
    path = 'main.db'

    dbname = 'main.db'
    conn = sqlite3.connect(dbname)

    # SQLiteを操作するためのカーソルを作成
    cur = conn.cursor()

    # データ登録
    cur.execute('INSERT INTO recoment values("kuwajima", "りんご","tes")')


    cur.execute('SELECT * FROM recoment')

    name=[]
    coment=[]
    date=[]

    # 取得したデータはカーソルの中に入る
    for row in cur:
        name.append(row[0])
        coment.append(row[1])
        date.append(row[2])

    conn.commit()

    return render_template("result.html",l=zip(name,coment,date),index=1)



@app.route("/kakikomi_write", methods=['GET', 'POST'])
def kakikomi_write():


    recoment= request.form.get('kaki')





    return render_template("kakikomi.html",come=recoment)
@app.route("/QR/<url>")
def QR(url):
    qr = qrcode.QRCode()
    qr.add_data(url)
    qr.make()
    img = qr.make_image()
    img.save('qrcode_test2.png')

    return render_template("QR.html")

@app.route("/henshudl", methods=["POST"])
def henshudl():

    file = request.files.get('file')


    #開始時刻
    start_minute = request.form.get('start_minute')



    start_second = request.form.get('start_second')


    #終了時刻
    end_minute= request.form.get('end_minute')

    end_second= request.form.get('end_second')


    user_folder = os.path.expanduser("~")
    folder = os.path.join(user_folder, "Downloads")


    print(folder+"\\"+str(file.filename))
    print(start_second)

    dougapath=folder+"\\"+str(file.filename)
    start =start_minute*60+start_second

    end =end_minute*60+end_second
    final_clip = VideoFileClip(folder+"\\"+str(file.filename)).subclip(start,end)

    final_clip.write_videofile(
        folder+"\\"+str("(編集済み)"+file.filename),
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )


    dougapath=folder+"\\"+str(file.filename)
    html="<html><head><script>alert('ダウンロード完了')</script></head><body></body></html>"

    return html


@app.route("/henshu")
def henshu():


    return render_template("henshu.html",index=3)



@app.route("/site_view")
def site_view():


    return render_template("site.html")


#コメント閲覧
@app.route("/coment_view")
def coment_view():


    return render_template("Mypage.html")



@app.route("/Live_comentget", methods=['GET', 'POST'])
def Live_comentget():


    key= request.form.get('liveid')
    livechat = pytchat.create(video_id=key)
    while livechat.is_alive():

        # チャットデータの取得
        chatdata = livechat.get()
        for c in chatdata.items:
            print(f"{c.datetime} {c.author.name} {c.message} {c.amountString}")

        time.sleep(1)


@app.route("/Live")
def Live():

    return render_template("live.html")

@app.route("/kakikomi/<titles>")
def kakikomi(titles):

    print(titles)

    return render_template("kakikomi.html",name=titles)


@app.route("/search", methods=['GET', 'POST'])
def search():

    key= request.form.get('kensaku')


    radi= request.form.get('radio')


    if radi=="ニュース":

        googlenews = GoogleNews(lang='ja', encode='utf-8')
        googlenews.get_news(key)
        result = googlenews.results()
        tezrt = googlenews.get_texts()
        title = []
        img = []
        link = []
        date = []
        for s in range(15):
            title.append(result[s]["title"])
            link.append("https://" + result[s]["link"])
            date.append(result[s]["datetime"])
            print(result[s]["link"])
            # img.append("http://"+result[s]["img"])
            print(result[s]["img"])
            print(tezrt[s])
        return render_template('result.html', l=zip(title, link, date))

    elif radi=="動画":


        # QR
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

        search = Search(key)
        # URLからhttps://削除
        customurls = []

        # print(len(search.results))
        videos, next_continuation = search.fetch_and_parse()


        for video in videos:
            # URL
            title.append(video.watch_url)

            # title
            l_empty.append(video.title)
            my_video = YouTube(video.watch_url)
            # サムネ格納
            #    thmna.append(my_video.thumbnail_url)
            # チャンネル名
            chmei.append(my_video.author)
            churl.append(my_video.channel_url)

            videoid.append(my_video.video_id)
            # 再生回数
            views.append(my_video.rating)

            # 動画サムネイル
            s = my_video.thumbnail_url

            urls = my_video.watch_url
            b = urls.strip("https://www.youtube.com/")
            print(b)
            customurls.append("w" + b)

            dougaimage.append(s[24:len(s)])

        return render_template('result.html', data=zip(title, l_empty, chmei, churl, videoid, customurls, views),dou=2)

@app.route("/shousai/<id>")
def shousai(id):

    channel = YouTube("https://www.youtube.com/watch?v="+id)


    c = Channel(channel.channel_url)




    titles=channel.title
    channel_ID=channel.channel_id
    views=channel.views
    shueki=views*0.09
    Length=channel.length/60


    chanpage=channel.channel_url
    description=channel.description

    channel_title=c.channel_name
    about=c.about_url

    featurea=c.featured_channels_url



    return render_template('shousai.html',chmei=titles,id=channel_ID,view=views,bikou=description,videoid=id,chan=chanpage,shunyu=shueki,chans=channel_title,About=about,fe=featurea,nagasa=Length)

@app.route("/dougaDL/<id>")
def dougaDL(id):
    yt = YouTube('https://www.youtube.com/watch?v='+id)
    stream = yt.streams.first()


    user_folder = os.path.expanduser("~")
    folder = os.path.join(user_folder, "Downloads")

    stream.download(folder)




    html="<html><head><script>alert('test')</script></head><body></body></html>"

    return html
@app.route("/onseiDL/<id>")
def onseiDL(id):
    urls = ["https://www.youtube.com/watch?v="+id]

    # 設定(mp3形式にするなど）
    ydl_opts = {
        "format": "mp3/bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }

    # ダウンロード
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.download(urls)

        html="<html><head><script>alert('test')</script></head><body></body></html>"

    return html

@app.route("/coment/<vid>")
def coment(vid):
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url('https://www.youtube.com/watch?v='+vid, sort_by=SORT_BY_POPULAR)
    photo=[]
    textlist=[]
    times=[]
    authors=[]

    for comment in islice(comments, 50):

        photo.append(comment["photo"])
        textlist.append(comment["text"])
        times.append(comment["time"])
        authors.append(comment["author"])
        #photo.append(coment["photo"])
        #text.append(coment["text"])

    return render_template('kakikomi.html',data=zip(photo,textlist,times,authors))


@app.route("/settings")
def settings():

    return render_template("settings.html")


@app.route('/result', methods=['GET', 'POST'])
def result():
    # index.htmlのinputタグ内にあるname属性itemを取得し、textに格納した


    # もしPOSTメソッドならresult.htmlに値textと一緒に飛ばす

    try:


        return render_template('result.html')


    except IndexError:
        print("Index Error")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)
