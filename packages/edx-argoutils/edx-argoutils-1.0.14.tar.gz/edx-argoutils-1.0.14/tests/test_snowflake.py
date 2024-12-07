#!/usr/bin/env python

"""
Tests for Snowflake utils in the `edx_argoutils` package.
"""

import json

import mock
import pytest
from prefect.core import Flow
from prefect.engine import signals
from prefect.utilities.debug import raise_on_exception
from pytest_mock import mocker  # noqa: F401
from snowflake.connector import ProgrammingError

from edx_argoutils import snowflake


def test_qualified_table_name():
    assert 'test_db.test_schema.test_table' == snowflake.qualified_table_name(
        'test_db', 'test_schema', 'test_table'
    )


def test_qualified_stage_name():
    assert 'test_db.test_schema.test_table_stage' == snowflake.qualified_stage_name(
        'test_db', 'test_schema', 'test_table'
    )


@pytest.fixture
def mock_sf_connection(mocker):  # noqa: F811
    # Mock the Snowflake connection and cursor.
    mocker.patch.object(snowflake, 'create_snowflake_connection')
    mock_cursor = mocker.Mock()
    mock_connection = mocker.Mock()
    mock_connection.cursor.return_value = mock_cursor
    snowflake.create_snowflake_connection.return_value = mock_connection
    return mock_connection


def test_create_snowflake_connection(mocker):  # noqa: F811
    # Mock out the snowflake connection method w/o mocking out the helper method.
    mocker.patch.object(snowflake.snowflake.connector, 'connect')
    mock_cursor = mocker.Mock()
    mock_connection = mocker.Mock()
    mock_connection.cursor.return_value = mock_cursor
    snowflake.snowflake.connector.connect.return_value = mock_connection
    # Mock the key decryption.
    mocker.patch.object(snowflake.serialization, 'load_pem_private_key')
    mock_key = mocker.Mock()
    mock_key.private_bytes.return_value = 1234
    snowflake.serialization.load_pem_private_key.return_value = mock_key
    # Call the connection method.
    snowflake.create_snowflake_connection(
        credentials={
            "private_key": "this_is_an_encrypted_private_key",
            "private_key_passphrase": "passphrase_for_the_private_key",
            "user": "test_user",
            "account": "company-cloud-region"
        },
        role="test_role"
    )
    snowflake.snowflake.connector.connect.assert_called_with(
        account='company-cloud-region',
        autocommit=False,
        private_key=1234,
        user='test_user',
        warehouse=None,
        password=None,
    )
    mock_cursor.execute.assert_has_calls(
        (
            mocker.call("USE ROLE test_role"),
            mocker.call("ALTER SESSION SET TIMEZONE = 'UTC'"),
        )
    )


def test_load_json_objects_to_snowflake_no_existing_table(mock_sf_connection):
    # Mock the Snowflake connection, cursor, and fetchone method.
    mock_cursor = mock_sf_connection.cursor()
    mock_fetchone = mock.Mock(side_effect=ProgrammingError("does not exist"))
    mock_cursor.fetchone = mock_fetchone

    with Flow("test") as f:
        snowflake.load_ga_data_to_snowflake(
            sf_credentials={},
            sf_database="test_database",
            sf_schema="test_schema",
            sf_table="test_table",
            sf_role="test_role",
            sf_warehouse="test_warehouse",
            sf_storage_integration="test_storage_integration",
            bq_dataset="test_dataset",
            gcs_url="gs://test-location",
            date="2020-01-01",
        )
    state = f.run()
    assert state.is_successful()
    mock_cursor.execute.assert_has_calls(
        [
            mock.call("\n        SELECT 1 FROM test_database.test_schema.test_table\n        WHERE session:date='2020-01-01'\n            AND ga_view_id='test_dataset'\n        "), # noqa
            mock.call('\n        CREATE TABLE IF NOT EXISTS test_database.test_schema.test_table (\n            id number autoincrement start 1 increment 1,\n            load_time timestamp_ltz default current_timestamp(),\n            ga_view_id string,\n            session VARIANT\n        );\n        '), # noqa
            mock.call("\n        CREATE OR REPLACE STAGE test_database.test_schema.test_table_stage\n            URL = 'gcs://test-location'\n            STORAGE_INTEGRATION = test_storage_integration\n            FILE_FORMAT = (TYPE = JSON);\n        "), # noqa
            mock.call("\n        COPY INTO test_database.test_schema.test_table (ga_view_id, session)\n            FROM (\n                SELECT\n                    'test_dataset',\n                    t.$1\n                FROM @test_database.test_schema.test_table_stage t\n            )\n        PATTERN='.*'\n        FORCE=False\n        "), # noqa
        ]
    )


