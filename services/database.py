import pandas as pd
import pyodbc
import time
from services.config import logger
from typing import List, Optional, Tuple

_CONN_STR = (
    "DRIVER={SQL Server};"
    "SERVER=172.16.0.239;"
    "DATABASE=SFI_DWH;"
    "UID=usersfi;"
    "PWD=sfi.100;"
)

_SP_REPPO = "[dbo].[SFIBI_RPT_PICKUP_ZEUS]"
_SP_MOBCOLL = (
    "[SFISVRDBMCOLL].Mobile_collection.dbo.[SP_ARO_LOCATION_REPORT_EXCEL_AREA_2]"
)
_MOBCOLL_PARAM = "'1502'"


def get_database_connection() -> Optional[pyodbc.Connection]:
    logger.info(
        "[DATABASE] INITIATING CONNECTION TO SQL SERVER -> 172.16.0.239 / SFI_DWH"
    )
    t0 = time.perf_counter()
    try:
        conn = pyodbc.connect(_CONN_STR, timeout=30)
        logger.info(
            f"[DATABASE] CONNECTION ESTABLISHED IN {time.perf_counter() - t0:.3f}s"
        )
        return conn
    except pyodbc.Error as e:
        logger.error(f"[DATABASE] CONNECTION FAILED : {e}")
        return None


def _run_query(
    sql: str,
    label: str,
    conn: Optional[pyodbc.Connection] = None,
) -> Tuple[Optional[List[str]], Optional[list]]:
    t0 = time.perf_counter()
    logger.info(f"[DATABASE] EXECUTING -> {label}")

    _shared_conn = conn is not None

    try:
        target = conn if _shared_conn else pyodbc.connect(_CONN_STR, timeout=30)
        df = pd.read_sql(sql, target)
        if not _shared_conn:
            target.close()
        elapsed = time.perf_counter() - t0
        logger.info(
            f"[DATABASE] QUERY COMPLETE — {len(df):,} ROWS x {len(df.columns)} COLUMNS "
            f"FETCHED IN {elapsed:.3f}s"
        )
        return list(df.columns), [tuple(r) for r in df.itertuples(index=False)]
    except Exception as e1:
        logger.warning(
            f"[DATABASE] pandas.read_sql FAILED ({e1}) — trying autocommit cursor"
        )

    try:
        ac_conn = pyodbc.connect(_CONN_STR, autocommit=True, timeout=30)
        cursor = ac_conn.cursor()
        cursor.execute(sql)

        columns = None
        for _ in range(20):
            if cursor.description is not None:
                columns = [col[0] for col in cursor.description]
                break
            try:
                if not cursor.nextset():
                    break
            except Exception:
                break

        if columns is None:
            logger.error("[DATABASE] NO RESULT SET WITH COLUMN METADATA FOUND")
            cursor.close()
            ac_conn.close()
            return None, None

        rows = cursor.fetchall()
        cursor.close()
        ac_conn.close()

        elapsed = time.perf_counter() - t0
        logger.info(
            f"[DATABASE] QUERY COMPLETE (via autocommit) — "
            f"{len(rows):,} ROWS x {len(columns)} COLUMNS "
            f"FETCHED IN {elapsed:.3f}s"
        )
        return columns, rows

    except pyodbc.Error as e2:
        logger.error(f"[DATABASE] ALL STRATEGIES FAILED. LAST ERROR : {e2}")
        return None, None


def fetch_reppo_data(
    conn: pyodbc.Connection,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
) -> Tuple[Optional[List[str]], Optional[list]]:
    if date_from and date_to:
        sql = f"EXEC {_SP_REPPO} @DATEFROM='{date_from}', @DATETO='{date_to}'"
        label = f"{_SP_REPPO} @DATEFROM='{date_from}', @DATETO='{date_to}'"
    else:
        sql = f"EXEC {_SP_REPPO}"
        label = _SP_REPPO

    return _run_query(sql, label, conn=conn)


def fetch_mobcoll_data() -> Tuple[Optional[List[str]], Optional[list]]:
    sql = f"EXEC {_SP_MOBCOLL} {_MOBCOLL_PARAM}"
    label = f"{_SP_MOBCOLL} {_MOBCOLL_PARAM}"
    return _run_query(sql, label)
