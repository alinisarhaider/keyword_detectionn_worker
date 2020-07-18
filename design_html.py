from datetime import datetime, timedelta
import math


def create_results_html(detections: dict):
    data = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Results</title><link href='https://fonts.googleapis.com/css?family=Pacifico' rel='stylesheet' type='text/css'><link href='https://fonts.googleapis.com/css?family=Arimo' rel='stylesheet' type='text/css'><link href='https://fonts.googleapis.com/css?family=Hind:300' rel='stylesheet' type='text/css'><link href='https://fonts.googleapis.com/css?family=Open+Sans+Condensed:300' rel='stylesheet' type='text/css'>"
    data += "<link type='text/css' rel='stylesheet' href='{{ url_for("
    data += '"static", filename="./style.css") }}'
    data += "'>"
    data += "</head><body style='overflow:auto'><div><center><table border=1><tr style='text-align:left'><th>Keyword</th><th>Occurrence time in video (Min:Sec)</th></tr>"

    for key, value in detections.items():
        if len(value) == 0:
            data += f"<tr><td>{key}</td><td> Not Found </td></tr>"
        elif len(value) == 1:
            d = datetime(1, 1, 1) + timedelta(seconds=math.ceil(value[0]))
            data += f"<tr><td>{key}</td><td>{d.minute}:{d.second}</td></tr>"
        else:
            data += f"<tr><td rowspan='{len(value) + 1}'>{key}</td></tr>"
            for i in value:
                d = datetime(1, 1, 1) + timedelta(seconds=math.ceil(i))
                data += f"<tr><td>{d.minute}:{d.second}</td></tr>"

    data += "</table></center><br><a style='color: rgba(255, 99, 71, 0.7)' href='{{ url_for("
    data += '"home")}}'
    data += "'>"
    data += 'Home</a><br><br></div></body></html>'
    return data


def create_error_html(error_statement):
    data = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Error</title><link href='https://fonts.googleapis.com/css?family=Pacifico' rel='stylesheet' type='text/css'><link href='https://fonts.googleapis.com/css?family=Arimo' rel='stylesheet' type='text/css'><link href='https://fonts.googleapis.com/css?family=Hind:300' rel='stylesheet' type='text/css'><link href='https://fonts.googleapis.com/css?family=Open+Sans+Condensed:300' rel='stylesheet' type='text/css'>"
    data += "<link type='text/css' rel='stylesheet' href='{{ url_for("
    data += '"static", filename="./style.css") }}'
    data += "'>"
    data += "</head><body><div  class='waiting_screen'><text style='font-size:23px'>"
    data += f'{error_statement}'
    data += "</text><a style='color: rgba(255, 99, 71, 0.7)' href='{{ url_for("
    data += '"home")}}'
    data += "'>Home</a></div></body></html>"
    return data
