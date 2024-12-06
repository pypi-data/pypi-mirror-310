import pysubs2
import argparse
import json
import glob
import os
from .utils.lambda_fetch import get_data

cyenv = os.getenv("CYENV", 'true').lower() in ('true', '1') #os.getenv('CYENV')

if cyenv:
    from c_delocalizer.modify_subs import overwrite_subs as modify_subs_py
else:
    from .md_subs import modify_subs_py
from subdeloc_tools.modules.merger import Merger

class Delocalizer:
    """
    Main delocalizer class
    """
    def __init__(self):
        self.LANGUAGES = ["eng", "spa"]
        self.ERRORS = []
        self.index = 0
        self.language = "eng"
        self.keep_subs = False
        self.nomux = False
        self.wordsfile = None
        self.file = None
        self.subfile = None
        self.merger = Merger()

    def modify_subs(self, f):
        """
        Modify the file by changing the words specified in the Words file.
        """
        try:
            name = modify_subs_py(str(f), str(self.wordsfile))
            if name:
                return name
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def shift_subs(self, delta):
        """
        Shift all subs a determined amount of time. To be depredecated.
        """
        try:
            subs1 = pysubs2.load(self.file, encoding="utf-8")
            subs1.shift(s=delta)
            msub = "m_" + self.file
            subs1.save(msub)

            return msub
        except Exception as e:
            print(e)
            return False

    def prepare_data(self, args):
        """
        Initialize data from the args.
        """
        try:
            if args.words:
                lambda_url = os.getenv("JSONLAMBDA", False)
                if lambda_url:
                    words = get_data(lambda_url)
                    self.wordsfile = words
                else:
                    raise Exception("No Lambda url in environment")
            else:
                if args.jfile:
                    self.wordsfile = args.jfile
                else:
                    raise Exception("No JSON file indicated")
            if args.language:
                if args.language in LANGUAGES:
                    self.language = args.language
            if args.index and args.index > 0:
                self.index = args.index
            if args.keep_subs:
                self.keep_subs = True
            if args.nomux:
                self.nomux = True

            return True
        except Exception as e:
            print(e)
            return False

    def print_errors(self):
        """
        Print error array.
        """
        try:
            if len(ERRORS) > 0:
                print("There were errors:")
                for i in ERRORS:
                    print("-", i)
            else:
                print("No errors")
        except Exception as e:
            print(e)

    def get_index(self):
        """
        Get index of the subtitle track for the requested language. 
        Default: eng.
        """
        try:
            streams = self.merger.get_streams()
            index = self.merger.get_language_index(self.language, selected_index=self.index)

            return index
        except Exception as e:
            print(e)
            return -1

    def clean_files(self, file, f):
        """
        Remove intermediate delocalized subtitle file.
        """
        try:
            if not self.keep_subs:
                os.remove(file)
            else:
                newfilename = "."+os.sep+"Subs"+os.sep+f.split(".")[0] + '.' + file.split(".")[1]
                os.rename(file, newfilename)

            return True
        except Exception as e:
            print(e)
            return False

    def delocalize(self, f):
        """
        Delocalize a single file.
        """
        try:
            index = -1
            print("Extracting: ", f)
            # Initial tasks
            self.file = f
            self.merger.set_file(f)
            index = self.get_index()

            if index > -1:
                print("Subtitles found at", index)
                if self.merger.codec_name == "ass":
                    outputf = "subfile.ass"
                elif self.merger.codec_name == "subrip":
                    outputf = "subfile.srt"
                else:
                    raise Exception("Subtitle codec not recognized")
                    
                self.subfile = self.merger.demux(self.file, index, outputf)
                if self.subfile:
                    print("Delocalizing...")
                    unloc_sub = self.modify_subs(self.subfile)
                    # For reference
                    # word_json = self.get_replace_file(self.subfile)
                    # unloc_sub = self.replace_words(word_json)

                    if unloc_sub:
                        # Remove sub file and Mux unlocalized
                        os.remove(self.subfile)
                        if self.nomux:
                            self.clean_files(unloc_sub, f)
                        else:
                            print("Muxxing with file:", unloc_sub)
                            r = self.merger.mux(f, unloc_sub, "./Finished")
                            if r:
                                #Clean
                                self.clean_files(unloc_sub, f)
                            else:
                                print("Failed to mux sub!")
                                self.ERRORS.append(str(self.file))
                    else:
                        print("Failed to modify subs!")
                        self.ERRORS.append(str(self.file))
                else:
                    print("Failed to extract Subtitle!")
                    self.ERRORS.append(str(self.file))
            else:
                print("Subtitles not found!")
                self.ERRORS.append(str(self.file))
            return True
        except Exception as e:
            print(e)
            return False

    def delocalize_all(self):
        """
        Delocalize all MKV files in current folder.
        """
        try:
            files = glob.glob('*.mkv')
            for f in files:
                status = self.delocalize(f)
            return True
        except Exception as e:
            print(e)
            return False