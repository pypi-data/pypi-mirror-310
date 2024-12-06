from tuoni.TuoniExceptions import *
from tuoni.TuoniCommand import *
from tuoni.TuoniAlias import *
from tuoni.TuoniDefaultCommands import *

class TuoniAgent:
    """
    Class providing data and functionality of the connected agent

    Attributes:
        guid (Guid): Agent GUID
        first_registration_time (datetime): First time the agent connected
        last_callback_time (datetime): Last time the agent connected
        metadata (cict): Agent metadata
        active (bool): Is agent active
        recentListeners (list): Over what listener the connection works
        availableCommands (dict): Available commands
    """

    def __init__(self, conf, c2):
        self.c2 = c2
        self._load_conf(conf)

    def _load_conf(self, conf):
        self.guid = conf["guid"]
        self.first_registration_time = conf["firstRegistrationTime"]
        self.last_callback_time = conf["lastCallbackTime"]
        self.metadata = conf["metadata"]
        self.active = conf["active"]
        self.recentListeners = conf["recentListeners"]
        self._fill_available_commands(conf["availableCommandTemplates"])

    def send_command(self, command_type, command_conf=None, execution_conf = None, files = None):
        """
        Send command to agent

        Args:
            command_type (str | TuoniAlias | TuoniDefaultCommand): What command to send.
            command_conf (dict): Command configuration
            execution_conf (dict): Execution configuration
            files (dict): Files to send with command

        Returns:
            TuoniCommand: Object referencing the created command
        """
        if self.guid is None:
            raise ExceptionTuoniDeleted("")
        if isinstance(command_type, TuoniDefaultCommand):
            command_conf = command_type.command_conf
            execution_conf = command_type.execution_conf
            files = command_type.files
            command_type = command_type.command_type
        if isinstance(command_type, TuoniAlias):
            command_type = command_type.alias_id
        if command_conf is None:
            command_conf = {}
        data = {
            "template": command_type,
            "configuration": command_conf
        }
        if execution_conf is not None:
            data["execConf"] = execution_conf
        data = self.c2.request_post("/api/v1/agents/%s/commands" % self.guid, data, files)
        return TuoniCommand(data, self.c2)

    def get_commands(self):
        """
        Get all agent commands

        Returns:
            list[TuoniCommand]: List of agent commands
        """
        if self.guid is None:
            raise ExceptionTuoniDeleted("")
        commands_data = self.c2.request_get("/api/v1/agents/%s/commands" % self.guid)
        commands = []
        for command_nr in commands_data:
            command_data = commands_data[command_nr]
            command_obj = TuoniCommand(command_data, self.c2)
            commands.append(command_obj)
        return commands

    def delete(self):
        """
        Deletes agent
        """
        if self.guid is None:
            raise ExceptionTuoniDeleted("")
        self.c2.request_delete("/api/v1/agents/%s" % self.guid)
        self.listener_id = None
        
    def _fill_available_commands(self, command_list):
        self.availableCommands = {}
        for cmd in self.c2.request_get("/api/v1/command-templates"):
            if cmd["id"] in command_list:
                self.availableCommands[cmd["name"]] = cmd["id"]
            

