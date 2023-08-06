#! /usr/bin/env python3
import sys
import argparse
import logging
import json
from typing import List, Union
from importlib.metadata import version
from credmark.client.dto.dto_error_schema import extract_error_codes_and_descriptions
from credmark.client.dto.dto_schema import dto_schema_viz, print_example, print_tree

sys.path.append('.')
from . import CredmarkClient

logger = logging.getLogger(__name__)


def main():

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Credmark developer tool')
    parser.add_argument('--log_level', default=None, required=False,
                        help='Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL')
    parser.add_argument('--api_url', required=False, default=None,
                        help='Credmark API url. '
                        'Defaults to the standard API gateway. '
                        'You do not normally need to set this.')

    subparsers = parser.add_subparsers(title='Commands',
                                       description='Supported commands',
                                       help='additional help')

    parser_version = subparsers.add_parser(
        'version', help='Show version of the package', aliases=[])
    parser_version.set_defaults(func=show_version)

    parser_models = subparsers.add_parser(
        'models', help='List models deployed on server', aliases=['deployed-models'])
    parser_models.add_argument('--manifests', action='store_true', default=False,
                               help="Show full manifests")
    parser_models.add_argument('--json', action='store_true',
                               default=False, help="Output as json")
    parser_models.add_argument('model-slug', nargs='?', default=None, type=str,
                               help='[OPTIONAL] Slug for the model to show.')
    parser_models.set_defaults(func=list_models)

    parser_desc = subparsers.add_parser(
        'describe', help='Show documentation for models',
        aliases=['describe-models', 'man'])
    parser_desc.add_argument('model-slug', nargs='?', default=None, type=str,
                             help='Slug or partial slug to describe.')
    parser_desc.set_defaults(func=describe_models)

    parser_run = subparsers.add_parser('run', help='Run a model', aliases=['run-model'])
    parser_run.add_argument('-b', '--block_number', type=int, required=False, default=None,
                            help='Block number used for the context of the model run.'
                            ' If not specified, it is set to the latest block of the chain.')
    parser_run.add_argument('-c', '--chain_id', type=int, default=1, required=False,
                            help='Chain ID. Defaults to 1.')
    parser_run.add_argument('-i', '--input', required=False, default='{}',
                            help='Input JSON or '
                            'if value is "-" it will read input JSON from stdin.')
    parser_run.add_argument('-v', '--model_version', default=None, required=False,
                            help='Version of the model to run. Defaults to latest.')
    parser_run.add_argument('-j', '--format_json', action='store_true', default=False,
                            help='Format output json to be more readable')
    parser_run.add_argument('model-slug', default='(missing model-slug arg)',
                            help='Slug for the model to run.')
    parser_run.set_defaults(func=run_model)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(vars(args))


def config_logging(args, default_level='WARNING'):
    level = args['log_level']
    if not level:
        level = default_level
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=level)


def show_version(_args):
    ver = version('credmark-client')
    print(f'credmark-client version {ver}')
    sys.exit(0)


def describe_models(args):
    config_logging(args)
    client = CredmarkClient(url=args.get('api_url'))

    try:
        manifests = client.get_models()
    except Exception:
        # Error will have been logged but we continue
        # so things work offline
        manifests = []

    model_slug = args.get('model-slug')
    if model_slug is not None:
        manifests = [m for m in manifests if model_slug in m['slug']]

    print('')
    if len(manifests) > 0:
        print_manifests(manifests, True)
        exit_code = 0
    else:
        print_no_models_found(model_slug)
        exit_code = 1
    sys.exit(exit_code)


def print_no_models_found(model_slug):
    if model_slug:
        print(f'No models matching slug {model_slug}')
    else:
        print('No models found')


def list_models(args):  # pylint: disable=too-many-branches
    config_logging(args)
    json_output = args.get('json')
    model_slug = args.get('model-slug')
    show_manifests = args.get('manifests') or model_slug
    client = CredmarkClient(url=args.get('api_url'))

    if model_slug:
        model = client.get_model(model_slug)
        if model is not None:
            deployments = client.get_model_deployments(model_slug)
            if deployments:
                model['versions'] = {
                    dep["version"]: dep.get("location", "") for dep in deployments}
            manifests = [model]
        else:
            manifests = []
    else:
        manifests = client.get_models()

    if not json_output:
        if model_slug:
            sys.stdout.write('\n')
            if len(manifests) == 0:
                sys.stdout.write(f'Model slug {model_slug} not found on server.\n\n')
        else:
            sys.stdout.write('\nDeployed Models:\n\n')

        if show_manifests:
            print_manifests(manifests)
        else:
            for model in manifests:
                print(f'{model["slug"]} : {model.get("displayName", "")}')
            print('')
    else:
        json.dump(manifests, sys.stdout)


