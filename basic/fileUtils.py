class fileUtils:


    def __init__(self, filePath):
        pass


    @staticmethod
    def save(filename,content,encoding='utf-8'):
        with open(filename, mode="w", encoding=encoding) as f:
            f.write(content)
            f.close()


    @staticmethod
    def append(filename,content,encoding='utf-8'):
        with open(filename, mode="a", encoding=encoding) as f:
            f.write(content)
            f.close()

    @staticmethod
    def appendBr(filename,content,encoding='utf-8'):
        with open(filename, mode="a", encoding=encoding) as f:
            f.write(f"{content}\n")
            f.close()



    ## 二进制
    @staticmethod
    def saveBytes(filename,bytes):
        with open(filename, mode="wb") as f:
            f.write(bytes)
            f.close()