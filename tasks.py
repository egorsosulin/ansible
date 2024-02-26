#!/usr/bin/env python3

from invoke import task, Collection
from socket import gethostname
from datetime import datetime
from rich import print


# Functions ===================================================================

def ansible_lint(c):
    'Run ansible linter'
    c.run('ansible-lint --force-color --offline playbook_*.yml')


def ansible_play(c, playbook):
    'Run ansible playbook'
    env = 'ANSIBLE_FORCE_COLOR=True'
    args = '--vault-password-file {}'
    file = 'playbook_' + playbook + '.yml'

    if playbook == gethostname():
        args += ' -e ansible_connection=local'

    cmd = f'sops exec-file .vault_password.sops "{env} ansible-playbook {args} {file}"'
    c.run(cmd)


# Vault Tasks =================================================================

@task(name='encrypt-string')
def vault_encrypt_string(c, string):
    env = 'ANSIBLE_FORCE_COLOR=True'
    args = '--vault-password-file {}'

    cmd = f'sops exec-file .vault_password.sops "{env} ansible-vault encrypt_string {args} \'{string}\'"'
    c.run(cmd)
    


# Lint Tasks ==================================================================

@task(name='playbooks')
def lint_playbooks(c):
    ansible_lint(c)


# Playbook Tasks ==============================================================

@task(name='e15')
def play_e15(c):
    ansible_play(c, 'e15')

@task(name='vps-ru-1')
def play_vps_ru_1(c):
    ansible_play(c, 'vps-ru-1')

@task(name='vps-eu-1')
def play_vps_eu_1(c):
    ansible_play(c, 'vps-eu-1')


# Namespaces ==================================================================

vault = Collection('vault', vault_encrypt_string)
lint = Collection('lint', lint_playbooks)
play = Collection('play', play_e15, 
                          play_vps_ru_1,
                          play_vps_eu_1)
ns = Collection(vault, lint, play)


# Configuration ===============================================================

ns.configure(
    {
        "run": {
            "echo": True,
        }
    }
)
