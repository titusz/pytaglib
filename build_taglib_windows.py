from pathlib import Path
import sys
import urllib.request
import tarfile
import shutil
import subprocess
from dataclasses import dataclass
from argparse import ArgumentParser
import hashlib


taglib_version = '1.12'
taglib_release = f'https://github.com/taglib/taglib/releases/download/v{taglib_version}/taglib-{taglib_version}.tar.gz'
taglib_sha256sum = '7fccd07669a523b07a15bd24c8da1bbb92206cb19e9366c3692af3d79253b703'
build_config = 'Release'

is_x64 = sys.maxsize > 2**32
arch = "x64" if is_x64 else "x32"

here = Path(__file__).resolve().parent


@dataclass
class Configuration:
    tl_install_dir: Path = here / 'build' / 'taglib-install'
    build_path: Path = here / 'build'
    clean: bool = True

    @property
    def tl_download_dest(self):
        return self.build_path / f'taglib-{taglib_version}.tar.gz'

    @property
    def tl_extract_dir(self):
        return self.build_path / f'taglib-{taglib_version}'


def download(config: Configuration):
    target = config.tl_download_dest
    if target.exists():
        print('skipping download, file exists')
    else:
        print(f'downloading taglib {taglib_version} ...')
        response = urllib.request.urlopen(taglib_release)
        data = response.read()
        target.parent.mkdir(exist_ok=True,parents=True)
        target.write_bytes(data)
    the_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    assert the_hash == taglib_sha256sum
 

def extract(config: Configuration):
    if config.tl_extract_dir.exists():
        print('extracted taglib found. Skipping tar')
    else:
        print('extracting tarball')
        tar = tarfile.open(config.tl_download_dest)
        tar.extractall(config.tl_extract_dir.parent)


def clean_cmake(config: Configuration):
    if not config.clean:
        return
    print('removing previous cmake cache ...')
    cache = config.tl_extract_dir / 'CMakeCache.txt'
    if cache.exists():
        cache.unlink()
        shutil.rmtree(config.tl_extract_dir / 'CMakeFiles', ignore_errors=True)
 

def call_cmake(config, *args):
    return subprocess.run(['cmake', *[a for a in args if a is not None]], cwd=config.tl_extract_dir, check=True)


def generate_vs_project(config: Configuration):
    print("generating VS projects with cmake ...")
    cmake_arch = 'x64' if is_x64 else "Win32"
    install_prefix = f'-DCMAKE_INSTALL_PREFIX={config.tl_install_dir}'
    config.tl_install_dir.mkdir(exist_ok=True, parents=True)
    call_cmake(config, '-A', cmake_arch, install_prefix, '.')


def build(config: Configuration):
    print("building ...")
    call_cmake(config, '--build', '.', '--config', build_config, '--clean-first' if config.clean else None)
    print("installing ...")
    call_cmake(config, '--install', '.', '--config', build_config)


def make_path(str_path: str) -> Path:
    path = Path(str_path)
    if not path.is_absolute():
        path = here / path
    return path


def parse_args() -> Configuration:
    parser = ArgumentParser()
    config = Configuration()
    parser.add_argument('--install-dest', help='destination directory for taglib', type=Path, default=config.tl_install_dir)
    args = parser.parse_args()
    config.tl_install_dir = make_path(args.install_dest)
    return config


def run():
    print(f"building taglib on {arch}...")
    config = parse_args()
    tag_lib = config.tl_install_dir / 'lib' / 'tag.lib'
    if tag_lib.exists():
        print('installed TagLib found, exiting')
        return
    download(config)
    extract(config)
    clean_cmake(config)
    generate_vs_project(config)
    build(config)
    

if __name__ == '__main__':
    run()
