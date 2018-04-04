from conans import ConanFile, tools
import os


class MsinttypesConan(ConanFile):
    name = "msinttypes"
    version = "r26"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Msinttypes here>"
    no_copy_source = True
    # No settings/options are necessary, this is header only

    def source(self):
        '''retrieval of the source code here. Remember you can also put the code in the folder and
        use exports instead of retrieving it with this source() method
        '''
        tools.download("https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/msinttypes/msinttypes-%s.zip" % (self.version), "file.zip")
        tools.unzip("file.zip" )
        tools.replace_in_file("inttypes.h",'#include "stdint.h"','')

    def package(self):
        self.copy("inttypes.h", "include")
