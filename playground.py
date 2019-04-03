import bashlint
from bashlint import data_tools, bast, nast
from bashlint.lint import safe_bashlex_parse
import os
import logging
import typing as T
import json

logger = logging.getLogger('playground')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def dump_nast(ast: nast.Node) -> dict:
    if ast is None:
        return None
    ret = {
        'kind': ast.kind,
    }
    children = []
    if len(ast.children) > 0:
        children = [dump_nast(child) for child in ast.children]

    ret['value'] = ast.value
    ret['children'] = children
    return ret



def parse_all():
    global cmd
    paths = os.path.join(os.path.abspath(os.pardir), "bash", "all.cm")
    logger.info("Reading from " + paths)
    with open(paths, "r") as f:
        cmds = f.readlines()
    for cmd in cmds:
        data_tools.bash_parser(cmd, verbose=True)


def print_nast(cmd):
    ast = bashlint.data_tools.bash_parser(cmd)
    print(json.dumps(dump_nast(ast), indent=2))

def print_bast(cmd):
    print(bashlint.parse(cmd)[0].dump())


def print_tokens(cmd):
    ast = bashlint.data_tools.bash_parser(cmd)
    tokens = data_tools.ast2tokens(ast)
    print(" ".join(tokens))


if __name__ == '__main__':

    cmd = "chmod -R 755 $d"
    print_bast(cmd)
    print_nast(cmd)
    print_tokens(cmd)

    cmd = 'while read d; do chmod -R 755 "$d"; done'
    print_bast(cmd)
    print_nast(cmd)
    print_tokens(cmd)

    cmd = "for D in `find . -iname \"*.php~\"`; do mv ${D} /mydir; done"
    ast = bashlint.parse(cmd)[0]
    print(ast.dump())
    print_nast(cmd)
    print_tokens(cmd)

    cmd = "echo a"


    # input("Wait...")
    ast = bashlint.data_tools.bash_parser(cmd)
    print(json.dumps(dump_nast(ast), indent=2))
    # parse_all()

    print_nast('`find . -iname "*.php~"`')
    print_bast('`find . -iname "*.php~"`')





