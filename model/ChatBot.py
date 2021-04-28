import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import pickle
import json
from Bot import path
from app.models import CartList,Product,Orders
import sqlite3
import app.models as dbmod
import string
import random
nltk.download('punkt')

class ChatBot(object):

    instance = None

    @classmethod
    def getBot(cls):
        if cls.instance is None:
            cls.instance = ChatBot()
        return cls.instance

    def __init__(self):
        print("Init")
        if self.instance is not None:
            raise ValueError("Did you forgot to call getBot function ? ")

        self.stemmer = LancasterStemmer()
        data = pickle.load(open(path.getPath('trained_data'), "rb"))
        self.words = data['words']
        self.classes = data['classes']
        train_x = data['train_x']
        train_y = data['train_y']
        with open(path.getJsonPath()) as json_data:
            self.intents = json.load(json_data)
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)
        self.model = tflearn.DNN(net, tensorboard_dir=path.getPath('train_logs'))
        self.model.load(path.getPath('model.tflearn'))

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.stemmer.stem(word.lower()) for word in sentence_words]
        # print(sentence_words)
        return sentence_words

    def bow(self, sentence, words, show_details=False):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return np.array(bag)

    def classify(self, sentence):
        ERROR_THRESHOLD = 0.25
        results = self.model.predict([self.bow(sentence, self.words)])[0]
        results = [[i, r] for i, r in enumerate(results) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append((self.classes[r[0]], r[1]))
            # print(return_list)
        return return_list

    def listToString(self,s):

        # initialize an empty string
        str1 = " "
        # s = s + k
        # print(s)
        # traverse in the string
        for ele in s:
            str1 += ele

            # return string
        return str1

    def data_merge(self,res,sentence):
        try:
            try:
                letters = string.digits;
                rand = ''.join(random.choice(letters) for i in range(10));

                Data = dbmod.AI_ChatBotDetails.objects.get(FruitsTag=res)
                res = f'<center><img src=\"{Data.ImageID}" width=\"100%\" height=\"100%\">\n</center><br><table style="width:100%"><tr><th>No</th><th>Organic Fruits</th><th>Size</th><th>Was Rs</th><th>Unit</th><th>Saving</th><th>Price</th></tr><tr><td>0{Data.FruitNo}</td><td>{Data.FruitsName}</td><td>{Data.FruitsSize}</td><td>{Data.FruitPrice}</td><td>{Data.Unit}</td><td>{Data.FruitDiscount}</td><td>{Data.FruitBill}</td></tr><tr></tr></table><br>Please Enter quantity in KG</b>&nbsp; <input type="text" id="quantity{rand}" />&nbsp; <button onclick=\"AddItemToCart(`{Data.FruitsName}`, `quantity{rand}`)\">Add to Cart</button> '
            except:
                sentence_words = self.clean_up_sentence(sentence)
                try:
                    res1 = sentence_words[0]
                    Data = dbmod.AI_ChatBotDetails.objects.get(FruitsID=res1)
                    res = f'<center><img src=\"{Data.ImageID}" width=\"100%\" height=\"100%\">\n</center><br><table style="width:100%"><tr><th>No</th><th>Organic Fruits</th><th>Size</th><th>Was Rs</th><th>Unit</th><th>Saving</th><th>Price</th></tr><tr><td>0{Data.FruitNo}</td><td>{Data.FruitsName}</td><td>{Data.FruitsSize}</td><td>{Data.FruitPrice}</td><td>{Data.Unit}</td><td>{Data.FruitDiscount}</td><td>{Data.FruitBill}</td></tr><tr></tr></table><br>Please Enter quantity in KG</b>&nbsp; <input type="text" id="quantity{rand}" />&nbsp; <button onclick=\"AddItemToCart(`{Data.FruitsName}`, `quantity{rand}`)\">Add to Cart</button> '
                except:
                    res = sentence_words[0]+' '+sentence_words[1]
                    Data = dbmod.AI_ChatBotDetails.objects.get(FruitsID=res)
                    res = f'<center><img src=\"{Data.ImageID}" width=\"100%\" height=\"100%\">\n</center><br><table style="width:100%"><tr><th>No</th><th>Organic Fruits</th><th>Size</th><th>Was Rs</th><th>Unit</th><th>Saving</th><th>Price</th></tr><tr><td>0{Data.FruitNo}</td><td>{Data.FruitsName}</td><td>{Data.FruitsSize}</td><td>{Data.FruitPrice}</td><td>{Data.Unit}</td><td>{Data.FruitDiscount}</td><td>{Data.FruitBill}</td></tr><tr></tr></table><br>Please Enter quantity in KG</b>&nbsp; <input type="text" id="quantity{rand}" />&nbsp; <button onclick=\"AddItemToCart(`{Data.FruitsName}`, `quantity{rand}`)\">Add to Cart</button> '
        except:
            res = ''
        return res

    def data(self,sentence):
        print(sentence)
        sentence_words = self.clean_up_sentence(sentence)
        sentence_words.pop(-1)
        try:
            try:
                res = sentence_words[0] +' '+ sentence_words[1]
            except:
                res = sentence_words[0]
        except:
            res = ' '
            print('res',res)
        return res

    def data_Calculaion(self,sentence):
        sentence_words = self.clean_up_sentence(sentence)
        temp = self.data(sentence)
        print('k',temp)
        try:
            Data = dbmod.fruits_List.objects.get(FruitsTag=temp)
            res = Data.FruitBill * int(sentence_words[-1])
            res1 = Data.FruitPrice * int(sentence_words[-1])
            res2 = Data.FruitDiscount * int(sentence_words[-1])
            fruitBill = res
            temp12 = f'<tr><td>{Data.FruitNo}</td><td>{Data.FruitsName}</td><td>{Data.FruitsSize}</td><td>{res1}.00</td><td>{Data.Unit}</td><td>{res2}.00</td><td>{res}.00</td></tr>'
            res = f'<table style="width:100%"><tr><th>No</th><th>Organic Fruits</th><th>Size</th><th>Was Rs</th><th>Unit</th><th>Saving</th><th>Price</th></tr><tr><td>0{Data.FruitNo}</td><td>{Data.FruitsName}</td><td>{Data.FruitsSize}</td><td>{res1}.00</td><td>{Data.Unit}</td><td>{res2}.00</td><td>{res}.00</td></tr><tr></tr></table><br>Show Your Cart Details Please click cart button <b><i class="fa fa-shopping-bag" aria-hidden="true"></i><button onclick="Command(`Cart`);">Cart</button></b><br>Conform Yor Order <button onclick="Command(`yes`);">yes</button>  <button onclick="Command(`No`);">No</button>'
            product = Product(fruitName = Data.FruitsName,FruitsSize = Data.FruitsSize,fruitPrice = res1,Unit = Data.Unit,fruitQuantity = sentence_words[-1],fruitDiscount = res2,fruitBill=fruitBill)
            product.save()
            orders = Orders(FruitNo=Data.FruitNo, CartItem = temp12)
            orders.save()
            cart = CartList(FruitNo=Data.FruitNo,CartItem=temp12)
            cart.save()
            return res
        except:
            res = ''
            return res

    def response(self, sentence, userID='1', show_details=False):
        results = self.classify(sentence)
        Product.objects.all()
        CartList.objects.all()
        Orders.objects.all()
        con = sqlite3.connect("db.sqlite3")
        cur = con.cursor()
        aj = []
        dj = []
        res = ''
        sentence_words = self.clean_up_sentence(sentence)
        print(sentence_words[0])
        context = {}
        if results:
            # print(results)
            while results:
                for j,i in enumerate(self.intents['intents']):

                    if i['tag'] == results[0][0]:
                        # print(i['tag'],results[0][0])
                        if 'context_set' in i['tag']:
                            if show_details:
                                print('context:', i['context_set'])
                            context[userID] = i['context_set']

                        if not 'context_filter' in i or (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                            if show_details:
                                print('tag:', i['tag'])

                            elif sentence_words[0] =='cart':
                                letters = string.digits;
                                rand = ''.join(random.choice(letters) for i in range(10));
                                for s in cur.execute('SELECT Cartitem FROM app_cartlist;'):
                                    for j in s:
                                        aj.append(j)

                                print(self.listToString(aj))
                                res = self.listToString(aj)+f'</table><br>If You Any Item Remove Enter Item No <input type="text" id="quantity{rand}" />&nbsp; <button onclick=\"AddItemToCart(`remove`, `quantity{rand}`)\">Remove</button> <br>Conform Yor Order <button onclick="Command(`yes`);">yes</button>  <button onclick="Command(`No`);">No</button>'

                            elif sentence_words[0] =='fruit':
                                cat =[]

                                for l,k in enumerate(cur.execute('SELECT FruitsName FROM app_ai_chatbotdetails;')):
                                    # print(l,k)
                                    Data = dbmod.AI_ChatBotDetails.objects.get(FruitNo=l+1)
                                    for j in k:
                                        j = j
                                        l +=1
                                        l = str(l)
                                        l = '0'+l
                                        # print(l,j)
                                        print(type(Data.ImageID))
                                        cat.append(l)
                                        dj.append(f'<img class="column" src="{Data.ImageID}" onclick="Command12(`{l}`);" />')
                                        # dj.append(f'<tr><td>{l}</td><td>{j}</td></tr>')
                                res =self.listToString(dj)

                            elif sentence_words[0] =='categ':
                                cat =[]

                                for l,k in enumerate(cur.execute('SELECT tag FROM app_category;')):
                                    # print(l,k)
                                    Data = dbmod.CateGory.objects.get(FruitNo=l+1)
                                    for j in k:
                                        j = j
                                        l +=1
                                        l = str(l)
                                        l = '0'+l
                                        # print(l,j)
                                        # print(type(Data.ImageID))
                                        cat.append(l)
                                        dj.append(f'<img class="column" src="{Data.category}" alt="{self.listToString(j)}" style="width:45%" alt="{j}" onclick="Command12(`{j}`);"/>')
                                        # dj.append(f'<tr><td>{l}</td><td>{j}</td></tr>')
                                res =self.listToString(dj)


                            elif sentence_words[0] == 'veget':
                                res ='</table><br><i class="fa fa-plus" aria-hidden="true"></i> Vegetables'

                            elif sentence_words[0] =='remov':
                                res454 = int(sentence_words[-1])
                                print(res454)
                                CartList.objects.get(FruitNo=res454).delete()
                                Orders.objects.get(FruitNo=res454).delete()

                                res = '<i class="fa fa-trash-o" aria-hidden="true"></i> Product Deleted Successfully<br>Show Your Cart Details Please click cart button <b><i class="fa fa-shopping-bag" aria-hidden="true"></i><button onclick="Command(`Cart`);">Cart</button></b><br>Conform Yor Order <b>YES / NO</b>'

                            elif sentence_words[0] == 'restart':
                                CartList.objects.all().delete()
                                Orders.objects.all().delete()
                                res = '<form action="/" method="get" > </form>'

                            elif sentence_words[0] == 'ord':

                                # CartList.objects.all().delete()
                                for s in cur.execute('SELECT Cartitem FROM app_orders;'):
                                    for j in s:
                                        dj.append(j)

                                print(self.listToString(dj))
                                res = self.listToString(dj) + f'</table>'

                            elif sentence_words[0] == 'ye':
                                letters = string.digits;
                                rand = ''.join(random.choice(letters) for i in range(10));
                                res = f'Order is Conform <i class="fa fa-check-circle" aria-hidden="true"></i><br><br><b>Enter Your Full Name</b><input type="text" style="width: 100%" id="quantity{rand}" />&nbsp;</input><br><b>Enter Your Full Address </b><input type="text" style="width: 100%" id="quantity{rand}" />&nbsp;</input><br><b>Enter your Phone Number </b><input type="number" style="width: 100%"> <br><button onclick="AddItemToCart(`data saved`, `quantity{rand}`)\">Submit</button>'

                            elif sentence_words[0] == 'dat':
                                CartList.objects.all().delete()

                            elif len(sentence_words) <= 1:
                                res = self.data_merge(sentence_words[0], sentence)
                                print('2', res)

                            elif len(sentence_words)>=1 and len(sentence_words)<=2:
                                if len(sentence_words[-1])<3:
                                    res = self.data_Calculaion(sentence)
                                    print('2', len(sentence_words[-1]))
                                else:
                                    res = self.data_merge(sentence_words[0], sentence)
                                    print('2', len(sentence_words[-1]))

                            elif len(sentence_words)>=2 and len(sentence_words)<=4:
                                if len(sentence_words[-1]) < 3:
                                    res = self.data_Calculaion(sentence)
                                    print('3', len(sentence_words[-1]))
                                else:
                                    res = self.data_merge(sentence_words[0], sentence)
                                    print('3', len(sentence_words[-1]))

                            return random.choice(i['responses']) + res

                return "I can't guess"
