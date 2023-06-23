from flask import Flask ,render_template ,request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/process',methods=['POST'])
def process():
    # Image Processing and Barcode Logic
     return 'Barcode Processed Sucessfully'


if __name__ == '__main__':
    app.run(debug=True)






