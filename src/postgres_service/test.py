import gspread

gc = gspread.oauth(
    credentials_filename='/Users/cursebow/.config/gspread/credentials.json',
    authorized_user_filename='/Users/cursebow/.config/gspread/authorized_user.json'
)

def get_and_convert_data():
    sh = gc.open("table_1")
    worksheet = sh.sheet1
    worksheet.pop(0)


# class BoardGame(SQLModel, table=True):
#     id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
#     gameName: str
#     minPlayers: int
#     maxPlayers: int
#     minIdealPlayers: int
#     maxIdealPlayers: int
#     minPlayTime: int
#     maxPlayTime: int
#     ruleTime: int
#     gameComplexity: str
#     minAge: int
#     year: int
#     gameShortDescription: str
#     gameFullDescription: str
#     coverImageLink: str
#     videoRulesLink: str
#     genre: str
#     status: str


    all_values = worksheet.get_all_values()

    for row in all_values:
        print(row)