# ds_homework1
Distributed Systems course homework 1

How to succesfully run the program (do only this actions):<br>
1. Change server IP on yours in server/server_side.py<br>
2. Write this IP also to all clients: client1/client_side1.py, client2/client_side2.py, client3/client_side3.py<br>
3. Check if ports 50001, 50002, 50003 on server are free. If not, using terminal kill processes in ports (in Unix sudo kill -9 PID).<br>
4. run server/server_side.py<br>
5. run all or some of clients: client1/client_side1.py, client2/client_side2.py, client3/client_side3.py<br>
6. Follow the instructions in clients' terminal. <br>
	a) Decision 1 means uploading existing file. You should have a txt file in clients directory and write its name when you are asked to. <br>
	b) Decision 2 means creating new file. Simply write a unique file name in format 'name.txt'<br>
	c) Decision 3 means working on exisiting file. You should write a filename from a list of existing file as well as to know password to the file. By default you can work on file 'file1.txt', the password for this file is '123'.<br>
7. GUI will be run if everything is entered correctly.<br>
<br>
How to use GUI of collaborative editor:<br>
In this version (1.0) for appropriate work it is not reccomended to <br>
	1. Use button bindings as Ctrl+x, Ctrl+v, except Ctrl+c.  <br>
	2. Push several buttons at once or hold button as long as you want.<br>
	3. Use all function buttons, as F1-F12, etc. <br>
	4. Because of GUI from Tkinter, you also should not press Backspace, in the empty string.<br>

You can use following functional buttons: Enter, Backspace (except case 4 above), Shift.   <br>
	
