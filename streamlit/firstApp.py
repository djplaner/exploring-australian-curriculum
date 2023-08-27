# Copyright (C) 2023 David Jones
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd

conn = st.experimental_connection('oz_curriculum_db', type="sql")

conn

st.markdown("# Main page")
st.sidebar.markdown("# Main page")

add_text = st.sidebar.text_input("Your name", key="name")

st.write("Hello " + st.session_state.name )
