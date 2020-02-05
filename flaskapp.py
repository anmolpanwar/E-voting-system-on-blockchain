from flask import *
import evote
app = Flask(__name__)

@app.route('/')
def func():
    return render_template('first.html')

@app.route('/home', methods = ['POST'])
def func2():
    choice = request.form['candidate']
    v1 = evote.vote(choice)
    print (evote.Blockchain.votepool)
    return redirect('/thanks')

@app.route('/thanks')
def thank():
    return "Dhanyavaad!"

if __name__=='__main__':
    app.run()

