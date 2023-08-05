import argparse
import os.path
import sys

from opencmiss.importer import ragpdata
from opencmiss.importer import colonhrm


def available_importers():
    return [
        ragpdata.identifier(),
        colonhrm.identifier(),
    ]


def import_data(importer, inputs, working_directory):
    outputs = None
    if importer == ragpdata.identifier():
        outputs = ragpdata.import_data(inputs, working_directory)
    elif importer == colonhrm.identifier():
        outputs = colonhrm.import_data(inputs, working_directory)

    return outputs


def import_parameters(importer):
    parameters = {}
    if importer == ragpdata.identifier():
        parameters = ragpdata.parameters()
    elif importer == colonhrm.identifier():
        parameters = colonhrm.parameters()

    return parameters


def main():
    parser = argparse.ArgumentParser(description='Import data into OpenCMISS-Zinc.')
    parser.add_argument("-o", "--output", default=os.curdir, help='output directory, default is the current directory.')
    parser.add_argument("-l", "--list", help="list available importers", action='store_true')
    subparsers = parser.add_subparsers(dest="importer", help="types of importer")

    ragp_parser = subparsers.add_parser(ragpdata.identifier())
    ragp_parser.add_argument("mbf_xml_file", nargs=1, help="MBF XML marker file.")
    ragp_parser.add_argument("csv_file", nargs=1, help="CSV file of gene, marker name, value matrix.")

    hrm_parser = subparsers.add_parser(colonhrm.identifier())
    hrm_parser.add_argument("colon_hrm_file", help="Colon HRM tab separated values file.")

    args = parser.parse_args()

    if args.list:
        print("Available importers:")
        for id_ in available_importers():
            print(f" - {id_}")
    else:
        if args.output and not os.path.isdir(args.output):
            sys.exit(1)

        inputs = []
        if args.importer == ragpdata.identifier():
            inputs.extend(args.mbf_xml_file)
            inputs.extend(args.csv_file)
        elif args.importer == colonhrm.identifier():
            inputs.extend(args.colon_hrm_file)

        import_data(args.importer, inputs, args.output)


if __name__ == "__main__":
    main()
