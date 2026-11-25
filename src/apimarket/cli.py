import argparse
import json
import logging
import sys

from apimarket import *
from apimarket import __version__, cli_help, services_cli

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
        response = self.fetch(*values)
        print(to_json(response))
        # Algunos modelos no declaran estos campos y quedan en additional_data.
        extra = getattr(response, "additional_data", {})
        status = getattr(response, "status", None) or extra.get("status")
        if isinstance(status, int) and status >= 500:
            # La API respondió HTTP 200, pero reporta la falla del proveedor en "status".
            message = getattr(response, "message", None) or extra.get("message")
            services_cli.report_error(ApiMarketError(200, {"status": status, "message": message}))
        _logger.debug("Script ends here")
        setattr(namespace, self.dest, values)


class CURPDetailsAction(CLIAction):
    def fetch(self, curp):
        return fetch_curp_details(curp)


class GetBirthRecordAction(CLIAction):
    def fetch(self, curp):
        return get_birth_record(curp)


class GetCURPFromDetailsAction(CLIAction):
    def fetch(self, nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento, claveEntidad, sexo):
        return get_curp_from_details(nombres, paterno, materno, diaNacimiento, mesNacimiento, anoNacimiento, claveEntidad, sexo)


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


class GetClinicByCURPAction(CLIAction):
    def fetch(self, curp):
        return get_clinic_by_curp(curp)


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
    def fetch(self, curp):
        return obtain_sep_cedula(curp)


class SearchLista69bAction(CLIAction):
    def fetch(self, rfc):
        return search_sat_lista69b(rfc=rfc)


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
        return store_token(name=name, company=company, description=description, permissions=permissions.split(","),
                           rfc=rfc, ciec=ciec)


class PermissionDetailsAction(CLIAction):
    def fetch(self):
        return retrieve_permissions()


class IdseListCertificatesAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        import dataclasses
        import json
        certs = idse_list_certificates()
        data = [
            {k: v for k, v in dataclasses.asdict(c).items() if k != 'additional_data' and v is not None}
            for c in certs
        ]
        print(json.dumps(data, default=str, ensure_ascii=False, indent=2))
        setattr(namespace, self.dest, values)


def _deprecated_action(new_flag: str, base_class):
    """Crea una subclase de acción que imprime aviso de deprecación antes de ejecutar."""
    class _DeprecatedAction(base_class):
        def __call__(self, parser, namespace, values, option_string=None):
            print(
                f"\n[DEPRECADO] '{option_string}' ya no estará disponible en futuras versiones. "
                f"Use '{new_flag}' en su lugar.\n",
                file=sys.stderr
            )
            super().__call__(parser, namespace, values, option_string)
    return _DeprecatedAction


class ObtainCedulaLegacyAction(argparse.Action):
    """Acción para la firma vieja --obtain-cedula NOMBRES PATERNO MATERNO (endpoint cambió)."""
    def __call__(self, parser, namespace, values, option_string=None):
        print(
            "\n[DEPRECADO] '--obtain-cedula NOMBRES PATERNO MATERNO' ya no es funcional.\n"
            "  El endpoint de SEP ahora requiere CURP en lugar de nombre y apellidos.\n"
            "  Use: -oc CURP  (ej: -oc XEXX010101MNEXXXA4)\n",
            file=sys.stderr
        )
        sys.exit(1)


class APIMarketParser(services_cli.Parser):
    """Los errores de uso se muestran con el código CLI_ARGUMENTS_INVALID."""


