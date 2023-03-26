#------------------------------------------------ GUI Game - The Ant and the Grasshopper -------------------------------------------------------

#------------------------------------------------------ Developed by Sharada Shehan -------------------------------------------------------------

# modules

import tkinter as tk
from tkinter import ttk
from random import sample , choice
from timeit import default_timer as timer

# main window

root = tk.Tk()
root.title("Main")
root.resizable(False,False)
root.geometry('1200x573+100+100')

# images

ant_img = tk.PhotoImage(file='./Images/ant.png')
grasshopper_forward_img = tk.PhotoImage(file='./Images/grasshopper_forward.png')
grasshopper_backward_img = tk.PhotoImage(file='./Images/grasshopper_backward.png')

ant_hill_0_img = tk.PhotoImage(file='./Images/ant_hill_0.png')
ant_hill_1_img = tk.PhotoImage(file='./Images/ant_hill_1.png')
ant_hill_2_img = tk.PhotoImage(file='./Images/ant_hill_2.png')
ant_hill_3_img = tk.PhotoImage(file='./Images/ant_hill_3.png')

log_0_img = tk.PhotoImage(file='./Images/log_0.png')
log_1_img = tk.PhotoImage(file='./Images/log_1.png')
log_2_img = tk.PhotoImage(file='./Images/log_2.png')
log_3_img = tk.PhotoImage(file='./Images/log_3.png')

heading_img = tk.PhotoImage(file='./Images/heading.png')
controls_img = tk.PhotoImage(file='./Images/controls.png')
highscores_img = tk.PhotoImage(file='./Images/highscores.png')
footer_img = tk.PhotoImage(file='./Images/footer.png')

Difficulty_img = tk.PhotoImage(file='./Images/Difficulty.png')
Easy_img = tk.PhotoImage(file='./Images/Easy.png')
Normal_img = tk.PhotoImage(file='./Images/Normal.png')
Hard_img = tk.PhotoImage(file='./Images/Hard.png')

Enter_name_img = tk.PhotoImage(file='./Images/Enter_name.png')
game_over_img = tk.PhotoImage(file='./Images/game_over.png')
you_win_img = tk.PhotoImage(file='./Images/you_win.png')
Exit_img = tk.PhotoImage(file='./Images/Exit.png')


ant_hill_images = [ant_hill_0_img,ant_hill_1_img,ant_hill_2_img,ant_hill_3_img]
log_images = [log_0_img,log_1_img,log_2_img,log_3_img]

# Top Frame

Top = tk.Frame(root)
Top.pack(side='top')
label = tk.Label(Top,image=heading_img)
label.pack(pady=(3,0))

# Middle Frame

Middle = tk.Frame(root)
Middle.pack(side='top')
canvas = tk.Canvas(Middle,width=1200,height=250,background='#00ff08')
canvas.pack()

# Bottom Frame

Bottom = tk.Frame(root)
Bottom.pack(side='top')
label = tk.Label(Bottom,image=controls_img)
label.pack(side='left')
label = tk.Label(Bottom,image=highscores_img)
label.pack(side='top')

# treeview 

style = ttk.Style()
style.configure('Treeview',background='#36e0ff',fieldbackground='#36e0ff',font=('Arial',10),rowheight=22)
style.map('Treeview',background=[('selected','#36e0ff')])

tv = ttk.Treeview(Bottom,height=5,show='headings',selectmode='none',columns=('#1','#2','#3'),padding=(5,5))

tv.heading('#1',text='Name',command=lambda:tree_sort(0))
tv.heading('#2',text='Time',command=lambda:tree_sort(1))
tv.heading('#3',text='Difficulty',command=lambda:tree_sort(2))

tv.column('#1',anchor='center')
tv.column('#2',anchor='center')
tv.column('#3',anchor='center')

tv.pack(side='top',padx=5,pady=5)

# footer

frame_foot = tk.Frame(root)
frame_foot.pack(side='top')
label_foot = tk.Label(frame_foot,image=footer_img)
label_foot.pack()

# difficulty selection window

