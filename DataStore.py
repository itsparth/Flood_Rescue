import pickle

class DataStore:
    @staticmethod
    def save(obj, name='data'):
        with open('data/' + name + '.pkl', 'wb+') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(name='data'):
        try:
            with open('data/' + name + '.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}
    
    @staticmethod
    def save_backup(obj, name='data'):
        with open('data/' + name + '_backup.pkl', 'wb+') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    
    @staticmethod
    def load_backup(name='data'):
        try:
            with open('data/' + name + '_backup.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}