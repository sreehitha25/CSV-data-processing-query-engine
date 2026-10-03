"""Execution logic for parsed CSV commands."""
import operator
import pandas as pd
from .loader import load_csv
from .utils import require_number, get_column

class QueryEngine:
    def __init__(self):
        self.data=None
        self.current_file=None

    def _need_data(self):
        if self.data is None: raise ValueError("Please load a CSV file first.")

    def execute(self, parsed):
        cmd=parsed.command; a=parsed.args
        if cmd=="LOAD":
            self.data=load_csv(a["file"]); self.current_file=a["file"]
            return f"File loaded successfully.\nRows: {len(self.data)}\nColumns: {len(self.data.columns)}"
        if cmd=="RESET":
            self.data=None; self.current_file=None; return "Data reset successfully."
        if cmd in {"CLEAR","HELP","EXIT"}: return None
        self._need_data()
        if cmd=="SHOW": return self.data
        if cmd=="HEAD": return self.data.head(require_number(a["number"]))
        if cmd=="TAIL": return self.data.tail(require_number(a["number"]))
        if cmd=="COLUMNS": return pd.DataFrame({"Column":self.data.columns})
        if cmd=="FILTER":
            get_column(self.data,a["column"])
            return self._filter(a["column"],a["operator"],a["value"])
        if cmd=="SEARCH":
            get_column(self.data,a["column"])
            return self.data[self.data[a["column"]].astype(str).str.lower()==a["value"].lower()].copy()
        if cmd=="SORT":
            get_column(self.data,a["column"])
            return self.data.sort_values(a["column"],ascending=a["order"]=="ASC",kind="stable").reset_index(drop=True)
        if cmd=="SELECT":
            for c in a["columns"]: get_column(self.data,c)
            return self.data[a["columns"]].copy()
        if cmd=="UNIQUE":
            get_column(self.data,a["column"])
            return pd.DataFrame({a["column"]:self.data[a["column"]].drop_duplicates().reset_index(drop=True)})
        if cmd=="COUNT":
            if a["column"]: get_column(self.data,a["column"]); return int(self.data[a["column"]].count())
            return int(len(self.data))
        if cmd=="SUMMARY":
            get_column(self.data,a["column"])
            series=pd.to_numeric(self.data[a["column"]],errors="coerce")
            if series.notna().sum()==0: raise ValueError(f"Column '{a['column']}' must contain numeric values.")
            return series.describe().to_frame(name=a["column"])
        if cmd=="GROUPBY":
            get_column(self.data,a["column"])
            op=a["operation"]; target=a["target_column"]
            if op=="COUNT":
                if target: get_column(self.data,target)
                return self.data.groupby(a["column"],dropna=False).size().reset_index(name="COUNT")
            if not target:
                raise ValueError(f"GROUPBY {op} requires a target column.")
            get_column(self.data,target)
            series=pd.to_numeric(self.data[target],errors="coerce")
            if series.notna().sum()==0: raise ValueError(f"Target column '{target}' must be numeric for {op}.")
            temp=self.data.copy(); temp[target]=series
            result=getattr(temp.groupby(a["column"],dropna=False)[target], {"AVG":"mean","SUM":"sum","MIN":"min","MAX":"max"}[op])().reset_index()
            result=result.rename(columns={target:op})
            return result
        if cmd=="TOP":
            get_column(self.data,a["column"])
            n=require_number(a["number"])
            numeric=pd.to_numeric(self.data[a["column"]],errors="coerce")
            if numeric.notna().sum()==0: raise ValueError(f"Column '{a['column']}' must contain numeric values.")
            return self.data.assign(_sort=numeric).nlargest(n,"_sort").drop(columns="_sort")
        raise ValueError("Unsupported command.")

    def _filter(self,column,op,value):
        series=self.data[column]
        numeric=pd.to_numeric(series,errors="coerce")
        try:
            if numeric.notna().all() and value.replace(".","",1).replace("-","",1).isdigit():
                right=float(value); left=numeric
            else: left=series.astype(str); right=value
        except Exception: left=series.astype(str); right=value
        ops={">":operator.gt,"<":operator.lt,">=":operator.ge,"<=":operator.le,"==":operator.eq,"!=":operator.ne}
        return self.data[ops[op](left,right)].copy()
