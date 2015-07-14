from fabric.api import run, env, prompt, execute, sudo, put
from fabric.contrib.files import append
from fabric.contrib import files
import boto.ec2
import time


# these env variables are available throughout
env.hosts = ['localhost', ]
env.aws_region = 'us-west-2'
env.key_filename = '/home/meslater/.ssh/pk-aws.pem'
git_user = 'meslater1030'
projname = 'taste-buddies'
git_path = git_user + "/" + projname
appname = 'helloworld.py'


def host_type():
    run('uname -s')


def get_ec2_connection():
    # env checks the environment to see if this variable has been set up
    if 'ec2' not in env:
        conn = boto.ec2.connect_to_region(env.aws_region)
        if conn is not None:
            # this will set up the ec2 variable throughout
            env.ec2 = conn
            print "Connected to EC2 region %s" % env.aws_region
        else:
            msg = "Unable to connect to EC2 region %s"
            raise IOError(msg % env.aws_region)
    return env.ec2


def provision_instance(wait_for_running=False, timeout=60, interval=2):
    wait_val = int(interval)
    timeout_val = int(timeout)
    conn = get_ec2_connection()
    instance_type = 't1.micro'
    key_name = 'private key'
    security_group = 'ssh-access'
    image_id = 'ami-d0d8b8e0'

    reservations = conn.run_instances(
        image_id,
        key_name=key_name,
        instance_type=instance_type,
        security_groups=[security_group, ]
    )
    new_instances = [i for i in reservations.instances if
                     i.state == u'pending']
    running_instance = []
    if wait_for_running:
        waited = 0
        while new_instances and (waited < timeout_val):
            time.sleep(wait_val)
            waited += int(wait_val)
            for instance in new_instances:
                state = instance.state
                print "Instance %s is %s" % (instance.id, state)
                if state == "running":
                    running_instance.append(
                        new_instances.pop(new_instances.index(i))
                    )
                instance.update()


def list_aws_instances(verbose=False, state='all'):
    conn = get_ec2_connection()

    reservations = conn.get_all_reservations()
    instances = []
    for res in reservations:
        for instance in res.instances:
            if state == 'all' or instance.state == state:
                instance = {
                    'id': instance.id,
                    'type': instance.instance_type,
                    'image': instance.image_id,
                    'state': instance.state,
                    'instance': instance,
                }
                instances.append(instance)
    env.instances = instances
    if verbose:
        import pprint
        pprint.pprint(env.instances)


def select_instance(state='running'):
    if env.get('active_instance', False):
        return

    list_aws_instances(state=state)

    prompt_text = "Please select from the following instances:\n"
    instance_template = " %(ct)d: %(state)s instance %(id)s\n"
    for idx, instance in enumerate(env.instances):
        ct = idx + 1
        args = {'ct': ct}
        args.update(instance)
        prompt_text += instance_template % args
    prompt_text += "Choose an instance: "

    def validation(input):
        choice = int(input)
        if choice not in range(1, len(env.instances) + 1):
            raise ValueError("%d is not a valid instance" % choice)
        return choice

    choice = prompt(prompt_text, validate=validation)
    env.active_instance = env.instances[choice - 1]['instance']


def run_command_on_selected_server(command):
    select_instance()
    selected_hosts = [
        'ubuntu@' + env.active_instance.public_dns_name
    ]
    execute(command, hosts=selected_hosts)


def _setup_suite():
    sudo('apt-get update')
    if files.exists('/tmp/supervisor.sock'):
        sudo('unlink /tmp/supervisor.sock')
    if files.exists('/var/run/supervisor.sock'):
        sudo('unlink /var/run/supervisor.sock')
    sudo('apt-get install -y '
         'nginx git python-pip postgresql '
         'postgresql-contrib libpq-dev python-dev')
    if not files.exists(
        'etc/nginx/sites-available/original-default',
        use_sudo=True
    ):
        sudo(
            'cp /etc/nginx/sites-available/default '
            '/etc/nginx/sites-available/original-default'
        )

    put(local_path="~/projects/t-buddies/simple_nginx_conf",
        remote_path="/etc/nginx/sites-available/default",
        use_sudo=True)

    append('/etc/nginx/sites-available/default',
           "server {listen 80;server_name " +
           env.active_instance.public_dns_name + "/;"
           "access_log /var/log/nginx/test.log;location /"
           "{proxy_pass http://127.0.0.1:8080;proxy_set_header Host $host;"
           "proxy_set_header X-Real-IP $remote_addr;"
           "proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;"
           "}}")

    if not files.exists("~/.previous/"):
        run('mkdir ~/.previous')

    sudo('service nginx start')


def _deploy():
    sudo('service nginx stop')

    from datetime import datetime
    now = datetime.now()
    d = now.strftime("%Y_%m_%e__%H_%M_%S")

    if files.exists('~/{p}'.format(p=projname)):
        run('mv ~/{p} ~/.previous/{d}'.format(p=projname, d=d))

    run(
        'git clone -b master'
        ' http://github.com/{gp}'.format(gp=git_path,)
    )

    if files.exists('/{p}/supervisord.conf'.format(p=projname),
                    use_sudo=True,):
        sudo('rm -f /{p}/supervisord.conf'.format(p=projname))
    sudo('mv {p}/supervisord.conf /etc/supervisord.conf'.format(p=projname))

    sudo('pip install -r ~/{p}/requirements.txt'.format(p=projname))
    sudo('cd taste-buddies ; python setup.py develop')
    sudo('reboot')
    time.sleep(90)
    sudo('service nginx start')
    sudo('supervisord')


def deploy_app():
    run_command_on_selected_server(_setup_suite)
    run_command_on_selected_server(_deploy)


# def setup_suite():
#     run_command_on_selected_server(_setup_suite)


# def _install_nginx():
#     sudo('/etc/init.d/nginx start')


def _setup_ngnix():
    try:
        sudo('mv /etc/nginx/sites-available/default '
             '/etc/nginx/sites-available/default.orig')
    except:
        pass
    sudo('mv simple_nginx_conf /etc/nginx/sites-available/default')
    append('/etc/nginx/sites-available/default',
           "server {listen 80;server_name " +
           env.active_instance.public_dns_name + "/;"
           "access_log /var/log/nginx/test.log;location /"
           "{proxy_pass http://127.0.0.1:8080;proxy_set_header Host $host;"
           "proxy_set_header X-Real-IP $remote_addr;"
           "proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;"
           "}}")
    sudo('/etc/init.d/nginx restart')


def setup_ngnix():
    run_command_on_selected_server(_setup_ngnix)


# def install_nginx():
#     run_command_on_selected_server(_install_nginx)


def stop_instance():
    select_instance()
    instance = env.active_instance
    instance.stop()


def terminate_instance():
    select_instance(state='stopped')
    instance = env.active_instance
    instance.terminate()


# def _supervisord():
#     sudo('mv supervisord.conf /etc/supervisord.conf')
#     sudo('apt-get install supervisor')
#     sudo('supervisord')


# def supervisord():
#     run_command_on_selected_server(_supervisord)


# def upload_files(files, host, remotePath):
#     for file in files:
#         local('scp -i ~/.ssh/pk-aws.pem {} {}:{}'.format(file,
#                                                          host, remotePath))


# def deploy_app():
#     install_nginx()
#     host = 'ubuntu@' + env.active_instance.public_dns_name
#     remotePath = '/home/ubuntu'
#     files = ['helloworld.py',
#              'simple_nginx_conf', 'supervisord.conf']
#     upload_files(files, host, remotePath)
#     setup_ngnix()
#     supervisord()
