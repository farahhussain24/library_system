from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os.path
from tkinter import messagebox
# # importing the csv module
import csv
filename = "CS20003_Library.csv"
fields = ['title', 'author', 'subject', 'year', 'availability']


class MyBook:
    """ Creates a book object by taking arguments of title, author, subject, year and availability
        of the book.
    """
    def __init__(self, title="", author="", subject="", year="", availability="available"):
        self.title = title
        self.author = author
        self.subject = subject
        self.year = year
        self.availability = availability
    def set_title(self, title):
        self.title = title
    def set_author(self, author):
        self.author = author
    def set_subject(self, subject):
        self.subject = subject
    def set_year(self, year):
        self.year = year
    def get_title(self):
        return self.title
    def get_author(self):
        return self.author
    def get_subejct(self):
        return self.subject
    def get_year(self):
        return self.year
    def set_availability(self, availability):
        self.availability = availability
    def get_availability(self):
        return self.availability

class MyLibrary:
    """ Stores the list of books and performs operations of adding, removing, reserving and sorting books
        in the library. Maintains the books data in the file named CS20003_library.csv
    """
    bookList = []
    def add_to_library(self, book=MyBook()):
        self.book = book
        record = [self.book.get_title(), self.book.get_author(), self.book.get_subejct(), self.book.get_year(), self.book.get_availability()]
        MyLibrary.bookList.append(record)
        MyLibrary.add_to_file(record)

    @staticmethod
    def add_to_file(record):
        # checking if the file is present
        if os.path.isfile(filename):
            # writing to csv file
            with open(filename, 'a',  newline="") as csvFile:
                csvWriter = csv.writer(csvFile)
                # writing the data rows
                csvWriter.writerow(record)
        else:
            fields = ['title', 'author', 'subject', 'year', 'availability']
            with open(filename, 'w',  newline="") as csvFile:
                # creating a csv writer object
                csvWriter = csv.writer(csvFile)
                # writing the fields
                csvWriter.writerow(fields)
                # writing the data rows
                csvWriter.writerow(record)

    @staticmethod
    def update_file(record):
        fields = ['title', 'author', 'subject', 'year', 'availability']
        with open(filename, 'w', newline="") as csvFile:
            # creating a csv writer object
            csvWriter = csv.writer(csvFile)
            # writing the fields
            csvWriter.writerow(fields)
            # writing the data rows
            csvWriter.writerows(record)

    def update_library(self, record):
        MyLibrary.update_file(record)

    @staticmethod
    def get_from_file():
        if os.path.isfile(filename):
            lst = []
            with open(filename, 'r') as csvFile:
                csvReader = csv.reader(csvFile)
                for row in csvReader:
                    if row:
                        if row != ["title", "author", "subject", "year", "availability"]:
                            lst.append(row)
            return lst
        else:
            return None

    def get_library(self):
        MyLibrary.bookList = MyLibrary.get_from_file()
        return MyLibrary.bookList

    def sorted_books(self):
        books_list = self.get_library()
        title_list = []
        for item in books_list:
            if item:
                title_list.append(item[0])

        titles_sorted = sorted(title_list)
        book_dict = {}
        for i in range(len(titles_sorted)):
            for j in books_list:
                if titles_sorted[i] == j[0]:
                    book_dict.update({titles_sorted[i]: j})
        return book_dict

    def search_book_title(self, searchword):
        result = None
        book_dict = self.sorted_books()
        for key in book_dict:
            if searchword == key.lower():
                result = book_dict.get(key)
                break

        return result


def callback(newWindow, button):
    response = messagebox.askokcancel("Quit", "Do you want to close this window?", parent=newWindow)
    if response == 1: # if window is closed (ok)
        newWindow.destroy()
        button["state"] = "active"

