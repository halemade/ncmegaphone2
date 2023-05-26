from dash import Dash, dcc, html, Input, Output, State
import dash_design_kit as ddk
import dash_mantine_components as dmc

app = Dash(__name__)
server = app.server  # expose server variable for Procfile

house = "https://www.ncleg.gov/Members/ContactInfo/H"
senate = "https://www.ncleg.gov/Members/ContactInfo/S"

sidebar = [
    ddk.CardHeader("Choose groups to email"),
    dcc.Checklist(
        id="bodies-of-legislature",
        value=["NC House", "NC Senate"],
        options=["NC House", "NC Senate"],
    ),
    dmc.Space(h=20),
    html.A(
        "NCGA Policy for emailing all legislators",
        href="http://www.ncleg.net/gascripts/Help/KnowledgeBase/viewItem.pl?nID=27",
        target="_blank",
    ),
]


app.layout = ddk.App(
    children=[
        ddk.Header(
            [
                ddk.Logo(src=app.get_asset_url("ncmegaphone-logo.png")),
                ddk.Title("NC Megaphone 2"),
            ]
        ),
        ddk.ControlCard(sidebar, width=30),
        ddk.Card(
            width=70,
            children=[
                ddk.CardHeader(dmc.Text("Please modify your message below.")),
                dmc.Space(h=12),
                dmc.Textarea(
                    label="Email Subject",
                    placeholder="Please refer to a bill number or issue in the subject of your email for best results.",
                    style={"width": 600},
                    spellCheck=True,
                    autosize=True,
                ),
                dmc.Textarea(
                    label="Email Body",
                    style={"width": 600},
                    spellCheck=True,
                    autosize=True,
                    value="""Dear Senator (or Representative) [last name]:
As your constituent, I write to urge your (support for/opposition) passage of [bill number], a bill introduced by Representative [member’s name], which would [describe what the bill would do and why]. 

Please advise me of the actions you intend to take with respect to this bill.

A concerned and active voter,
[your name]
                    """,
                ),
                dmc.Space(h=20),
                ddk.Row(
                    [
                        dmc.Button(
                            "Send with Gmail",
                            id="send-email",
                            variant="gradient",
                            gradient={"from": "indigo", "to": "cyan"},
                            radius="xl",
                        ),
                        html.Div(
                            id="email-sent",
                            style=dict(paddingLeft="15px", paddingTop="7px"),
                        ),
                    ]
                ),
            ],
        ),
    ],
    show_editor=True,
)


@app.callback(
    Output("email-sent", "children"),
    Input("send-email", "n_clicks"),
    State("bodies-of-legislature", "value"),
    prevent_initial_call=True,
)
def send_email(nclicks, selectedBodies):
    if len(selectedBodies) == 1:
        return f"Emails sent to the {selectedBodies[0]}! (not really, the google integration is in active development)"
    else:
        return f"Emails sent to the {selectedBodies[0]} and the {selectedBodies[1]}! (not really, the google integration is in active development)"


if __name__ == "__main__":
    app.run_server(debug=True)
