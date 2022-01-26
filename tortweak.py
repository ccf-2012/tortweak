import torclient
import os, shutil
import re
import sys
import argparse
import logging

parser = argparse.ArgumentParser(
    description='Hardlink tweaks of file/folder to get more crossed.')
parser.add_argument('-s',
                    '--host',
                    type=str,
                    required=True,
                    help='host of transmission')
parser.add_argument('-p',
                    '--port',
                    type=str,
                    required=True,
                    help='port of transmission')
parser.add_argument('-u',
                    '--username',
                    type=str,
                    required=True,
                    help='username of transmission')
parser.add_argument('-w',
                    '--password',
                    type=str,
                    required=True,
                    help='password of transmission')
parser.add_argument('-d',
                    '--docker_dir',
                    type=str,
                    required=True,
                    help='root dir in docker')
parser.add_argument('-r',
                    '--real_dir',
                    type=str,
                    required=True,
                    help='real dir path')
ARGS = parser.parse_args()

# ARGS.real_dir = os.path.expanduser(ARGS.input_path)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))
# formatter = logging.Formatter(
#     '\n%(asctime)s - Module: %(module)s - Line: %(lineno)d - Message: %(message)s'
# )

# file_handler = logging.FileHandler('file_dup.log', encoding='utf8')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


def ensureDir(file_path):
    if os.path.isfile(file_path):
        file_path = os.path.dirname(file_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def hdlinkCopy(fromLoc, toDir):
    destDir = toDir
    ensureDir(destDir)
    if os.path.isfile(fromLoc):
        destFile = os.path.join(destDir, os.path.basename(fromLoc))
        if not os.path.exists(destFile):
            # print('ln ', fromLoc, destFile)
            os.link(fromLoc, destFile)
        else:
            print('\033[36mExisted: %s =>  %s \033[0m' % (fromLoc, destFile))
    else:
        destDir = os.path.join(destDir, os.path.basename(fromLoc))
        if not os.path.exists(destDir):
            # print('copytree ', fromLoc, destDir)
            shutil.copytree(fromLoc, destDir, copy_function=os.link)
        else:
            print('\033[36mExisted: %s =>  %s \033[0m' % (fromLoc, destDir))


def dockerDirToReal(dlclient, path):
    if path.startswith(dlclient.scsetting.map_docker_dir):
        return path.replace(dlclient.scsetting.map_docker_dir,
                            dlclient.scsetting.map_real_dir, 1)
    else:
        return path


def tweakTask(dlclient):
    torList = dlclient.loadTorrents()
    for tor in torList:
        if tor.status not in ['stopped']:
            continue

        filename, fileext = os.path.splitext(tor.name)
        # logger.info('Torrent: ' + tor.name)
        origin_path = os.path.join(dockerDirToReal(dlclient, tor.save_path),
                                   tor.name)
        if os.path.exists(origin_path):
            logger.info('Exists: ' + origin_path)
            continue

        # CultFilms™
        if tor.name.find('™') > 0:
            if os.path.exists(
                    os.path.join(dockerDirToReal(dlclient, tor.save_path),
                                 tor.name.replace('™', ''))):
                hdlinkCopy(
                    os.path.join(dockerDirToReal(dlclient, tor.save_path),
                                 tor.name.replace('™', '')), origin_path)
                logger.info('Hardlink to : ' + origin_path)
                continue

        if tor.name.endswith('CultFilms'):
            if os.path.exists(
                    os.path.join(dockerDirToReal(dlclient, tor.save_path),
                                 tor.name.replace('CultFilms', 'CultFilms™'))):
                hdlinkCopy(
                    os.path.join(dockerDirToReal(dlclient, tor.save_path),
                                 tor.name.replace('CultFilms', 'CultFilms™')), origin_path)
                logger.info('Hardlink to : ' + origin_path)
                continue


        # `FraMeSToR.mkv` 和 `FraMeSToR/`
        if (fileext == '.mkv'):
            indir_path = os.path.join(dockerDirToReal(dlclient, tor.save_path),
                                      filename)
            if os.path.exists(indir_path) and os.path.exists(
                    os.path.join(indir_path, tor.name)):
                logger.info('Re-location to: ' +
                            os.path.join(tor.save_path, filename))
                dlclient.setLocation(tor.torrent_hash,
                                     os.path.join(tor.save_path, filename))
                continue
        # `FraMeSToR/`  and `FraMeSToR.mkv`
        if os.path.exists(
                os.path.join(dockerDirToReal(dlclient, tor.save_path),
                             tor.name + '.mkv')):
            hdlinkCopy(
                os.path.join(dockerDirToReal(dlclient, tor.save_path),
                             tor.name + '.mkv'), origin_path)
            logger.info('Hardlink to : ' + origin_path)
            continue


class ClientSetting:
    def __init__(self, clienttype, host, port, username, password,
                 map_docker_dir, map_real_dir):
        self.clienttype = clienttype
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.map_docker_dir = map_docker_dir
        self.map_real_dir = map_real_dir


def main():
    client = ClientSetting('tr', ARGS.host, ARGS.port, ARGS.username,
                           ARGS.password, ARGS.docker_dir, ARGS.real_dir)
    dlclient = torclient.getDownloadClient(client)
    if dlclient:
        logger.info('Connecting: ' + dlclient.scsetting.host)
        c = dlclient.connect()
        if c:
            tweakTask(dlclient)
        else:
            logger.info('Connect failed: ' + dlclient.scsetting.host)
    else:
        logger.info('Connect failed: ' + dlclient.scsetting.host)


if __name__ == '__main__':
    main()
