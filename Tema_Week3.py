def sum_function(*args, **kwargs):
    sum = 0
    for elem in args:
        if "int" in str(type(elem)) or "float" in str(type(elem)):
            sum += elem
    print(sum)

def rec_function(n, my_list = [0,0,0]):
    res_list = my_list.copy() # copy  the partial result
    my_list = [0, 0, 0] # set the value  on 0 list, to don t maintain it


    if n <= 0:
        return  res_list

    if n %2 == 0:
        res_list[1]+= n # even position sum
    else:
        res_list[2] += n # oodd position sum
    res_list[0] += n # position for total sum

    return rec_function(n-1, res_list)
def ret_int():
    try:
        my_var = input("input a int number: ")
        int_val = int(my_var)
    except ValueError as e:
        return 0
    else:
        return int_val

if __name__=="__main__":
    sum_function(1, 5, -3, 'abc', [12, 56, 'cad'])
    sum_function()
    sum_function(2, 4, 'abc', param_1 = 2)

    print(rec_function(10))
    print(rec_function(5))
    print("Your values is " + str(ret_int()))