top_window = tk.Toplevel()
top_window.geometry('500x310+300+150')
top_window.transient(root)
top_win_frame = tk.Frame(top_window)
top_win_frame.pack()
label = tk.Label(top_win_frame,image=Difficulty_img)
label.pack(side='top',pady=(20,0))

top_btn_1 = tk.Button(top_win_frame,image=Easy_img,command=lambda:main(1))
top_btn_1.pack(side='top')
top_btn_2 = tk.Button(top_win_frame,image=Normal_img,command=lambda:main(2))
top_btn_2.pack(side='top')
top_btn_3 = tk.Button(top_win_frame,image=Hard_img,command=lambda:main(3))
top_btn_3.pack(side='top')

# sorting highscores

def tree_sort(column) :
	
	global highscores
	
	for x in range(len(highscores)) :
		tv.delete(f'i{x}')
	highscores = sorted(highscores,key=lambda item:item[column])
	for x in range(len(highscores)) :
		tv.insert('',x,values=highscores[x],iid=f'i{x}')

# automated ants' motion

def ant_animations () :
	
	global ant_positions
	global number_of_ants
	global positions
	global ants
	global canvas
	
	selections = [-100,0,100]
	new_ant_positions = [0 for x in range(number_of_ants)]
	
	while True :
		
		choiced = [0 for x in range(number_of_ants)]
		for x in range(number_of_ants) :
			choiced[x] = choice(selections)
			new_ant_positions[x] = ant_positions[x] + choiced[x]
		if len(new_ant_positions) == len(set(new_ant_positions)) and set(new_ant_positions).issubset(set(positions)) :
			ant_positions = new_ant_positions
			break

	for x in range(number_of_ants) :
		tag = f'tag{x}'
		canvas.move(tag,choiced[x],0)
		canvas.update()

	root.after(2000,ant_animations)

# save new highscore

def highscore_set(name,difficulty,time) :
	
	if len(name.strip()) > 0 :
		file = open('highscores.txt','a')
		txt = str(name) + '\t' + str(difficulty) + '\t' + str(time) + '\n'
		file.write(txt)
		file.close()
	
	root.destroy()

# check states

def check (difficulty) :
	
	global grasshopper_position
	global ant_positions
	global log_number
	global start
	global root
	
	while True :
		
		if grasshopper_position in ant_positions :
			lost_window = tk.Toplevel()
			lost_window.geometry('400x265+400+180')
			label_l = tk.Label(lost_window,image=game_over_img)
			label_l.pack(side='top')
			root.unbind('<Key>')
			exit_btn = tk.Button(lost_window,image=Exit_img,command=root.destroy)
			exit_btn.pack(side='top')
			break
		
		if log_number == 3 :
			stop = timer()
			win_window = tk.Toplevel()
			win_window.geometry('500x300+200+200')
			#win_window.overrideredirect(True)
			root.unbind('<Key>')
			label_l = tk.Label(win_window,image=you_win_img)
			label_l.pack(side='top')
			new_score_window = tk.Toplevel()
			new_score_window.geometry('500x220+700+250')
			new_score_window.transient(win_window)
			label_top = tk.Label(new_score_window,image=Enter_name_img)
			label_top.pack(side='top',pady=(20,0))
			entry = tk.Entry(new_score_window,font=('Arial',20))
			entry.pack(side='top')
			exit_btn = tk.Button(new_score_window,image=Exit_img,command=lambda:highscore_set(entry.get(),stop-start,difficulty))
			exit_btn.pack(side='top',padx=5,pady=5)
			break
		
		root.update()

# user's responses

