from sheets_tools import create_spreadsheet, read_range, update_range

def main():
    # sheet = create_spreadsheet("Tabula Test")

    # print(sheet)

    SPREADSHEET_ID = "19aNDs4yLdmDgQ2u49DJlDOFUf8aZ0H8t59QmcUvhtcQ"

    data = read_range(
        spreadsheet_id=SPREADSHEET_ID,
        range_name="A1:Z100"
    )

    print(data)

    updated_data = update_range(
        spreadsheet_id=SPREADSHEET_ID,
        range_name="A1:B3",
        values=[
            ["Name", "Revenue"],
            ["Harsh", 1000],
            ["John", 2000]
        ]
    )

    print(updated_data)

if __name__ == "__main__":
    main()