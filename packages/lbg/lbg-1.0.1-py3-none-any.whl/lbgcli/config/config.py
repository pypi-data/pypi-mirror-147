from getpass import getpass

import validators

from lbgcli.const import ConfigKey, GlobalConfig
from lbgcli.module_impl import Module
from lbgcli.module_impl import OutputFormat


class ConfigModule(Module):
    def __init__(self, cli):
        super().__init__(cli)

    def add_to_parser(self, subparser):
        self.parser = subparser.add_parser('config', help='Operating Config Module')
        self.parser.set_defaults(func=lambda _: self.parser.print_help())
        self.sub_parser = self.parser.add_subparsers()
        self.load_format()
        self.load_account()
        self.load_base_url()

    def load_format(self):
        parser_format = self.sub_parser.add_parser('format',
                                                   help=f'change default output format, current is {self.cli.output_format()}')
        parser_format.set_defaults(func=lambda args: self.func_format(args))
        parser_format.add_argument('format', action='store', type=str,
                                   help='current available format: json csv yaml table(default)')

    def func_format(self, args):
        if args.format not in OutputFormat.list():
            raise ValueError("unrecognized format, current allow json csv yaml and table")
        self.cli.put(ConfigKey.DEFAULT_OUTPUT_FORMAT, args.format)

    def load_account(self):
        parser_format = self.sub_parser.add_parser('account', help='change login account')
        parser_format.set_defaults(func=lambda args: self.func_account(args))

    def func_account(self, args):
        config = self.cli.get_account_info()
        email = ''
        while True:
            email = self._ask_for('email',
                                  default=config.get('email'),
                                  optional=(config.get('email') is not None))
            if not validators.email(email):
                self.cli.print(f'invalid email: {email}')
            else:
                break
        password = self._ask_for('password',
                                 default=config.get('password'),
                                 optional=(config.get('password') is not None),
                                 secret=True)
        self.cli.save_account_info(email, password)

    def _ask_for(self, query, default=None, optional=False, secret=False):
        while True:
            old_default = default
            if secret and default:
                if len(default) >= 4:
                    default = '*' * (len(default) - 4) + default[-4:]
                else:
                    default = '*' * len(default)
            if optional:
                question = f"{query} current: [{default}]: "
            else:
                question = f"{query}: "
            result = None
            if secret:
                result = getpass(prompt=question)
            else:
                result = input(question)
            if not result and not optional:
                self.cli.print("This is required")
                continue
            if result:
                return result
            if optional:
                return old_default

    def load_base_url(self):
        parser_format = self.sub_parser.add_parser('baseurl', help='change baseurl of lebesgue')
        parser_format.set_defaults(func=lambda args: self.func_base_url(args))
        parser_format.add_argument('url', action='store', type=str, nargs='?',
                                   help=f"lebesgue url (type '{GlobalConfig.CALLER_NAME} config baseurl reset' to default), "
                                        f'default: {GlobalConfig.LEBESGUE_ADDRESS} '
                                        f'current: {self.cli.get(ConfigKey.LEBESGUE_ADDRESS, GlobalConfig.LEBESGUE_ADDRESS)}')

    def func_base_url(self, args):
        if args.url:
            select = args.url
            if select == 'reset':
                select = GlobalConfig.LEBESGUE_ADDRESS
                self.cli.put(ConfigKey.LEBESGUE_ADDRESS, GlobalConfig.LEBESGUE_ADDRESS)
                self.cli.print(f'current lebesgue address is {select}')
                return
            if not validators.url(select):
                self.cli.print(f'invalid url: {select}')
                return
            self.cli.put(ConfigKey.LEBESGUE_ADDRESS, select)
            self.cli.print(f'current lebesgue address is {select}')
        else:
            select = self.cli.get(ConfigKey.LEBESGUE_ADDRESS, GlobalConfig.LEBESGUE_ADDRESS)
            self.cli.print(f'current lebesgue address is {select}')