def keyboard (event) :
	
	global grasshopper_position
	global grasshopper_positions
	global grasshopper_tag
	global ant_hill_tag
	global log_tag
	global ant_hill_images
	global log_number
	global canvas
	
	grasshopper_positions = [x for x in range(100,1100,100)]
	
	if event.char == 'd' :
		new_grasshopper_position = grasshopper_position + 100
		if new_grasshopper_position in grasshopper_positions :
			grasshopper_position = new_grasshopper_position
			canvas.move(grasshopper_tag,100,0)
			canvas.update()
	
	if event.char == 'a' :
		new_grasshopper_position = grasshopper_position - 100
		if new_grasshopper_position in grasshopper_positions :
			grasshopper_position = new_grasshopper_position
			canvas.move(grasshopper_tag,-100,0)
			canvas.update()
	
	if event.char == 'e' :
		new_grasshopper_position = grasshopper_position + 200
		if new_grasshopper_position in grasshopper_positions :
			grasshopper_position = new_grasshopper_position
			canvas.move(grasshopper_tag,200,0)
			canvas.update()
	
	if event.char == 'q' :
		new_grasshopper_position = grasshopper_position - 200
		if new_grasshopper_position in grasshopper_positions :
			grasshopper_position = new_grasshopper_position
			canvas.move(grasshopper_tag,-200,0)
			canvas.update()
	
	if event.char == 'w' :
		if grasshopper_position == 1000 and grasshopper_tag == 'grasshopper_forward':
			canvas.delete('grasshopper_forward')
			grasshopper_tag = 'grasshopper_backward'
			canvas.create_image(1000,230,image=grasshopper_backward_img,anchor='sw',tags=grasshopper_tag)
			canvas.delete(ant_hill_tag)
			new_ant_hill_number = int(float(ant_hill_tag[-1]))-1
			ant_hill_tag = ant_hill_tag[:-1] + str(new_ant_hill_number)
			canvas.create_image(980,150,image=ant_hill_images[new_ant_hill_number],anchor='sw',tags=ant_hill_tag)
			canvas.update()
	
	if event.char == 's' :
		if grasshopper_position == 100 and grasshopper_tag == 'grasshopper_backward':
			canvas.delete('grasshopper_backward')
			grasshopper_tag = 'grasshopper_forward'
			canvas.create_image(100,230,image=grasshopper_forward_img,anchor='sw',tags=grasshopper_tag)
			canvas.delete(log_tag)
			log_number = int(float(log_tag[-1]))+1
			log_tag = log_tag[:-1] + str(log_number)
			canvas.create_image(20,150,image=log_images[log_number],anchor='sw',tags=log_tag)
			canvas.update()

# basic settings before user's response

def main(level) :
	
	global ant_positions
	global number_of_ants
	global positions
	global ants
	global grasshopper_position
	global grasshopper_tag
	global ant_hill_tag
	global log_tag
	global log_number
	global start
	global canvas
	global root
	global tv
	global highscores

	top_window.destroy()

	number_of_ants = level
	if level == 1 :
		difficulty = 'Easy'
	elif level == 2 :
		difficulty = 'Normal'
	elif level == 3 :
		difficulty = 'Hard'

	positions = [x for x in range(200,1100,100)]
	ant_positions = sample(positions,number_of_ants)
	ant_positions.sort()
	ants = []
	for x in range(number_of_ants) :
		tag = f'tag{x}'
		ants.append(canvas.create_image(ant_positions[x],230,image=ant_img,anchor='sw',tags=tag))

	ant_hill_tag = 'ant_hill_3'
	ant_hill_3_obj = canvas.create_image(980,150,image=ant_hill_3_img,anchor='sw',tags=ant_hill_tag)

	log_tag = 'log_0'
	log_number = 0
	log_0_obj = canvas.create_image(20,150,image=log_0_img,anchor='sw',tags=log_tag)

	file = open('highscores.txt','a')
	file.close()

	highscores = []
	file = open('highscores.txt','r')
	for record in file :
		highscores.append(record.strip().split('\t'))
	file.close()

	for item in highscores :
		item[1] = float(item[1])

	weight = {
	'Easy' : 125 ,
	'Normal' : 25 ,
	'Hard' : 5 
	}

	highscores = sorted(highscores,key=lambda item:weight[item[2]]*float(item[1]))
	for x in range(len(highscores)) :
		tv.insert('',x,values=highscores[x],iid=f'i{x}')

	start = timer()
	
	root.after(2000,ant_animations)
	
	grasshopper_tag = 'grasshopper_forward'
	grasshopper_forward_obj = canvas.create_image(100,230,image=grasshopper_forward_img,anchor='sw',tags=grasshopper_tag)
	grasshopper_position = 100
	
	root.after(0,lambda:check(difficulty))

	root.bind('<Key>',keyboard)	


root.mainloop()


