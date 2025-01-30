a = int(input("enter a size:"))
for i in range(a):
    if i==0 or i==a-1:
        print(" *" * a)
    else:
      print(" *" + " " *((a-2)*2) +" *")   
