# Copyright (C) 2023-2024 BlueLightAI, Inc. All Rights Reserved.
#
# Any use, distribution, or modification of this software is subject to the
# terms of the BlueLightAI Software License Agreement.

from typing import Optional

import ipyvuetify as v

from cobalt.config import handle_cb_exceptions
from cobalt.event_bus import EventBusController
from cobalt.groups.groups_ui import GroupDisplay, GroupSaveButton
from cobalt.selection_details import SelectionDetails
from cobalt.selection_manager import SelectionManager
from cobalt.state import State
from cobalt.visualization import EmbeddingVisualization


class UserGroups(v.Flex):
    def __init__(
        self,
        dataselector: SelectionManager,
        visualization: EmbeddingVisualization,
        state: State,
        num_of_failure_groups: Optional[int] = 0,
    ):
        self.state = state
        self.dataselector = dataselector
        self.visualization = visualization
        self.num_of_failure_groups = num_of_failure_groups

        self.selection_details = SelectionDetails(self.dataselector, self.state)
        self.number_of_points = self.selection_details.number_of_points
        self.selection_details.update_details_from_graph(
            self.dataselector.graph_selection
        )

        self.bind_selection_details()

        self.number_of_groups = v.Text(children="")

        self.group_display = GroupDisplay(dataselector, visualization, state)
        group_event_bus = EventBusController.get_group_event_bus(
            self.state.workspace_id
        )

        group_event_bus.add_callback(self.update_empty_state)
        group_event_bus.add_callback(self.visualization.update_data_source_options)
        self.group_display.set_update_callback(self.update_empty_state)
        self.group_display.set_update_callback(
            self.visualization.update_data_source_options
        )

        self.save_button = GroupSaveButton(
            self.dataselector, self.state, group_display=self.group_display
        )

        self.groups_header = v.Flex(
            children=[
                v.Text(
                    children="Data groups",
                    class_="font-weight-bold",
                    style_="font-size: 16px",
                ),
                self.save_button,
            ],
            class_="d-flex justify-space-between align-center pa-4",
            style_="width: 100%;",
        )

        self.title = v.Text(
            children=[
                self.number_of_groups,
                v.Text(
                    children="Saved Groups",
                ),
            ],
            class_="pt-4 px-4 text-uppercase",
            style_="font-size: 14px;",
        )

        self.list_box = v.List(
            dense=True,
            children=[self.group_display.list_item_group],
            class_="overflow-y-auto",
        )

        self.empty_state_groups_container = v.Flex(
            children=[
                v.Text(
                    children="No groups",
                    style_="font-size: 20px;",
                    class_="font-weight-medium",
                ),
                v.Text(
                    children="To create a new group, make a selection in the graph.",
                    class_="pt-4",
                ),
            ],
            class_="d-flex align-center flex-column pt-9",
        )

        self.user_groups_layout = v.Layout(
            children=[],
            class_="flex-column",
            style_="max-height: 400px;",
            v_model=False,
        )

        self.update_empty_state()

        super().__init__(
            children=[
                self.groups_header,
                v.Divider(),
                self.user_groups_layout,
            ],
        )

    def on_selection_source_change(self, source):
        if source != "Graph":
            self.save_button.disabled = True
        else:
            self.save_button.disabled = False

    def bind_selection_details(self):
        self.selection_details = SelectionDetails(
            self.dataselector, self.state, self.on_selection_source_change
        )

    @handle_cb_exceptions
    def update_empty_state(self):
        groups = self.state.get_groups()
        num_saved_groups = len(groups)
        self.number_of_groups.children = str(num_saved_groups)

        groups_title = "Saved Group" if num_saved_groups == 1 else "Saved Groups"
        self.title.children = [
            self.number_of_groups,
            v.Text(children=f" {groups_title}"),
        ]

        if num_saved_groups == 0 and self.num_of_failure_groups == 0:
            self.user_groups_layout.children = [self.empty_state_groups_container]
        elif num_saved_groups > 0:
            self.user_groups_layout.children = [
                self.title,
                self.list_box,
            ]
        else:
            self.user_groups_layout.children = []

        self.user_groups_layout.v_model = True
        self.selection_details.update_details_from_graph(
            self.dataselector.graph_selection
        )
