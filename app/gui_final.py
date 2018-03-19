import Tkinter as tk
import ScrolledText as tkst
from collections import defaultdict
import math

def tf(dict, word, docid):
    # term freq per document
    # format : {"term" : { docid: count, docid: count ... } }
    # uses unigram dict
    tf = dict[word][docid]
    return 1.0 + math.log(tf, 10)


def idf(dict, word):
    # uses term_count dict
    try:
        return math.log(37498 / float(1 + dict[word]), 10)
    except Exception as e:
        print ("Error while computing idf: " + e.message)
        return 0


def tf_idf(uniD, termD, word, docid, skew):
    if skew == 1:
        return .005 * idf(termD, word)
    return tf(uniD, word, docid) * idf(termD, word)


class GUI:

    def __init__(self, term_count_dict, unigram_dict, url_dict, stopwords_set):
        # initialize variables
        self.term_count_dict = term_count_dict
        self.unigram_dict = unigram_dict
        self.url_dict = url_dict
        self.stopwords_set = stopwords_set

        # ~~~ Creating the container for the GUI
        win = tk.Tk()
        win.title("J&J Search Engine")
        win.iconbitmap("view.ico")

        # ~~~ Search Frame for Button and Input Box
        topFrame = tk.Frame(master=win, bg='#8A0707')
        topFrame.pack(fill='both', expand='yes', side=tk.TOP)
        # ~~~ Output Frame
        outFrame = tk.Frame(master=win, bg='#8A0707')
        outFrame.pack(fill='both', expand='yes')

        # ~~~ Add Label, Input Box, and Search Button to topFrame
        myLabel = tk.Label(topFrame, text="QUERY:")
        self.myEntry = tk.Entry(topFrame, width=50)  # 20 characters wide, can type more than that
        myButton = tk.Button(topFrame, text='Search', command=self.perform_search)
        # ~~~ Every Frame has a built in grid(), thus we are placing them into columns 0, 1 and 2
        myLabel.grid(row=0, column=0)
        self.myEntry.grid(row=0, column=1)
        self.myEntry.bind('<Return>', lambda _: self.perform_search())
        myButton.grid(row=0, column=2)

        # ~~~ Add Scrollable Text Area to outFrame, fills and expands as frame size changes
        self.editArea = tkst.ScrolledText(outFrame, wrap=tk.WORD, width=140, height=40)
        # ~~~ pack() automagically places and sets up the object, otherwise have to use grid()
        #    These functions are mutually exclusive and do not behave well together.
        self.editArea.pack(padx=4, pady=4, fill=tk.BOTH, expand=True)
        win.mainloop()

    def perform_search(self):
        data = self.myEntry.get()
        if not data.strip():
            return
        print("Search Terms: %s\n" % (self.get_input()))
        query = [word for word in sorted(self.get_input()) if word not in self.stopwords_set]
        q_len = len(query)
        self.myEntry.delete(0, tk.END)
        self.editArea.insert(tk.INSERT, "\n")
        self.editArea.insert(tk.INSERT, "Searching for {}\n".format(query))

        # query search
        self.multi_word_query(query, q_len)

        self.editArea.see(tk.END)

    def get_input(self):
        data = self.myEntry.get().strip()
        return data.split(" ")


    def multi_word_query(self, query, q_len):
        try:
            if (q_len >= 1):
                terms = defaultdict(float)
                matching_docid = defaultdict(int)
                for i in range(q_len):
                    term = query[i]
                    for docid in self.unigram_dict[term]:
                        matching_docid[docid] += 1
                for i in range(q_len):
                    term = query[i]
                    for docid, val in matching_docid.iteritems():
                        if val == q_len:
                            if ("facebook" in self.url_dict[docid].lower()):
                                terms[docid] += tf_idf(self.unigram_dict, self.term_count_dict, term, docid, 1)
                            else:
                                terms[docid] += tf_idf(self.unigram_dict, self.term_count_dict, term, docid, 0)
                for docid in sorted(terms, key=terms.get, reverse=True)[:10]:
                    self.editArea.insert(tk.INSERT, "URL: {} | tfidf: {}\n".format(self.url_dict[docid], terms[docid]))
        except KeyError as e:
            print "Word not found in collection..."
