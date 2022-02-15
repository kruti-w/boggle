import GUI


def main():
    # pop up a window when run
    root = GUI.tk.Tk()                  # creates root object,
    window = GUI.Boggle(master=root)    # initializes main GUI class.
    window.mainloop()                   # enters GUI loop


if __name__ == '__main__':
    main()
