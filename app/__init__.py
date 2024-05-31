'''
my_posts=[{"title" : "title of post 1" , "content" : "content of post 1" , "id" : 1} ,
          {"title" : "favorite food" , "content" : "pizzas" , "id" : 2}] 
# as of now creating a a memory here rather in database and retrieve it in get post

def find_post(id): # this is the logic to get post by id without this manually is also possible but
    for p in my_posts:
        if p["id"]==id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts): # enumerate is used for iteration in my_posts default value is 0
        if p['id'] == id:
            return i
            ''' # this code should be in main this is for hardcoding the info which is not used nows