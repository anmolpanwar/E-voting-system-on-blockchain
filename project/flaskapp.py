from flask import *
import blockchain as b1
import csv
import pickle
app = Flask(__name__)

@app.route('/')
def func():
    return render_template('first.html')

@app.route('/home', methods = ['POST'])
def func2():
    choice = request.form['candidate']
    v1 = b1.vote(int(choice))
    with open('votefile.csv','a',newline="") as votefile:
        writer = csv.writer(votefile)
        for key,value in v1.voteobject.items():
            writer.writerow([key,value])
    if b1.vote.count%4==0:
        block1 = b1.Block()
        blockx = block1.mineblock()
        with open('blockchain.abc','ab') as blockfile:
            pickle._dump(blockx,blockfile)
        print("block added")
    return redirect('/thanks')

@app.route('/thanks', methods = ['GET'])
def thank():
    return render_template('home.html')

if __name__=='__main__':
    app.run(port = 5002)