def print_manifests(manifests: List[dict], describe_schemas=False):
    for m in manifests:  # pylint: disable=too-many-nested-blocks
        for i, v in m.items():
            if i == 'slug':
                sys.stdout.write(f'{v}\n')
                sys.stdout.write(f' - {i}: {v}\n')
            else:
                if not describe_schemas:
                    sys.stdout.write(f' - {i}: {v}\n')
                else:
                    if i == 'input':
                        input_tree = dto_schema_viz(
                            v, v.get('title', 'Object'), v, 0, 'tree',
                            only_required=False, tag='top', limit=10)
                        input_examples = dto_schema_viz(
                            v, v.get('title', 'Object'), v, 0, 'example',
                            only_required=False, tag='top', limit=10)

                        print(' - input schema (* for required field):')
                        print_tree(input_tree, '   ', sys.stdout.write)

                        print(' - input example:')
                        print_example(input_examples, '   ', sys.stdout.write)

                    elif i == 'output':
                        output_tree = dto_schema_viz(
                            v, v.get('title', 'Object'), v, 0, 'tree',
                            only_required=False, tag='top', limit=1)
                        output_examples = dto_schema_viz(
                            v, v.get('title', 'Object'), v, 0, 'example',
                            only_required=True, tag='top', limit=1)

                        print(' - output schema (* for required field):')
                        print_tree(output_tree, '   ', sys.stdout.write)

                        print(' - output example:')
                        print_example(output_examples, '   ', sys.stdout.write)

                    elif i == 'error':
                        codes = extract_error_codes_and_descriptions(v)
                        print(' - errors:')
                        if len(codes) > 0:
                            for ct in codes:
                                print(f'   {ct[0]}')
                                print(f'     codes={ct[1]}')
                                print(f'     {ct[2]}')
                            title = v.get('title', 'Error')
                            output_tree = dto_schema_viz(
                                v, title, v, 0, 'tree', only_required=False, tag='top', limit=1)
                            output_examples = dto_schema_viz(
                                v, title, v, 0, 'example', only_required=False, tag='top', limit=1)
                            print(' - error schema:')
                            print_tree(output_tree, '   ', sys.stdout.write)
                        else:
                            print('   No defined errors')

                    else:
                        sys.stdout.write(f' - {i}: {v}\n')

        sys.stdout.write('\n')


def run_model(args):  # pylint: disable=too-many-statements,too-many-branches,too-many-locals
    exit_code = 0

    try:
        config_logging(args, 'INFO')

        chain_id: int = args['chain_id']
        block_number: Union[int, None, str] = args['block_number']
        model_slug: str = args['model-slug']
        model_version: Union[str, None] = args['model_version']
        format_json: bool = args['format_json']

        if args['input'] != '-':
            input = json.loads(args['input'])
        else:
            sys.stderr.write('Reading input JSON on stdin\n')
            input = json.load(sys.stdin)

        if block_number is None:
            block_number = 'latest'

        client = CredmarkClient(url=args.get('api_url'))

        result = client.run_model(
            slug=model_slug,
            chain_id=chain_id,
            block_number=block_number,
            version=model_version,
            input=input)

        if 'error' in result:
            etype = result.get('error', {}).get('type')
            if etype == 'ModelInputError':
                exit_code = 2
            elif etype == 'ModelNotFoundError':
                exit_code = 126
            elif etype == 'ModelDataError':
                exit_code = 3
            else:
                exit_code = 1

        if format_json:
            print(json.dumps(result, indent=4).replace('\\n', '\n').replace('\\"', '\''))
        else:
            json.dump(result, sys.stdout)

    except Exception as e:
        # this exception would only happen have been raised
        # within this file itself
        logger.exception('Run model error')
        msg = {
            "error": {
                "type": "ModelEngineError",
                "message": f'Error in credmark-dev: {str(e)}'
            }
        }
        json.dump(msg, sys.stdout)
        exit_code = 1
    finally:
        sys.stdout.write('\n')
        sys.stdout.flush()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
