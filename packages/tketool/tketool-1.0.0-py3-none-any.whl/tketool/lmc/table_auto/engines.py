import abc
import pandas as pd
import os.path
import openpyxl
import re, math, json
from tketool.lmc.prompts.prompt_controller import get_prompt, get_prompt_by_path
from tketool.utils.progressbar import process_status_bar
from tketool.utils.MultiTask import do_multitask
from tketool.lmc.lmc_linked import *
from tketool.lmc.lmc_linked_flow import lmc_linked_flow_model


class excel_agent(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def match_str(self):
        pass

    @abc.abstractmethod
    def call(self, llm, row_dict, cur_col_name, sheet_obj, params, content):
        pass


class double_shape(excel_agent):

    @property
    def match_str(self):
        return "##"

    def call(self, llm, row_dict, cur_name, sheet_obj, params, content):
        llm_invoker = lmc_linked_model(llm).set_prompt_template(content)
        result = llm_invoker(**row_dict)
        if len(result.results) > 0:
            return str(result.result)
        else:
            return ""


class prompt_file_shape(excel_agent):

    def __init__(self):
        self.invoker_dict = {}

    @property
    def match_str(self):
        return "#promptfile"

    def call(self, llm, row_dict, cur_name, sheet_obj, params, content):
        invoker_key = "#".join(list(cur_name))
        if invoker_key not in self.invoker_dict:
            path = params[0][1:-1]
            parse_field = get_prompt_by_path(path)
            self.invoker_dict[invoker_key] = lmc_linked_flow_model(parse_field, retry_time=2)
        mapping_dict = {}
        for k, v in row_dict.items():
            if isinstance(v, str):
                mapping_dict[k] = v
            else:
                if not math.isnan(v):
                    mapping_dict[k] = v
        if len(params) > 1:
            mapping_change_dict = {}
            mapping_change = params[1][1:-1].split("#")
            for spp in mapping_change:
                s = spp.split("=")
                if len(s) == 2:
                    mapping_change_dict[s[0]] = s[1]

            for k, v in mapping_change_dict.items():
                if k in mapping_dict:
                    mapping_dict[v] = mapping_dict[k]
                if v in mapping_dict:
                    mapping_dict[k] = mapping_dict[v]

        llmresult = self.invoker_dict[invoker_key](llm, **mapping_dict)
        if not llmresult.passed:
            return "Invoke error"
        if len(params) > 2:
            output_str = params[2][1:-1]
            result_str = eval("llmresult.result." + output_str)
            return result_str
        else:
            return llmresult.result.json()


class sheet_data:
    def __init__(self, sheet_obj, all_agents):
        self.sheet_obj = sheet_obj
        self.all_agents = all_agents
        self.column_names = []
        self.column_name_index = {}
        self.excel_column_names = []
        self.column_agent = []
        self.rows = []

        for col_name in sheet_obj.columns.tolist():
            self.column_names.append(col_name)
            excel_col_name = openpyxl.utils.get_column_letter(sheet_obj.columns.get_loc(col_name) + 1)
            self.excel_column_names.append(excel_col_name)
            self.column_agent.append(self.parse_colstr(col_name))

        self.mapping_agent = [all_agents[cmd] if cmd in all_agents else None for cmd, par, con in self.column_agent]

        for idx, row in sheet_obj.iterrows():
            cur_row = []
            for c_idx in self.column_names:
                cur_row.append(row[c_idx])
            self.rows.append(cur_row)

        self.column_name_index = {colname: idx for idx, colname in enumerate(self.column_names)}

    def parse_colstr(self, col_str):
        if not isinstance(col_str, str):
            return (None, None, None)
        if col_str.startswith("##"):
            return ("##", [], col_str[2:])
        else:
            pattern = r'(#\w+)(?:\(([^)]+)\))?(?::\s*(.*))?'
            match = re.match(pattern, col_str)
            if match:
                command = match.group(1).strip()  # 提取指令
                params = match.group(2)  # 提取参数，可能为None
                content = match.group(3)

                if params:
                    params_list = [param.strip() for param in params.split(',')]
                else:
                    params_list = []

                if command in self.all_agents:
                    return (command, params_list, content)

        return (None, None, None)

    def set(self, row_index, col_name, value):
        self.sheet_obj.at[row_index, col_name] = value
        col_index = self.column_name_index[col_name]
        self.rows[row_index][col_index] = value
        pass


class excel_engine:
    def __init__(self, llm, *args, thread=1):
        self.all_agents = {}
        self.llm = llm
        self.thread_count = thread
        for arg in args:
            if isinstance(arg, excel_agent):
                self.all_agents[arg.match_str] = arg

    def parse_sheet(self, sheet_obj_dict, sheet_key, pass_row_count, pb):
        def do_task(idx):
            sheet_obj = sheet_obj_dict[sheet_key]


            for op, row_tile, coln, coln2 in zip(sheet_obj.mapping_agent, sheet_obj.column_agent,
                                                 sheet_obj.column_names,
                                                 sheet_obj.excel_column_names):
                if op is None:
                    continue

                row_dict = {k: v for k, v in
                            zip(sheet_obj.excel_column_names, sheet_obj.rows[idx])}

                if not isinstance(row_dict[coln2], str) and math.isnan(row_dict[coln2]):
                    params = row_tile[1]
                    content = row_tile[2]
                    call_result = op.call(self.llm, row_dict, (sheet_key, coln2), sheet_obj_dict, params, content)
                    sheet_obj_dict[sheet_key].set(idx, coln, call_result)

        pass
        rows_index = list(range(pass_row_count,
                                len(sheet_obj_dict[sheet_key].rows)))  # sheet_obj_dict[sheet_key].rows[pass_row_count:]
        for row, c_row in pb.iter_bar(
                do_multitask(rows_index, do_task, self.thread_count, self.thread_count * 2),
                key="row", max=len(rows_index)):
            pass

    def call_file(self, excel_file_path: str, write_log_if_error=False, start_row_index=0):
        xls = pd.ExcelFile(excel_file_path)
        pb = process_status_bar()

        all_sheets = {}

        for sheet in xls.sheet_names:
            sheet_content = sheet_data(xls.parse(sheet), all_agents=self.all_agents)
            all_sheets[sheet] = sheet_content

        for s_name, op_sheet in pb.iter_bar(all_sheets.items(), key="sheet"):
            self.parse_sheet(all_sheets, s_name, start_row_index, pb=pb)

            with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
                all_sheets[s_name].sheet_obj.to_excel(writer, sheet_name=s_name, index=False)

# ee = excel_engine(local_model(), double_shape(), prompt_file_shape())
# ee.call_file("/Users/kejiang/Downloads/test.xlsx", start_row_index=1)
