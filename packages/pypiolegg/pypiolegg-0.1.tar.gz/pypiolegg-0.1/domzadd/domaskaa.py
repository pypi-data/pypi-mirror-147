import re
value = input('Value: ')
email_rgx = re.compile(r'''([0-9A-Za-z!#=?/^_`{|}~%&'*+-]{1,}([0-9A-Za-z!#=?/^_`{|}~%&'*+-]{0,}[.]{0,1}
|[.]{0,1}[0-9A-Za-z!#=?/^_`{|}~%&'*+-]{1,})[0-9A-Za-z!#=?/^_`{|}~%&'*+-]{0,})@([A-Za-z0-9]{1,}[A-Za-z0-9-]{0,}
[A-Za-z0-9]{1,}\.[A-Za-z0-9]{1,}[A-Za-z0-9-]{0,}[A-Za-z0-9]{1,}){0,63}''',re.X)
if re.fullmatch(email_rgx, value):
    print('Match.')
else:
    print("Not match")
    
    
def some_num(numbers:int)->int:
    numbers=int(input("число:"))
    numbers =[i for i in range(numbers+1)]
    return(numbers)
print(some_num(3))