def test_load_json_objects_to_snowflake_error_on_table_exist_check(mock_sf_connection):
    # Mock the Snowflake connection, cursor, and fetchone method.
    mock_cursor = mock_sf_connection.cursor()
    mock_fetchone = mock.Mock(side_effect=ProgrammingError())
    mock_cursor.fetchone = mock_fetchone

    with Flow("test") as f:
        snowflake.load_ga_data_to_snowflake(
            sf_credentials={},
            sf_database="test_database",
            sf_schema="test_schema",
            sf_table="test_table",
            sf_role="test_role",
            sf_warehouse="test_warehouse",
            sf_storage_integration="test_storage_integration",
            bq_dataset="test_dataset",
            gcs_url="gs://test-location",
            date="2020-01-01",
        )
    with raise_on_exception():
        with pytest.raises(ProgrammingError):
            f.run()


def test_load_json_objects_to_snowflake_overwrite(mock_sf_connection):
    # Mock the Snowflake connection, cursor, and fetchone method.
    mock_cursor = mock_sf_connection.cursor()
    mock_fetchone = mock.Mock(return_value=None)
    mock_cursor.fetchone = mock_fetchone

    with Flow("test") as f:
        snowflake.load_ga_data_to_snowflake(
            sf_credentials={},
            sf_database="test_database",
            sf_schema="test_schema",
            sf_table="test_table",
            sf_role="test_role",
            sf_warehouse="test_warehouse",
            sf_storage_integration="test_storage_integration",
            bq_dataset="test_dataset",
            gcs_url="gs://test-location",
            date="2020-01-01",
            overwrite=True
        )
    state = f.run()
    assert state.is_successful()
    mock_cursor.execute.assert_has_calls(
        [
            mock.call("\n        SELECT 1 FROM test_database.test_schema.test_table\n        WHERE session:date='2020-01-01'\n            AND ga_view_id='test_dataset'\n        "), # noqa
            mock.call('\n        CREATE TABLE IF NOT EXISTS test_database.test_schema.test_table (\n            id number autoincrement start 1 increment 1,\n            load_time timestamp_ltz default current_timestamp(),\n            ga_view_id string,\n            session VARIANT\n        );\n        '), # noqa
            mock.call("\n            DELETE FROM test_database.test_schema.test_table\n            WHERE session:date='2020-01-01'\n                AND ga_view_id='test_dataset'\n            "), # noqa
            mock.call("\n        CREATE OR REPLACE STAGE test_database.test_schema.test_table_stage\n            URL = 'gcs://test-location'\n            STORAGE_INTEGRATION = test_storage_integration\n            FILE_FORMAT = (TYPE = JSON);\n        "), # noqa
            mock.call("\n        COPY INTO test_database.test_schema.test_table (ga_view_id, session)\n            FROM (\n                SELECT\n                    'test_dataset',\n                    t.$1\n                FROM @test_database.test_schema.test_table_stage t\n            )\n        PATTERN='.*'\n        FORCE=True\n        "), # noqa
        ]
    )


def test_load_json_objects_to_snowflake_table_exists_no_overwrite(mock_sf_connection):  # noqa: F811
    # Mock the Snowflake connection, cursor, and fetchone method.
    mock_cursor = mock_sf_connection.cursor()
    mock_fetchone = mock.Mock()
    mock_cursor.fetchone = mock_fetchone

    with Flow("test") as f:
        snowflake.load_ga_data_to_snowflake(
            sf_credentials={},
            sf_database="test_database",
            sf_schema="test_schema",
            sf_table="test_table",
            sf_role="test_role",
            sf_warehouse="test_warehouse",
            sf_storage_integration="test_storage_integration",
            bq_dataset="test_dataset",
            gcs_url="gs://test-location",
            date="2020-01-01",
        )
    state = f.run()
    assert state.is_successful()
    mock_cursor.execute.assert_called_once_with("\n        SELECT 1 FROM test_database.test_schema.test_table\n        WHERE session:date='2020-01-01'\n            AND ga_view_id='test_dataset'\n        ") # noqa


