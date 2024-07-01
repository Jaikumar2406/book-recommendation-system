from flask import Flask , render_template , request
import pickle
import numpy as np


popular_df = pickle.load(open('popular.pkl' , 'rb'))
books = pickle.load(open('books.pkl' , 'rb'))
df = pickle.load(open('df.pkl' , 'rb'))
cs= pickle.load(open('similarity_score.pkl' , 'rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           num_ratings = list(popular_df['num_ratings'].values),
                           avg_ratting = list(popular_df['avg-rating'].values),
                           Book_Author = list(popular_df['Book-Author'].values),
                           Image = list(popular_df['Image-URL-M'].values),
                           )



@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommendation' , methods =['post'])
def recommendation():
    user_input= request.form.get('user_input')
    index = np.where(df.index ==user_input)[0][0]
    #index nikalne ke liye cosine_similarity ka use kiye  phir usko list me daal diye usko enumerate karke phir uako sorted kar diye jisse wo jaada se kam similat kaise hojaaye and then colum na ho karke lambda ka use kiye 
    
    similar_item = sorted(list(enumerate(cs[index])) , key=lambda x:x[1] , reverse=True)[1:6]


    data = []
    for i in similar_item:
        lists = []
        temp_df = books[books['Book-Title'] == df.index[i[0]]]
        lists.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        lists.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        lists.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(lists)
        
    print(data)

    return render_template('recommend.html' , data=data)


if __name__ == '__main__':
    app.run(debug=True)