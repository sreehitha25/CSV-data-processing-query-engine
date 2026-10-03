from src.parser import parse_command
from src.executor import QueryEngine
from src.formatter import format_table

HELP="""Available commands:
LOAD <file>                         Load a CSV file
SHOW                                Show all loaded rows
HEAD [number]                       Show first rows
TAIL [number]                       Show last rows
COLUMNS                             Show column names
FILTER <column> <operator> <value> Filter rows
SEARCH <column> = <value>           Find exact text matches
SORT <column> [ASC|DESC]            Sort rows
SELECT <column1>, <column2>, ...    Select columns
UNIQUE <column>                     Show unique values
COUNT [column]                      Count rows or non-empty values
SUMMARY <column>                    Show numeric summary
GROUPBY <column> <operation> [...]  Group and aggregate
TOP <number> <column>               Show largest values
EXPORT <file>                       Export the current result
RESET                               Clear loaded data
CLEAR                               Clear the screen
HELP                                Show this help
EXIT                                Quit"""

def main():
    engine=QueryEngine()
    last_result=None
    print("CSV Data Processing Query Engine")
    print("--------------------------------")
    print("Type HELP for commands.")
    while True:
        try: line=input("query> ")
        except (EOFError,KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not line.strip(): continue
        try:
            parsed=parse_command(line)
            if parsed.command=="HELP":
                print(HELP); continue
            if parsed.command=="EXIT":
                print("Goodbye!"); break
            if parsed.command=="CLEAR":
                print("\033[2J\033[H",end=""); continue
            if parsed.command=="EXPORT":
                if last_result is None: raise ValueError("Nothing to export. Run a data command first.")
                last_result.to_csv(parsed.args["file"],index=False)
                print(f"Exported successfully to {parsed.args['file']}")
                continue
            result=engine.execute(parsed)
            last_result=result if hasattr(result,"to_csv") else None
            if result is not None: print(format_table(result))
        except (ValueError,FileNotFoundError) as exc:
            print(f"Error: {exc}")

if __name__=="__main__":
    main()
