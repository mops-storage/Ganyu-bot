from flask import Flask, render_template, url_for

app = Flask(__name__, static_folder='static')




@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('error/404.html')





if __name__ == "__main__":
    app.run(debug=True)
    logo = url_for( 'static', filename='assets/logo.gif')
    
