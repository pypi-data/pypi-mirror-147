from typing import Dict

from flask import Blueprint, current_app, render_template

from raspcuterie.config.schema import RaspcuterieConfigSchema
from raspcuterie.dashboard.apexcharts import ChartObject, YAxis, Label
from raspcuterie.devices import OutputDevice, InputDevice
from raspcuterie.devices.series import Series

bp = Blueprint("dashboard", __name__, template_folder="./templates")


@bp.route("/")
def dashboard():

    charts_json: Dict[str, str] = {}

    s: RaspcuterieConfigSchema = current_app.schema

    for name, schema in s.charts.items():
        obj = ChartObject()
        obj.title.text = schema.title
        obj.chart.id = name

        show = True
        group_series_name = None

        for series in schema.series:
            series_obj = Series.registry.get(series, None)

            if series_obj is None:
                raise Exception(f"{series} does not exists")

            if series_obj.type == "boolean":
                obj.stroke.curve.append("stepline")
                obj.markers.size.append(2)
                obj.yaxis.append(
                    YAxis(
                        # tickAmount=1,
                        opposite=True,
                        show=False,
                        min=-2,
                        max=1,
                        seriesName=series,
                        reversed=True,
                    )
                )
            elif series_obj.type == "integer":
                obj.markers.size.append(0)

                if group_series_name is None:
                    group_series_name = series

                obj.yaxis.append(
                    YAxis(
                        tickAmount=4,
                        opposite=False,
                        show=show,
                        labels=Label(minWidth=20),
                        # min=series_obj.min,
                        # max=series_obj.max,
                        seriesName=group_series_name,
                    )
                )
                obj.stroke.curve.append("smooth")
                show = False

        charts_json[name] = obj.json(exclude_none=True)

    return render_template(
        "dashboard.html",
        output_devices=OutputDevice.registry,
        input_devices=InputDevice.registry,
        charts=current_app.schema.charts,
        charts_json=charts_json,
        name=s.name,
    )
