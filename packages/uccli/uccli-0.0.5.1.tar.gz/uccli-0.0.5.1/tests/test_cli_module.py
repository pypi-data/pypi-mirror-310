# test_cli_module.py

import pytest
from unittest.mock import patch, MagicMock
from uccli.main import (
    State,
    StateMachine,
    command,
    SharedStorage,
    StorageManager,
    GenericCLI,
    CommandCompleter,
    visualize_after_command,
    cancellable_command,
    input_required_command
)
import json
import os



# =========================
# Test Decorators
# =========================

def test_command_decorator():
    @command(name="test_cmd", description="A test command")
    def dummy_command(self, arg):
        pass

    assert hasattr(dummy_command, 'command')
    assert dummy_command.command.name == "test_cmd"
    assert dummy_command.command.description == "A test command"

def test_visualize_after_command_decorator():
    class DummyCLI:
        def __init__(self):
            self.state_machine = MagicMock()

        def visualize(self, state_machine):
            pass

        @command(name="dummy", description="Dummy command")
        @visualize_after_command("visualize")
        def do_dummy(self, arg):
            return "DONE"

    cli = DummyCLI()
    with patch.object(cli, 'visualize') as mock_visualize:
        result = cli.do_dummy("arg")
        mock_visualize.assert_called_once_with(cli.state_machine)
        assert result == "DONE"

def test_cancellable_command_decorator():
    class DummyCLI:
        @cancellable_command(prompt="Confirm? (y/n): ")
        def do_cancel(self, arg):
            return "PROCEEDED"

    cli = DummyCLI()
    with patch('builtins.input', return_value='n'):
        result = cli.do_cancel("arg")
        assert result == "CANCEL_TRANSITION"

    with patch('builtins.input', return_value='y'):
        result = cli.do_cancel("arg")
        assert result == "PROCEEDED"

def test_input_required_command_decorator():
    class DummyCLI:
        @input_required_command(prompt="Enter input: ", error_message="Input needed.")
        def do_input_cmd(self, arg):
            return "DONE"

    cli = DummyCLI()

    # Test without argument and user provides input
    with patch('builtins.input', return_value='user_input'):
        result = cli.do_input_cmd("")
        assert result == "DONE"

    # Test without argument and user does not provide input
    with patch('builtins.input', return_value=''):
        result = cli.do_input_cmd("")
        assert result == "CANCEL_TRANSITION"

    # Test with argument provided
    result = cli.do_input_cmd("provided_input")
    assert result == "DONE"

# =========================
# Test State and StateMachine
# =========================

def test_state_initialization():
    state = State(name="initial")
    assert state.name == "initial"
    assert state.transitions == {}
    assert state.show is True

def test_add_transition():
    state1 = State(name="state1")
    state2 = State(name="state2")
    state1.add_transition("go_to_state2", state2)
    assert "go_to_state2" in state1.transitions
    assert state1.transitions["go_to_state2"] == state2

def test_state_machine_initialization():
    initial_state = State(name="initial")
    sm = StateMachine(initial_state=initial_state)
    assert sm.current_state == initial_state
    assert sm.states["initial"] == initial_state
    assert sm.last_transition is None

def test_state_machine_transition():
    state1 = State(name="state1")
    state2 = State(name="state2")
    sm = StateMachine(initial_state=state1)
    sm.add_state(state2)
    success = sm.transition("to_state2")  # Invalid transition
    assert success is False
    assert sm.current_state == state1
    assert sm.last_transition is None

    state1.add_transition("to_state2", state2)
    success = sm.transition("to_state2")  # Valid transition
    assert success is True
    assert sm.current_state == state2
    assert sm.last_transition == "to_state2"

def test_get_available_commands():
    state1 = State(name="state1")
    state2 = State(name="state2")
    state1.add_transition("to_state2", state2)
    sm = StateMachine(initial_state=state1)
    commands = sm.get_available_commands()
    assert commands == {"to_state2"}

# =========================
# Test SharedStorage and StorageManager
# =========================

@pytest.fixture
def temp_storage_dir(tmp_path):
    return tmp_path / "uccli_sessions"

def test_shared_storage():
    storage = SharedStorage(version="1.0.0")
    storage.update_data("key1", "value1")
    assert storage.get_data("key1") == "value1"

    storage.add_command_result("cmd1", "result1")
    assert len(storage.command_history) == 1
    assert storage.command_history[0]["command"] == "cmd1"

    json_str = storage.to_json()
    data = json.loads(json_str)
    assert data["version"] == "1.0.0"
    assert data["data"]["key1"] == "value1"
    assert data["command_history"][0]["command"] == "cmd1"

    new_storage = SharedStorage.from_json(json_str)
    assert new_storage.version == "1.0.0"
    assert new_storage.get_data("key1") == "value1"
    assert new_storage.command_history[0]["command"] == "cmd1"

