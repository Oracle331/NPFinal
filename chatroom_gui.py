import tkinter as tk


class Gui():
    def __init__(self):
        self.root = tk.Tk()

    def exitClick(self, event):
        exit(0)

    def sendMessageClick(self, event, textField, chat):
        chat.insert(tk.END, textField.get())
        print(textField.get())
        textField.delete(0, "end")  # clears textField

    def updateUsers(self, userPanel, username):
        userPanel.insert(tk.END, username)

    def run(self):
        # root = tk.Tk()
        self.root.title("Laucer's chat")
        # self.root.minsize(600, 400)
        self.root.bind("<Return>", lambda event: self.sendMessageClick(event, textField))  # enter

        mainFrame = tk.Frame(self.root)
        mainFrame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # ChatField
        chat = tk.Listbox(mainFrame, width=200, height=40)
        chat.insert(tk.END, 'Chat History')
        # chat.configure(state="disabled")  #
        chat.grid(column=0, row=0, sticky=tk.N + tk.S + tk.W + tk.E)

        # TextFieldToSend
        textField = tk.Entry(mainFrame)
        textField.grid(column=0, row=1, sticky=tk.N + tk.S + tk.W + tk.E)

        # SendMessageButton
        buttonSend = tk.Button(mainFrame)
        buttonSend["text"] = "Send Message"
        buttonSend.grid(column=0, row=2, sticky=tk.N + tk.S + tk.W + tk.E)
        buttonSend.bind("<Button-1>", lambda event: self.sendMessageClick(event, textField, chat))

        # usersPanel
        usersPanel = tk.Listbox(mainFrame)
        usersPanel.insert(1, "Connected Users")
        usersPanel.grid(column=2, row=0, sticky=tk.N + tk.S + tk.W + tk.E)
        # usersPanel.bind("<Button-1>", lambda event: self.updateUsers(usersPanel,username))

        # ExitButton
        buttonExit = tk.Button(mainFrame)
        buttonExit["text"] = "Exit"
        buttonExit["background"] = "gray"
        buttonExit.grid(column=2, row=2, sticky=tk.N + tk.S + tk.W + tk.E)
        buttonExit.bind("<Button-1>", self.exitClick)

        self.root.mainloop()


GuiThread = Gui()
GuiThread.run()
