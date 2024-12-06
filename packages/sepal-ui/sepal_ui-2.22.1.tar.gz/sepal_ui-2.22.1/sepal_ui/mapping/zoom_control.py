"""Customized ``Control`` to zoom in and out on the map."""
from typing import Optional

from ipyleaflet import Map, WidgetControl

from sepal_ui import sepalwidgets as sw
from sepal_ui.mapping.map_btn import MapBtn


class ZoomControl(WidgetControl):

    plus: Optional[MapBtn] = None
    "The plus btn"

    minus: Optional[MapBtn] = None
    "the minus btn"

    m: Optional[Map] = None
    "the map to manipulate"

    def __init__(self, m: Map, **kwargs) -> None:
        """Customized ``Control`` to zoom in and out on the map.

        Replace the built-in zoom control of ipyleaflet to match the theme of sepal-ui based applications. It is by default positioned in the top-right corner

        Args:
            m: the map to manipulate
            kwargs: any ``ipyleaflet.widgetControl`` arguments
        """
        # init the map
        self.m = m

        # create the 2 btns
        self.plus = MapBtn("fa-solid fa-plus", attributes={"data-step": 1})
        self.minus = MapBtn("fa-solid fa-minus", attributes={"data-step": -1})

        # customize their layout by removing the bottom radius
        self.plus.class_list.add("v-zoom-plus")
        self.minus.class_list.add("v-zoom-minus")

        # aggregate them in a layout
        content = sw.Layout(column=True, children=[self.plus, self.minus])

        # by default Zoomcontrols will be displayed in the topright corner
        kwargs.setdefault("position", "topright")
        kwargs["widget"] = content

        super().__init__(**kwargs)

        # add js behaviour
        self.plus.on_event("click", self.zoom)
        self.minus.on_event("click", self.zoom)

    def zoom(self, widget: MapBtn, *args) -> None:
        """update the zoom according to the clicked btn."""
        # read min and max zoom
        max_zoom = self.m.max_zoom or 24
        min_zoom = self.m.min_zoom or 0

        # computed zoom
        zoom = self.m.zoom + widget.attributes["data-step"]

        # adapt to the limitations of the map
        self.m.zoom = max(min(zoom, max_zoom), min_zoom)

        return
