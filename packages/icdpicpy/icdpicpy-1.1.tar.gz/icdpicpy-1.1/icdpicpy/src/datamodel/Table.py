class BaseColumns:
    code = 'dx'
    severity = 'severity'
    issbr = 'issbr'


class injury_cause:
    file_name = 'etab_s1.csv'
    code = "dx"
    mechmaj = "mechmaj"
    mechmin = "mechmin"
    intent = "intent"


class severity_data:
    file_name = 'ntab_s1.csv'
    code = "dx"
    severity = "severity"
    issbr = "issbr"


class i10_ecode:
    file_name = 'i10_ecode.csv'
    code = "dx"
    mechmaj = "mechmaj"
    mechmin = "mechmin"
    intent = "intent"


class i10_map_max:
    file_name = 'i10_map_max.csv'
    code = "dx"
    severiy = "severity"
    issbr = "issbr"


class i10_map_min:
    file_name = 'i10_map_min.csv'
    code = "dx"
    severiy = "severity"
    issbr = "issbr"


class i10_map_roc:
    file_name = 'i10cm_map_roc.csv'
    code = "dx"
    TQIP_severity = "TQIP_severity"
    TQIP_issbr = "TQIP_issbr"
    NIS_severity = "NIS_severity"
    NIS_issbr = "NIS_issbr"
    TQIP_only_severity = "TQIP_only_severity"
    TQIP_only_issbr = "TQIP_only_issbr"
    NIS_only_severity = "NIS_only_severity"
    NIS_only_issbr = "NIS_only_issbr"
    TQIP_effect = "TQIP_effect"
    TQIP_intercept = "TQIP_intercept"
    NIS_effect = "NIS_effect"
    NIS_intercept = "NIS_intercept"


class Result:
    mortality = 'mortality'
    patient = 'patient'
    iss = 'ISS'
    niss = 'NISS'
    mechmaj = "mechmaj"
    mechmin = "mechmin"
    intent = "intent"

