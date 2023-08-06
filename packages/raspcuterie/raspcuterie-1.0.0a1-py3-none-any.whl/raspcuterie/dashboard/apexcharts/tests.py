from raspcuterie.dashboard.apexcharts import ChartObject, YAxis


def test_chart_object():

    x = ChartObject()
    x.title.text = "MyGraph"
    x.chart.id = "MyGraphID"

    x.stroke.curve.append("smooth")
    x.stroke.curve.append("stepline")

    x.markers.size.append(0)
    x.markers.size.append(2)
    x.markers.size.append(2)
    x.yaxis.append(
        YAxis(tickAmount=4, max=4, min=0, serieName="Pinda", opposite=False, show=True)
    )

    assert len(x.stroke.curve) == 2

    t = x.json()
    print(t)

    assert t
