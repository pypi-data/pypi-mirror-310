#
# Copyright (c) 2024, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#

from asyncio import iscoroutinefunction
from typing import Callable, Dict, List, Optional

from loguru import logger
from pipecat.frames.frames import (
    EndFrame,
    LLMMessagesAppendFrame,
    LLMMessagesUpdateFrame,
    LLMSetToolsFrame,
    TTSSpeakFrame,
)

from .state import FlowState


class FlowManager:
    """Manages conversation flows in a Pipecat pipeline.

    This manager handles the progression through a flow defined by nodes, where each node
    represents a state in the conversation. Each node has:
    - Messages for the LLM (system/user/assistant messages)
    - Available functions that can be called
    - Optional pre-actions to execute before LLM inference
    - Optional post-actions to execute after LLM inference

    The flow is defined by a configuration that specifies:
    - Initial node
    - Available nodes and their configurations
    - Transitions between nodes via function calls
    """

    def __init__(self, flow_config: dict, task, tts=None):
        """Initialize the flow manager.

        Args:
            flow_config: Dictionary containing the complete flow configuration,
                        including initial_node and node configurations
            task: PipelineTask instance used to queue frames into the pipeline
        """
        self.flow = FlowState(flow_config)
        self.initialized = False
        self.task = task
        self.tts = tts
        self.action_handlers: Dict[str, Callable] = {}

        # Register built-in actions
        self.register_action("tts_say", self._handle_tts_action)
        self.register_action("end_conversation", self._handle_end_action)

    async def initialize(self, initial_messages: List[dict]):
        """Initialize the flow with starting messages and functions.

        This method sets up the initial context, combining any system-level
        messages with the initial node's message and functions.

        Args:
            initial_messages: List of initial messages (typically system messages)
                            to include in the context
        """
        if not self.initialized:
            messages = initial_messages + self.flow.get_current_messages()
            await self.task.queue_frame(LLMMessagesUpdateFrame(messages=messages))
            await self.task.queue_frame(LLMSetToolsFrame(tools=self.flow.get_current_functions()))
            self.initialized = True
            logger.debug(f"Initialized flow at node: {self.flow.current_node}")
        else:
            logger.warning("Attempted to initialize FlowManager multiple times")

    async def register_functions(self, llm_service):
        """Register all functions from the flow configuration with the LLM service.

        This method sets up function handlers for all functions defined across all nodes.
        When a function is called, it will automatically trigger the appropriate node
        transition.

        Note: This registers handlers for all possible functions, but the LLM's access
        to functions is controlled separately through LLMSetToolsFrame. The LLM will
        only see the functions available in the current node.

        Args:
            llm_service: The LLM service to register functions with
        """

        async def handle_function_call(
            function_name, tool_call_id, arguments, llm, context, result_callback
        ):
            await self.handle_transition(function_name)
            await result_callback("Acknowledged")

        # Register all functions from all nodes
        for node in self.flow.nodes.values():
            for function in node.functions:
                function_name = function["function"]["name"]
                llm_service.register_function(function_name, handle_function_call)

    def register_action(self, action_type: str, handler: Callable):
        """Register a handler for a specific action type.

        Args:
            action_type: String identifier for the action (e.g., "tts_say")
            handler: Async or sync function that handles the action.
                    Should accept action configuration as parameter.
        """
        if not callable(handler):
            raise ValueError("Action handler must be callable")
        self.action_handlers[action_type] = handler

    async def _execute_actions(self, actions: Optional[List[dict]]) -> None:
        """Execute actions specified for the current node.

        Args:
            actions: List of action configurations to execute

        Note:
            Each action must have a 'type' field matching a registered handler
        """
        if not actions:
            return

        for action in actions:
            action_type = action["type"]
            if action_type in self.action_handlers:
                handler = self.action_handlers[action_type]
                try:
                    if iscoroutinefunction(handler):
                        await handler(action)
                    else:
                        handler(action)
                except Exception as e:
                    logger.warning(f"Error executing action {action_type}: {e}")
            else:
                logger.warning(f"No handler registered for action type: {action_type}")

    async def _handle_tts_action(self, action: dict):
        """Built-in handler for TTS actions that speak immediately.

        This handler attempts to use the TTS service directly to speak the text
        immediately, bypassing the pipeline queue. If no TTS service is available,
        it falls back to queueing the text through the pipeline.

        Args:
            action: Dictionary containing the action configuration.
                Must include a 'text' key with the text to speak.
        """
        if self.tts:
            # Direct call to TTS service to speak text immediately
            await self.tts.say(action["text"])
        else:
            # Fall back to queued TTS if no direct service available
            await self.task.queue_frame(TTSSpeakFrame(text=action["text"]))

    async def _handle_end_action(self, action: dict):
        """Built-in handler for ending the conversation.

        This handler queues an EndFrame to terminate the conversation. If the action
        includes a 'text' key, it will queue that text to be spoken before ending.

        Args:
            action: Dictionary containing the action configuration.
                Optional 'text' key for a goodbye message.
        """
        if action.get("text"):  # Optional goodbye message
            await self.task.queue_frame(TTSSpeakFrame(text=action["text"]))
        await self.task.queue_frame(EndFrame())

    async def handle_transition(self, function_name: str):
        """Handle the execution of functions and potential node transitions.

        This method implements the core state transition logic of the conversation flow.
        It distinguishes between two types of functions:

        1. Transitional Functions:
           - Function names that match existing node names
           - Trigger a full node transition with:
             * Pre-action execution
             * Context and tool updates
             * Post-action execution

        2. Terminal Functions:
           - Function names that don't match any node names
           - Execute without changing the conversation state
           - Don't trigger context updates or actions

        The transition process for transitional functions:
        1. Validates the function call against available functions
        2. Executes pre-actions of the new node
        3. Updates the LLM context with new messages
        4. Updates available tools for the new node
        5. Executes post-actions of the new node

        Args:
            function_name: Name of the function to execute

        Raises:
            RuntimeError: If handle_transition is called before initialization
        """
        if not self.initialized:
            raise RuntimeError("FlowManager must be initialized before handling transitions")

        available_functions = self.flow.get_available_function_names()

        if function_name not in available_functions:
            logger.warning(
                f"Received invalid function call '{function_name}' for node '{self.flow.current_node}'. "
                f"Available functions are: {available_functions}"
            )
            return

        # Attempt transition - returns new node ID for transitional functions,
        # None for terminal functions
        new_node = self.flow.transition(function_name)

        # Only perform node transition logic if we got a new node
        # (meaning it was a transitional function, not a terminal one)
        if new_node is not None:
            # Execute pre-actions before updating LLM context
            if self.flow.get_current_pre_actions():
                logger.debug(f"Executing pre-actions for node {new_node}")
                await self._execute_actions(self.flow.get_current_pre_actions())

            # Update LLM context and tools
            current_messages = self.flow.get_current_messages()
            await self.task.queue_frame(LLMMessagesAppendFrame(messages=current_messages))
            await self.task.queue_frame(LLMSetToolsFrame(tools=self.flow.get_current_functions()))

            # Execute post-actions after updating LLM context
            if self.flow.get_current_post_actions():
                logger.debug(f"Executing post-actions for node {new_node}")
                await self._execute_actions(self.flow.get_current_post_actions())

            logger.debug(f"Transition to node {new_node} complete")
        else:
            logger.debug(f"Terminal function {function_name} executed without node transition")
