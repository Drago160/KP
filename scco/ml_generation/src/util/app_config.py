import util.parse_env as pe

################################################################################
# Global setup.

RMQ_NET_ALIAS = pe.get_or_default(
    "RMQ_NET_ALIAS",
    "not_presented"
)
# ----------------------------------------------------------

ML_GENERATION_EXCHANGE = pe.get_or_default(
    "ML_GENERATION_EXCHANGE",
    "not_presented"
)
ML_GENERATION_QUEUE = pe.get_or_default(
    "ML_GENERATION_QUEUE",
    "not_presented"
)
ML_GENERATION_ROUTING_KEY = pe.get_or_default(
    "ML_GENERATION_ROUTING_KEY",
    "not_presented"
)
# ----------------------------------------------------------

DB_FUNCTIONAL_SERVICE_EXCHANGE = pe.get_or_default(
    "DB_FUNCTIONAL_SERVICE_EXCHANGE",
    "not_presented",
)
DB_FUNCTIONAL_SERVICE_QUEUE = pe.get_or_default(
    "DB_FUNCTIONAL_SERVICE_QUEUE",
    "not_presented"
)
DB_FUNCTIONAL_SERVICE_ROUTING_KEY = pe.get_or_default(
    "DB_FUNCTIONAL_SERVICE_ROUTING_KEY",
    "not_presented"
)
# ----------------------------------------------------------

PDF_GENERATION_EXCHANGE = pe.get_or_default(
    "PDF_GENERATION_EXCHANGE",
    "not_presented"
)
PDF_GENERATION_QUEUE = pe.get_or_default(
    "PDF_GENERATION_QUEUE",
    "not_presented"
)
PDF_GENERATION_ROUTING_KEY = pe.get_or_default(
    "PDF_GENERATION_ROUTING_KEY",
    "not_presented"
)

################################################################################
# Local setup.

CO_GEN_EXCHANGE = ML_GENERATION_EXCHANGE
CO_GEN_QUEUE = f"{ML_GENERATION_QUEUE}_co_gen"
CO_GEN_ROUTING_KEY = "ml_gen.co_gen"
