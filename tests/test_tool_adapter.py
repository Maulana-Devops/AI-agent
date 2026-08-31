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


def test_search_tools_match_python_defaults():
    from tools.registry import list_tools

    tools = list_tools()

    search_files = tools["search_files"]["parameters"]
    search_contents = tools["search_file_contents"]["parameters"]

    assert "required" not in search_files
    assert "required" not in search_contents


def test_search_file_contents_documents_non_empty_query_requirement():
    from tools.registry import list_tools

    schema = list_tools()["search_file_contents"]["parameters"]

    query_description = (
        schema["properties"]["query"]["description"]
    )

    assert "empty" in query_description.lower()
