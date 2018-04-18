from shutil import copyfile

import codecs


class FileProcessor(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def file_read(self, codeType, spliteCode):
        with codecs.open(self.file_path, 'r', codeType) as f:
            result = [file_item.strip(spliteCode) for file_item in f.readlines()]

        return result

    def file_writeLines(self, codeType, arrayContents):
        with codecs.open(self.file_path, 'w', codeType) as f:
            f.writelines(arrayContents)

        return self.file_path

    def file_write(self, codeType, content):
        with codecs.open(self.file_path, 'w', codeType) as f:
            f.writelines(content)

        return self.file_path

    def file_read_iterator(self, codeType, spliteCode):
        with codecs.open(self.file_path, 'r', codeType) as f:
            result = (file_item.strip(spliteCode) for file_item in f.readlines())

        return result

    def file_copy(self, dist_path):
        copyfile(self.file_path, dist_path)


# class DirProcessor(object):
#     def __init__(self, dir_path):
#         self.dir_path = dir_path
#
#     def dir_read_iterator(self, fileReader, **kwargs):
#         files = os.listdir(self.dir_path)
#         files_list = []
#         for file in files:
#             file_path = os.path.join(self.dir_path, file)
#             file_data = fileReader(file_path, **kwargs)
#             files_list.append((file, file_data))
#
#         return dict(files_list)

