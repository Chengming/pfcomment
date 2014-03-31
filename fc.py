from optparse import OptionParser
import os
import CommentDB

class InvalidFileException(Exception):
    """
    """
    pass
        
        


class CFile(object):
    """
    """
    File = 0
    Folder = 1
    
    def __init__(self, filename):
        """
        """
        if os.path.exists(filename)==False:
            raise InvalidFileException
        if os.path.isfile(filename):
            self._type = CFile.File
        else:
            self._type = CFile.Folder
        # the abslute path name 
        self.abspath = os.path.abspath(filename)
        # the basename
        self.basename = os.path.basename(self.abspath)
        # the abslute path name of parient folder
        self.dirname = os.path.dirname(self.abspath)
                    
    def isFolder(self, ):
        return self._type==CFile.Folder

    def isFile(self,):
        return self._type==CFile.File

        
# import sys, tempfile, os
# from subprocess import call
# def getNewComment(filename):
#     EDITOR = os.environ.get('EDITOR','vim') #that easy!
#     initial_message = "\n\n#Comments for file "+filename # if you want to set up the file somehow
#     with tempfile.NamedTemporaryFile(suffix=".tmp") as tempfile:
#         tempfile.write(initial_message)
#         tempfile.flush()
#         call([EDITOR, tempfile.name])
#         ret = ""
#         with open(tempfile.name) as fd:
#             for line in fd.readlines():
#                 ret = ret+line
#     return ret

import sys, tempfile, os
from subprocess import call

def editCommentMessage(filename):
    """
    Open the editor to edit the comment of a file
    """
    EDITOR = os.environ.get('EDITOR','vim') #that easy!
    
    initial_message = "\n\n# Comment for file "+filename # if you want to set up the file somehow
    ret = ""
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tmpfile:
        tmpfile.write(initial_message)
        tmpfile.flush()
        call([EDITOR, tmpfile.name])
        isEmpty = True
        with open(tmpfile.name) as fd:
            for line in fd.readlines():
                tmp = line.lstrip()
                if len(tmp) is not 0 and tmp[0] is not "#":
                        ret = ret+line
                        isEmpty = False
                # if len(tmp) is 0 or tmp[0] is not "#":
                #     ret = ret+line
    if isEmpty is True:
        return ""
    else:
        return ret

from tabulate import tabulate

class CommentPrinter:
    def __init__(self, ):
        self._comment = []
        self._header = ["File Name","Comment","Added Time"]
    def addComment(self, filename, commentInfo):
        """
        commentInfo: [u'sdfsdfsdfsdfsdf today\n\n', datetime.datetime(2014, 3, 31, 13, 38, 24)]
        """
        flag = True
        for comment in commentInfo[0].split("\n"):
#        if len(commentInfo) is not 0 :
            if flag :
                self._comment.append([filename,comment,str(commentInfo[1])])
                flag = False
            elif comment!="":
                self._comment.append(["",comment,""])

    def addCommentList(self, filename, commentInfoList):
        if commentInfoList is not []:
            for commentInfo in commentInfoList:
                self._comment.append([filename,commentInfo[0],str(commentInfo[1])])

    def printTable(self,):
        print tabulate(self._comment,headers=self._header,tablefmt="orgtbl")

    
import argparse

# TODO: The comment of a folder should be in the .FileComment.json file of the patrent folder
# TODO: Should check if the folder is / , since / will not have a parient folder

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='*')
    parser.add_argument("-f", "--full", help="Show all comments of a file, will only show the latest by default",
                        action="store_true")
    parser.add_argument("-a", "--add", help="Add new comments to file",
                        action="store_true")
    parser.add_argument("-m", "--message", nargs=1, help="Working with -a, specify the comment message")
    args = parser.parse_args()

    if args.add : # add new comments to file
        if len(args.filename)==0:
            args.filename.append("./")
        for filename in args.filename:
            if args.message is not None:
                commentMessage = args.message[0]
            else:
                commentMessage = editCommentMessage(filename) # get the comment of a file
            if commentMessage is "":
                continue
            commentFile = CFile(filename)
            commentDB = CommentDB.CommentDB(commentFile.dirname)
            commentDB.addComment(commentFile.basename,commentMessage)
            print "Comment message saved for file "+filename
    else: # show comments of files
        commentPrinter = CommentPrinter()
        for filename in args.filename:
            commentFile = CFile(filename)
            commentDB = CommentDB.CommentDB(commentFile.dirname)
            if args.full: # show all comments
                comments = commentDB.getAllComment(commentFile.basename)
                commentPrinter.addCommentList(filename,comments)
            else:
                comment = commentDB.getLatestComment(commentFile.basename)
                commentPrinter.addComment(filename,comment)
        commentPrinter.printTable()
        
    
    
    # parser = OptionParser(usage="Usage: %prog [options] [file name] [comment message]", version="%prog v1.0")
    # parser.add_option("-f", "--full", action="store_true", dest="showFullHistory", default=False, help="Display all comments history")

    # (options, args) = parser.parse_args()
    # try:
    #     if len(args)==1:
    #         commentFile = CFile(args[0])
    #         commentDB = CommentDB.CommentDB(commentFile.dirname)
    #         print "show comment of file "+ args[0]
    #         if options.showFullHistory:
    #             print "showing full history"
    #             print commentDB.getAllComment(commentFile.basename)
    #         else:
    #             print "showing latest comment"
    #             print commentDB.getLatestComment(commentFile.basename)
    #     elif len(args)==2:
    #         commentFile = CFile(args[0])
    #         commentDB = CommentDB.CommentDB(commentFile.dirname)
    #         print "add comment: \""+args[1]+"\" on file "+args[0]
    #         commentDB.addComment(commentFile.basename,args[1])
    #     else:
    #         print "error"
    #         print args
    # except InvalidFileException:
    #     print "File does not exist"

            