def test_load_json_objects_to_snowflake_table_general_exception(mock_sf_connection):
    # Mock the Snowflake connection, cursor, and fetchone method.
    mock_commit = mock.Mock(side_effect=Exception)
    mock_sf_connection.commit = mock_commit

    with Flow("test") as f:
        snowflake.load_ga_data_to_snowflake(
            sf_credentials={},
            sf_database="test_database",
            sf_schema="test_schema",
            sf_table="test_table",
            sf_role="test_role",
            sf_warehouse="test_warehouse",
            sf_storage_integration="test_storage_integration",
            bq_dataset="test_dataset",
            gcs_url="gs://test-location",
            date="2020-01-01",
            overwrite=True
        )
    with raise_on_exception():
        with pytest.raises(Exception):
            f.run()


def test_load_s3_data_to_snowflake_missing_parameters():
    task = snowflake.load_s3_data_to_snowflake
    with pytest.raises(signals.FAIL, match="Either `file` or `pattern` must be specified to run this task."):
        task.run(
            date="2020-01-01",
            date_property='date',
            sf_credentials={},
            sf_database="test_database",
            sf_schema="test_schema",
            sf_table="test_table",
            sf_role="test_role",
            sf_warehouse="test_warehouse",
            sf_storage_integration_name="test_storage_integration",
            s3_url="s3://edx-test/test/",
        )


def test_load_s3_data_to_snowflake_no_existing_table(mock_sf_connection):
    # Mock the Snowflake connection, cursor, and fetchone method.
    mock_cursor = mock_sf_connection.cursor()
    mock_fetchone = mock.Mock(side_effect=ProgrammingError("does not exist"))
    mock_cursor.fetchone = mock_fetchone

    task = snowflake.load_s3_data_to_snowflake
    task.run(
        date="2020-01-01",
        date_property='date',
        sf_credentials={},
        sf_database="test_database",
        sf_schema="test_schema",
        sf_table="test_table",
        sf_role="test_role",
        sf_warehouse="test_warehouse",
        sf_storage_integration_name="test_storage_integration",
        s3_url="s3://edx-test/test/",
        file="test_file.csv",
        pattern=".*",
    )
    mock_cursor.execute.assert_has_calls(
        [
            mock.call("\n            SELECT 1 FROM test_database.test_schema.test_table\n            WHERE date(PROPERTIES:date)=date('2020-01-01')\n            "),  # noqa
            mock.call('\n        CREATE TABLE IF NOT EXISTS test_database.test_schema.test_table (\n            ID NUMBER AUTOINCREMENT START 1 INCREMENT 1,\n            LOAD_TIME TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),\n            ORIGIN_FILE_NAME VARCHAR(16777216),\n            ORIGIN_FILE_LINE NUMBER(38,0),\n            ORIGIN_STR VARCHAR(16777216),\n            PROPERTIES VARIANT\n        );\n        '),  # noqa
            mock.call("\n        CREATE STAGE IF NOT EXISTS test_database.test_schema.test_table_stage\n            URL = 's3://edx-test/test/'\n            STORAGE_INTEGRATION = test_storage_integration\n            FILE_FORMAT = (TYPE='JSON', STRIP_OUTER_ARRAY=TRUE);\n        "),  # noqa
            mock.call("\n        COPY INTO test_database.test_schema.test_table (origin_file_name, origin_file_line, origin_str, properties)\n            FROM (\n                SELECT\n                    metadata$filename,\n                    metadata$file_row_number,\n                    t.$1,\n                    CASE\n                        WHEN CHECK_JSON(t.$1) IS NULL THEN t.$1\n                        ELSE NULL\n                    END\n                FROM @test_database.test_schema.test_table_stage t\n            )\n        FILES = ( 'test_file.csv' )\n        PATTERN = '.*'\n        FORCE=False\n        ")  # noqa
        ]
    )


def test_load_s3_data_to_snowflake_data_exists_no_overwrite(mock_sf_connection):
    mock_cursor = mock_sf_connection.cursor()
    mock_fetchone = mock.Mock()
    mock_cursor.fetchone = mock_fetchone

    task = snowflake.load_s3_data_to_snowflake
    with pytest.raises(signals.SKIP, match="Skipping task as data for the date exists and no overwrite was provided."):
        task.run(
            date="2020-01-01",
            date_property='date',
            sf_credentials={},
            sf_database="test_database",
            sf_schema="test_schema",
            sf_table="test_table",
            sf_role="test_role",
            sf_warehouse="test_warehouse",
            sf_storage_integration_name="test_storage_integration",
            s3_url="s3://edx-test/test/",
            pattern=".*",
        )


