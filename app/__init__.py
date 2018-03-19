from Milestone1 import *
from gui_final import *

##############################################################################
# Author  : Jerry Granillo & John Shipley
# Modified: 03/11/18
# Summary : To process files and run the program from scratch
#           uncomment the line in main that says "Uncomment if
#           you want to process files" The processed inverted index
#           is already provided. unigramdict.json contains the inverted
#           index. Make sure both files totaltermcount.json & unigramdict.json
#           are in the same directory.
#
#           If running WINDOWS you must change Milestone1.py -> Parser -> construct()
#           Comment out under OSX and uncomment under Windows. Else run the program.
#
#           To process the WEBPAGES_RAW you must specify the path to the directory.
#           At the top of start_program change "dirpath=" to your path where
#           WEBPAGES_RAW is located.
#
#           If you want to use the GUI without processing, ensure that the two
#           files are in your directory. Comment out the start_program call in
#           main. Ensure that the load_inverted_index method is not commented.
#           Run __init__.py and the GUI will start.
##############################################################################


def load_inverted_index():
    # load json files
    print ("Loading json files...")
    starttime = time.time()
    with open("totaltermcount.json", "r") as termcountfile:
        term_count_dict = json.load(termcountfile)

    with open("unigramdict.json", "r") as unifile:
        unigram_dict = json.load(unifile)

    # with open("InvertedIndexTrigrams.json", "r") as trifile:
    #     trigram_dict = json.load(trifile)
    print ("Done loading. Time: {}".format(time.time() - starttime))

    return term_count_dict, unigram_dict


def start_program():
    print "Creating index... START!"
    totaltime = time.time()
    start = RunProgram()

    dirpath = r'PATH'
    start.walking(dirpath)
    print ("Total time to complete program : {}".format(time.time() - totaltime))

    starttime = time.time()
    print "Dumping term count dictionary into json..."
    with open("totaltermcount.json", "w+") as tfile:
        json.dump(start.term_count_dict, tfile)
    print "DONE. Dumped term count dictionary into json file"

    print "Dumping unigram inverted index into json..."
    with open("unigramdict.json", "w+") as ufile:
        json.dump(start.unigram_dict, ufile)
    print "DONE. Dumped unigram inverted index into json file"

    # print "Dumping bigram inverted index into json..."
    # with open("bigramdict.json", "a+") as bfile:
    #     json.dump(start.bigram_dict, bfile)
    # print "DONE. Dumped bigram inverted index into json file"

    # print "Dumping the trigram inverted index into json..."
    # with open("InvertedIndexTrigrams.json", "a+") as outfile:
    #     json.dump(start.inverted_index, outfile)
    # print "DONE. Dumped trigram inverted index."
    print ("Time to dump into json: {}".format(time.time() - starttime))

    # print ("Computing trigram index size...")
    # t = time.time()
    # index_size = start.size_of_index()
    # print ("Time to compute index size: {}".format(time.time() - t))
    # print ("Index Size: {}".format(index_size))
    print ("Document count: {}".format(start.document_count))

    return start.term_count_dict, start.unigram_dict


if __name__ == "__main__":
    try:
        # Uncomment if you want to process files
        # term_count_dict, unigram_dict = start_program()

        # load json files
        term_count_dict, unigram_dict = load_inverted_index()

        # Instantiate Dicts
        url_dict = json_dict()
        stopwords_set = set(stopwords.words('english'))

        # Start GUI
        print "Initializing GUI..."
        gui = GUI(term_count_dict, unigram_dict, url_dict, stopwords_set)


        print ("Program complete. Successfully created inverted index.")
        print ("Exiting. Goodbye...")
    except Exception as e:
        print "Program failed: " + e.message