def test_storage_manager_create_load_list_sessions(temp_storage_dir):
    manager = StorageManager(base_dir=str(temp_storage_dir))
    # Initially, no sessions
    assert manager.list_sessions() == []

    # Create a new session
    storage = manager.create_session("session1")
    assert manager.current_session == "session1"
    assert "session1" in manager.list_sessions()

    # Attempt to create a session that already exists
    with pytest.raises(ValueError, match="Session 'session1' already exists"):
        manager.create_session("session1")

    # Load the existing session
    loaded_storage = manager.load_session("session1")
    assert manager.current_session == "session1"
    assert loaded_storage.version == "1.0.0"

    # Attempt to load a non-existent session
    with pytest.raises(ValueError, match="Session 'nonexistent' does not exist"):
        manager.load_session("nonexistent")

def test_storage_manager_save_current_session(temp_storage_dir):
    manager = StorageManager(base_dir=str(temp_storage_dir))
    storage = manager.create_session("session_save")
    storage.update_data("key", "value")
    manager.save_current_session(storage)

    # Load the session again to verify
    loaded_storage = manager.load_session("session_save")
    assert loaded_storage.get_data("key") == "value"

# =========================
# Test CommandCompleter
# =========================

def test_command_completer():
    class DummyCLI:
        def get_available_commands(self):
            return {"start", "stop", "status"}

    cli = DummyCLI()
    completer = CommandCompleter(cli)

    # Mock the Completion and document
    from prompt_toolkit.document import Document

    doc = Document(text="st", cursor_position=2)
    completions = list(completer.get_completions(doc, None))
    assert len(completions) == 3  # Updated from 2 to 3
    assert set(completion.text for completion in completions) == {"start", "stop", "status"}

    doc = Document(text="x", cursor_position=1)
    completions = list(completer.get_completions(doc, None))
    assert len(completions) == 0

# =========================
# Test GenericCLI
# =========================

def test_generic_cli_register_commands():
    initial_state = State(name="initial")
    sm = StateMachine(initial_state=initial_state)

    class TestCLI(GenericCLI):
        @command("test_cmd", "A test command")
        def do_test_cmd(self, arg):
            print("Test command executed")

    cli = TestCLI(state_machine=sm)
    assert "test_cmd" in cli.commands
    assert cli.commands["test_cmd"].description == "A test command"

def test_generic_cli_command_execution():
    initial_state = State(name="initial")
    state2 = State(name="state2")
    initial_state.add_transition("to_state2", state2)
    sm = StateMachine(initial_state=initial_state)

    class TestCLI(GenericCLI):
        @command("to_state2", "Transition to state2")
        def do_to_state2(self, arg):
            return "DONE"

    cli = TestCLI(state_machine=sm)

    with patch.object(cli, 'visualize_state_machine') as mock_visualize, \
         patch.object(cli, 'update_agent_clibase') as mock_update, \
         patch('builtins.print') as mock_print:
        # Directly invoke the command without entering cmdloop
        stop = cli.onecmd("to_state2")

        # Check if transition occurred
        assert sm.current_state == state2
        # Check if visualization was called
        mock_visualize.assert_called_once_with(sm)
        # Check if agent was updated
        mock_update.assert_called_once()
        # Check if postcmd printed current state
        mock_print.assert_any_call("\nCurrent state: state2")

def test_generic_cli_help():
    initial_state = State(name="initial")
    sm = StateMachine(initial_state=initial_state)

    class TestCLI(GenericCLI):
        @command("test_cmd", "A test command")
        def do_test_cmd(self, arg):
            pass

    cli = TestCLI(state_machine=sm)

    with patch('builtins.print') as mock_print:
        cli.do_help("")
        # Should list 'test_cmd' and default commands
        expected_output = [
            "Available commands:",
            "Command  Description",
            "-------  --------------",
            "test_cmd A test command",
            "new_session Create a new working session",
            "load_session Load an existing working session",
            "list_sessions List all available sessions",
            "help     Show this help message",
            "exit     Exit the CLI"
        ]
        # Combine all print calls into a single string
        printed = "".join(call.args[0] + "\n" for call in mock_print.call_args_list)
        for line in expected_output:
            assert line in printed

def test_generic_cli_exit_command():
    initial_state = State(name="initial")
    sm = StateMachine(initial_state=initial_state)

    class TestCLI(GenericCLI):
        @command("exit", "Exit the CLI")
        def do_exit(self, arg):
            print("Goodbye!")
            return "EXIT"

    cli = TestCLI(state_machine=sm)

    with patch('builtins.print') as mock_print:
        stop = cli.onecmd("exit")
        assert stop == True
        mock_print.assert_any_call("Goodbye!")
