
Installation
-------------


    ```pip install listinfo```

Example
---------



from listinfo import listinfo

sample_list=[1,2,3,4,5,6]

ls=listinfo(sample_list)

print(ls.liststats())

print(ls.listtochunks(chunk=3))

print(ls.splitlist(splitval=2))



Params
---------


Below are few parameters and functions we have to provide according to our requirements:


1 `liststats:(No Parameters Required)`

Here we get statistics of list. The ouput what we get will be in `dict` fromat.
There will be four values(`length`,`datatype and count`,`list to tuple`,`size of list`) in the output.

`length`:It shows the length of list.
`datatype and count`:It demonstrates how many types of datatypes and thier count.
`list to tuple`: It is the tuple version of list.
`memory usage`: It shows memory storaged used by list(in bytes).

OUTPUT EXAMPLE:
`{'length': 6, 'datatype and count': {<class 'int'>: 6}, 'list to tuple': (1, 2, 3, 4, 5, 6), 'memory usage': '136 bytes'}`


2 `listtochunks(chunk='')`

DEFAULT VALUE=1

It converts list to chunks. chunk is the param,where we have to size of chunk.

OUTPUT EXAMPLE:
`[[1, 2, 3], [4, 5, 6]]`


3 `splitlist(splitval='')` 

DEFAULT VALUE=1

It splits list to lists of list of size splival.

OUTPUT EXAMPLE:
`[[1, 2], [3, 4], [5, 6]]`


`More Updates Coming Soon...` 😄


Contact
---------
I would like to get feedback from the community. If you have feature suggestions, support questions or general comments, please email me at susmit.vssut@gmail.com

