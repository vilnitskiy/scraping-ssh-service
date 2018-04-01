import datetime

import paramiko


class SSHController(object):
    def __init__(self, host, user, key):
        self.local = '/var/lib/jenkins/workspace/{project}/{folder}/{name}.csv'
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connection.connect(host, username=user, key_filename=key)

    def execute(self, args):
        # transport = self.connection.get_transport()
        # channel = transport.open_session()
        cmd = 'scrapy crawl %s ' % args.spider[0]
        if args.url:
            cmd += '-a start_urls=%s ' % args.url
        if args.file:
            cmd += '-o %s.csv -t csv ' % args.file
        if args.nohup:
            cmd = 'nohup ' + cmd + '&\n'
        commands = [
            'source {}/bin/activate'.format(args.venv),
            'cd {}'.format(args.path),
            'rm {}.csv'.format(args.file),
            cmd
        ]
        try:
            self.connection.invoke_shell()
            stdin, stdout, stderr = self.connection.exec_command('\n'.join(commands))
            print(stdout.read())
        except IOError as e:
            print(e)
            return False
        return True

    def get_result(self, args):
        sftp = self.connection.open_sftp()
        try:
            remote = '{path}/{file}.csv'.format(path=args.path, file=args.file) if args.file else '~/results/res.csv'
            sftp.get(remote, self.local.format(
                project=args.project,
                folder=args.spider[0],
                name=str(datetime.date.today())
            ))
            self.connection.close()
        except IOError:
            return False
        return True