def test_export_snowflake_table_to_s3_with_exception(mock_sf_connection):
    mock_cursor = mock_sf_connection.cursor()
    mock_execute = mock.Mock(side_effect=ProgrammingError('Files already existing at the unload destination'))
    mock_cursor.execute = mock_execute

    task = snowflake.export_snowflake_table_to_s3
    with pytest.raises(signals.FAIL, match="Files already exist. Use overwrite option to force unloading."):
        task.run(
            sf_credentials={},
            sf_database="test_database",
            sf_schema="test_schema",
            sf_table="test_table",
            sf_role="test_role",
            sf_warehouse="test_warehouse",
            sf_storage_integration="test_storage_integration",
            s3_path="s3://edx-test/test/",
            overwrite=False,
        )


def test_export_snowflake_table_to_s3_overwrite(mock_sf_connection):  # noqa: F811
    mock_cursor = mock_sf_connection.cursor()
    with mock.patch('edx_argoutils.s3.delete_s3_directory.run') as mock_delete_s3_directory:
        with Flow("test") as f:
            snowflake.export_snowflake_table_to_s3(
                sf_credentials={},
                sf_database="test_database",
                sf_schema="test_schema",
                sf_table="test_table",
                sf_role="test_role",
                sf_warehouse="test_warehouse",
                sf_storage_integration="test_storage_integration",
                s3_path="s3://edx-test/test/",
                overwrite=True,
                enclosed_by='NONE',
                escape_unenclosed_field='\\\\',
                null_marker='NULL',
            )
        state = f.run()
        assert state.is_successful()

        mock_cursor.execute.assert_has_calls(
            [
                mock.call("\n        COPY INTO 's3://edx-test/test/test_database-test_schema-test_table/'\n            FROM test_database.test_schema.test_table\n            STORAGE_INTEGRATION = test_storage_integration\n            FILE_FORMAT = ( TYPE = CSV EMPTY_FIELD_AS_NULL = FALSE\n            FIELD_DELIMITER = ',' FIELD_OPTIONALLY_ENCLOSED_BY = NONE\n            ESCAPE_UNENCLOSED_FIELD = '\\\\'\n            NULL_IF = ( 'NULL' )\n            \n            COMPRESSION = NONE\n            )\n            OVERWRITE=True\n            SINGLE=False\n            DETAILED_OUTPUT = TRUE\n            MAX_FILE_SIZE = 104857600\n    "),  # noqa
            ]
        )

        mock_delete_s3_directory.assert_called_once_with('edx-test', 'test/test_database-test_schema-test_table/')


def test_export_snowflake_table_to_s3_no_escape(mock_sf_connection):  # noqa: F811
    mock_cursor = mock_sf_connection.cursor()
    with mock.patch('edx_argoutils.s3.delete_s3_directory.run'):
        with Flow("test") as f:
            snowflake.export_snowflake_table_to_s3(
                sf_credentials={},
                sf_database="test_database",
                sf_schema="test_schema",
                sf_table="test_table",
                sf_role="test_role",
                sf_warehouse="test_warehouse",
                sf_storage_integration="test_storage_integration",
                s3_path="s3://edx-test/test/",
                overwrite=True,
                enclosed_by='NONE',
                null_marker='NULL',
            )
        state = f.run()
        assert state.is_successful()

        mock_cursor.execute.assert_has_calls(
            [
                mock.call("\n        COPY INTO 's3://edx-test/test/test_database-test_schema-test_table/'\n            FROM test_database.test_schema.test_table\n            STORAGE_INTEGRATION = test_storage_integration\n            FILE_FORMAT = ( TYPE = CSV EMPTY_FIELD_AS_NULL = FALSE\n            FIELD_DELIMITER = ',' FIELD_OPTIONALLY_ENCLOSED_BY = NONE\n            \n            NULL_IF = ( 'NULL' )\n            \n            COMPRESSION = NONE\n            )\n            OVERWRITE=True\n            SINGLE=False\n            DETAILED_OUTPUT = TRUE\n            MAX_FILE_SIZE = 104857600\n    "),  # noqa
            ]
        )


