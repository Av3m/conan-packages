import os, sys
from distutils.spawn import find_executable
from conans import ConanFile, CMake
from conans.tools import download, unzip, vcvars_command, os_info, SystemPackageTool

class QtConan(ConanFile):
    name = "Qt"
    version = "4.8.7"
    ZIP_FOLDER_NAME = "qt-everywhere-opensource-src-%s" % (version)
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "opengl": ["desktop", "dynamic"]}
    default_options = "shared=True", "opengl=desktop"
    url="http://github.com/av3m/conan-qt"
    license="LGPLv3"
    exports_sources="qt.conf","test_package"

    def requirements(self):
        if self.settings.os == "Windows":
            self.requires("icu/[>57.0]@*/*")

    def source(self):
        major = ".".join(self.version.split(".")[:2])
        url = "http://download.qt.io/official_releases/qt/{major}/{v}/qt-everywhere-opensource-src-{v}".format(major=major, v=self.version)
        if self.settings.os == "Windows":
            zip_name = "qt.zip"
            url += ".zip"
        else:
            zip_name = "qt.tar.gz"
            url += ".tar.gz"

        download(url, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)
            
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)

    @property
    def _thread_count(self):
        concurrency = 1
        try:
            import multiprocessing
            concurrency = multiprocessing.cpu_count()
        except (ImportError, NotImplementedError):
            pass
        return concurrency

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        args = ["-opensource", "-confirm-license", "-nomake examples", "-nomake tests", "-prefix _dist"]
        if not self.options.shared:
            args.insert(0, "-static")
        if self.settings.build_type == "Debug":
            args.append("-debug")
        else:
            args.append("-release")

        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                self._build_msvc(args)
            else:
                self._build_mingw(args)
        else:
            self._build_unix(args)

    def _build_msvc(self, args):
        build_command = find_executable("jom.exe")
        if build_command:
            build_args = ["-j", str(self._thread_count)]
        else:
            build_command = "nmake.exe"
            build_args = []
        self.output.info("Using '%s %s' to build" % (build_command, " ".join(build_args)))

        vcvars = vcvars_command(self.settings)
        set_env = 'SET PATH={dir}/qtbase/bin;{dir}/gnuwin32/bin;%PATH%'.format(dir=self.conanfile_directory)
        args += ["-opengl %s" % self.options.opengl]
        # it seems not enough to set the vcvars for older versions, it works fine with MSVC2015 without -platform
        if self.settings.compiler == "Visual Studio":
            if self.settings.compiler.version == "12":
                args += ["-platform win32-msvc2013"]
            if self.settings.compiler.version == "11":
                args += ["-platform win32-msvc2012"]
            if self.settings.compiler.version == "10":
                args += ["-platform win32-msvc2010"]

        self.run("cd %s && %s && %s && configure %s" % (self.ZIP_FOLDER_NAME, set_env, vcvars, " ".join(args)))
        self.run("cd %s && %s && %s %s" % (self.ZIP_FOLDER_NAME, vcvars, build_command, " ".join(build_args)))
        self.run("cd %s && %s && %s install" % (self.ZIP_FOLDER_NAME, vcvars, build_command))

    def _build_mingw(self, args):
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        args += ["-developer-build", "-opengl %s" % self.options.opengl, "-platform win32-g++"]

        self.run("%s && cd %s && configure.bat %s" % (env.command_line_env, self.ZIP_FOLDER_NAME, " ".join(args)))
        self.run("%s && cd %s && mingw32-make -j %s" % (env.command_line_env, self.ZIP_FOLDER_NAME, str(self._thread_count)))
        self.run("%s && cd %s && mingw32-make install" % (env.command_line_env, self.ZIP_FOLDER_NAME))

    def _build_unix(self, args):
        if self.settings.os == "Linux":
            args += ["-silent", "-xcb"]
        else:
            args += ["-silent"]

        self.run("cd %s && ./configure %s" % (self.ZIP_FOLDER_NAME, " ".join(args)))
        self.run("cd %s && make -j %s" % (self.ZIP_FOLDER_NAME, str(self._thread_count)))
        self.run("cd %s && make install" % (self.ZIP_FOLDER_NAME))

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        src = "%s/bin/_dist" % (self.ZIP_FOLDER_NAME)
        if self.settings.os == "Windows":
            src = "%s/bin/_dist/_dist" % (self.ZIP_FOLDER_NAME)
        self.copy(pattern="*", src=src)
        self.copy("qt.conf",dst="bin",keep_paths=False)

    def package_info(self):
        libs = ['3Support',
                'Core','Declarative','Designer',
                'Gui','Help','Multimedia','Network','OpenGL','Script','ScriptTools','Sql',
                'Svg','Test','UiTools','WebKit','Xml','XmlPatterns']
        if self.settings.os != "Windows":
            libs += ['X11Extras', 'XcbQpa']

        self.cpp_info.libs = []
        self.cpp_info.includedirs = ["include"]
        for lib in libs:
            if self.settings.os == "Windows" and self.settings.build_type == "Debug":
                suffix = "4d"
            else:
                suffix = "4"
            self.cpp_info.libs += ["Qt%s%s" % (lib, suffix)]
            self.cpp_info.includedirs += ["include/Qt%s" % lib]

        if self.settings.os == "Windows":
            # Some missing shared libs inside QML and others, but for the test it works
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
