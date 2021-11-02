

alphabet = []      #список для алфавита 
code = []          #список для зашифрованного текста


with open('alph.txt') as file:       #считываем из файла алфавит "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789 .,!?:"%-+=/"
    for items in file:
        alphabet += list(items)

with open('sec.txt') as file:       #считываем из файла зашифрованный текст
    for items in file:
        code += list(items)


freq_dict = {}                     #словарь для значений частотного анализа. значения взяты из Вики
current_dict = {}                  #словарь для значений частотного анализа текущего текста

with open('frequency analysis.txt') as file:   #считываем значения частотного анализа из файла, где key - символ, value - вероятность встречаемости 
    for items in file:
        key, value = items.split()
        freq_dict[key] = value
        current_dict[key] = 0

sumbCnt = 0.0
for i in code:                     #анализируем текст и в словарь записываем, сколько раз буква встречается в тексте. игнорируем "123456789 .,!?:"%-+=/"
    sumbCnt += 1
    if i in current_dict:
        current_dict[i] += 1

for key in current_dict:                                       #рассчитывем вероятности для каждой буквы
    current_dict[key] = (current_dict[key] / sumbCnt) * 100

deff = 0.25                                                    #допустимая погрешность
slides = []                                                    #список для вероятных значений шага в шифре
curr_ind = 1
freq_ind = 1

for key in current_dict:                                       #находим вероятные ключи для заданного шифра

    for k in freq_dict:
        if (float(current_dict.get(key)) >= (float(freq_dict.get(k)) - deff)) and (float(current_dict.get(key)) <= (float(freq_dict.get(k)) + deff)):
            slides.append(curr_ind-freq_ind)
        freq_ind += 1
    curr_ind += 1
    freq_ind = 0

slides.sort(reverse=False)                                   #сортируем список с найденными ключами по возрастанию

cnt = 0
max_cnt = 0
slide = 0
repeat_slides = []                                           #список для ключей шифра, которые с одинаковой вероятностью могут быть заданы
repeat_ind = 0

for i in range(1, len(slides)):                              #находим вероятные ключи шифра
    if slides[i-1] == slides[i]:
        cnt += 1
    else:
        if cnt > max_cnt:
            max_cnt = cnt
            slide = slides[i-1]
        elif cnt == max_cnt and cnt != 0 and max_cnt != 0:
            repeat_slides.append(slides[i-1])
            repeat_ind += 1
        cnt = 0

repeat_slides.insert(0, slide)



def hack(slide):                                           #функция расшифровки текста, где на вход мы подаем возможный ключ 
    list = []
    list.clear()
    for i in code:
        t = alphabet.index(i)
        new = t + slide
        if abs(new) > len(alphabet):
            new = abs(new) - len(alphabet)

        if i in alphabet:
            list += alphabet[new]
        else:
            list += i

    return list

text = []
filename = "test"
f = open(filename + ".txt", "a", encoding='utf-8')
for i in repeat_slides:                                    #проходим по всем найденным вероятным ключам и записываем расшифрованное сообщение в файл
    text = hack(i)
    f.write('key is ')
    f.write(str(i))
    f.write(' --- ')
    for j in range(len(text)):
        f.write(str(text[j]))
    f.write("\n")

f.write("\n")
f.close()





