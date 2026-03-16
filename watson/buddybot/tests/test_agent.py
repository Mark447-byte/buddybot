import pytest
from unittest.mock import MagicMock
from agent.loop import AgentLoop

def test_agent_loop_basic():
    # Mock LLM Client
    mock_llm = MagicMock()
    # Mock planner response (JSON steps)
    mock_llm.generate.side_effect = [
        '[{"description": "Test step", "tool": "list_files", "args": {"directory": "."}}]', # Planner
        'CONTINUE - Step succeeded' # Reflector
    ]
    
    # Mock TaskTools
    mock_task_tools = MagicMock()
    
    # Mock Memories
    mock_long_term_mem = MagicMock()
    mock_short_term_mem = MagicMock()
    mock_short_term_mem.get_formatted_history.return_value = ""
    
    agent = AgentLoop(mock_llm, mock_task_tools, mock_long_term_mem, mock_short_term_mem)
    
    response = agent.run("Test goal")
    
    assert "Test step" in response
    assert mock_llm.generate.call_count == 2
    mock_long_term_mem.store_interaction.assert_called_once()
    mock_short_term_mem.add_interaction.assert_called_once()

def test_planner_parsing_error():
    mock_llm = MagicMock()
    mock_llm.generate.return_value = "No JSON here"
    
    from agent.planner import Planner
    planner = Planner(mock_llm)
    plan = planner.plan("goal")
    
    assert "Error" in plan[0]["description"]

def test_agent_loop_with_memory():
    mock_llm = MagicMock()
    mock_llm.generate.side_effect = [
        '[{"description": "Follow-up step", "tool": "list_files", "args": {"directory": "."}}]', # Planner
        'CONTINUE' # Reflector
    ]
    
    mock_task_tools = MagicMock()
    mock_long_term_mem = MagicMock()
    mock_short_term_mem = MagicMock()
    mock_short_term_mem.get_formatted_history.return_value = "User: Hello\nAssistant: Hi!"
    
    agent = AgentLoop(mock_llm, mock_task_tools, mock_long_term_mem, mock_short_term_mem)
    agent.run("What's next?")
    
    # Verify context was retrieved
    mock_short_term_mem.get_formatted_history.assert_called_once()
    # Verify context was passed to planner (via LLM call)
    planner_prompt = mock_llm.generate.call_args_list[0][0][0]
    assert "Recent Interaction History" in planner_prompt
    assert "Hello" in planner_prompt
