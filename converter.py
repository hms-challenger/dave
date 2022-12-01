import os

#convert to mp3
class mp3_converter():
    def __init__(self, path, ext, dirName):
        self.path = path
        self.ext = ext
        self.dirName = dirName
  
    def lower_underscore(self):
        directory = self.path
        [os.rename(os.path.join(directory, f), os.path.join(directory, f).replace(' ', '§').lower()) for f in os.listdir(directory)]

    def mp3(self):
        directory = self.path
        for f in os.listdir(directory):
            if (f.endswith(self.ext)):
                os.system("ffmpeg -i {} -ar 44100 -ac 2 -b:a 192k {}/{}.mp3".format(os.path.join((directory), f), (directory), os.path.splitext(f)[0]))

    def wav16(self):
        directory = self.path
        for f in os.listdir(directory):
            if (f.endswith(self.ext)):
                os.system("ffmpeg -i {} -ab 16000 -ar 44100 -ac 2 -b:a 192k {}/{}.wav".format(os.path.join((directory), f), (directory + "/wav"), os.path.splitext(f)[0]))