from .filling import Filling
from ...ingredients import Resize


class ResizeFilling(Filling):
    type_name = 'resize'
    type = Resize

    @classmethod
    def add_parser_arguments(cls, parser):
        """
        add palette and palette size to this parser
        add rscolorq params to the parser and parent
        """

        # add palette and palette size
        parser.add_argument(
            '--width',
            type=int,
            help='width to resize to'
        )
        parser.add_argument(
            '--height',
            type=int,
            help='height to resize to'
        )
        parser.add_argument(
            '-s', '--scale',
            type=float, default=1,
            help='scale multiplier of size (can be used with width and height or alone)'
        )
        parser.add_argument(
            '--resample-filter',
            dest='resample',
            default=Resize.FILTERS['default'],
            choices=Resize.FILTERS.keys(),
            help='resample filter for resize'
        )
