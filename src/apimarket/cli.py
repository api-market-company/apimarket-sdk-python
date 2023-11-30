import argparse
import logging
import json
from apimarket import __version__
from apimarket import *

__author__ = "Carlos Eduardo Sanchez Torres (sanchezcarlosjr)"
__copyright__ = "API MARKET"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


class CLIAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        _logger.debug("Fetching apimarket...")
        if isinstance(values, (str, int)):
            values = [values]
        print(f"{json.dumps(self.fetch(*values))}")
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, values)


class CURPDetailsAction(CLIAction):
    def fetch(self, curp):
        return fetch_curp_details(curp)


class GetCURPFromDetailsAction(CLIAction):
    def fetch(self, nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento, claveEntidad, sexo):
        return get_curp_from_details(nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento,
                                     claveEntidad, sexo)


class GetRFCFromCURPAction(CLIAction):
    def fetch(self, curp):
        return get_rfc_from_curp(curp)


class CalculateRFCAction(CLIAction):
    def fetch(self, nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento):
        return calculate_rfc(nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento)


class LocateUMFByCPAction(CLIAction):
    def fetch(self, cp):
        return locate_umf_by_cp(cp)


class LocateNSSByCURPAction(CLIAction):
    def fetch(self, curp):
        return locate_nss_by_curp(curp)


class CheckVigencyAction(CLIAction):
    def fetch(self, nss, curp):
        return check_nss_validity(nss, curp)


class GetClinicaByCURPAction(CLIAction):
    def fetch(self, curp):
        return get_clinica_by_curp(curp)


class GetLaborHistoryAction(CLIAction):
    def fetch(self, curp, nss):
        return get_labor_history(curp, nss)


class ValidateCedulaAction(CLIAction):
    def fetch(self, cedula):
        return validate_sep_cedula(cedula)


class ValidateCertificateAction(CLIAction):
    def fetch(self, folio):
        return validate_sep_certificate(folio)


class ObtainCedulaAction(CLIAction):
    def fetch(self, nombres, paterno, materno):
        return obtain_sep_cedula(nombres, paterno, materno)


class ValidateSATDataAction(CLIAction):
    def fetch(self, nombre, rfc, regimen, cp):
        return validate_sat_data(nombre, rfc, regimen, cp)


class SearchCreditByNSSAction(CLIAction):
    def fetch(self, nss):
        return search_credit_by_nss(nss)


class FiscalDataRetrieverAction(CLIAction):
    def fetch(self, rfc):
        return get_mexican_fiscal_data_with_rfc(rfc)


class InfonavitSubAccountRetrieverAction(CLIAction):
    def fetch(self, nss):
        return get_infonavit_subaccount(nss)


class StoreTokenAction(CLIAction):
    def fetch(self, name, company="", description="", permissions="", rfc="", ciec=""):
        return store_token(name=name, company=company, description=description, permissions=permissions.split(","), rfc=rfc, ciec=ciec)


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
    parser.add_argument(
        "-st",
        "--store-token",
        help="Store a new token in your account",
        nargs=6,
        metavar=('Nombre', 'Empresa', 'Descripcion', 'Permisos', 'RFC', 'CIEC'),
        action=StoreTokenAction
    )
    parser.add_argument('-cd', '--get-curp-details',
                        nargs=8,
                        metavar=('NOMBRES', 'PATERNO', 'MATERNO', 'DIA_NACIMIENTO', 'MES_NACIMIENTO', 'ANO_NACIMIENTO',
                                 'CLAVE_ENTIDAD', 'SEXO'),
                        action=GetCURPFromDetailsAction,
                        help='Fetch CURP based on personal details.'
                        )
    parser.add_argument('-rfc', '--get-rfc-from-curp', action=GetRFCFromCURPAction, help='Fetch RFC based on CURP.')
    parser.add_argument('-crfc', '--calculate-rfc', nargs=6,
                        metavar=('NOMBRES', 'PATERNO', 'MATERNO', 'DIA_NACIMIENTO', 'MES_NACIMIENTO', 'ANO_NACIMIENTO'),
                        action=CalculateRFCAction, help='Calculate RFC based on personal details.')
    parser.add_argument('-lucp', '--locate-umf-by-cp', nargs=1, metavar=('CP'), action=LocateUMFByCPAction,
                        help='Locate UMF based on postal code.')
    parser.add_argument('-lnc', '--locate-nss-by-curp', nargs=1, metavar=('CURP'), action=LocateNSSByCURPAction,
                        help='Locate NSS based on CURP.')
    parser.add_argument('-cv', '--check-vigency', nargs=2, metavar=('NSS', 'CURP'), action=CheckVigencyAction,
                        help='Check vigency of NSS and CURP.')
    parser.add_argument('-cc', '--get-clinica-by-curp', nargs=1, metavar=('CURP'), action=GetClinicaByCURPAction,
                        help='Get clinic details by CURP.')
    parser.add_argument('-l', '--get-labor-history', nargs=2, metavar=('CURP', 'NSS'), action=GetLaborHistoryAction,
                        help='Get labor history by CURP and NSS.')
    parser.add_argument('-vc', '--validate-cedula', action=ValidateCedulaAction, help='Validate a cedula.')
    parser.add_argument('-vce', '--validate-certificate', action=ValidateCertificateAction,
                        help='Validate a certificate by its folio.')
    parser.add_argument('-oc', '--obtain-cedula', nargs=3, metavar=('NOMBRES', 'PATERNO', 'MATERNO'),
                        action=ObtainCedulaAction, help='Obtain cedula based on personal details.')
    parser.add_argument('--validate-sat-data', nargs=4, metavar=('NOMBRE', 'RFC', 'REGIMEN', 'CP'),
                        action=ValidateSATDataAction, help='Validate SAT data.')
    parser.add_argument('-cn', '--search-credit-by-nss', nargs=1, metavar=('NSS'), action=SearchCreditByNSSAction,
                        help='Search credit by NSS.')
    parser.add_argument('-fd', '--get-fiscal-data-by-rfc', nargs=1, metavar=('RFC'), action=FiscalDataRetrieverAction,
                        help='Fetch Fiscal Data by RFC.')
    parser.add_argument('-sa', '--get-infonavit-subaccount-by-nss', nargs=1, metavar=('NSS'),
                        action=FiscalDataRetrieverAction, help='Fetch INFONAVIT subaccount by NSS.')
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
