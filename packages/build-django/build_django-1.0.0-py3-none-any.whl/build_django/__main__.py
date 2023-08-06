import os
import asyncio
import secrets
import argparse
import subprocess

ENV_EXAMPLE = '''
SECRET_KEY=

# List of comma separated values
ALLOWED_HOSTS=

# Remove if production
DEBUG=
'''

REQUIRED_PACKAGES = (
    'wheel',
    'django',
    'django-environ',
    'gunicorn'
)

parser = argparse.ArgumentParser(description='Build Django project')

parser.add_argument('name', metavar='name', help='Django project name')

parser.add_argument('--dir', dest='dir', type=str, default='./', required=False, help='Django project directory')

parser.add_argument('--debug', dest='debug', action='store_true', required=False, help='Should create env with DEBUG=True')

parser.add_argument('--hosts', dest='hosts', required=False, default='', help='List of comma separated ALLOWED_HOSTS values')

parser.add_argument('--python', dest='python', required=False, default='python3', help='Python command')

parser.add_argument('--migrate', dest='migrate', required=False, action='store_true', help='Apply default migrations after creation')

parser.add_argument('--git', dest='git', required=False, action='store_true', help='Initialize git repo')

parser.add_argument('--commit', dest='commit', required=False, action='store_true', help='Make initial git commit')

parser.add_argument('--commit-message', dest='commit_message', required=False, default='Initial commit', help='Initial commit name')

parser.add_argument('--packages', dest='packages', nargs='+', help='Additional pip packages', required=False, default=[])

def generate_env(debug=False, hosts='*'):
    items = [
        f'SECRET_KEY={secrets.token_hex(128)}',
        f'ALLOWED_HOSTS={hosts}'
    ]

    if debug:
        items.append('DEBUG=True')

    return '\n\n'.join(items)

async def write_file(path, content, mode='w'):
    with open(path, mode) as file:
        file.write(content)


async def run_cmd(args, **kwargs):
    result = subprocess.run(args, encoding='utf-8', capture_output=True, **kwargs)

    if result.returncode != 0:
        raise subprocess.SubprocessError(result.stderr)

    print(result.stdout)

    return result

async def exec():
    args = parser.parse_args()

    project_dir = args.dir

    print('Checking project directory...')

    if not os.path.exists(project_dir):
        print('Project directory not found, creating project directory')

        os.mkdir(project_dir)
    else:
        print('Project directory found')

    name = args.name 

    print('Creating Django project...')

    await run_cmd(('django-admin', 'startproject', name, project_dir))

    print('Django project created')

    venv_dir = os.path.join(project_dir, 'venv/')

    print('Creating files...')

    tasks = [
        write_file(
            os.path.join(project_dir, '.gitignore'),
            '/venv\n/static\n/media\n__pycache__\n*.sqlite*\n*.log\n.env'
        ),
        write_file(
            os.path.join(project_dir, '.env'),
            generate_env(args.debug, args.hosts)
        ),
        write_file(
            os.path.join(project_dir, 'env.example'),
            ENV_EXAMPLE
        ),
        run_cmd([args.python, '-m', 'venv', venv_dir])
    ]

    if args.git:
       tasks.append(run_cmd(('git', 'init', project_dir))) 

    await asyncio.gather(*tasks)

    bin_path = os.path.join(venv_dir, 'bin')

    pip_path = os.path.join(bin_path, 'pip') 

    print('Installing required packages...')

    packages = (*REQUIRED_PACKAGES, *args.packages)

    tasks = (
        run_cmd(
            (pip_path, 'install', pkg)
        ) for pkg in packages
    )

    await asyncio.gather(*tasks)

    print('Installed required packages')

    print('Getting requirements...')

    requirements = (await run_cmd((pip_path, 'freeze'))).stdout

    print('Writing requirements...')

    with open(os.path.join(project_dir, 'requirements.txt'), 'w') as file:
        file.write(requirements)

    print('Added requirements')


    print('Editing settings file...')

    with open(os.path.join(project_dir, args.name, 'settings.py'), 'r+') as file:
        lines = file.readlines() 

        result = []

        for line in lines:
            if line.startswith('BASE_DIR'):
                result.append('\nfrom environ import Env\n')

                result.append(f'\n{line}\n')

                result.append('\nenv = Env(DEBUG=(bool, False))\n')
                
                result.append('\nEnv.read_env(BASE_DIR / \'.env\')\n')

            elif line.startswith('SECRET_KEY'):
                result.append(f'SECRET_KEY = env(\'SECRET_KEY\')\n')
            elif line.startswith('ALLOWED_HOSTS'):
                result.append('ALLOWED_HOSTS = env.tuple(\'ALLOWED_HOSTS\')')
            elif line.startswith('DEBUG'):
                result.append('DEBUG = env(\'DEBUG\')\n')
            else:
                result.append(line)

        file.seek(0)

        file.writelines(result)

    print('Edited settings file')

    if args.git and args.commit:
        await run_cmd(('git', 'add', '.'))

        await run_cmd(('git', 'commit', '-m', f'"{args.commit_message}"'))


    if args.migrate:
        python_path = os.path.join(bin_path, 'python')

        manage_path = os.path.join(project_dir, 'manage.py')

        await run_cmd((python_path, manage_path, 'migrate', '--no-input'))
    
def main():
    asyncio.run(exec())

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
