from . import sqlt
from .sqlt import (
    establish_connection,
    collect_id_into_js,
    update_by_id,
)
import time
from .jobspec import example_js
from . import pgsql


def example_run_js_job(js: example_js) -> float:
    """
    example_run_js_job
    """
    v1 = js.val + 1
    v2 = js.val + 2
    return [v1, v2]


def truncated_output(lst, max_length_str=30):
    trunc_lst = []
    for i in lst:
        if isinstance(i, str) and len(i) > max_length_str:
            trunc_lst.append(i[:max_length_str] + "...")
        else:
            trunc_lst.append(i)
    return trunc_lst


def ms_sl_extra_info_pg(
    pgsql_op: pgsql.pgsql_operations,
    id_list=[0, 50],
    run_js_job=example_run_js_job,
    extra_info={},  # memory requirements should be set here
    js_obj=example_js,
    print_insertion=False,
):
    start = time.time()
    first = True
    conn, cur = pgsql_op.connect_db()
    for n, active_ind in enumerate(id_list):
        print(f"{active_ind=}, {n+1}/{len(id_list)}")
        js = pgsql_op.job_query(conn, active_ind, js_obj, extra_info)
        output = run_js_job(js)
        insertion_str = ""
        if print_insertion:
            tmp = truncated_output(output)
            insertion_str = f", output={tmp}"
        print(f"\nMAIN: id {active_ind} inserted{insertion_str}\n")
        pgsql_op.update(conn, output, active_ind)
    print((time.time() - start) / 60, "Minutes")
    print("COMPLETED MAIN")
    return


def ms_sl_extra_info(
    id_list=[0, 50],
    db_path="db/dimers_all.db",
    run_js_job=example_run_js_job,
    update_func=update_by_id,
    extra_info={},
    headers_sql=["main_id", "id", "RA", "RB", "ZA", "ZB", "TQA", "TQB"],
    js_obj=example_js,
    ppm="4gb",
    table_name="main",
    id_label="id",
    output_columns=[
        "env_multipole_A",
        "env_multipole_B",
        "vac_widths_A",
        "vac_widths_B",
        "vac_vol_rat_A",
        "vac_vol_rat_B",
    ],
    print_insertion=False,
):
    """
    To use ms_sl_serial_extra_info properly, write your own
    collect_rows_into_js_ls and collect_row_specific_into_js functions to pass
    as arguements to this function. Ensure that collect_rows_into_js_ls returns
    the correct js for your own run_js_job function.
    """

    start = time.time()
    con, cur = establish_connection(db_p=db_path)
    for n, active_ind in enumerate(id_list):
        js = collect_id_into_js(
            cur,
            mem=ppm,
            headers=headers_sql,
            extra_info=extra_info,
            dataclass_obj=js_obj,
            id_value=active_ind,
            id_label=id_label,
            table=table_name,
        )
        output = run_js_job(js)
        insertion_str = ""
        if print_insertion:
            tmp = truncated_output(output)
            insertion_str = f", output={tmp}"
        print(f"\nMAIN: id {active_ind} inserted{insertion_str}\n")
        update_func(
            con,
            cur,
            output,
            id_value=active_ind,
            id_label=id_label,
            table=table_name,
            output_columns=output_columns,
        )
    print((time.time() - start) / 60, "Minutes")
    print("COMPLETED MAIN")
    return

def ms_sl_serial(
    id_list=[0, 50],
    db_path="db/dimers_all.db",
    collect_id_into_js=collect_id_into_js,
    run_js_job=example_run_js_job,
    update_func=update_by_id,
    headers_sql=["main_id", "id", "RA", "RB", "ZA", "ZB", "TQA", "TQB"],
    level_theory=["hf/aug-cc-pV(D+d)Z"],
    js_obj=example_js,
    ppm="4gb",
    table="main",
    id_label="main_id",
    output_columns=[
        "env_multipole_A",
        "env_multipole_B",
        "vac_widths_A",
        "vac_widths_B",
        "vac_vol_rat_A",
        "vac_vol_rat_B",
    ],
):
    """
    To use ms_sl_serial properly, write your own collect_rows_into_js_ls and
    collect_row_specific_into_js functions to pass as arguements to this
    function. Ensure that collect_rows_into_js_ls returns the correct js for
    your own run_js_job function.

    This is designed to work with psi4 jobs using python api.
    """

    start = time.time()
    first = True
    con, cur = establish_connection(db_p=db_path)
    for n, active_ind in enumerate(id_list):
        js = collect_id_into_js(
            cur,
            mem=ppm,
            headers=headers_sql,
            extra_info=level_theory,
            dataclass_obj=js_obj,
            id_value=active_ind,
            id_label=id_label,
            table=table,
        )
        output = run_js_job(js)
        update_func(
            con,
            cur,
            output,
            id_label=id_label,
            id_value=active_ind,
            table=table,
            output_columns=output_columns,
        )
    print((time.time() - start) / 60, "Minutes")
    print("COMPLETED MAIN")
    return


def job_runner(
    id_list=[0, 50],
    db_path="db/schr.db",
    table_name="main",
    js_obj=example_js,
    headers_sql=["id", "RA", "RB", "ZA", "ZB", "TQA", "TQB"],
    run_js_job=example_run_js_job,
    extra_info=["sapt0/aug-cc-pV(D+d)Z"],
    ppm="4gb",
    id_label="id",
    output_columns=[
        "env_multipole_A",
        "env_multipole_B",
    ],
    # The user does not need to change the following unless desired
    collect_id_into_js=collect_id_into_js,
    update_func=update_by_id,
):
    """
    This is designed to work with psi4 jobs using python api.
    """

    start = time.time()
    first = True
    con, cur = establish_connection(db_p=db_path)
    for n, active_ind in enumerate(id_list):
        js = collect_id_into_js(
            cur,
            mem=ppm,
            headers=headers_sql,
            extra_info=extra_info,
            dataclass_obj=js_obj,
            id_value=active_ind,
            id_label=id_label,
            table=table_name,
        )
        output = run_js_job(js)
        update_func(
            con,
            cur,
            output,
            id_label=id_label,
            id_value=active_ind,
            table=table,
            output_columns=output_columns,
        )
    print((time.time() - start) / 60, "Minutes")
    print("COMPLETED MAIN")
    return


def job_runner_qcf(
    id_list=[0, 50],
    db_path="db/schr.db",
    table_name="main",
    js_obj=example_js,
    headers_sql=["id", "RA", "RB", "ZA", "ZB", "TQA", "TQB"],
    run_js_job=example_run_js_job,
    extra_info=["sapt0/aug-cc-pV(D+d)Z"],
    ppm="4gb",
    id_label="id",
    output_columns=[
        "env_multipole_A",
        "env_multipole_B",
    ],
    client_url="localhost:7778",
    # The user does not need to change the following unless desired
):
    from qcfractal.interface import FractalClient
    from qcfractal import FractalServer
    client = FractalClient(client_url, verify=False)

    start = time.time()
    first = True
    con, cur = establish_connection(db_p=db_path)
    for n, active_ind in enumerate(id_list):
        js = sqlt.collect_id_into_js(
            cur,
            headers_sql,
            ppm,
            extra_info,
            js_obj,
            active_ind,
            id_label,
            table_name,
            client,
        )
        output = run_js_job(js)
        update_by_id(
            con,
            cur,
            output,
            id_label=id_label,
            id_value=active_ind,
            table=table_name,
            output_columns=output_columns,
        )
    print((time.time() - start) / 60, "Minutes")
    print("COMPLETED MAIN")
    return
