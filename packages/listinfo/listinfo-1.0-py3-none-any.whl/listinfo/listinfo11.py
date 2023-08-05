import numpy as np
from collections import Counter

class listinfo():
    
    def __init__(self,ls):
        self.ls=ls
        
    def liststats(self):
        try:
            if  isinstance(self.ls, list)==True:
                return {
                    "length":len(self.ls),
                    "datatype and count":dict(Counter([type(i) for i in self.ls])),
                    "list to tuple": tuple(self.ls),
                    "memory usage":str(self.ls.__sizeof__())+" bytes"
                }
            else:
                return "Input  is not a list"
        except Exception as e:
            return e
        
    def listtochunks(self,chunk=''):
        try:
            if isinstance(self.ls, list)==True:
                if chunk=='':
                    n=1
                    return [self.ls[i * n:(i + 1) * n] for i in range((len(self.ls) + n - 1) // n )]
                else:
                    n=chunk
                    return [self.ls[i * n:(i + 1) * n] for i in range((len(self.ls) + n - 1) // n )]
        except Exception as e:
            return e
        
    
    def splitlist(self,splitval=''):
        try:
            if isinstance(self.ls, list)==True:
                if splitval=='':
                    final_list = np.array_split(self.ls,1)
                    split_items = []
                    for i in final_list:
                        split_items.append(list(i))
                    return split_items
                else:
                    final_list = np.array_split(self.ls,splitval)
                    split_items = []
                    for i in final_list:
                        split_items.append(list(i))
                    return split_items
        except Exception as e:
            return e
    

                

if __name__ == "__main__":
    ls=['11','44','55']
    aa = listinfo(ls)
    print(aa.liststats())
    print(aa.listtochunks(chunk='jkjkj'))
    print(aa.splitlist(splitval='hughg'))
    
   