def test_export_snowflake_table_to_s3_no_enclosure(mock_sf_connection):  # noqa: F811
    mock_cursor = mock_sf_connection.cursor()
    with mock.patch('edx_argoutils.s3.delete_s3_directory.run'):
        with Flow("test") as f:
            snowflake.export_snowflake_table_to_s3(
                sf_credentials={},
                sf_database="test_database",
                sf_schema="test_schema",
                sf_table="test_table",
                sf_role="test_role",
                sf_warehouse="test_warehouse",
                sf_storage_integration="test_storage_integration",
                s3_path="s3://edx-test/test/",
                overwrite=True,
                escape_unenclosed_field='\\\\',
                null_marker='NULL',
            )
        state = f.run()
        assert state.is_successful()

        mock_cursor.execute.assert_has_calls(
            [
                mock.call("\n        COPY INTO 's3://edx-test/test/test_database-test_schema-test_table/'\n            FROM test_database.test_schema.test_table\n            STORAGE_INTEGRATION = test_storage_integration\n            FILE_FORMAT = ( TYPE = CSV EMPTY_FIELD_AS_NULL = FALSE\n            FIELD_DELIMITER = ',' \n            ESCAPE_UNENCLOSED_FIELD = '\\\\'\n            NULL_IF = ( 'NULL' )\n            \n            COMPRESSION = NONE\n            )\n            OVERWRITE=True\n            SINGLE=False\n            DETAILED_OUTPUT = TRUE\n            MAX_FILE_SIZE = 104857600\n    "),  # noqa
            ]
        )


def test_export_snowflake_table_to_s3_no_null_if(mock_sf_connection):  # noqa: F811
    mock_cursor = mock_sf_connection.cursor()
    with mock.patch('edx_argoutils.s3.delete_s3_directory.run'):
        with Flow("test") as f:
            snowflake.export_snowflake_table_to_s3(
                sf_credentials={},
                sf_database="test_database",
                sf_schema="test_schema",
                sf_table="test_table",
                sf_role="test_role",
                sf_warehouse="test_warehouse",
                sf_storage_integration="test_storage_integration",
                s3_path="s3://edx-test/test/",
                overwrite=True,
                enclosed_by='NONE',
                escape_unenclosed_field='\\\\',
            )
        state = f.run()
        assert state.is_successful()

        mock_cursor.execute.assert_has_calls(
            [
                mock.call("\n        COPY INTO 's3://edx-test/test/test_database-test_schema-test_table/'\n            FROM test_database.test_schema.test_table\n            STORAGE_INTEGRATION = test_storage_integration\n            FILE_FORMAT = ( TYPE = CSV EMPTY_FIELD_AS_NULL = FALSE\n            FIELD_DELIMITER = ',' FIELD_OPTIONALLY_ENCLOSED_BY = NONE\n            ESCAPE_UNENCLOSED_FIELD = '\\\\'\n            \n            \n            COMPRESSION = NONE\n            )\n            OVERWRITE=True\n            SINGLE=False\n            DETAILED_OUTPUT = TRUE\n            MAX_FILE_SIZE = 104857600\n    "),  # noqa
            ]
        )


def test_export_snowflake_table_to_s3_with_manifest(mock_sf_connection):  # noqa: F811
    mock_cursor = mock_sf_connection.cursor()
    mock_fetchall = mock.Mock()
    s3_files = ['data_0_0_0.csv', 'data_0_0_1.csv']
    mock_fetchall.return_value = [[file] for file in s3_files]
    mock_cursor.fetchall = mock_fetchall

    with mock.patch('prefect.tasks.aws.s3.S3Upload.run') as mock_s3_upload:
        with Flow("test") as f:
            snowflake.export_snowflake_table_to_s3(
                sf_credentials={},
                sf_database="test_database",
                sf_schema="test_schema",
                sf_table="test_table",
                sf_role="test_role",
                sf_warehouse="test_warehouse",
                sf_storage_integration="test_storage_integration",
                s3_path="s3://edx-test/test/",
                overwrite=False,
                generate_manifest=True,
            )
        state = f.run()
        assert state.is_successful()

        expected_manifest_content = {
            "entries": [
                {"url": "s3://edx-test/test/test_database-test_schema-test_table/" + s3_file, "mandatory": True} for s3_file in s3_files # noqa
            ]
        }
        mock_s3_upload.assert_called_once_with(
            json.dumps(expected_manifest_content), key="test/test_database-test_schema-test_table/manifest.json"
        )


