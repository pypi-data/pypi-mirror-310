import argparse
import json
import os
import textwrap
import multiprocessing as mp

from modernmetric.cls.importer.pick import importer_pick
from modernmetric.cls.modules import get_additional_parser_args
from modernmetric.cls.modules import get_modules_calculated
from modernmetric.cls.modules import get_modules_metrics
from modernmetric.cls.modules import get_modules_stats
from modernmetric.fp import file_process
from modernmetric.license import report


def ArgParser(custom_args=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        prog="modernmetric",
        description='Calculate code metrics in various languages',
        epilog=textwrap.dedent("""
        Currently you could import files of the following types for --warn_* or --coverage  # noqa: E501

        Following information can be read

            <file> = full path to file
            <content> = either a string
            <severity> = optional severity

            Note: you could also add a single line, then <content>
                has to be a number reflecting to total number of findings

        File formats

        csv: CSV file of following line format
             <file>,<content>,<severity>

        json: JSON file
             <file>: {
                 "content": <content>,
                 "severity": <severity>
             }
        """))
    parser.add_argument(
        "--output_file",
        default=None,
        help="File to write the output to")
    parser.add_argument(
        "--warn_compiler",
        default=None,
        help="File(s) holding information about compiler warnings")
    parser.add_argument(
        "--warn_duplication",
        default=None,
        help="File(s) holding information about code duplications")
    parser.add_argument(
        "--warn_functional",
        default=None,
        help="File(s) holding information about static code analysis findings")
    parser.add_argument(
        "--warn_standard",
        default=None,
        help="File(s) holding information about language standard violations")
    parser.add_argument(
        "--warn_security",
        default=None,
        help="File(s) File(s) holding information about found security issue")
    parser.add_argument(
        "--coverage",
        default=None,
        help="File(s) with compiler warningsFile(s) holding information about testing coverage")  # noqa: E501
    parser.add_argument(
        "--dump",
        default=False,
        action="store_true",
        help="Just dump the token tree")
    parser.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="Run x jobs in parallel")
    parser.add_argument(
        "--ignore_lexer_errors",
        default=True,
        help="Ignore unparseable files")
    get_additional_parser_args(parser)

    parser.add_argument('--file', type=str, help='Path to the JSON file list of file paths')  # noqa: E501
    parser.add_argument('files', metavar='file', type=str, nargs='*', help='List of file paths')  # noqa: E501

    if custom_args:
        RUNARGS = parser.parse_args(custom_args)
    else:
        RUNARGS = parser.parse_args()

    file_paths = RUNARGS.files
    input_file = RUNARGS.file

    if not file_paths and not input_file:  # No file passed in, read filelist from command line  # noqa: E501
        raise Exception("No filelist provided. Provide path to file list with --file=<path>")  # noqa: E501
    if input_file:
        with open(input_file) as file:
            data = json.load(file)
            for file in data:
                RUNARGS.files.append(file["path"])

    # Turn all paths to abs-paths right here
    RUNARGS.oldfiles = {}
    for x in RUNARGS.files:
        RUNARGS.oldfiles[os.path.abspath(x)] = x
    RUNARGS.files = [os.path.abspath(x) for x in RUNARGS.files]
    return RUNARGS

# custom_args is an optional list of strings args,
# e.g. ["--file=path/to/filelist.json"]


def main(custom_args=None, license_identifier: str | int = None):
    if license_identifier:
        report(
            identifier=license_identifier,
            product="modernmetric"
        )
    if custom_args:
        _args = ArgParser(custom_args)
    else:
        _args = ArgParser()
    _result = {"files": {}, "overall": {}}

    # Get importer
    _importer = {}
    _importer["import_compiler"] = importer_pick(_args, _args.warn_compiler)
    _importer["import_coverage"] = importer_pick(_args, _args.coverage)
    _importer["import_duplication"] = importer_pick(
        _args, _args.warn_duplication)
    _importer["import_functional"] = importer_pick(
        _args, _args.warn_functional)
    _importer["import_security"] = importer_pick(_args, _args.warn_standard)
    _importer["import_standard"] = importer_pick(_args, _args.warn_security)
    # sanity check
    _importer = {k: v for k, v in _importer.items() if v}

    # instance metric modules
    _overallMetrics = get_modules_metrics(_args, **_importer)
    _overallCalc = get_modules_calculated(_args, **_importer)

    with mp.Pool(processes=_args.jobs) as pool:
        results = [pool.apply(file_process, args=(
            f, _args, _importer)) for f in _args.files]

    for x in results:
        oldpath = _args.oldfiles[x[1]]
        _result["files"][oldpath] = x[0]

    for y in _overallMetrics:
        _result["overall"].update(y.get_results_global([x[4] for x in results]))  # noqa: E501
    for y in _overallCalc:
        _result["overall"].update(y.get_results(_result["overall"]))
    for m in get_modules_stats(_args, **_importer):
        _result = m.get_results(_result, "files", "overall")
    if _args.dump:
        # Output
        print(json.dumps(_result, indent=2, sort_keys=True))
    if _args.output_file:
        with open(_args.output_file, "w") as f:
            f.write(json.dumps(_result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
