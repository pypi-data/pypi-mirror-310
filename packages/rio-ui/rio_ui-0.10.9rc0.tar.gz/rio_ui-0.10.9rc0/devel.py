import imy.inject

imy.inject.clear()


import qtpy
import gc
import random
import asyncio
import numpy as np
from pathlib import Path
import pandas as pd
import fastapi
import rio.docs
import plotly
import json
import rio
import rio.components.class_container
import rio.data_models
import rio.debug
import rio.debug.dev_tools
import rio.debug.dev_tools.dev_tools_connector
import rio.debug.dev_tools.icons_page
import rio.debug.dev_tools.layout_display
from datetime import datetime
import rio.debug.layouter


class TableRoot(rio.Component):
    async def _on_refresh(self) -> None:
        await self.force_refresh()

    def build(self) -> rio.Component:
        data_df = pd.DataFrame(
            {
                "Text": ["A", "B", "C", "D", "E"],
                "Ones": [1, 2, 3, 4, 5],
                "Tens": [10, 20, 30, 40, 50],
                "Hundreds": [100, 200, 300, 400, 500],
                "Foos": ["Foo", "Bar", "Baz", "Qux", "Quux"],
                "Randoms": [random.randint(1, 6) for ii in range(5)],
            }
        )

        data_np = np.random.rand(5, 3)

        return rio.Column(
            rio.Table(
                data_np,
                show_row_numbers=False,
            ),
            rio.Table(
                data_np,
                show_row_numbers=True,
            ),
            rio.Table(
                data_df,
                show_row_numbers=False,
            )["header", :].style(
                font_weight="normal",
            ),
            rio.Table(
                data_df,
                show_row_numbers=True,
            )[1:3, 2:4].style(
                font_weight="bold",
            ),
            rio.Button(
                "Refresh",
                icon="refresh",
                on_press=self._on_refresh,
            ),
            spacing=1,
            align_x=0.5,
            align_y=0.5,
        )


class MyRoot(rio.Component):
    foo: bool = False

    def build(self) -> rio.Component:
        min_width = 0
        min_height = 0

        return rio.Column(
            rio.FilePickerArea(
                content=None,
                files=[
                    rio.FileInfo(
                        name="File.txt",
                        size_in_bytes=0,
                        media_type="text/plain",
                        contents=bytes(),
                    ),
                    rio.FileInfo(
                        name="Super Duper Long Filename.mp3",
                        size_in_bytes=0,
                        media_type="audio/mpeg",
                        contents=bytes(),
                    ),
                    rio.FileInfo(
                        name="Multi.zip",
                        size_in_bytes=0,
                        media_type="application/zip",
                        contents=bytes(),
                    ),
                ],
                multiple=True,
                on_choose_file=lambda files: print(f"PICKED: {files}"),
                min_height=min_height,
            ),
            rio.FilePickerArea(
                content="Foobar",
                files=[
                    rio.FileInfo(
                        name="File.txt",
                        size_in_bytes=0,
                        media_type="text/plain",
                        contents=bytes(),
                    ),
                ],
                min_height=min_height,
            ),
            rio.FilePickerArea(
                content=rio.Text(
                    "Foobar",
                    justify="center",
                    margin=2,
                ),
                files=[
                    rio.FileInfo(
                        name="File.txt",
                        size_in_bytes=0,
                        media_type="text/plain",
                        contents=bytes(),
                    ),
                ],
                min_height=min_height,
            ),
            rio.Switch(
                is_on=self.bind().foo,
            ),
            rio.Link(
                "Text Content" if self.foo else rio.Button("Custom Content"),
                icon="material/castle",
                target_url=rio.URL("https://www.google.com"),
                # align_x=1,
            ),
            min_width=min_width,
            spacing=2,
            align_x=0.5,
            align_y=0.5,
        )

        return rio.Rectangle(
            fill=rio.ImageFill(
                # image=rio.URL("https://picsum.photos/id/237/200/300"),
                image=Path.home() / "patt.svg",
                fill_mode="tile",
                tile_size=(1, 3),
            )
        )

        return rio.GraphEditor(
            rio.Text(
                "foo",
            ),
            rio.NodeOutput(
                "Out 1",
                rio.Color.GREEN,
                key="out_1",
            ),
            rio.Column(
                rio.NodeInput(
                    "In 1",
                    rio.Color.BLUE,
                    key="in_1",
                ),
                rio.Button(
                    "Button",
                    style="plain-text",
                ),
                rio.NodeOutput(
                    "Out 2",
                    rio.Color.BLUE,
                    key="out_2",
                ),
                spacing=0.5,
            ),
            rio.NodeInput(
                "In 2",
                rio.Color.YELLOW,
                key="in_2",
                margin_top=5,
            ),
            margin_left=5,
            margin_top=5,
        )

        # Prepare the component that will be displayed in the current tab
        if self.selected_tab == "Tab 1":
            tab_content = rio.Text(
                "Tab 1",
                justify="center",
            )
        elif self.selected_tab == "Tab 2":
            tab_content = rio.Text(
                "Tab 2",
                justify="center",
            )
        else:
            tab_content = rio.Text(
                "Tab 3",
                justify="center",
            )

        # Build the UI
        return rio.Column(
            # This component will allow the user to switch between tabs
            rio.SwitcherBar(
                values=["Tab 1", "Tab 2", "Tab 3"],
                # By binding the SwitcherBar's value to this components value,
                # it will be automatically updated when the user switches tab
                selected_value=self.bind().selected_tab,
                align_x=0.5,
            ),
            # This will display the tab content. We want to make sure it takes
            # up as much space as possible, so make sure to set it to grow
            # vertically.
            #
            # We'll also use a `rio.Switcher`. This component will transition
            # smoothly between the content when it changes.
            rio.Switcher(
                tab_content,
                grow_y=True,
            ),
            # Leave some spacing between the components
            spacing=1,
            margin=1,
        )


class Upload(rio.Component):
    async def _on_press(self):
        # await self.call_event_handler(self.on_press)
        await self.session.pick_file()

    def build(self) -> rio.Component:
        return rio.Column(
            rio.MediaPlayer(
                Path("/mnt/nas/general/Videos/Movies/Summer Wars.mp4"),
                grow_y=True,
            ),
            rio.Button(
                "File upload",
                on_press=self._on_press,
                align_x=0.5,
                margin=1,
            ),
            # align_y=0.5,
        )


app = rio.App(
    build=MyRoot,
    # build=Upload,
    theme=rio.Theme.from_colors(mode="dark"),
    default_attachments=[],
)

# app.run_in_window()
