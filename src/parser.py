"""Command parsing for the CSV query engine."""
import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class ParsedCommand:
    command: str
    args: dict

COMMANDS = {
    "LOAD","SHOW","HEAD","TAIL","COLUMNS","FILTER","SEARCH","SORT","SELECT",
    "UNIQUE","COUNT","SUMMARY","GROUPBY","TOP","EXPORT","RESET","CLEAR","HELP","EXIT"
}

def parse_command(line: str) -> ParsedCommand:
    line=line.strip()
    if not line:
        raise ValueError("Empty command.")
    parts=line.split()
    command=parts[0].upper()
    if command not in COMMANDS:
        raise ValueError("Unknown command. Type HELP to see available commands.")
    if command in {"SHOW","COLUMNS","RESET","CLEAR","HELP","EXIT"}:
        if len(parts)!=1: raise ValueError(f"{command} does not take arguments.")
        return ParsedCommand(command,{})
    if command in {"LOAD","EXPORT"}:
        if len(parts)!=2: raise ValueError(f"Usage: {command} <file>")
        return ParsedCommand(command,{"file":parts[1]})
    if command in {"HEAD","TAIL","TOP"}:
        if len(parts)!=2 and command!="TOP" or (command=="TOP" and len(parts)!=3):
            raise ValueError(f"Usage: {command} {'<number>' if command!='TOP' else '<number> <column>'}")
        if command=="TOP": return ParsedCommand(command,{"number":parts[1],"column":parts[2]})
        return ParsedCommand(command,{"number":parts[1]})
    if command=="FILTER":
        m=re.match(r'^\s*FILTER\s+(\S+)\s+(>=|<=|==|!=|>|<)\s+(.+?)\s*$',line,re.I)
        if not m: raise ValueError("Usage: FILTER <column> <operator> <value>")
        return ParsedCommand(command,{"column":m.group(1),"operator":m.group(2),"value":m.group(3).strip()})
    if command=="SEARCH":
        m=re.match(r'^\s*SEARCH\s+(\S+)\s*=\s*(.+?)\s*$',line,re.I)
        if not m: raise ValueError("Usage: SEARCH <column> = <value>")
        return ParsedCommand(command,{"column":m.group(1),"value":m.group(2).strip()})
    if command=="SORT":
        if len(parts) not in (2,3): raise ValueError("Usage: SORT <column> [ASC|DESC]")
        order=parts[2].upper() if len(parts)==3 else "ASC"
        if order not in {"ASC","DESC"}: raise ValueError("Sort order must be ASC or DESC.")
        return ParsedCommand(command,{"column":parts[1],"order":order})
    if command=="SELECT":
        cols=line[len("SELECT"):].strip()
        if not cols: raise ValueError("Usage: SELECT <column1>, <column2>, ...")
        return ParsedCommand(command,{"columns":[c.strip() for c in cols.split(",") if c.strip()]})
    if command=="UNIQUE":
        if len(parts)!=2: raise ValueError("Usage: UNIQUE <column>")
        return ParsedCommand(command,{"column":parts[1]})
    if command=="COUNT":
        if len(parts)>2: raise ValueError("Usage: COUNT [column]")
        return ParsedCommand(command,{"column":parts[1] if len(parts)==2 else None})
    if command=="SUMMARY":
        if len(parts)!=2: raise ValueError("Usage: SUMMARY <column>")
        return ParsedCommand(command,{"column":parts[1]})
    if command=="GROUPBY":
        if len(parts) not in (3,4): raise ValueError("Usage: GROUPBY <column> <operation> [target_column]")
        op=parts[2].upper()
        if op not in {"SUM","AVG","COUNT","MIN","MAX"}: raise ValueError("GROUPBY operation must be SUM, AVG, COUNT, MIN, or MAX.")
        return ParsedCommand(command,{"column":parts[1],"operation":op,"target_column":parts[3] if len(parts)==4 else None})
    raise ValueError("Invalid command.")
