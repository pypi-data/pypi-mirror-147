import logging
import math
from typing import Optional

import pandas as pd

from icdpicpy.src.datamodel import Constants, Table, Score
from icdpicpy.src.datamodel.CodeMappingMethod import ICD10CodeMappingMethod, ISSCalcMethod
from icdpicpy.src.repository.DataRepository import DataRepository


class CalcScore:
    def __init__(self, data_repo: DataRepository):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__data_repo = data_repo

    def execute(self, patient_code_dict: dict, score_list: list = None, use_icd10: bool = True,
                icd10_method: str = 'gem_max', iss_calc_method: int = 1) -> Optional[pd.DataFrame]:
        self.__logger.debug(
            f'execute for {len(patient_code_dict)} patients, scores {score_list}, use_icd10: {use_icd10},'
            f' icd10 method: {icd10_method}, iss calculation method:{iss_calc_method}')

        if not self.__validate_params(patient_code_dict, use_icd10, icd10_method, iss_calc_method, score_list):
            return
        if score_list is None:
            score_list = Score.all_scores
        iss_calc_method = ISSCalcMethod.from_int(iss_calc_method)
        injury_cause_df = self.__data_repo.read_data_file(Table.injury_cause.file_name)
        severity_data_df = self.__data_repo.read_data_file(Table.severity_data.file_name)
        severity_data_df[Table.severity_data.code] = severity_data_df[Table.severity_data.code].astype(str)
        # add i10 codes
        if use_icd10:
            map_df = self.__add_i10_injury_codes(icd10_method)
            if map_df is None or map_df.empty:
                self.__logger.warning('No ICD10 mapping data')
            else:
                severity_data_df = pd.concat([severity_data_df, map_df])
            injury_cause_icd10_df = self.__data_repo.read_data_file(Table.i10_ecode.file_name)
            injury_cause_df = pd.concat([injury_cause_df, injury_cause_icd10_df])

        res_df = None
        if Score.ISS_score in score_list:
            patient_iss_df = self.__calc_iss(patient_code_dict, severity_data_df, iss_calc_method)
            res_df = patient_iss_df
        if Score.NISS_score in score_list:
            patient_niss_df = self.__calc_niss(patient_code_dict, severity_data_df, iss_calc_method)
            res_df = patient_niss_df if res_df is None else \
                res_df.merge(patient_niss_df, on=Table.Result.patient)
        if use_icd10 and Score.Mortality_score in score_list:
            mortality_df = self.__calc_mortality(patient_code_dict, icd10_method)
            if mortality_df is not None:
                res_df = mortality_df if res_df is None else \
                    res_df.merge(mortality_df, on=Table.Result.patient)
        if Score.Injury_cause in score_list:
            patient_injury_cause_df = self.__get_injury_cause(patient_code_dict, injury_cause_df)
            if patient_injury_cause_df is not None:
                res_df = patient_injury_cause_df if res_df is None else \
                    res_df.merge(patient_injury_cause_df, on=Table.Result.patient)
        return res_df

    def __calc_iss(self, patient_code_dict: dict, severity_df: pd.DataFrame,
                   iss_calc_method: ISSCalcMethod) -> pd.DataFrame:
        self.__logger.debug('calc ISS')
        res = {Table.Result.patient: [], Table.Result.iss: []}
        for patient, codes in patient_code_dict.items():
            codes = [self.__prepare_code(c) for c in codes]
            # get only codes of the current patient
            curr_severity_df = severity_df[severity_df[Table.severity_data.code].isin(codes)]
            # severity score of 9 implies unknown severity.
            # Thus we want to exclude these as long as there is at least one known severity for the body region
            # However if all severity scores for the body region are 9 then we will assign max value of 9
            for br in curr_severity_df[Table.BaseColumns.issbr].unique():
                unique_values = curr_severity_df[Table.BaseColumns.severity].unique()
                if len(unique_values) > 1 and Constants.UnknownSeverityValue in unique_values:
                    # there are other values so Unknown can be removed
                    known_values_cond = (curr_severity_df[Table.BaseColumns.issbr] != br) | \
                                        (curr_severity_df[Table.BaseColumns.severity] != Constants.UnknownSeverityValue)
                    curr_severity_df = curr_severity_df.loc[known_values_cond, :]
            # find max severity for each body region
            br_df = curr_severity_df.groupby([Table.BaseColumns.issbr])[Table.BaseColumns.severity].max()
            # find iss as a sum of square of the largest severity scores but 75 is max
            severity_values: list = br_df.reset_index()[Table.BaseColumns.severity].tolist()
            severity_values.sort(reverse=True)
            max_pos = min(3, len(severity_values))
            severity_values = severity_values[:max_pos]
            if all([x == Constants.UnknownSeverityValue for x in severity_values]):
                iss_value = 'NA'
            else:
                severity_values = [0 if x == Constants.UnknownSeverityValue else x
                                   for x in severity_values]
                sqr_sum = 0
                if Constants.SeverityMaxValue in severity_values:
                    if iss_calc_method == ISSCalcMethod.default:
                        sqr_sum = Constants.MaxISSValue
                    elif iss_calc_method == ISSCalcMethod.extreme_cut:
                        severity_values = [x - 1 if x == Constants.MaxISSValue else x
                                           for x in severity_values]
                        sqr_sum = sum([x * x for x in severity_values])
                else:
                    sqr_sum = sum([x * x for x in severity_values])
                iss_value = min(sqr_sum, Constants.MaxISSValue)
            res[Table.Result.patient].append(patient)
            res[Table.Result.iss].append(iss_value)
        res_df = pd.DataFrame.from_dict(res)
        return res_df

    def __calc_niss(self, patient_code_dict: dict, severity_df: pd.DataFrame,
                    iss_calc_method: ISSCalcMethod) -> pd.DataFrame:
        self.__logger.debug('calc NISS')
        res = {Table.Result.patient: [], Table.Result.niss: []}
        for patient, codes in patient_code_dict.items():
            codes = [self.__prepare_code(c) for c in codes]
            # get only codes of the current patient
            severity_values = severity_df.loc[severity_df[Table.severity_data.code].isin(codes),
                                              Table.severity_data.severity].tolist()
            # severity score of 9 implies unknown severity.
            # Thus we want to exclude these as long as there is at least one known severity for the patient
            # However if all severity scores for the patient are 9 then we will assign value NA
            if all([x == Constants.UnknownSeverityValue for x in severity_values]):
                niss_value = 'NA'
            else:
                severity_values = [0 if x == Constants.UnknownSeverityValue else x
                                   for x in severity_values]
                severity_values.sort(reverse=True)
                max_pos = min(3, len(severity_values))
                severity_values = severity_values[:max_pos]
                if iss_calc_method == ISSCalcMethod.default:
                    if any([x == Constants.SeverityMaxValue for x in severity_values]):
                        niss_value = Constants.MaxISSValue
                    else:
                        niss_value = sum([x * x for x in severity_values])
                elif iss_calc_method == ISSCalcMethod.extreme_cut:
                    severity_values = [x - 1 if x == Constants.SeverityMaxValue else x
                                       for x in severity_values]
                    niss_value = sum([x * x for x in severity_values])
                else:
                    niss_value = 0
                niss_value = min(niss_value, Constants.MaxISSValue)

            res[Table.Result.patient].append(patient)
            res[Table.Result.niss].append(niss_value)

        res_df = pd.DataFrame.from_dict(res)
        return res_df

    def __prepare_code(self, code: str) -> str:
        code = code.strip().replace(".", "")
        if len(code) > 5 and code[5] == "X":
            return code[:5]
        if len(code) > 6 and code[6] == "X":
            return code[:6]
        return code

    def __validate_params(self, patient_code_dict: dict, use_icd10: bool, icd10_method: str,
                          iss_calc_method: int, score_list: Optional[list]) -> bool:
        self.__logger.debug('validate parameters')
        if not patient_code_dict:
            self.__logger.error(f'No patient data')
            return False

        if use_icd10 and ICD10CodeMappingMethod.from_string(icd10_method) is None:
            self.__logger.error(f'Unknown ICD10 mapping method {icd10_method}. '
                                f'Value should be one of {ICD10CodeMappingMethod.all_values()}')
            return False
        if ISSCalcMethod.from_int(iss_calc_method) is None:
            self.__logger.error(f'Unknown ISS calculation method {iss_calc_method}. '
                                f'Value should be one of {ISSCalcMethod.all_values()}')
            return False
        if score_list is not None:
            if any([x not in Score.all_scores for x in score_list]):
                self.__logger.error(f'Unknown score: {[x for x in score_list if x not in Score.all_scores]}. '
                                    f'Score can be one of {Score.all_scores}')
                return False
        return True

    def __add_i10_injury_codes(self, icd10_method: str) -> Optional[pd.DataFrame]:
        method = ICD10CodeMappingMethod.from_string(icd10_method)
        if method is None:
            self.__logger.error(f'Unknown ICD10 mapping method {icd10_method}')
        map_df: Optional[pd.DataFrame] = None
        if method == ICD10CodeMappingMethod.roc_max_NIS:
            map_df = self.__data_repo.read_data_file(Table.i10_map_roc.file_name)
            map_df = map_df[[Table.i10_map_roc.code, Table.i10_map_roc.NIS_severity, Table.i10_map_roc.NIS_issbr]]
        elif method == ICD10CodeMappingMethod.roc_max_NIS_only:
            map_df = self.__data_repo.read_data_file(Table.i10_map_roc.file_name)
            map_df = map_df[
                [Table.i10_map_roc.code, Table.i10_map_roc.NIS_only_severity, Table.i10_map_roc.NIS_only_issbr]
            ]
        elif method == ICD10CodeMappingMethod.roc_max_TQIP:
            map_df = self.__data_repo.read_data_file(Table.i10_map_roc.file_name)
            map_df = map_df[[Table.i10_map_roc.code, Table.i10_map_roc.TQIP_severity, Table.i10_map_roc.TQIP_issbr]]
        elif method == ICD10CodeMappingMethod.roc_max_TQIP_only:
            map_df = self.__data_repo.read_data_file(Table.i10_map_roc.file_name)
            map_df = map_df[
                [Table.i10_map_roc.code, Table.i10_map_roc.TQIP_only_severity, Table.i10_map_roc.TQIP_only_issbr]
            ]
        elif method == ICD10CodeMappingMethod.gem_min:
            map_df = self.__data_repo.read_data_file(Table.i10_map_min.file_name)
            map_df = map_df[[Table.i10_map_min.code, Table.i10_map_min.severiy, Table.i10_map_min.issbr]]
        elif method == ICD10CodeMappingMethod.gem_max:
            map_df = self.__data_repo.read_data_file(Table.i10_map_max.file_name)
            map_df = map_df[[Table.i10_map_max.code, Table.i10_map_max.severiy, Table.i10_map_max.issbr]]
        # rename columns with severity and issbr
        map_df.columns = [Table.BaseColumns.severity if Table.BaseColumns.severity in c else c
                          for c in map_df.columns]
        map_df.columns = [Table.BaseColumns.issbr if Table.BaseColumns.issbr in c else c
                          for c in map_df.columns]
        return map_df

    def __get_injury_cause(self, patient_code_dict: dict, injury_cause_df: pd.DataFrame) -> Optional[pd.DataFrame]:
        self.__logger.debug('get injury cause')
        injury_cause_df[Table.injury_cause.code] = injury_cause_df[Table.injury_cause.code].apply(lambda x: x.strip())
        res = {Table.Result.patient: list(patient_code_dict.keys()),
               Table.Result.mechmaj: [], Table.Result.mechmin: [], Table.Result.intent: []}
        for p, codes in patient_code_dict.items():
            codes = [self.__prepare_code(c) for c in codes]
            curr_injury_cause_df = injury_cause_df[injury_cause_df[Table.injury_cause.code].isin(codes)]
            res[Table.Result.mechmin].append(curr_injury_cause_df[Table.injury_cause.mechmin].unique().tolist())
            res[Table.Result.mechmaj].append(curr_injury_cause_df[Table.injury_cause.mechmaj].unique().tolist())
            res[Table.Result.intent].append(curr_injury_cause_df[Table.injury_cause.intent].unique().tolist())
        return pd.DataFrame(data=res)

    def __calc_mortality(self, patient_code_dict: dict, icd10_method: str) -> Optional[pd.DataFrame]:
        self.__logger.debug(f'calc mortality for method {icd10_method}')
        method = ICD10CodeMappingMethod.from_string(icd10_method)
        if method is None:
            self.__logger.error(f'Can not calculate mortality: Unknown ICD10 mapping method {icd10_method}')
            return None
        if method in [ICD10CodeMappingMethod.roc_max_NIS, ICD10CodeMappingMethod.roc_max_NIS_only]:
            mortality_df = self.__data_repo.read_data_file(Table.i10_map_roc.file_name)
            mortality_df = mortality_df[
                [Table.i10_map_roc.code, Table.i10_map_roc.NIS_intercept, Table.i10_map_roc.NIS_effect]
            ]
            intercept_col, effect_col = Table.i10_map_roc.NIS_intercept, Table.i10_map_roc.NIS_effect
        elif method in [ICD10CodeMappingMethod.roc_max_TQIP, ICD10CodeMappingMethod.roc_max_TQIP_only]:
            mortality_df = self.__data_repo.read_data_file(Table.i10_map_roc.file_name)
            mortality_df = mortality_df[
                [Table.i10_map_roc.code, Table.i10_map_roc.TQIP_intercept, Table.i10_map_roc.TQIP_effect]
            ]
            intercept_col, effect_col = Table.i10_map_roc.TQIP_intercept, Table.i10_map_roc.TQIP_effect
        else:
            return None
        # calc mortality for each patient
        res = {Table.Result.patient: [], Table.Result.mortality: []}
        for p, codes in patient_code_dict.items():
            codes = [self.__prepare_code(c) for c in codes]
            curr_mortality_df = mortality_df[mortality_df[Table.i10_map_roc.code].isin(codes)]
            if curr_mortality_df[intercept_col].min() != curr_mortality_df[intercept_col].max():
                continue
            x = curr_mortality_df[effect_col].sum() + curr_mortality_df[intercept_col].min()
            mortality = 1 / (1 + math.exp(-x))
            res[Table.Result.patient].append(p)
            res[Table.Result.mortality].append(mortality)
        return pd.DataFrame(res)
