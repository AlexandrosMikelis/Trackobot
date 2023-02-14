
class Constants(object):
    
    def __init__(self):
    
        self._APP_CONF = {
            "constants" : {
                "video_width" : 500,
                "video_height" : 500
            }
        }
        
        self._BARCODE_NAMES = {
            "5200309851012" : "Bepanthol",
            "4005800171468" : "Hansaplast",
            "7622210982537" : "Dentyne"
        }
        
    @property
    def app_conf(self):
        return self._APP_CONF

    @property
    def barcode_names(self):
        return self._BARCODE_NAMES
    
    