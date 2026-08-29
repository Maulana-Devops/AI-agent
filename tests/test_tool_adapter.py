from app.tool_adapter import get_tool_declarations


def test_git_log_has_limit_parameter():
    declarations = get_tool_declarations()

    git_log = next(
        item
        for item in declarations
        if item["name"] == "git_log"
    )

    assert "limit" in git_log["parameters"]["properties"]
    assert (
        git_log["parameters"]["properties"]["limit"]["type"]
        == "integer"
    )


def test_read_only_tools_have_empty_parameters():
    declarations = get_tool_declarations()

    names = {
        item["name"]: item
        for item in declarations
    }

    assert names["git_status"]["parameters"]["properties"] == {}
    assert names["git_branch"]["parameters"]["properties"] == {}
    assert names["git_diff"]["parameters"]["properties"] == {}
    assert names["git_remote"]["parameters"]["properties"] == {}
