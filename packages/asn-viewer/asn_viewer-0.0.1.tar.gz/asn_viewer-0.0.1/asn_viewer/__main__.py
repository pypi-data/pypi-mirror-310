from pathlib import Path

from .asn_decoder import ASNDecoder
from .asn_viewer_config import ASNViewerConfig, ASNViewerCmdArguments

if __name__ == '__main__':
    try:
        args = ASNViewerCmdArguments().parse_args()

        conf = ASNViewerConfig(Path(args.config)) if args.config else None

        decoder = ASNDecoder(args.definition or conf.definition, args.object_name or conf.object_name)
        decoder.load_files(args.files or conf.files or tuple())

        if args.output or conf:
            decoder.save_decoded_to_file(Path(args.output or conf.output), args.search or conf.search or None)
        else:
            decoder.print_file_data_json(args.search or conf.search or None)

    except AttributeError as e:
        print(f'Missing parameter: {e.name.replace("_", "-")}')
        exit(1)
    except KeyError as ke:
        print(f'Field name {ke} is not in the ASN object definition')
        exit(2)
