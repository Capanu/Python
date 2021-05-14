
my_list = [7,8,9,2,3,1,4,10,5,6]
sort_asc = my_list.copy()
sort_desc = my_list.copy()

sort_asc.sort(reverse=False)
sort_desc.sort(reverse=True)
print("Lista mea este: " + str(my_list))
print("Lista mea sortata ascendent: " + str(sort_asc))
print("Lista mea sortata descendent:" + str(sort_desc))
print("Elementele impare ale listei sunt: " + str(sort_asc[0:len(my_list):2]))
print("Elemente pare ale  listei sunt: " + str(sort_asc[1:len(my_list):2]))
print("Elemente multiplii de 3 sunt: " + str(sort_asc[2:len(my_list):3]))