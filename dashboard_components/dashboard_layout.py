from dash import html, dcc
import dash_bootstrap_components as dbc

email_input = dbc.Row([
        dbc.Label("Email"
                , html_for="email-row"
                , width=2),
        dbc.Col(dbc.Input(
                type="email"
                , id="email-row"
                , placeholder="Enter email"
            ),width=10,
        )],className="mb-3"
)
name_input = dbc.Row([
        dbc.Label("Name", html_for="name-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text"
                , id="name-row"
                , placeholder="Enter name"
                , maxLength = 80
            ),width=10
        )], className="mb-3"
)
message = dbc.Row([
        dbc.Label("Message"
         , html_for="message-row", width=2)
        ,dbc.Col(
            dbc.Textarea(id = "message-row"
                , className="mb-3"
                , placeholder="Enter message"
                , required = True)
            , width=10)
        ], className="mb-3")

contact_form = html.Div([ dbc.Container([
            html.H2("Want to learn more? We'd love to hear from you!"),
            dbc.Card(
                dbc.CardBody([
                     dbc.Form([name_input,email_input,message])
                ,html.Div(id = 'submit-div', children = [
                    dbc.Button('Submit'
                    , color = 'primary'
                    , id='button-submit'
                    , n_clicks=0)
                ]) 
                ])
            )
        ])
        ])

LAYOUT = html.Div([
    #hidden components
    dcc.Interval(id='update_interval',interval=30000),
    #header
    dbc.Row([
            dbc.Col([html.A(
                        href="https://www.tegnology.dk/",
                        children=html.Img(src='assets/logo.png',style={'width':'100%'}))],width=3),
            dbc.Col([html.H1(children='ABB Pressure Sensor IoT Demo')],width=9)],
            style={'padding':10}),
    #temperature graph
    dcc.Graph(id='temp-graph'),
    html.Div([
        dcc.Markdown('Number of data points:'),
        dcc.Input(id='n_points',type='number',value=100,debounce=True),
        dbc.Tooltip(id='npoints-tooltip',children='Input desired number of data points, then press enter to refresh graph.',target='n_points'),
        dbc.Button(html.I(className="fa fa-download") ,id='download-button',n_clicks=0,color='secondary'),
        dcc.Download(id='data-download')],className ="d-grid gap-2 d-md-flex",style={'padding':10}),
    dbc.Row([
        dcc.Markdown(id='last-updated',style={'padding':10,'font-size':'10px'}),
    ],style={'padding':10}),
    dbc.Row([
        dbc.Col([html.Img(src='assets/setup.png',style={'width':'100%'})],width=4),
        dbc.Col([dcc.Markdown(children=open('assets/graph_description.md').read())],width=8)],
        style={'padding':10}),
    contact_form
])

