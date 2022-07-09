from unittest.mock import patch, mock_open
from dirsync import run
from dirsync import options


def test_run_from_cmd_line_then_create_user_config_file_when_not_exist():
    with patch.object(run, "os") as os_mock:
        os_mock.path.isfile.return_value = False

        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            with patch.object(run, "sync"), patch.object(run, "ArgParser"):
                run.from_cmdline()

        assert mock_file.called
        handle = mock_file()
        handle.write.assert_called_once_with(options.DEFAULT_USER_CFG)


def test_run_from_cmd_line_error_with_exit_2():
    with patch.object(run, "os") as os_mock:
        os_mock.path.isfile.return_value = True

        with patch.object(run, "sync"), patch.object(run, "ArgParser") as arg_parser_mock:
            arg_parser_mock.side_effect = Exception()
            with patch.object(run, "sys") as sys_mock:
                run.from_cmdline()
                sys_mock.exit.assert_called_with(2)