def test_export_snowflake_table_to_s3_no_overwrite(mock_sf_connection):  # noqa: F811
    mock_cursor = mock_sf_connection.cursor()

    with Flow("test") as f:
        snowflake.export_snowflake_table_to_s3(
            sf_credentials={},
            sf_database="test_database",
            sf_schema="test_schema",
            sf_table="test_table",
            sf_role="test_role",
            sf_warehouse="test_warehouse",
            sf_storage_integration="test_storage_integration",
            s3_path="s3://edx-test/test/",
            overwrite=False,
            enclosed_by='"',
            escape_unenclosed_field='\\\\',
            null_marker='NULL',
        )
    state = f.run()
    assert state.is_successful()

    mock_cursor.execute.assert_has_calls(
        [
            mock.call("""\n        COPY INTO 's3://edx-test/test/test_database-test_schema-test_table/'\n            FROM test_database.test_schema.test_table\n            STORAGE_INTEGRATION = test_storage_integration\n            FILE_FORMAT = ( TYPE = CSV EMPTY_FIELD_AS_NULL = FALSE\n            FIELD_DELIMITER = ',' FIELD_OPTIONALLY_ENCLOSED_BY = '"'\n            ESCAPE_UNENCLOSED_FIELD = '\\\\'\n            NULL_IF = ( 'NULL' )\n            \n            COMPRESSION = NONE\n            )\n            OVERWRITE=False\n            SINGLE=False\n            DETAILED_OUTPUT = TRUE\n            MAX_FILE_SIZE = 104857600\n    """),  # noqa
        ]
    )


def test_export_snowflake_table_to_s3_with_binary_format(mock_sf_connection):  # noqa: F811
    mock_cursor = mock_sf_connection.cursor()

    with Flow("test") as f:
        snowflake.export_snowflake_table_to_s3(
            sf_credentials={},
            sf_database="test_database",
            sf_schema="test_schema",
            sf_table="test_table",
            sf_role="test_role",
            sf_warehouse="test_warehouse",
            sf_storage_integration="test_storage_integration",
            s3_path="s3://edx-test/test/",
            overwrite=False,
            enclosed_by='"',
            escape_unenclosed_field='\\\\',
            null_marker='NULL',
            binary_format='UTF8',
        )
    state = f.run()
    assert state.is_successful()

    mock_cursor.execute.assert_has_calls(
        [
            mock.call("""\n        COPY INTO 's3://edx-test/test/test_database-test_schema-test_table/'\n            FROM test_database.test_schema.test_table\n            STORAGE_INTEGRATION = test_storage_integration\n            FILE_FORMAT = ( TYPE = CSV EMPTY_FIELD_AS_NULL = FALSE\n            FIELD_DELIMITER = ',' FIELD_OPTIONALLY_ENCLOSED_BY = '"'\n            ESCAPE_UNENCLOSED_FIELD = '\\\\'\n            NULL_IF = ( 'NULL' )\n            BINARY_FORMAT = UTF8\n            COMPRESSION = NONE\n            )\n            OVERWRITE=False\n            SINGLE=False\n            DETAILED_OUTPUT = TRUE\n            MAX_FILE_SIZE = 104857600\n    """),  # noqa
        ]
    )


def test_load_s3_data_to_snowflake_data_disable_check(mock_sf_connection):
    mock_cursor = mock_sf_connection.cursor()
    mock_fetchone = mock.Mock()
    mock_cursor.fetchone = mock_fetchone

    task = snowflake.load_s3_data_to_snowflake
    task.run(
        date="2020-01-01",
        date_property='date',
        sf_credentials={},
        sf_database="test_database",
        sf_schema="test_schema",
        sf_table="test_table",
        sf_role="test_role",
        sf_warehouse="test_warehouse",
        sf_storage_integration_name="test_storage_integration",
        s3_url="s3://edx-test/test/",
        file="test_file.csv",
        pattern=".*",
        overwrite=True,
        disable_existence_check=True,
    )
    mock_call = mock.call("\n            SELECT 1 FROM test_database.test_schema.test_table\n            WHERE date(PROPERTIES:date)=date('2020-01-01')\n            ")  # noqa

    assert mock_call not in mock_cursor.execute.mock_calls

    task.run(
        date="2020-01-01",
        date_property='date',
        sf_credentials={},
        sf_database="test_database",
        sf_schema="test_schema",
        sf_table="test_table",
        sf_role="test_role",
        sf_warehouse="test_warehouse",
        sf_storage_integration_name="test_storage_integration",
        s3_url="s3://edx-test/test/",
        file="test_file.csv",
        pattern=".*",
        overwrite=True,
        disable_existence_check=False,
    )
    mock_cursor.execute.assert_has_calls(
        [
            mock_call
        ]
    )
