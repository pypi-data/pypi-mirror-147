import webbrowser

class Mangostk :
    '''
	Example:
	m = Mangostk()
    m.trend(open=True) # True = open in webrowser
    m.what_is_it()
    m.how2make(open=True)
    m.ingredient()
    m.showpic()
	'''
    
    def __init__(self) :
        self.pic = 'https://upload.wikimedia.org/wikipedia/commons/5/5d/Mango_sticy_rice_%283859549574%29.jpg'
        self.youtube = 'https://www.youtube.com/results?search_query=how+to+make+mango+sticky+rice'
        self.trends = 'https://trends.google.com/trends/explore?q=mango%20sticky%20rice'

    def trend(self,open=False):
        print(f'trending : {self.trends}')
        if open :
            webbrowser.open(self.trends)

    def what_is_it(self):
        text = '''
        mango sticky rice is Thai dessert made with glutinous rice, fresh mango and coconut milk
        that treding from MILLI (https://www.facebook.com/profile.php?id=100044389129163) 
        she is a Thai female rapper and singer. in coachella 2022 
        '''
        print(text)

    def how2make(self,open=False):
        print(f'how to make : {self.youtube}')
        if open :
            webbrowser.open(self.youtube)
    
    def ingredient(self):
        text = '''
        For the sticky rice :
        1 kg. Thai sticky rice (ข้าวเหนียว)
        800 ml. coconut cream (หัวกะทิ) 
        - If you can't get fresh coconut milk, this is my favorite type in the box.
        150 g. sugar (น้ำตาลทราย)
        1 tsp. salt (เกลือ)
        For the mango

        Sweet yellow mangoes (มะม่วงนำ้ดอกไม้)
        100 g. yellow mung beans (ถั่วเหลือง) - optional
        For the coconut cream topping

        200 ml. coconut cream (หัวกะทิ)
        1/3 tsp. salt (เกลือ)
        '''
        print(text)

    def showpic(self):
        webbrowser.open(self.pic) 

    def show_ascii(self):
        text = '''
        ad88                        88          
        d8"                          ""   ,d     
        88                                88     
        MM88MMM 8b,dPPYba, 88       88 88 MM88MMM  
        88    88P'   "Y8 88       88 88   88     
        88    88         88       88 88   88     
        88    88         "8a,   ,a88 88   88,    
        88    88          `"YbbdP'Y8 88   "Y888  
                
    '''
        print(text)


if __name__ == '__main__' :

    m = Mangostk()
    m.trend(open=True)
    m.what_is_it()
    m.how2make(open=True)
    m.ingredient()
    m.showpic()
    m.show_ascii()