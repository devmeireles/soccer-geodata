import re
import unidecode

class TreatData():

    @staticmethod
    def slugify(text):
        text = unidecode.unidecode(text).lower()
        return re.sub(r'[\W_]+', '-', text)
