from flask import Flask, render_template, request, redirect, send_file
from job import save_to_file 
from extractor.jobb import extractor_job
from job import save_to_file

app = Flask('Jobkorea')

db={}

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/search")
def search():
    keyword = request.args.get('keyword')
    if keyword == None:
        return redirect('/')
    if keyword in db:
      krs=db[keyword]
    else:
        krs = extractor_job(keyword)
        db[keyword]=krs
    return render_template('search.html', keyword=keyword, krs=krs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
      return redirect("/")
    if keyword not in db:
      return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv",mimetype='text/csv',as_attachment=True)

app.run('127.0.0.1')