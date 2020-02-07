from flask import *
import evote
app = Flask(__name__)

@app.route('/')
def func():
    return render_template('first.html')

@app.route('/home', methods = ['POST'])
def func2():
    choice = request.form['candidate']
    v1 = evote.vote(int(choice))
    print (evote.Blockchain.votepool)
    return redirect('/thanks')

@app.route('/thanks', methods = ['GET'])
def thank():
    return render_template('home.html')

if __name__=='__main__':
    app.run()