def openTreeView(container, bookList):
    tree = ttk.Treeview(container, columns=fields, show='headings')
    # define headings
    tree.heading('title', text='Book Title')
    tree.heading('author', text='Author')
    tree.heading('subject', text='Subject')
    tree.heading('year', text='Publication year')
    tree.heading('availability', text='Availability')
    for row in bookList:
        tree.insert('', END, values=row)
    tree.grid(row=0, column=0, sticky='nsew')
    # add a scrollbar
    scrollbar = Scrollbar(container, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')
    return tree

def openNewWindow(title, button):
    newWindow = Toplevel(root)
    button["state"] = "disabled"
    newWindow.title(title)
    newWindow.geometry("1300x1000")
    newWindow.protocol("WM_DELETE_WINDOW", lambda: callback(newWindow, button))
    return newWindow


# Add A book in record
def addBookWindow():
    newWindow = openNewWindow("Add A book", btnAddWindow)
    # labels prompt msg
    frame = Frame(newWindow, bd=5)
    Label(frame, font=fontBig, text="Enter the Book Title").pack()
    title = Entry(frame, font=fontBig)
    title.pack()
    Label(frame, width=19, font=fontBig, text="Enter author name").pack()
    author = Entry(frame, font=fontBig)
    author.pack()
    Label(frame, width=19, font=fontBig, text="Subject").pack()
    subject = Entry(frame, font=fontBig)
    subject.pack()
    Label(frame, width=19, font=fontBig, text="Publication year").pack()
    year = Entry(frame, font=fontBig)
    year.pack()
    frame.pack()
    # Creating an object of book and library
    def add():
        book = MyBook(str(title.get()), str(author.get()), str(subject.get()), str(year.get()))
        # if str(title.get())=="" or str(author.get())=="" or str(subject.get())==" " or str(year.get()==" "):
        #     messagebox.showerror("Invalid Input", "Please enter valid input in all the fields.", parent=newWindow)
        # else:
        messagebox.showinfo("Added", "Book Added to the library.", parent=newWindow)
        library = MyLibrary()
        library.add_to_library(book)


    addBookBtn = Button(newWindow, command=add, width=20, bg=bgConfirmButton, font=fontBig, bd=5, padx=50, pady=5, text="Add To Library")
    addBookBtn.pack(pady=30)


# Sort alphabetically in record
def sortBookWindow():
    newWindow = openNewWindow("Sorted Books", btnSortWindow)
    # display sorted books in treeview
    library = MyLibrary()
    book_dict = library.sorted_books()
    rows = book_dict.values()
    openTreeView(newWindow, bookList=rows)

# see all books record
def seeAllBooksWindow():
    newWindow = openNewWindow("All Books", btnSeeBooksWindow)
    library = MyLibrary()
    rows = library.get_library()
    openTreeView(newWindow, bookList=rows)

# search A book in record
def SearchWindow():
    newWindow = openNewWindow("Search a book", btnSearchWindow)
    searchFrame = Frame(newWindow, bd=5)
    Label(searchFrame, text="Enter the book title to search in library", font=fontBig).pack(pady=10)
    enterWord = Entry(searchFrame, font=fontBig)
    enterWord.pack(pady=10)

    def search_title():
        search_word = str(enterWord.get()).lower()
        library = MyLibrary()
        # returns a book list or returns none if not found
        book = library.search_book_title(search_word)
        if book is not None:
            title["text"] = "Book Title: " + book[0]
            author["text"] = "Book Author: " + book[1]
            subject["text"] = "Subject: " + book[2]
            year["text"] = "Publication Year: " + book[3]
            availability["text"] = "Availability: " + book[4]
        else:
            messagebox.showinfo("Not Found", "No book is found by this title in the library", parent=newWindow)

    searchButton = Button(searchFrame, command=search_title, bg=bgConfirmButton, bd=5, font=fontBig, pady=3, text="Search")
    searchButton.pack(pady=10)
    searchFrame.pack()

    resultFrame = Frame(newWindow)
    resultFrame.pack()

    title = Label(resultFrame, font=fontBig)
    title.pack(pady=10)
    author = Label(resultFrame, font=fontBig)
    author.pack(pady=10)
    subject = Label(resultFrame, font=fontBig)
    subject.pack(pady=10)
    year = Label(resultFrame, font=fontBig)
    year.pack(pady=10)
    availability = Label(resultFrame, font=fontBig)
    availability.pack(pady=10)

def bookReserveWindow():
    newWindow = openNewWindow("Reserve a book", btnReserveBookWindow)
    treeFrame = Frame(newWindow)
    library = MyLibrary()
    rows = library.get_library()
    tree = openTreeView(treeFrame, bookList=rows)
    treeFrame.pack()
    btnFrame = Frame(newWindow)

    def remove():
        list_of_rows = []
        # Get selected item to remove
        selected_item = tree.selection()[0]
        tree.delete(selected_item)
        row_id = tree.get_children()
        for id in row_id:
            row = list(tree.item(id, 'values'))
            if row:
                list_of_rows.append(row)
        print(list_of_rows)
        library.update_library(list_of_rows)

    def reserve():
        list_of_rows = []
        selected = tree.focus()
        temp = tree.item(selected, 'values')
        tree.item(selected, values=(temp[0], temp[1], temp[2], temp[3], "reserved"))
        row_id = tree.get_children()
        for id in row_id:
            row = list(tree.item(id, 'values'))
            if row:
                list_of_rows.append(row)
        print(list_of_rows)
        library.update_library(list_of_rows)

    lab = Label(btnFrame, font=fontBig, bd=5, fg="blue", padx=50, pady=5, text="Select a row above and perform your desired option")
    lab.pack(pady=20)

    reserveBtn= Button(btnFrame, command=reserve, width=20, bg=bgConfirmButton, font=fontBig, bd=5, padx=50, pady=5, text="Reserve book")
    reserveBtn.pack(pady=30)
    removeBtn = Button(btnFrame, command=remove, width=20, bg=bgConfirmButton, font=fontBig, bd=5, padx=50, pady=5, text="Remove book")
    removeBtn.pack(pady=30)
    btnFrame.pack()


# main code runs from here
root = Tk()
root.title("CS_20003 Library Management System")
root.geometry("1300x1000")
root.maxsize(width=1300, height=1000)
root.minsize(width=1300, height=1000)
bgConfirmButton = "#009688"
theme = "#616161"
fontBig = ("Times", "20")
fontsmall = ("Times", "18")
root.configure(background="#616161")
Label(root, text="Choose from the options below", bg="#FFFFFF", padx=5, pady=5, width=40, font=fontBig).pack(pady=50)

# Main screen buttons
# add a book
btnAddWindow = Button(root, command=addBookWindow, text="Add new books", bg="#009688", padx=5, pady=15, width=40, font=fontBig)
btnAddWindow.pack(pady=12)
# sorting alphabetically
btnSortWindow = Button(root, command=sortBookWindow, text="Sorted Books in alphabetical order", bg="#FF4081", padx=5, pady=15, width=40, font=fontBig)
btnSortWindow.pack(pady=12)
# see the collection of books
btnSeeBooksWindow = Button(root, command=seeAllBooksWindow, text="See all Books", bg="#673AB7", padx=5, pady=15, width=40, font=fontBig)
btnSeeBooksWindow.pack(pady=12)
# search a book by title
btnSearchWindow = Button(root, command=SearchWindow, text="Search a book by it's title", bg="#FFEB3B", padx=5, pady=15, width=40, font=fontBig)
btnSearchWindow.pack(pady=12)
# Book Reserve Book
btnReserveBookWindow = Button(root, command=bookReserveWindow, text="Remove or Reserve a book", bg="#E1BEE7", padx=5, pady=15, width=40, font=fontBig)
btnReserveBookWindow.pack(pady=12)

root.mainloop()

