import argparse
import logging
import sys
import json

from apimarket import __version__
from apimarket import *

__author__ = "Carlos Eduardo Sanchez Torres (sanchezcarlosjr)"
__copyright__ = "API MARKET"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from apimarket.skeleton import fib`,
# when using this Python module as a library.


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


class CURPDetailsAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, curp, option_string=None):
        _logger.debug("Fetching apimarket...")
        print(f"{json.dumps(fetch_curp_details(curp))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, curp)


class GetCURPFromDetailsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento, claveEntidad, sexo, api_key = values
        _logger.debug("Fetching apimarket...")
        print(f"{json.dumps(get_curp_from_details(nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento, claveEntidad, sexo, api_key))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, values)


class GetRFCFromCURPAction(argparse.Action):
    def __call__(self, parser, namespace, curp, option_string=None):
        _logger.debug("Fetching RFC from CURP...")
        print(f"{json.dumps(get_rfc_from_curp(curp))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, curp)

class CalculateRFCAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento, api_key = values
        _logger.debug("Calculating RFC...")
        print(f"{json.dumps(calculate_rfc(nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento, api_key))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, values)

class LocateUMFByCPAction(argparse.Action):
    def __call__(self, parser, namespace, cp, option_string=None):
        _logger.debug("Locating UMF by CP...")
        print(f"{json.dumps(locate_umf_by_cp(cp))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, cp)


class LocateNSSByCURPAction(argparse.Action):
    def __call__(self, parser, namespace, curp, option_string=None):
        _logger.debug("Locating NSS by CURP...")
        print(f"{json.dumps(locate_nss_by_curp(curp))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, curp)


class CheckVigencyAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        nss, curp, api_key = values
        _logger.debug("Checking vigency...")
        print(f"{json.dumps(check_vigency(nss, curp, api_key))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, values)


class GetClinicaByCURPAction(argparse.Action):
    def __call__(self, parser, namespace, curp, option_string=None):
        _logger.debug("Getting clinic by CURP...")
        print(f"{json.dumps(get_clinica_by_curp(curp))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, curp)


class GetLaborHistoryAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        curp, nss, api_key = values
        _logger.debug("Fetching labor history...")
        print(f"{json.dumps(get_labor_history(curp, nss, api_key))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, values)


class ValidateCedulaAction(argparse.Action):
    def __call__(self, parser, namespace, cedula, option_string=None):
        _logger.debug("Validating cedula...")
        print(f"{json.dumps(validate_cedula(cedula))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, cedula)

class ValidateCertificateAction(argparse.Action):
    def __call__(self, parser, namespace, folio, option_string=None):
        _logger.debug("Validating certificate...")
        print(f"{json.dumps(validate_certificate(folio))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, folio)

class ObtainCedulaAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        nombres, paterno, materno, api_key = values
        _logger.debug("Obtaining cedula...")
        print(f"{json.dumps(obtain_cedula(nombres, paterno, materno, api_key))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, values)

class ValidateSATDataAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        nombre, rfc, regimen, cp, api_key = values
        _logger.debug("Validating SAT data...")
        print(f"{json.dumps(validate_sat_data(nombre, rfc, regimen, cp, api_key))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, values)

class SearchCreditByNSSAction(argparse.Action):
    def __call__(self, parser, namespace, nss, option_string=None):
        _logger.debug("Searching credit by NSS...")
        print(f"{json.dumps(search_credit_by_nss(nss))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, nss)


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="API Market Python Open Source Development")
    parser.add_argument(
        "--version",
        action="version",
        version=f"apimarket {__version__}",
    )
    parser.add_argument(
        "-c",
        "--curp",
        dest="curp", 
        help="Write a valid CURP. For instance, LOOA531113HTCPBN07", 
        type=str, 
        metavar="CURP",
        action=CURPDetailsAction
    )
    parser.add_argument('--get-curp-details', 
                        nargs=9,
                        metavar=('NOMBRES', 'PATERNO', 'MATERNO', 'DIA_NACIMIENTO', 'MES_NACIMIENTO', 'ANO_NACIMIENTO', 'CLAVE_ENTIDAD', 'SEXO', 'API_KEY'),
                        action=GetCURPFromDetailsAction,
                        help='Fetch CURP based on personal details.'
                       )
    parser.add_argument('--get-rfc-from-curp', action=GetRFCFromCURPAction, help='Fetch RFC based on CURP.')
    parser.add_argument('--calculate-rfc', nargs=7, metavar=('NOMBRES', 'PATERNO', 'MATERNO', 'DIA_NACIMIENTO', 'MES_NACIMIENTO', 'ANO_NACIMIENTO', 'API_KEY'), action=CalculateRFCAction, help='Calculate RFC based on personal details.')
    parser.add_argument('--locate-umf-by-cp', action=LocateUMFByCPAction, help='Locate UMF based on postal code.')
    parser.add_argument('--locate-nss-by-curp', action=LocateNSSByCURPAction, help='Locate NSS based on CURP.')
    parser.add_argument('--check-vigency', nargs=3, metavar=('NSS', 'CURP', 'API_KEY'), action=CheckVigencyAction, help='Check vigency of NSS and CURP.')
    parser.add_argument('--get-clinica-by-curp', action=GetClinicaByCURPAction, help='Get clinic details by CURP.')
    parser.add_argument('--get-labor-history', nargs=3, metavar=('CURP', 'NSS', 'API_KEY'), action=GetLaborHistoryAction, help='Get labor history by CURP and NSS.')
    parser.add_argument('--validate-cedula', action=ValidateCedulaAction, help='Validate a cedula.')
    parser.add_argument('--validate-certificate', action=ValidateCertificateAction, help='Validate a certificate by its folio.')
    parser.add_argument('--obtain-cedula', nargs=4, metavar=('NOMBRES', 'PATERNO', 'MATERNO', 'API_KEY'), action=ObtainCedulaAction, help='Obtain cedula based on personal details.')
    parser.add_argument('--validate-sat-data', nargs=5, metavar=('NOMBRE', 'RFC', 'REGIMEN', 'CP', 'API_KEY'), action=ValidateSATDataAction, help='Validate SAT data.')
    parser.add_argument('--search-credit-by-nss', action=SearchCreditByNSSAction, help='Search credit by NSS.')
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m apimarket.cli 42
    #
    run()
