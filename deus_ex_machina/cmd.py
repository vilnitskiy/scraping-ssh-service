import argparse

from .control import SSHController


def ssh():
    parser = argparse.ArgumentParser(prog='deus', description='Wrapper for executing ssh commands')

    parser.add_argument('-H', '--host', action='store', dest='host', default='localhost')
    parser.add_argument('-U', '--user', action='store', dest='user', default='root')
    parser.add_argument('-K', '--key', action='store', dest='key', default='~/.ssh/id_rsa.pub')

    action = parser.add_subparsers(dest='action')

    run = action.add_parser('run')
    run.add_argument('-n', '--nohup', action='store', dest='nohup', help='nohup')
    run.add_argument('-u', '--url', action='store', dest='url', help='Start url')
    run.add_argument('-f', '--file', action='store', dest='file', help='Export feed to file')
    run.add_argument('-p', '--project', action='store', dest='project', help='Jenkins project name')
    run.add_argument('-v', '--virtualenv', action='store', dest='venv', help='Path to venv')
    run.add_argument('path', action='store', default='~', help='Scrapy project destination')
    run.add_argument('spider', action='append', help='Spider name')

    args = parser.parse_args()

    connection = SSHController(args.host, args.user, args.key)
    connection.execute(args)
    connection.get_result(args)
