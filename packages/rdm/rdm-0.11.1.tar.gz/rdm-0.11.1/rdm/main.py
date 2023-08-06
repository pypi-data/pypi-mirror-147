import argparse
import sys
import traceback

import yaml

from rdm.gaps import audit_for_gaps, list_default_checklists
from rdm.collect import collect_from_files
from rdm.hooks import install_hooks
from rdm.init import init
from rdm.pull import pull_from_project_manager
from rdm.render import render_template_to_file
from rdm.translate import translate_test_results, XML_FORMATS
from rdm.util import context_from_data_files, print_error, load_yaml
from rdm.version import __version__


def main():
    try:
        exit_code = cli(sys.argv[1:])
        sys.exit(exit_code)
    except Exception:
        print_error(traceback.format_exc())
        sys.exit(1)


def cli(raw_arguments):
    exit_code = 0
    args = parse_arguments(raw_arguments)
    if args.command is None:
        parse_arguments(['-h'])
    elif args.command == 'render':
        context = context_from_data_files(args.data_files)
        config = load_yaml(args.config)
        render_template_to_file(config, args.template, context, sys.stdout)
    elif args.command == 'init':
        init(args.output)
    elif args.command == 'pull':
        pull_from_project_manager(args.config)
    elif args.command == 'hooks':
        install_hooks(args.dest)
    elif args.command == 'collect':
        snippets = collect_from_files(args.files)
        yaml.dump(snippets, sys.stdout, default_style='|')
    elif args.command == 'translate':
        translate_test_results(args.format, args.input, args.output)
    elif args.command == 'gap' and args.list:
        list_default_checklists()
    elif args.command == 'gap':
        exit_code = audit_for_gaps(args.checklist, args.files)
    return exit_code


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(prog='rdm')
    parser.add_argument('--version', action='version', version=__version__)
    subparsers = parser.add_subparsers(dest='command', metavar='<command>')

    init_help = 'copy the default templates etc. into the output directory'
    init_parser = subparsers.add_parser('init', help=init_help)
    init_output_help = 'Path where templates are copied'
    init_parser.add_argument('-o', '--output', default='dhf', help=init_output_help)

    render_help = 'render a template using the specified data files'
    render_parser = subparsers.add_parser('render', help=render_help)
    render_parser.add_argument('template')
    render_parser.add_argument('config', help='Path to project `config.yml` file')
    render_parser.add_argument('data_files', nargs='*')

    pull_help = 'pull data from the project management tool'
    pull_parser = subparsers.add_parser('pull', help=pull_help)
    pull_parser.add_argument('config', help='Path to project `config.yml` file')

    gap_help = 'use checklist to verify documents have expected references to particular standard(s)'
    gap_parser = subparsers.add_parser('gap', help=gap_help)
    gap_parser.add_argument('-l', '--list', action='store_true', help='List built-in checklists')
    gap_parser.add_argument('checklist', nargs='?')
    gap_parser.add_argument('files', nargs='*')

    hooks_help = 'install githooks in current repository'
    hooks_parser = subparsers.add_parser('hooks', help=hooks_help)
    hooks_parser.add_argument('dest', nargs='?', help='Path where hooks are saved')

    collect_help = 'collect documentation snippets into a yaml file'
    collect_parser = subparsers.add_parser('collect', help=collect_help)
    collect_parser.add_argument('files', nargs='*')

    translate_help = 'translate test output to create test result yaml file'
    translate_parser = subparsers.add_parser('translate', help=translate_help)
    translate_parser.add_argument('format', choices=XML_FORMATS)
    translate_parser.add_argument('input')
    translate_parser.add_argument('output')

    return parser.parse_args(arguments)


if __name__ == '__main__':
    main()
