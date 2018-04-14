import codecs

class FileProcessor(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def file_read(self, codeType, spliteCode):
        with codecs.open(self.file_path, 'r', codeType) as f:
            result = [file_item.strip(spliteCode) for file_item in f.readlines()]

        return result

    def file_write(self, codeType, arrayContents):
        with codecs.open(self.file_path, 'w', codeType) as f:
            f.writelines(arrayContents)

        return self.file_path

    def file_read_iterator(self, codeType, spliteCode):
        with codecs.open(self.file_path, 'r', codeType) as f:
            result = (file_item.strip(spliteCode) for file_item in f.readlines())

        return result


