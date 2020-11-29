import sys
import numpy as np
from PIL import Image, ImageDraw

# Вказуємо розмір зображення
WIDTH = 540
HEIGHT = 960

# Колір вказується у форматі Red Green Blue, тобто займає
# 3 числа якщо зберігати їх у списку
RGB = 3

# Колір фона - чорный
# Колір точок - білий
BG_COLOR = [255, 255, 255]
TEXT_COLOR = [0, 0, 0]
LINES=[50,5,100]

# Шлях до файлу вказується або при виклику програми (можна так само
# просто перетягнути датасет на іконку програми і воно спрацює)
# Або ж якщо нічого не вказувати, то за стандартом візьме 7-ий DS
try:
    file_path = sys.argv[1]
except Exception:
    file_path = "DS7.txt"

# Зберігається підсумковий результат під тим же ім'ям що і файл,
# тільки у форматі .png: DS7.txt -> DS7.png
save_path = file_path[:file_path.rfind('.') + 1] + 'png'

# Відкриваємо файл на зчитування
with open(file_path, 'r') as file:
    # Проходимся по рядках файлу, ділимо їх по пропуску, записуємо
    # координати в список у вигляді числа
    data = [[int(single_cord) for single_cord in line.split()] for line in file]


# Картинка це тривимірний масив який задається висотою,
# Шириною і форматом RGB
# Задається саме в такому порядку!
# Приклад кінцевого виду:
# [ #       x_0             x_1               x_width
#   [ [255, 255, 255], [0, 144, 131], ..., [100, 200, 0] ], # y_0
#   [ [255, 255, 255], [0, 144, 131], ..., [100, 200, 0] ], # y_1
#   ...
#   [ [255, 255, 255], [0, 144, 131], ..., [100, 200, 0] ]  # y_height
# ]



image_array = np.full([HEIGHT, WIDTH, RGB], BG_COLOR, dtype=np.uint8)


# Заповнюємо масив даними з датасета
for coords_pare in data:
    x = coords_pare[0]
    y = coords_pare[1]
    image_array[y][x] = TEXT_COLOR


# Перетворюємо масив в зображення у форматі RGB
img = Image.fromarray(image_array, 'RGB')
# Перевертаємо зображення в читабельний формат
img = img.rotate(90, expand=True)


def rotate(a,b,c):  #функція порівняння двох точок
  return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])

def jarvismarch(A): #функція реалізації алгоритму Джарвіса
  n = len(A)         
  P = []
  for i in range(0,n): P.append(i)
  for i in range(1,n):
    if ((a[P[i]][0] <  a[P[0]][0]) or 
    	((a[P[i]][0] == a[P[0]][0]) and (a[P[i]][1] < a[P[0]][1]))): 
           P[i], P[0] = P[0], P[i]  
  H = [P[0]]
  line=True;   
  dj=abs(a[0][0]-a[1][0])+abs(a[0][1]-a[1][1])
  j=1
  for i in range(2,n):
    line=line and (rotate(a[P[0]],a[P[1]],a[P[i]])==0)
    di=abs(a[P[0]][0]-a[P[i]][0])+abs(a[P[0]][1]-a[P[i]][1])
    if dj<di:
      j=i
      dj=di
    if (not line): break
  if (line):
    H.append(P[j])
    return H  
  del P[0]
  P.append(H[0])
  while True:  
    right = 0
    for i in range(1,len(P)):
      if rotate(A[H[-1]],A[P[right]],A[P[i]])<0:
        right = i
    if P[right]==H[0]: 
      break
    else:
      H.append(P[right])
      del P[right]
  return H
a = data

numbers=jarvismarch(a)

data_dots=[]

for i in numbers:
	data_dots.append(data[i])

#створюємо новий файл, де запишемо датасет опуклої оболонки	
new_file= open('new_dataset.txt','w')

for i in data_dots:
	i[0]=540-i[0]
	new_file.write(str(i))
	new_file.write('\n')
print(data_dots)

all=[]
for lst in data_dots:
	all.extend(list(reversed(lst)))
print (all)
new_line='#0000ff'

MyDraw=ImageDraw.Draw(img)
MyDraw.line(all,width=2,fill=new_line,joint='curve')

# Показуємо зображення
img.show()
# Зберігаємо зображення
img.save(save_path)