import pymongo

from functools import wraps

db = None

def singleton(cls):
    @wraps(cls)
    def paramholder ( *param):
        global db
        if db == None:
            db = cls( *param )
        return db
    return paramholder

@singleton
class DbConnection(object):
    '''MongoDB connection class'''
    
    db = None
    
    def __init__(self,dbname,host='localhost',port=27017):
        '''DbConnection constructor'''
        self.host=host
        self.port=port
        self.dbname=dbname
        self.connect()
    
    def connect(self):
        '''Connect to database'''
        conn = pymongo.Connection(self.host,self.port)
        self.db = conn[self.dbname]


class Model(object):
    '''Base class for models'''
    data = {}
    def put(self):
        '''Save object to Mongo'''
        collection = db[self.__class__.__name__]
        if not '_id' in self.data.keys():
            collection.insert(self.data)
        else:
            collection.update({'_id':self.data['_id']},self.data)
        
    def get(self,id=None):
        '''Get object from Mongo'''
        if not id:
            if not '_id' in self.data.keys():
                raise Exception('No _id provided. Unable get object from Mongo!')
            else:
                _id = self.data['_id']
        else:
            _id = id
        collection = db[self.__class__.__name__]
        self.data = collection.find_one({'_id':_id})

if __name__  == '__main__':
    db = DbConnection('test').db
    test = Model()
    test.data = {'a':'b'}
    print(test.data)
    test.put()
    test.get()
    print(test.data)
    