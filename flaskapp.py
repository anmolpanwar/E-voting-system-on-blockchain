from flask import *
import evote
import csv
app = Flask(__name__)

@app.route('/')
def func():
    return render_template('first.html')

@app.route('/home', methods = ['POST'])
def func2():
    choice = request.form['candidate']
    v1 = evote.vote(int(choice))
    with open('votefile.csv','a',newline="") as votefile:
        writer = csv.writer(votefile)
        for key,value in v1.voteobject.items():
            writer.writerow([key,value])
    votefile.close()
    return redirect('/thanks')

@app.route('/thanks', methods = ['GET'])
def thank():
    return render_template('home.html')

if __name__=='__main__':
    app.run()

