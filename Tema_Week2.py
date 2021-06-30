my_list = [7,8,9,2,3,1,4,10,5,6]

asc_list = my_list.copy()
asc_list.sort()

print("Lista initiala: " + str(my_list))
print("Lista ascendet ordonata " + str(asc_list))
print("Lista descendet ordonata " + str(asc_list[::-1]))
print("Lista elementele pare " + str(asc_list[1::2]))
print("Lista elementele impare " + str(asc_list[0::2]))
print("Lista elementele multiplu 3 " + str(asc_list[2::3]))






