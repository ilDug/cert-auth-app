# from sys import exc_info
# from fastapi import HTTPException
# from mysql import connector
# from mysql.connector import connection, errorcode
# from dataclasses import asdict, dataclass


# class DbConnector:
#     """imposta la connessione alla creazione dell'istanza"""

#     connection: connector.MySQLConnection
#     cursor: connector.connection.MySQLCursor

#     @property
#     def items(self):
#         return self._cursor, self.connection

#     def __init__(
#         self, host, user, password, database=None, prepared: bool = True
#     ) -> None:
#         try:
#             self.connection = connector.connect(
#                 host=host, user=user, password=password, database=database
#             )
#             self.cursor = self.connection.cursor(prepared=prepared)
#         except Exception as e:
#             raise HTTPException(500, "errore di connessione al database: " + str(e))

#     def __enter__(self):
#         return self.cursor, self.connection, self
#         pass

#     def __exit__(self, exc_type, exc_value, tb):
#         try:
#             self.close_connection()
#             if exc_type is not None:
#                 return False  # uncomment to pass exc through
#             return True
#         except Exception as e:
#             raise HTTPException(500, str(e))

#     def close_connection(self) -> None:
#         """chiude la connessione ed il cursore"""
#         self.cursor.close()
#         self.connection.close()

#     def set(
#         self,
#         sql,
#         data,
#     ):
#         try:
#             self.cursor.execute(sql, data)
#             self.cursor.fetchall()
#             return self.cursor.rowcount > 0
#         except Exception as err:
#             print("Something went wrong: {}".format(err))
#             raise HTTPException(500, "DATABASE ERROR: " + str(err))

#     def get(self, sql, data: tuple, asdict=True, aslist=False):
#         try:
#             self.cursor.execute(sql, data)
#             results = []
#             for row in self.cursor:
#                 row = list(row)
#                 if asdict:
#                     row = dict(zip(self.cursor.column_names, row))
#                     print(row)
#                 results.append(row)
#             if aslist:
#                 return results
#             else:
#                 if len(results) == 0:
#                     return print(results)
#                 return results if len(results) > 1 else results[0]

#         except Exception as err:
#             print("Something went wrong: {}".format(err))
#             raise HTTPException(500, "DATABASE ERROR: " + str(err))
