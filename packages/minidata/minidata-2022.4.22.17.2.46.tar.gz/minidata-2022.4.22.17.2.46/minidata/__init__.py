"""Top-level package for minidata."""
from meutils.pipe import *

__author__ = """minidata"""
__email__ = 'yuanjie@xiaomi.com'
__version__ = time.strftime("%Y.%m.%d.%H.%M.%S", time.localtime())

DATA_HOME = Path(get_module_path('data', __file__))
MODEL_HOME = Path(get_module_path('model', __file__))


class Data(object):

    def __init__(self, path='同花顺相似问'):

        self.df = pd.DataFrame()

        if Path(path).is_file():
            pass

        elif Path(path + '.pkl').is_file():
            self.df = joblib.load(path + '.pkl')


if __name__ == '__main__':
    from transformers import AutoModel, AutoTokenizer, AutoConfig, AdamW

    PRE_TRAINED_MODEL_NAME = 'ckiplab/albert-tiny-chinese'

    tokenizer = AutoTokenizer.from_pretrained(MODEL_HOME / PRE_TRAINED_MODEL_NAME)

    print(tokenizer)
