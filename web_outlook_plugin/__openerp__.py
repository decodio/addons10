{
    'name': "Outlook plugin",
    'version': '8.0.0.1.5',
    'author': 'Decodio',
    'category': 'Project',
    'website': '',
    'sequence': 1,
    'description': """
Install as server-wide component!

Use:
/web_outlook_plugin/<db>/Manifest.xml
as URL for Outlook manifest.


 License: MIT

    """,
    'depends': ['base', 'web', 'crm', 'web_oauth_o365'],
    'qweb': [],
    'data': ['views/TaskPane.xml', 'views/Home.xml', 'views/Manifest.xml'],
}
