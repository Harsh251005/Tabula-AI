from sheets_tools import create_spreadsheet, read_range

def main():
    # sheet = create_spreadsheet("Tabula Test")

    # print(sheet)

    data = read_range(
        spreadsheet_id="19aNDs4yLdmDgQ2u49DJlDOFUf8aZ0H8t59QmcUvhtcQ",
        range_name="A1:Z100"
    )

    print(data)

if __name__ == "__main__":
    main()