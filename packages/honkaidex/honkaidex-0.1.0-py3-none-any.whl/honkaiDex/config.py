from honkaiDex.__config__ import _gconfig, _cconfig, has_gconfig

class gconfig(_gconfig):
    STIGAMATA = "stigamata_1"

class config(_cconfig):
    class data(_cconfig):
        class stigamata_1(_cconfig):
            FILENAME = "stigamata_1.json"

    class profile(_cconfig):
        class cached(_cconfig):
            STIGAMATA = gconfig

        class just_stigamata(_cconfig):
            STIGAMATA = gconfig

    
            