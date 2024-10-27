import streamlit as st
from sqlalchemy import create_engine, text as sql_text
import pandas as pd

FETCH_QUERY = "SELECT * from items WHERE deleted = FALSE ORDER BY creation_time DESC;"
INSERT_QUERY = 'INSERT INTO `items` (`id`, `creation_time`, `deleted`, `name`, `text`) VALUES (NULL, CURRENT_TIMESTAMP, FALSE, :name, :text);'
DELETE_QUERY = 'UPDATE `items` SET deleted = TRUE WHERE id = :id;'

class Database:
    def __init__(self):
        user = st.secrets["connections"]["mysql"]["username"]
        database = st.secrets["connections"]["mysql"]["database"]
        password = st.secrets["connections"]["mysql"]["password"]
        host = st.secrets["connections"]["mysql"]["host"]

        self.engine = create_engine(
            f"mysql+pymysql://{user}:{password}@{host}/{database}"
        )

    def _read(self, query, params=None):
        with self.engine.connect() as connection:
            return pd.read_sql(query, connection, params=params)
        
    def _query(self, query, params=None):
        with self.engine.connect() as connection:
            connection.execute(sql_text(query), params)
            connection.commit()

    def get_items(self):
        return self._read(FETCH_QUERY)
    
    def add_item(self, name, text):
        self._query(INSERT_QUERY, params={"name": name, "text": text})

    def delete_item(self, id):
        self._query(DELETE_QUERY, params={"id": id})