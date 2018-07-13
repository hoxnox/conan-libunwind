from nxtools import NxConanFile
from conans import AutoToolsBuildEnvironment, tools

class GperfToolsConan(NxConanFile):
    name = "libunwind"
    description = "Implementation of the libunwind API."
    version = "1.2"
    options = {"shared":[True, False]}
    default_options = "shared=False"
    url = "https://www.nongnu.org/libunwind/download.html"
    license = "MIT"

    def do_source(self):
        self.retrieve("1de38ffbdc88bd694d10081865871cd2bfbb02ad8ef9e1606aee18d65532b992",
            [
                'vendor://nongnu/libunwind/libunwind-{version}.tar.gz'.format(version=self.version),
                'http://download.savannah.nongnu.org/releases/libunwind/libunwind-{version}.tar.gz'.format(version=self.version)
            ], "libunwind-{v}.tar.gz".format(v = self.version))

    def do_build(self):
        build_dir = "{staging_dir}/src".format(staging_dir=self.staging_dir)
        tools.untargz("libunwind-{v}.tar.gz".format(v=self.version), build_dir)
        env_build = AutoToolsBuildEnvironment(self)
        
        with tools.environment_append(env_build.vars):
            self.run("cd {build_dir}/libunwind-{v} && ./configure --prefix=\"{staging}\" --disable-minidebuginfo --disable-documentation {shared}".format(
                         v = self.version,
                         build_dir=build_dir,
                         staging=self.staging_dir,
                         shared="--enable-shared --disable-static" if self.options.shared else "--enable-static --disable-shared"))
            self.run("cd {build_dir}/libunwind-{v} && make install".format(v = self.version, build_dir = build_dir))

    def do_package_info(self):
        self.cpp_info.libs = ["unwind"]


