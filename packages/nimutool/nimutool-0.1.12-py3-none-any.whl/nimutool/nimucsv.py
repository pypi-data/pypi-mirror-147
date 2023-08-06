import argparse
import nimutool.parser
import nimutool.canbus
import nimutool.data
import can


class NimuCSVDefaultArguments:

    file_format: str = 'n/a'
    input_file: str = 'n/a'
    output: str = 'ni_data.csv'
    file_parser: str = 'nimu'
    can_adapter: str = 'pcan'
    can_channel: str = 'PCAN_USBBUS1'
    can_bitrate: int = 1000000
    traffic_study_period: float = 1.5
    downsample: int = 1
    console_output: bool = False


class NimuCSV:

    def __init__(self, arguments: NimuCSVDefaultArguments = None):
        args = arguments if arguments else self.parse_arguments()
        self.run(args)

    def run(self, args):
        if args.file_format:
            bus = nimutool.canbus.READERS[args.file_format](args.input_file)
        else:
            bus = nimutool.canbus.CanBusReader(can.interface.Bus(bustype=args.can_adapter, channel=args.can_channel, bitrate=args.can_bitrate))
        processor = nimutool.parser.PARSERS[args.file_parser]()
        csv = nimutool.data.CsvWriter(args.output, args.downsample)
        console = nimutool.data.ConsoleWriter()
        outputs = [csv, console] if args.console_output else [csv]
        show_progress = len(outputs) == 1
        block_processor = nimutool.canbus.BusBlockReader(input=bus,
                                                         processor=processor,
                                                         outputs=outputs,
                                                         traffic_study_period=args.traffic_study_period,
                                                         show_progress=show_progress)
        block_processor.process()
        print(f'{args.output} written')

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Tool for reading nimu data from CAN bus')
        parser.add_argument('--file-format', choices=nimutool.canbus.READERS.keys(), type=str, help='Parse raw can message CSV file')
        parser.add_argument('--input-file', type=str, help='Parse can messages from input file, determine parser with --file-parser argument')
        parser.add_argument('--output', help='Output file name', default='ni_data.csv')
        parser.add_argument('--file-parser', default='nimu', choices=nimutool.parser.PARSERS.keys(),
                            help='What kind of messages are parsed amongst all CAN messages')
        parser.add_argument('--can-adapter', default='pcan', help='Can adapter to use, see options from python-can documentation')
        parser.add_argument('--can-channel', default='PCAN_USBBUS1', help='Can adapter channel to use, see options from python-can documentation')
        parser.add_argument('--can-bitrate', default=1000000, help='Can bus bitrate')
        parser.add_argument('--traffic-study-period', type=float, default=1.5, help='How long to study CAN bus traffic before starting logging')
        parser.add_argument('--downsample', type=int, default=1, help='Skip n measurements when logging to file, useful for trend analysis')
        parser.add_argument('--console-output', action='store_true', help='Show messages in console in addition to saving them to file')
        return parser.parse_args()


if __name__ == '__main__':
    NimuCSV()