def parse_args(args):
    parser = APIMarketParser(prog="apimarket")
    parser.renderer = lambda: cli_help.main_help(parser, __version__)
    parser.add_argument("--version", action="version", version=f"apimarket {__version__}")

    renapo = parser.add_argument_group("RENAPO")
    renapo.add_argument("-bn", "--birth-record", dest="birth_record",
        metavar="CURP", type=str, action=GetBirthRecordAction,
        help="Busca el acta de nacimiento por CURP.\n  Ejemplo: XEXX010101MNEXXXA4")
    renapo.add_argument("-vc", "--validate-curp", dest="curp",
        metavar="CURP", type=str, action=CURPDetailsAction,
        help="Valida un CURP.\n  Ejemplo: XEXX010101MNEXXXA4")
    renapo.add_argument("-cc", "--calculate-curp", nargs=8,
        metavar=("NOMBRES", "PATERNO", "MATERNO", "DIA_NACIMIENTO", "MES_NACIMIENTO", "ANO_NACIMIENTO", "CLAVE_ENTIDAD", "SEXO"),
        action=GetCURPFromDetailsAction,
        help="Obtiene CURP a partir de datos personales.\n  Ejemplo: -cc \"Juan Carlos\" Garcia Lopez 01 01 1990 DF H\n  Nota: use comillas si el nombre tiene espacios.")

    sat = parser.add_argument_group("SAT")
    sat.add_argument("-ro", "--get-rfc", metavar="CURP",
        action=GetRFCFromCURPAction,
        help="Obtiene RFC a partir de CURP.")
    sat.add_argument("-cr", "--calculate-rfc", nargs=6,
        metavar=("NOMBRES", "PATERNO", "MATERNO", "DIA_NACIMIENTO", "MES_NACIMIENTO", "ANO_NACIMIENTO"),
        action=CalculateRFCAction,
        help="Calcula RFC a partir de datos personales.\n  Ejemplo: -cr \"Juan Carlos\" Garcia Lopez 01 01 1990\n  Nota: use comillas si el nombre tiene espacios.")
    sat.add_argument("-vs", "--validate-sat", nargs=4,
        metavar=("NOMBRE", "RFC", "REGIMEN", "CP"),
        action=ValidateSATDataAction,
        help="Valida datos en el SAT.")
    sat.add_argument("-df", "--fiscal-data", nargs=1, metavar="RFC",
        action=FiscalDataRetrieverAction,
        help="Obtiene datos fiscales por RFC.")
    sat.add_argument("-l69", "--lista69b", metavar="RFC",
        action=SearchLista69bAction,
        help="Consulta la Lista 69-B del SAT (lista negra) por RFC.\n  Ejemplo: -l69 GOAJ900101AB1")

    imss = parser.add_argument_group("IMSS")
    imss.add_argument("-lu", "--locate-umf", nargs=1, metavar="CP",
        action=LocateUMFByCPAction,
        help="Localiza UMF por código postal.")
    imss.add_argument("-ln", "--locate-nss", nargs=1, metavar="CURP",
        action=LocateNSSByCURPAction,
        help="Localiza NSS por CURP.")
    imss.add_argument("-vi", "--check-validity", nargs=2, metavar=("NSS", "CURP"),
        action=CheckVigencyAction,
        help="Verifica vigencia de NSS y CURP.")
    imss.add_argument("-cl", "--get-clinic", nargs=1, metavar="CURP",
        action=GetClinicByCURPAction,
        help="Obtiene clínica asignada por CURP.")
    imss.add_argument("-hl", "--labor-history", nargs=2, metavar=("CURP", "NSS"),
        action=GetLaborHistoryAction,
        help="Consulta historial laboral por CURP y NSS.")

    sep = parser.add_argument_group("SEP")
    sep.add_argument("-ce", "--validate-cedula", metavar="CEDULA",
        action=ValidateCedulaAction,
        help="Valida una cédula profesional.")
    sep.add_argument("-vr", "--validate-certificate", metavar="FOLIO",
        action=ValidateCertificateAction,
        help="Valida un certificado por folio.")
    sep.add_argument("-oc", "--get-cedula", metavar="CURP",
        action=ObtainCedulaAction,
        help="Obtiene cédulas profesionales por CURP.\n  Ejemplo: -oc XEXX010101MNEXXXA4")

    infonavit = parser.add_argument_group("INFONAVIT")
    infonavit.add_argument("-bc", "--search-credit", nargs=1, metavar="NSS",
        action=SearchCreditByNSSAction,
        help="Busca crédito INFONAVIT por NSS.")
    infonavit.add_argument("-si", "--infonavit-subaccount", nargs=1, metavar="NSS",
        action=InfonavitSubAccountRetrieverAction,
        help="Obtiene subcuenta INFONAVIT por NSS.")

    idse = parser.add_argument_group("IDSE Pro")
    idse.add_argument("-lc", "--list-certificates", nargs=0,
        action=IdseListCertificatesAction,
        help="Lista los certificados disponibles en IDSE Pro.")

    cuenta = parser.add_argument_group("Cuenta")
    cuenta.add_argument("-pm", "--permissions", nargs=0,
        action=PermissionDetailsAction,
        help="Muestra los permisos de la cuenta.")
    cuenta.add_argument("-gt", "--store-token", nargs=6,
        metavar=("NOMBRE", "EMPRESA", "DESCRIPCION", "PERMISOS", "RFC", "CIEC"),
        action=StoreTokenAction,
        help="Guarda un nuevo token en la cuenta.")

    # Logging
    parser.add_argument("-v", "--verbose", dest="loglevel", help="Nivel de log: INFO",
        action="store_const", const=logging.INFO)
    parser.add_argument("-vv", "--very-verbose", dest="loglevel", help="Nivel de log: DEBUG",
        action="store_const", const=logging.DEBUG)

    # -----------------------------------------------------------------------
    # Flags deprecados — ocultos de --help, mantenidos por compatibilidad.
    # Serán eliminados en una versión futura.
    # Nota: -cc, -vc y -oc (firma de 3 args) no pueden restaurarse porque sus
    # short flags ahora tienen otro significado en el nuevo CLI.
    # -----------------------------------------------------------------------
    parser.add_argument("-c", dest="_dep_c", metavar="CURP", type=str,
        action=_deprecated_action("-vc", CURPDetailsAction),
        help=argparse.SUPPRESS)
    parser.add_argument("-cd", dest="_dep_cd",
        nargs=8, metavar=("NOMBRES", "PATERNO", "MATERNO", "DIA", "MES", "ANO", "ENTIDAD", "SEXO"),
        action=_deprecated_action("-cc", GetCURPFromDetailsAction),
        help=argparse.SUPPRESS)
    parser.add_argument("-rfc", dest="_dep_rfc", metavar="CURP",
        action=_deprecated_action("-ro", GetRFCFromCURPAction),
        help=argparse.SUPPRESS)
    parser.add_argument("-crfc", dest="_dep_crfc",
        nargs=6, metavar=("NOMBRES", "PATERNO", "MATERNO", "DIA", "MES", "ANO"),
        action=_deprecated_action("-cr", CalculateRFCAction),
        help=argparse.SUPPRESS)
    parser.add_argument("-lucp", dest="_dep_lucp", nargs=1, metavar="CP",
        action=_deprecated_action("-lu", LocateUMFByCPAction),
        help=argparse.SUPPRESS)
    parser.add_argument("-lnc", dest="_dep_lnc", nargs=1, metavar="CURP",
        action=_deprecated_action("-ln", LocateNSSByCURPAction),
        help=argparse.SUPPRESS)
    parser.add_argument("-cv", dest="_dep_cv", nargs=2, metavar=("NSS", "CURP"),
        action=_deprecated_action("-vi", CheckVigencyAction),
        help=argparse.SUPPRESS)
    parser.add_argument("--get-clinica-by-curp", dest="_dep_cc_clinic", nargs=1, metavar="CURP",
        action=_deprecated_action("-cl", GetClinicByCURPAction),
        help=argparse.SUPPRESS)
    parser.add_argument("-l", dest="_dep_l", nargs=2, metavar=("CURP", "NSS"),
        action=_deprecated_action("-hl", GetLaborHistoryAction),
        help=argparse.SUPPRESS)
    parser.add_argument("-vce", dest="_dep_vce", metavar="FOLIO",
        action=_deprecated_action("-vr", ValidateCertificateAction),
        help=argparse.SUPPRESS)
    parser.add_argument("--obtain-cedula", dest="_dep_oc_legacy",
        nargs=3, metavar=("NOMBRES", "PATERNO", "MATERNO"),
        action=ObtainCedulaLegacyAction,
        help=argparse.SUPPRESS)
    parser.add_argument("--validate-sat-data", dest="_dep_vs", nargs=4,
        metavar=("NOMBRE", "RFC", "REGIMEN", "CP"),
        action=_deprecated_action("-vs", ValidateSATDataAction),
        help=argparse.SUPPRESS)
    parser.add_argument("-cn", dest="_dep_cn", nargs=1, metavar="NSS",
        action=_deprecated_action("-bc", SearchCreditByNSSAction),
        help=argparse.SUPPRESS)
    parser.add_argument("-fd", dest="_dep_fd", nargs=1, metavar="RFC",
        action=_deprecated_action("-df", FiscalDataRetrieverAction),
        help=argparse.SUPPRESS)
    parser.add_argument("-sa", dest="_dep_sa", nargs=1, metavar="NSS",
        action=_deprecated_action("-si", InfonavitSubAccountRetrieverAction),
        help=argparse.SUPPRESS)
    parser.add_argument("-st", dest="_dep_st", nargs=6,
        metavar=("NOMBRE", "EMPRESA", "DESCRIPCION", "PERMISOS", "RFC", "CIEC"),
        action=_deprecated_action("-gt", StoreTokenAction),
        help=argparse.SUPPRESS)

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    if services_cli.handles(args):
        services_cli.main(args)
        return
    args = list(args) or ["--help"]  # sin argumentos se muestra la ayuda
    if not args[0].startswith("-"):
        services_cli.unknown_area(args[0])
    # Las acciones consultan la API mientras se leen los argumentos.
    try:
        args = parse_args(args)
    except services_cli.HANDLED_ERRORS as e:
        services_cli.report_error(e)
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
