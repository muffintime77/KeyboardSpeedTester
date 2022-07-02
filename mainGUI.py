from tkinter import *
from tkinter import filedialog as fd
import datetime 
import os
import time
import random
#-----------------------------------------------------------------------
#	
def to_file():
	global config_dict
	with open('tester.conf','w') as out:
		for key,val in config_dict.items():
			out.write('{}={}\n'.format(key,val))
#	
def file_to():
	global config_dict
	with open('tester.conf') as inp:
		for i in inp.readlines():
			key,val = i.strip().split('=')
			config_dict[key] = val
		config_dict["sumTodayGame"] = int(config_dict["sumTodayGame"])
		config_dict["last_score"] = int(config_dict["last_score"])
		config_dict["leader_score"] = int(config_dict["leader_score"])
	print(config_dict)
#	
def openDict():
	global DictList
	global patchFileAbsolute 
	patchFileAbsolute = fd.askopenfilename(
					filetypes=(("TXT files", "*.txt"),
						("ALL files", "*.*")
						)
						)
	lbl_dict = Label(win, text = os.path.basename(patchFileAbsolute), font=(20)).grid(row=4, column=0,stick="n", padx=15,pady=1)
	DictList = [line.rstrip('\n') for line in open(patchFileAbsolute)]
#		
def startGame():
	# запускаем игру, не трогаем фичу сворачивания окон.она под вопросом
	win.iconify()
	# переменные начала и разницы времени тренеровки
	global rand_text
	global sec_game_start
	global sum_slov
	global DictList
	now = datetime.datetime.now()
	sec_game_start = now.second + (now.minute * 60) + (now.hour * 60 * 60) + (now.day * 60 * 60 * 60)
	score_int = 0
	sum_slov = 0
	rand_text = 0
	#	функция обработки ввода 
	def inputText(event):
		global rand_text
		global sum_slov
		global DictList
		global max_slov
		global score_int
		# обработка исключения пустого поля лимита слов в главном окне
		try:
			max_slov = int(ent_key_set.get())
		except ValueError:
			max_slov = 60
		# получаем введоное слово
		tempGetEnt = ent_key.get()
		# рудимент
		print(tempGetEnt)
		# очищаем и пересоздаем окно ввода слова
		ent_key.delete(0, END)
		ent_key.grid(row=2, column=0, stick="e", padx=5, pady=5)
		#--------------------------------------------------------------- # если случайное из словаря == введеному то
		if DictList[rand_text] == tempGetEnt:
			# увеличить счетчик угаданых символов
			sum_slov += len(DictList[rand_text])
			# загадать новое слово
			rand_text = random.randint(0, len(DictList)-1)
			# перевывести новое слово в окно
			lbl_text = Label(winGame, text=DictList[rand_text], font=(20), ).grid(row=0, column=0, stick="we", padx=5, pady=15)
			print(sum_slov)
		else:
			lbl_text = Label(winGame, text=DictList[rand_text], font=(20), bg="red").grid(row=0, column=0, stick="we", padx=5, pady=15)
		#--------------------------------------------------------------- # если набрали заданное значение
		if sum_slov > max_slov:
			# увеличиваем значение сегодняшних тренировок
			config_dict["sumTodayGame"] += 1
			# считаем симв\мин, записываем результаты, сохраняем в файл
			now = datetime.datetime.now()
			sec_game_stop = now.second + (now.minute * 60) + (now.hour * 60 * 60) + (now.day * 60 * 60 * 60)
			global sec_game_start
			sec_game_start = sec_game_stop - sec_game_start
			print(sec_game_start) # выводим сколько шла тренировка
			try:
				score_int = int(sum_slov // (sec_game_start / 60))
			except ZeroDivisionError:
				score_int = 0
			config_dict["last_date"] = now.strftime("%d-%m-%Y %H:%M")
			config_dict["last_score"] = score_int
			# удаляем лимит слов из поля главного окна
			ent_key_set.delete(0, END)
			# проверяем не установлен ли новый рекорд
			if config_dict["last_score"] > config_dict["leader_score"]:
				config_dict["leader_score"] = config_dict["last_score"]
				config_dict["leader_date"] = config_dict["last_date"]
			# сохраняем в файл
			to_file()
			# выводим в консоль
			print(score_int)
			
			# развернуть окно и удалить дочернее 
			win.deiconify()
			winGame.destroy() 
			# обновить значения в главном окне
			lbl_leaderScore = Label(win, text="Лучшее : {0} символов/мин".format(config_dict["leader_score"]), font=(20)).grid(row=0, column=0, stick="ws", padx=15,pady=15)
			lbl_leaderDate = Label(win, text = 'от: {}'.format(config_dict["leader_date"]), font=(20)).grid(row=0, column=1, stick="s", padx=15,pady=15)
			lbl_lastScore = Label(win, text="Последнее: {0} символов/мин".format(config_dict["last_score"]), font=(20)).grid(row=1, column=0,stick="wn", padx=15,pady=1)
			lbl_lastDate = Label(win, text = 'от: {}'.format(config_dict["last_date"]), font=(20)).grid(row=1, column=1,stick="n", padx=15,pady=1)
			lbl_sumToday = Label(win, text = "сегодня тренировок: {0}".format(config_dict["sumTodayGame"]), font=(20)).grid(row=3, column=1,stick="n", padx=15,pady=1)
			# обнуляем переменные 
		sec_game_stop = 0
		#--------------------------------------------------------------- #
	winGame = Toplevel(win)
	winGame.grab_set()
	winGame.focus_set()
	winGame.title("Keyboard Speed Tester")
	winGame.geometry('180x150')
	winGame.minsize(180,150)
	winGame.maxsize(180,150)
	ent_key = Entry(winGame)
	ent_key.grid(row=2, column=0, stick="e", padx=5, pady=5)
	rand_text = random.randint(0, len(DictList)-1)
	lbl_text = Label(winGame, text=DictList[rand_text], font=(20), ).grid(row=0, column=0, stick="we", padx=5, pady=15)
	winGame.bind('<Return>', inputText)
	winGame.mainloop()
#----------------------------------------------------------------------- # 
win = Tk()
win.title("Keyboard Speed Tester")
win.geometry('600x400')
win.minsize(600,400)
win.maxsize(600,400)
#----------------------------------------------------------------------- #

rbt_var = IntVar()
rbt_var.set(0)

# словарь конфигурации
config_dict = {}
# символов на 1 тренировку
max_slov = 0
# подсчет количества угаданных символов
sum_slov = 0
# переменная идекса загаданного символа
rand_text = 0
# путь до словаря
patchFileAbsolute = "base.txt"
#список слов которые будут загадыватся
DictList = [line.rstrip('\n') for line in open(patchFileAbsolute)]
#счетчик очков
score_int = 0
# таймер начала отсчета игры
sec_game_start = 0

# подсасываем сохраненные данные
file_to()
# проверяем не настал ли новый день и обновляем счетчик
now = datetime.datetime.now()
day = now.strftime("%d-%m-%Y %H:%M")
if config_dict["last_date"][0:2] != day[0:2]:
	config_dict["sumTodayGame"] = 0
	to_file()
#----------------------------------------------------------------------- #
lbl_leaderScore = Label(win, text="Лучшее: {0} символов/мин".format(config_dict["leader_score"]), font=(20)).grid(row=0, column=0, stick="ws", padx=15,pady=15)
lbl_leaderDate = Label(win, text = 'от: {}'.format(config_dict["leader_date"]), font=(20)).grid(row=0, column=1, stick="s", padx=15,pady=15)
lbl_lastScore = Label(win, text="Последнее: {0} символов/мин".format(config_dict["last_score"]), font=(20)).grid(row=1, column=0,stick="wn", padx=15,pady=1)
lbl_lastDate = Label(win, text = 'от: {}'.format(config_dict["last_date"]), font=(20)).grid(row=1, column=1,stick="n", padx=15,pady=1)

lbl_spaser = Label(win, text="	").grid(row=2, column=0, columnspan=3, stick="we", padx=5, pady=5)

btn_dict = Button(win, text="изменить словарь", command=openDict, font=(20)).grid(row=3, column=0, stick="we", padx=15,pady=5)

lbl_dict = Label(win, text = os.path.basename(patchFileAbsolute), font=(20)).grid(row=4, column=0,stick="n", padx=15,pady=1)


lbl_sumToday = Label(win, text = "сегодня тренировок: {0}".format(config_dict["sumTodayGame"]), font=(20)).grid(row=3, column=1,stick="n", padx=15,pady=1)

btn_dict = Button(win, text="тренировка", command=startGame, font=(20)).grid(row=4, column=1, stick="w", padx=75,pady=5)

time_rbt = Radiobutton(text="по кол-ву символов", variable=rbt_var, value=0).grid(row=5, column=1, stick="w", padx=5,pady=5)
ent_key_set = Entry(win)
ent_key_set.grid(row=6, column=1, stick="w", padx=5, pady=5)
#----------------------------------------------------------------------- #
win.mainloop()
#----------------------------------------------------------------------- #
